#!/usr/bin/env python3
"""Generate static, SEO-readable pages and feeds from data/deals.json.

The JSON remains the single source of truth. JavaScript enhances these pages;
it is not required for search engines or no-JS visitors to see the deals.
"""
from __future__ import annotations

import html
import json
from collections import Counter
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "deals.json").read_text())
TEMPLATE = (ROOT / "templates" / "base.html").read_text()
META = DATA["meta"]
TODAY = date.fromisoformat(META["generated"])
BASE_URL = "https://singahi1.github.io/awesome-ai-blackfriday/"


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def fmt_date(value: str | None, year: bool = False) -> str:
    if not value:
        return "—"
    d = date.fromisoformat(value)
    return d.strftime("%-d %b %Y" if year else "%-d %b")


def days_left(value: str | None) -> int | None:
    if not value:
        return None
    return (date.fromisoformat(value) - TODAY).days


def end_label(d: dict) -> str:
    n = days_left(d.get("valid_until"))
    if d.get("lifecycle") == "expired":
        return "Ended " + fmt_date(d.get("valid_until"))
    if n == 0:
        return "Ends today"
    if n == 1:
        return "Ends tomorrow"
    if n is not None and n < 0:
        return "Ended " + fmt_date(d.get("valid_until"))
    if n is not None and n <= 14:
        return f"{n} days left"
    if d.get("valid_until"):
        return "Ends " + fmt_date(d.get("valid_until"))
    return "No end date"


def end_class(d: dict) -> str:
    n = days_left(d.get("valid_until"))
    if d.get("lifecycle") == "expired" or (n is not None and n < 0):
        return "gone"
    if n == 0 or n == 1:
        return "hot"
    if n is not None and n <= 7:
        return "warm"
    if n is None:
        return "open"
    return ""


def card(d: dict) -> str:
    dl = days_left(d.get("valid_until"))
    cls = end_class(d)
    disc = (
        f'<div class="disc">{d["discount"]}%<span style="font-size:11px;opacity:.6"> off</span></div>'
        if isinstance(d.get("discount"), (int, float))
        else f'<div class="disc na">{esc(d.get("offer_type") or "no %")}</div>'
    )
    price = ""
    if d.get("price_before") or d.get("price_after"):
        price = (
            '<div class="price">'
            + (f'<span class="before">{esc(d["price_before"])}</span><span class="arrow">→</span>' if d.get("price_before") else "")
            + f'<span class="after">{esc(d.get("price_after") or "")}</span></div>'
        )
    code = ""
    if d.get("code"):
        code = (
            '<div class="code-row"><button class="code" data-code="'
            + esc(d["code"])
            + '" title="Click to copy"><span>'
            + esc(d["code"])
            + '</span><span class="hint">copy code</span></button></div>'
        )
    pills = []
    if d.get("sponsored"):
        pills.append('<span class="tagpill pick">Partner</span>')
    if d.get("lifecycle") == "announced":
        pills.append('<span class="tagpill">announced</span>')
    if d.get("verification") == "stale":
        pills.append('<span class="tagpill stale">recheck due</span>')
    if d.get("verification") == "conflicting":
        pills.append('<span class="tagpill stale">conflicting</span>')
    for tag in d.get("tags", []):
        if tag in {"announced", "partner", "perk", "expired"}:
            continue
        pills.append('<span class="tagpill pick">Editor’s pick</span>' if tag == "editor-pick" else f'<span class="tagpill">{esc(tag)}</span>')
    if d.get("regions"):
        pills.append(f'<span class="tagpill">{esc(", ".join(d["regions"]))}</span>')
    evidence = (d.get("evidence") or [{}])[-1]
    evidence_type = evidence.get("type", "tracker")
    evidence_url = evidence.get("url", d["source"])
    evidence_label = "vendor" if evidence_type.startswith("vendor_") else "tracker"
    classes = [
        "card",
        "ending" if cls in {"hot", "warm"} else "",
        "expired-card" if d.get("lifecycle") == "expired" else "",
        "stale-card" if d.get("verification") == "stale" else "",
        "sponsored" if d.get("sponsored") else "",
    ]
    return (
        f'<article class="{" ".join(c for c in classes if c)}">'
        f'<a class="stretched" href="{esc(d["url"])}" target="_blank" rel="noopener" aria-label="Open {esc(d["name"])} offer"></a>'
        '<div class="card-head">'
        f'<span class="cat">{esc(d["category"])}</span>{disc}</div>'
        f'<h3>{esc(d["name"])}</h3>'
        f'<p class="what">{esc(d["what"])}</p>'
        f'<p class="deal">{esc(d["deal"])}</p>'
        f'{price}{code}'
        + (f'<p class="renewal">{esc(d["renewal"])}</p>' if d.get("renewal") else "")
        + '<div class="meta">'
        + f'<span class="ends {cls}" title="{esc(d.get("ends_note") or "")}">{esc(end_label(d))}</span>'
        + "".join(pills)
        + '</div><p class="src">'
        + f'<a href="{esc(d["url"])}" target="_blank" rel="noopener">vendor ↗</a>'
        + f'<a href="{esc(evidence_url)}" target="_blank" rel="noopener">source · {esc(fmt_date(d.get("last_verified")))} ({evidence_label})</a>'
        + '</p></article>'
    )


