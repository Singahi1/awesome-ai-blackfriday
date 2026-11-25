#!/usr/bin/env python3
"""Regenerate README.md from the canonical year-round dataset."""
import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "deals.json").read_text())
deals, meta = data["deals"], data["meta"]
OWNER = os.environ.get("GH_OWNER", "Singahi1")
REPO = os.environ.get("GH_REPO", "awesome-ai-blackfriday")
SITE = f"https://{OWNER}.github.io/{REPO}/"


def fmt(value):
    return date.fromisoformat(value).strftime("%-d %b") if value else "—"


def row(d):
    name = f"[{d['name']}]({d['url']})"
    deal = d["deal"].replace("|", "\\|")
    if d.get("sponsored"):
        deal = "**Partner offer** — " + deal
    if d.get("lifecycle") == "expired":
        deal = "**Expired** — " + deal
    price = f"{d.get('price_before')} → {d.get('price_after')}" if d.get("price_before") and d.get("price_after") else (d.get("price_after") or "—")
    code = f"`{d['code']}`" if d.get("code") else "—"
    evidence = (d.get("evidence") or [{}])[0].get("type", "tracker")
    evidence = "vendor" if evidence.startswith("vendor_") else "tracker"
    return f"| {name} | {deal} | {price} | {code} | {fmt(d.get('valid_until'))} | {fmt(d.get('last_verified'))} ({evidence}) |"


def table(rows):
    out = ["| Tool | Deal | Before → after | Code | Ends | Checked |", "| --- | --- | --- | --- | --- | --- |"]
    out.extend(row(d) for d in sorted(rows, key=lambda x: (-x.get("useful", 0), x["name"])))
    return out


live = [d for d in deals if d["lifecycle"] == "live"]
announced = [d for d in deals if d["lifecycle"] == "announced"]
expired = [d for d in deals if d["lifecycle"] in {"expired", "archived"}]
stale = [d for d in live if d["verification"] == "stale"]

lines = [
    "# Awesome AI Deals [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)",
    "",
    "> A year-round list of useful AI and software deals — live offers, standing discounts and seasonal campaigns — with prices, deadlines, renewal terms and dated evidence.",
    "",
    f"**[Browse the site →]({SITE})** · **[RSS]({SITE}feed.xml)** · **[JSON]({SITE}data/deals.json)**",
    f"**{len(live)} live** · {len(announced)} announced · {len(expired)} expired · {len(stale)} recheck due · snapshot {meta['generated']}",
    "",
    "**Current campaign:** [Black Friday 2026](https://singahi1.github.io/awesome-ai-blackfriday/black-friday/) — November 27.",
    "**Next up:** Christmas 2026 — collecting verified offers; no thin page launched yet.",
    "",
    "**Supported by [Singahi](https://singahi.com)** — compliance (ISO 27001, SOC 2), penetration testing and managed security. Readers get **30% off all services**; the row is marked as a partner offer, because it is one.",
    "",
    "## Contents",
    "",
]
for category in data["categories"]:
    if any(d["category"] == category for d in live):
        lines.append(f"- [{category}](#{category.lower().replace(' & ', '--').replace(' ', '-')})")
lines.extend([
    "- [Announced](#announced)",
    "- [Expired archive](#expired-archive)",
    "- [Verified: no deal](#-verified-no-deal)",
    "- [Standing discounts](#standing-discounts)",
    "- [Method](#method)",
    "- [Contributing](#contributing)",
    "",
    "## Live now",
    "",
    "Default order is **usefulness**, not percentage. `recheck due` means the stored next-check date has passed; it does not mean the offer is expired.",
    "",
])
for category in data["categories"]:
    rows = [d for d in live if d["category"] == category]
    if not rows:
        continue
    lines.extend([f"## {category}", ""])
    lines.extend(table(rows))
    lines.append("")

lines.extend(["## Announced", ""])
lines.extend(table(announced))
lines.extend(["", "## Expired archive", "", "Retained for price history; nothing here is presented as live.", ""])
lines.extend(table(expired))
lines.extend([
    "",
    "## 🚫 Verified: no deal",
    "",
    "| Tool | What we found | Checked |",
    "| --- | --- | --- |",
])
for n in data["no_deal"]:
    lines.append(f"| [{n['name']}]({n['url']}) | {n['note'].replace('|', chr(92) + '|')} | {fmt(n.get('last_verified'))} |")
lines.extend(["", "## Standing discounts", "", "Not Black Friday, but they never expire.", ""])
for a in data["always_on"]:
    lines.append(f"- **[{a['name']}]({a['url']})** _({a['kind'].lower()})_ — {a['note']}")
lines.extend([
    "",
    "## Method",
    "",
    "1. **Evidence, not folklore.** Vendor pricing pages and offer terms come first. Dated trackers are labelled `(tracker)` on each row; vendor-owned sources are labelled `(vendor)`.",
    "2. **Lifecycle is explicit.** `announced`, `scheduled`, `live`, `expired` and `archived` are separate from verification state. A blocked page becomes `stale`, not `expired`.",
    "3. **Freshness is stored.** Every deal has `last_verified`, `next_check`, an evidence excerpt and a price-history entry.",
    "4. **Renewal terms matter.** A first-month price that renews high is a coupon, not a deal. Where the vendor prints the renewal price, it is recorded.",
    "5. **Usefulness first.** Audience breadth, price quality, renewal risk and friction determine the default order. Percentage remains an optional sort.",
    "6. **Sponsorship is separated.** Partner offers are labelled and do not buy an editorial ranking.",
    "",
    "## Contributing",
    "",
    "Edit **`data/deals.source.json`** — it is the canonical, human-editable source. Do not edit `data/deals.json`, `data/deals.js`, `README.md`, `index.html`, `black-friday/index.html`, `archive/index.html`, `feed.xml` or `sitemap.xml` directly; they are generated.",
    "",
    "```bash",
    "python3 scripts/dataset.py",
    "python3 scripts/validate.py",
    "python3 scripts/build_readme.py",
    "python3 scripts/build_site.py",
    "```",
    "",
    "CI regenerates every artifact and fails if the diff is not committed. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [deal submission form](https://github.com/Singahi1/awesome-ai-blackfriday/issues/new?template=deal-submission.yml).",
    "",
    "## License",
    "",
    "[MIT](LICENSE) for the code, [CC0](https://creativecommons.org/publicdomain/zero/1.0/) for the data.",
    "",
])
(ROOT / "README.md").write_text("\n".join(lines).rstrip() + "\n")
print(f"wrote README.md with {len(live)} live, {len(announced)} announced, {len(expired)} expired")
