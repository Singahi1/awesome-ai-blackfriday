#!/usr/bin/env python3
"""Conservative vendor verification and seasonal deal discovery bot.

Safety boundary:
- May refresh verification metadata when strong evidence is present.
- May mark a failed fetch stale (never expired).
- Never rewrites prices, discounts, deadlines or expiry automatically.
- New deals and possible price changes are emitted as evidence-backed review items.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "deals.source.json"
OUT = ROOT / "bot-output"
TODAY = date.today()
MAX_CHECKS = int(os.environ.get("BOT_MAX_CHECKS", "12"))
MAX_CANDIDATES = int(os.environ.get("BOT_MAX_CANDIDATES", "6"))
TIMEOUT = int(os.environ.get("BOT_TIMEOUT_MS", "30000"))

TRACKERS = [
    "https://aideals.app/deals",
    "https://geotoolbox.ai/blog",
    "https://blackfridaydeals.dev/blog",
    "https://fourthfeed.com/deals",
]
BLOCKED_MARKERS = [
    "just a moment", "access denied", "verify you are human", "captcha",
    "cloudflare", "unsupported client", "are you a robot", "security check",
]
SALE_WORDS = [
    "black friday", "cyber monday", "christmas", "diwali", "big billion",
    "sale", "offer", "discount", "limited time", "deal", "off",
]


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def sale_words(campaign: str | None) -> list[str]:
    words = ["sale", "offer", "discount", "limited time", "deal", "off"]
    if campaign:
        words.extend(campaign.replace("-", " ").split())
    return list(dict.fromkeys(words))


def code_tokens(code: str | None) -> list[str]:
    if not code:
        return []
    parts = re.split(r"\s*/\s*|\s*,\s*|\s+or\s+", code, flags=re.I)
    out = []
    for part in parts:
        token = re.sub(r"\([^)]*\)", "", part).strip().upper()
        if len(token) >= 4 and re.match(r"^[A-Z0-9_-]+$", token):
            out.append(token)
    return out


def price_tokens(value: str | None) -> list[str]:
    if not value:
        return []
    return re.findall(r"(?:[$€£₹]\s*)?\d+(?:[.,]\d+)?", value)


def excerpt_around(text: str, needles: Iterable[str], length: int = 420) -> str:
    lower = text.lower()
    positions = [lower.find(str(n).lower()) for n in needles if n and lower.find(str(n).lower()) >= 0]
    start = max(0, min(positions) - 90) if positions else 0
    return re.sub(r"\s+", " ", text[start:start + length]).strip()


def next_check(d: dict) -> str:
    days = 30 if d.get("offer_type") in {"evergreen", "partner"} else 1
    return (TODAY + timedelta(days=days)).isoformat()


def due_deals(data: dict) -> list[dict]:
    rows = []
    for d in data["deals"]:
        if d.get("lifecycle") not in {"live", "announced"}:
            continue
        nc = d.get("next_check")
        if d.get("verification") == "stale" or (nc and date.fromisoformat(nc) <= TODAY):
            rows.append(d)
    return sorted(rows, key=lambda d: (d.get("valid_until") or "9999-12-31", -d.get("useful", 0), d["name"]))[:MAX_CHECKS]


class Fetcher:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True, args=["--no-sandbox"])

    def get(self, url: str) -> tuple[int, str, str]:
        page = self.browser.new_page(user_agent="Mozilla/5.0 (compatible; AwesomeAIDealsBot/1.0)")
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT)
            page.wait_for_timeout(1400)
            text = page.locator("body").inner_text(timeout=8000)
            return (response.status if response else 0), page.url, text
        except Exception as exc:
            return 0, url, f"FETCH_ERROR: {exc}"
        finally:
            page.close()

    def close(self):
        self.browser.close()
        self.playwright.stop()


def verify(d: dict, fetched: tuple[int, str, str]) -> dict:
    status, final_url, text = fetched
    lower = text.lower()
    words = sale_words(d.get("campaign"))
    code_hits = [c for c in code_tokens(d.get("code")) if c.lower() in lower]
    discount_hit = isinstance(d.get("discount"), (int, float)) and re.search(rf"\b{int(d['discount'])}\s*%", text) is not None
    after_tokens = price_tokens(d.get("price_after"))
    before_tokens = price_tokens(d.get("price_before"))
    after_hit = any(t in text for t in after_tokens)
    before_hit = any(t in text for t in before_tokens)
    sale_hit = any(w in lower for w in words)
    blocked = status == 0 or status >= 400 or any(m in lower for m in BLOCKED_MARKERS)
    strong = bool(code_hits) or (discount_hit and sale_hit) or (after_hit and sale_hit)
    score = (4 if code_hits else 0) + (2 if discount_hit else 0) + (2 if after_hit else 0) + (1 if sale_hit else 0) + (1 if 200 <= status < 400 else 0)
    result = {"name": d["name"], "status": status, "final_url": final_url, "score": score, "strong": strong}
    if blocked:
        d["verification"] = "stale"
        d["next_check"] = next_check(d)
        result["outcome"] = "stale-fetch"
        return result
    if strong and score >= 5:
        d["last_verified"] = TODAY.isoformat()
        d["next_check"] = next_check(d)
        d["verification"] = "verified"
        if d.get("lifecycle") == "announced":
            d["lifecycle"] = "live"
            result["outcome"] = "promoted-to-live"
        else:
            result["outcome"] = "reverified"
        evidence = {
            "type": "vendor_page",
            "url": final_url,
            "checked_at": TODAY.isoformat(),
            "excerpt": excerpt_around(text, code_hits + words),
        }
        d["evidence"] = (d.get("evidence") or [])[-4:] + [evidence]
        return result
    d["verification"] = "conflicting"
    d["next_check"] = next_check(d)
    result["outcome"] = "needs-review"
    result["excerpt"] = excerpt_around(text, words + code_tokens(d.get("code")))
    if (code_hits or discount_hit) and before_hit and not after_hit:
        result["possible_price_change"] = True
    return result


def tracker_candidates() -> list[dict]:
    found: dict[str, dict] = {}
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; AwesomeAIDealsBot/1.0)"})
    for tracker in TRACKERS:
        try:
            response = session.get(tracker, timeout=25)
            if response.status_code >= 400:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception:
            continue
        tracker_host = urlparse(tracker).netloc
        blocks = []
        for row in soup.select("tr"):
            text = re.sub(r"\s+", " ", row.get_text(" ", strip=True))
            if len(text) > 20 and ("%" in text or "$" in text or "€" in text) and any(w in text.lower() for w in SALE_WORDS):
                blocks.append((row.get_text(" ", strip=True)[:100], row))
        for heading in soup.select("h2, h3, h4"):
            text = re.sub(r"\s+", " ", heading.get_text(" ", strip=True))
            siblings = []
            for sib in heading.find_next_siblings(limit=4):
                if sib.name in {"h2", "h3", "h4"}:
                    break
                siblings.append(sib.get_text(" ", strip=True))
            blob = text + " " + " ".join(siblings)
            if ("%" in blob or "$" in blob or "€" in blob) and any(w in blob.lower() for w in SALE_WORDS):
                blocks.append((text[:100], heading.parent))
        for name_hint, block in blocks:
            links = block.select("a[href]") if hasattr(block, "select") else []
            vendor = None
            for a in links:
                href = a.get("href", "")
                if href.startswith("http") and urlparse(href).netloc != tracker_host:
                    vendor = href
                    break
            if not vendor:
                continue
            name = re.sub(r"\s+", " ", name_hint).strip(" -–—|:")
            if not name or len(name) > 80:
                continue
            key = norm(name)
            if key and key not in found:
                found[key] = {"name": name, "url": vendor, "source": tracker, "raw": block.get_text(" ", strip=True)[:700]}
    return list(found.values())


def campaign_for(text: str) -> str | None:
    text = text.lower()
    for slug, words in {
        "christmas-2026": ["christmas", "holiday"],
        "diwali-2026": ["diwali"],
        "big-billion-days-2026": ["big billion", "billion days"],
        "black-friday-2026": ["black friday", "cyber monday"],
    }.items():
        if any(w in text for w in words):
            return slug
    return None


def discover(fetcher: Fetcher, existing: set[str]) -> tuple[list[dict], list[dict]]:
    verified, leads = [], []
    for candidate in tracker_candidates():
        if norm(candidate["name"]) in existing:
            continue
        campaign = campaign_for(candidate["raw"])
        if not campaign:
            continue
        if len(verified) >= MAX_CANDIDATES:
            leads.append({**candidate, "campaign": campaign, "state": "not-fetched-limit"})
            continue
        status, final_url, text = fetcher.get(candidate["url"])
        lower = text.lower()
        pct = re.search(r"(\d{1,3})\s*%\s*(?:off|discount)?", lower)
        strong = 200 <= status < 400 and pct is not None and any(w in lower for w in sale_words(campaign))
        item = {
            **candidate,
            "campaign": campaign,
            "detected_discount": int(pct.group(1)) if pct else None,
            "vendor_status": status,
            "vendor_url": final_url,
            "excerpt": excerpt_around(text, sale_words(campaign)),
            "state": "vendor-verified" if strong else "needs-review",
        }
        (verified if strong else leads).append(item)
    return verified, leads


def write_reports(summary: dict, results: list[dict], verified: list[dict], leads: list[dict]) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "## Automated deal refresh",
        "",
        f"- Checked: **{summary['checked']}**",
        f"- Re-verified: **{summary['reverified']}**",
        f"- Stale after failed fetch: **{summary['stale']}**",
        f"- Need review: **{summary['conflicting']}**",
        f"- Promoted to live: **{summary['promoted']}**",
        f"- Possible price changes: **{summary['price_candidates']}**",
        f"- New vendor-verified candidates: **{summary['new_candidates']}**",
        "",
        "No price, discount, deadline or expiry was rewritten automatically. Failed fetches become stale, never expired.",
        "",
        "### Checked offers",
        "",
        "| Tool | Outcome | Score | Note |",
        "| --- | --- | --- | --- |",
    ]
    for r in results:
        note = "Possible price change" if r.get("possible_price_change") else (r.get("excerpt", "")[:160].replace("|", "/"))
        lines.append(f"| {r['name']} | {r['outcome']} | {r['score']} | {note} |")
    if verified or leads:
        lines.extend(["", "### New offer candidates", ""])
        for c in verified + leads:
            lines.append(f"- **{c['name']}** — {c['campaign']} — {c['state']} — [source]({c['source']}) — [vendor]({c['url']})")
            lines.append(f"  - {c.get('excerpt', '')[:260]}")
    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    candidate_lines = ["# Deal bot — new offer candidates", ""]
    if not verified and not leads:
        candidate_lines.append("No new vendor-verified candidates in this run.")
    for c in verified + leads:
        candidate_lines.extend([
            f"## {c['name']}",
            "",
            f"- Campaign: `{c['campaign']}`",
            f"- State: **{c['state']}**",
            f"- Detected discount: {c.get('detected_discount') or 'unknown'}%",
            f"- Tracker: {c['source']}",
            f"- Vendor: {c['url']}",
            f"- Excerpt: {c.get('excerpt', '')}",
            "",
        ])
    (OUT / "candidates.md").write_text("\n".join(candidate_lines) + "\n")


def main() -> int:
    data = json.loads(SOURCE.read_text())
    existing = {norm(d["name"]) for d in data["deals"]}
    fetcher = Fetcher()
    results = []
    try:
        for d in due_deals(data):
            results.append(verify(d, fetcher.get(d["url"])))
        verified, leads = discover(fetcher, existing)
    finally:
        fetcher.close()

    metadata_fields = {"last_verified", "next_check", "verification", "evidence"}
    original = json.loads(SOURCE.read_text())
    before = {d["id"]: d for d in original["deals"]}
    content_changes = []
    for d in data["deals"]:
        old = before.get(d["id"], {})
        if old == d:
            continue
        changed = {k for k in set(old) | set(d) if old.get(k) != d.get(k)}
        if not changed <= metadata_fields:
            content_changes.append({"name": d["name"], "fields": sorted(changed)})
    if data != original:
        SOURCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    summary = {
        "date": TODAY.isoformat(),
        "checked": len(results),
        "reverified": sum(r["outcome"] == "reverified" for r in results),
        "stale": sum(r["outcome"] == "stale-fetch" for r in results),
        "conflicting": sum(r["outcome"] == "needs-review" for r in results),
        "promoted": sum(r["outcome"] == "promoted-to-live" for r in results),
        "price_candidates": sum(bool(r.get("possible_price_change")) for r in results),
        "new_candidates": len(verified),
        "verification_only": not content_changes and not verified and not leads,
        "content_changes": content_changes,
    }
    write_reports(summary, results, verified, leads)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