def chips(deals: list[dict]) -> str:
    counts = Counter(d["category"] for d in deals)
    out = [f'<button class="chip" data-cat="All" aria-pressed="true">All<small>{len(deals)}</small></button>']
    for category in DATA["categories"]:
        if counts.get(category):
            out.append(f'<button class="chip" data-cat="{esc(category)}" aria-pressed="false">{esc(category)}<small>{counts[category]}</small></button>')
    return "".join(out)


def stats(deals: list[dict], view: str) -> str:
    live = [d for d in deals if d.get("lifecycle") == "live"]
    top = sorted(live or deals, key=lambda d: d.get("useful", 0), reverse=True)[0] if deals else {}
    ending = []
    for d in live:
        n = days_left(d.get("valid_until"))
        if n is not None and 0 <= n <= 7:
            ending.append(d)
    stale = [d for d in live if d.get("verification") == "stale"]
    if view == "archive":
        expiries: list[str] = [d["valid_until"] for d in deals if isinstance(d.get("valid_until"), str)]
        items = [
            (len(deals), "expired offers", False),
            (len({d.get("campaign") or "other" for d in deals}), "campaigns", False),
            (fmt_date(max(expiries) if expiries else None), "latest expiry", True),
            (fmt_date(min(expiries) if expiries else None), "oldest expiry", False),
        ]
    elif view == "campaign":
        announced = [d for d in deals if d.get("lifecycle") == "announced"]
        items = [
            (len(live), "live offers", False),
            (top.get("useful", "—"), "top pick: " + top.get("name", "—"), True),
            (len(ending), "ending in 7 days", False),
            (len(announced), "announced", False),
        ]
    else:
        items = [
            (len(live), "live deals", False),
            (top.get("useful", "—"), "top pick: " + top.get("name", "—"), True),
            (len(ending), "ending in 7 days", False),
            (len(stale), "recheck due", False),
        ]
    return "".join(
        f'<div class="stat{" acid" if acid else ""}"><b>{esc(value)}</b><span>{esc(label)}</span></div>'
        for value, label, acid in items
    )


def ticker(deals: list[dict]) -> str:
    top = sorted(deals, key=lambda d: d.get("useful", 0), reverse=True)[:9]
    line = "".join(f'<span><b>{esc(d.get("useful", "—"))}</b> {esc(d["name"])}</span>' for d in top)
    return f'<div class="ticker-track">{line}{line}</div>'


def nodeal_section() -> str:
    rows = "".join(
        f'<tr><td><a href="{esc(n["url"])}" target="_blank" rel="noopener">{esc(n["name"])}</a></td>'
        f'<td>{esc(n["note"])}</td><td>{esc(fmt_date(n.get("last_verified")))}</td></tr>'
        for n in DATA["no_deal"]
    )
    return (
        '<section class="wrap block" id="nodeal"><h2>The big names that <span class="strike">aren’t</span> discounting</h2>'
        '<p class="sub">Checked on the dates shown. A live-looking banner that leads to an expired page does not count.</p>'
        '<div class="tablewrap"><table class="plain" id="nodeal-table"><thead><tr><th>Tool</th><th>What we found</th><th>Checked</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div></section>'
    )


def notes_section(include_watch: bool = True) -> str:
    watch = ""
    if include_watch:
        items = "".join(
            f'<li><b><a href="{esc(w["url"])}" target="_blank" rel="noopener">{esc(w["name"])}</a></b>{esc(w["note"])}</li>'
            for w in DATA["watchlist"]
        )
        watch = f'<div><h2>Watching — not live yet</h2><ul class="notes" id="watchlist">{items}</ul></div>'
    standing = "".join(
        f'<li><b><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["name"])}</a></b>'
        f'<span class="kind">{esc(a["kind"])}</span><br>{esc(a["note"])}</li>'
        for a in DATA["always_on"]
    )
    return f'<section class="wrap block two-col">{watch}<div><h2>Standing discounts</h2><ul class="notes" id="always-on">{standing}</ul></div></section>'


def season_strip(view: str) -> str:
    if view == "campaign":
        return (
            '<div class="season-strip"><div><span>Live campaign</span><b>Black Friday 2026</b></div>'
            '<div><span>Cyber Monday</span><b>30 Nov 2026</b></div>'
            '<div><span>Next up</span><b>Christmas 2026 — collecting verified offers</b></div></div>'
        )
    if view == "archive":
        return '<div class="season-strip"><div><span>Archive</span><b>Expired offers retained for price history</b></div><div><span>Live now</span><b><a href="../">Back to current deals</a></b></div></div>'
    return (
        '<div class="season-strip"><div><span>Live campaign</span><b><a href="black-friday/">Black Friday 2026 · ends 27 Nov</a></b></div>'
        '<div><span>Next up</span><b>Christmas 2026 — collecting verified offers</b></div>'
        '<div><span>Year-round</span><b><a href="archive/">Expired-deal archive</a></b></div></div>'
    )


def render_page(view: str, campaign: str | None, deals: list[dict]) -> str:
    is_root = view == "home"
    prefix = "" if is_root else "../"
    base_href = "./" if is_root else "../"
    if view == "campaign":
        title = "Black Friday AI Deals 2026 — Awesome AI Deals"
        description = "Verified Black Friday and Cyber Monday 2026 deals on AI, coding, video, voice, writing and hosting tools."
        hero_title = 'Black Friday deals that are <em>actually</em> on sale.'
        hero_lede = "Every offer carries its price before and after, deadline, renewal terms, evidence source and last-verified date. Percentage is optional; usefulness is the default order."
    elif view == "archive":
        title = "Expired AI Deals Archive — Awesome AI Deals"
        description = "Expired AI and software offers retained for price history and verification."
        hero_title = 'The archive: deals that have <em>ended</em>.'
        hero_lede = "Nothing here is presented as live. Expired offers stay searchable so price claims can be audited instead of quietly disappearing."
    else:
        title = "Awesome AI Deals 2026 — Live, Verified Discounts"
        description = "A year-round list of useful AI and software deals, ranked by usefulness with prices, deadlines, renewal terms and dated evidence."
        hero_title = 'AI deals worth knowing about — <em>all year</em>.'
        hero_lede = "Live offers, standing discounts and seasonal campaigns in one place. Every row carries evidence, a last-verified date and a next check. Usefulness comes first; percentage is optional."
    canonical = BASE_URL if is_root else BASE_URL + ("black-friday/" if view == "campaign" else "archive/")
    count_label = (
        f"{len(deals)} expired offers" if view == "archive"
        else f"{sum(d['lifecycle'] == 'live' for d in deals)} live offers · {len(deals)} total"
    )
    replacements = {
        "PAGE_TITLE": title,
        "PAGE_DESCRIPTION": description,
        "OG_TITLE": title,
        "OG_DESCRIPTION": description,
        "CANONICAL": canonical,
        "PREFIX": prefix,
        "BASE_HREF": base_href,
        "VIEW": view,
        "CAMPAIGN": campaign or "",
        "SNAPSHOT": META["generated"],
        "UPDATED": "Snapshot " + fmt_date(META["generated"], year=True),
        "HERO_TITLE": hero_title,
        "HERO_LEDE": hero_lede,
        "STATIC_STATS": stats(deals, view),
        "STATIC_TICKER": ticker(deals),
        "SEASON_STRIP": season_strip(view),
        "STALE_CONTROL": "" if view == "archive" else '<label class="switch"><input type="checkbox" id="hide-stale"><span>Hide stale</span></label>',
        "STATIC_CHIPS": chips(deals),
        "STATIC_COUNT": count_label,
        "STATIC_CARDS": "".join(card(d) for d in sorted(deals, key=lambda d: (-d.get("useful", 0), d["name"]))),
        "NODEAL_SECTION": nodeal_section() if view == "campaign" else "",
        "WATCHLIST_SECTION": notes_section(include_watch=True) if view in {"home", "campaign"} else "",
        "ALWAYS_ON_SECTION": "" if view in {"home", "campaign"} else "",
        "CHECKED_WINDOW": META["checked_window"],
        "FOOT_DATE": fmt_date(META["generated"], year=True),
    }
    # WATCHLIST_SECTION already includes standing discounts; avoid a duplicate placeholder.
    replacements["ALWAYS_ON_SECTION"] = ""
    page = TEMPLATE
    for key, value in replacements.items():
        page = page.replace("{{" + key + "}}", value)
    page = "\n".join(line.rstrip() for line in page.splitlines()) + "\n"
    return page


def write_feeds() -> None:
    live = sorted(
        [d for d in DATA["deals"] if d.get("lifecycle") == "live"],
        key=lambda d: (-d.get("useful", 0), d["name"]),
    )[:50]
    items = []
    for d in live:
        title = f"{d['name']}: {d['deal']}"
        description = (
            f"{d.get('price_before') or ''} → {d.get('price_after') or ''}. "
            f"{d.get('renewal') or ''} Ends: {end_label(d)}. "
            f"Evidence: {d['source']} (checked {fmt_date(d.get('last_verified'), year=True)})."
        )
        pub = datetime.combine(date.fromisoformat(d["last_verified"]), datetime.min.time(), tzinfo=timezone.utc)
        items.append(
            "<item>"
            f"<title>{esc(title)}</title>"
            f"<link>{esc(d['url'])}</link>"
            f"<guid isPermaLink=\"true\">{esc(d['url'])}</guid>"
            f"<description>{esc(description)}</description>"
            f"<pubDate>{format_datetime(pub)}</pubDate>"
            f"<category>{esc(d['category'])}</category>"
            "</item>"
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0"><channel>'
        '<title>Awesome AI Deals</title>'
        f'<link>{BASE_URL}</link>'
        '<description>Useful AI and software deals with dated evidence and renewal terms.</description>'
        '<language>en</language>'
        + "".join(items)
        + '</channel></rss>'
    )
    (ROOT / "feed.xml").write_text(rss + "\n")
    urls = [BASE_URL, BASE_URL + "black-friday/", BASE_URL + "archive/"]
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc><lastmod>{META['generated']}</lastmod></url>" for u in urls)
        + '</urlset>'
    )
    (ROOT / "sitemap.xml").write_text(sitemap + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")


def main() -> None:
    home = [d for d in DATA["deals"] if d.get("lifecycle") == "live"]
    campaign = [d for d in DATA["deals"] if d.get("campaign") == META["current_campaign"] and d.get("lifecycle") in {"live", "announced"}]
    archive = [d for d in DATA["deals"] if d.get("lifecycle") in {"expired", "archived"}]
    (ROOT / "index.html").write_text(render_page("home", None, home))
    (ROOT / "black-friday").mkdir(exist_ok=True)
    (ROOT / "black-friday" / "index.html").write_text(render_page("campaign", META["current_campaign"], campaign))
    (ROOT / "archive").mkdir(exist_ok=True)
    (ROOT / "archive" / "index.html").write_text(render_page("archive", None, archive))
    write_feeds()
    print(f"built home ({len(home)} live), black-friday ({len(campaign)}), archive ({len(archive)}), RSS and sitemap")


if __name__ == "__main__":
    main()
