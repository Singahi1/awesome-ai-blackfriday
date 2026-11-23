#!/usr/bin/env python3
"""Regenerate README.md from data/deals.json so the repo and the site never drift."""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "data", "deals.json")))
deals, meta = data["deals"], data["meta"]


def fmt_end(iso):
    if not iso:
        return "—"
    d = date.fromisoformat(iso)
    return d.strftime("%-d %b")


def pct(d):
    return f"**{d['discount']}%**" if isinstance(d.get("discount"), int) else "—"


def price(d):
    if d.get("price_before") and d.get("price_after"):
        return f"{d['price_before']} → {d['price_after']}"
    return d.get("price_after") or "—"


lines = []
lines.append("# Awesome AI Black Friday Deals [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)\n")
lines.append(
    "> A curated list of Black Friday and Cyber Monday deals on AI tools — chat, coding, image, video, "
    "voice, writing and research. Every row was read on the **vendor's own pricing or offer-terms page**, "
    "with the date it was checked, the price before and after, and what the plan renews at.\n"
)
OWNER = os.environ.get("GH_OWNER", "Singahi1")
REPO = os.environ.get("GH_REPO", "awesome-ai-blackfriday")

lines.append(
    f"**[Browse the filterable site →](https://{OWNER}.github.io/{REPO}/)** · "
    f"**{len(deals)} deals** · snapshot {meta['generated']} · "
    f"Black Friday {meta['black_friday']} · Cyber Monday {meta['cyber_monday']}\n"
)
lines.append(
    "No affiliate links. No coupon-site folklore. If a vendor's page doesn't state the offer, it isn't here — "
    "that's why ChatGPT, Claude, Cursor and Midjourney appear in [the no-deal table](#-verified-no-deal) "
    "instead of the list.\n"
)
lines.append(
    "**Supported by [Singahi](https://singahi.com)** — compliance (ISO 27001, SOC 2), penetration testing and "
    "managed security for growing companies. Readers get **30% off all services**; the row is marked as a "
    "partner offer, because it is one.\n"
)

lines.append("## Contents\n")
for c in data["categories"]:
    anchor = c.lower().replace(" & ", "--").replace(" ", "-")
    lines.append(f"- [{c}](#{anchor})")
lines.append("- [Verified: no deal](#-verified-no-deal)")
lines.append("- [Watching / not live yet](#-watching--not-live-yet)")
lines.append("- [Standing discounts](#-standing-discounts)")
lines.append("- [Method](#method)\n")

for c in data["categories"]:
    rows = [d for d in deals if d["category"] == c]
    if not rows:
        continue
    lines.append(f"## {c}\n")
    lines.append("| Tool | Deal | Before → after | Code | Ends | Checked |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for d in sorted(rows, key=lambda x: -(x.get("discount") or 0)):
        name = f"[{d['name']}]({d['url']})"
        deal = d["deal"].replace("|", "\\|")
        if d.get("sponsored"):
            deal = "**Partner offer** — " + deal
        code = f"`{d['code']}`" if d.get("code") else "—"
        end = fmt_end(d.get("ends")) + ("*" if d.get("ends_note") else "")
        lines.append(f"| {name} | {deal} | {price(d)} | {code} | {end} | {fmt_end(d['verified'])} |")
    lines.append("")

lines.append("## 🚫 Verified: no deal\n")
lines.append("Vendors whose own pricing pages showed **no** Black Friday offer on the date checked. "
             "Any coupon site claiming otherwise is guessing, recycling last year, or monetising your click.\n")
lines.append("| Tool | What we found | Checked |")
lines.append("| --- | --- | --- |")
for n in data["no_deal"]:
    lines.append(f"| [{n['name']}]({n['url']}) | {n['note'].replace('|', chr(92) + '|')} | {fmt_end(n['checked'])} |")
lines.append("")

lines.append("## 👀 Watching / not live yet\n")
for w in data["watchlist"]:
    lines.append(f"- **[{w['name']}]({w['url']})** — {w['note']}")
lines.append("")

lines.append("## ♾️ Standing discounts\n")
lines.append("Not Black Friday, but they never expire and they're usually better than the flash sale.\n")
for a in data["always_on"]:
    lines.append(f"- **[{a['name']}]({a['url']})** _({a['kind'].lower()})_ — {a['note']}")
lines.append("")

lines.append("""## Method

1. **Vendor page or nothing.** A deal is listed only if the vendor's own pricing, promo or terms page states
   it. Banners that lead to expired pages, newsletters and coupon aggregators are excluded.
2. **Dated, not timeless.** Every row carries the date it was checked. Last year's discount is not this
   year's offer.
3. **The renewal price is the point.** A $0.29 first month that renews at $15 is a one-month coupon, not a
   deal. Where the vendor prints a renewal price, it's in the row (marked with `*` when the end date was
   inferred from offer terms).
4. **First-party links only.** No affiliate tags, no redirects, no paid placement.

Prices change hourly during Black Friday week — always confirm at checkout.

## Contributing

Found a deal that meets the bar, or one that has ended? See [CONTRIBUTING.md](CONTRIBUTING.md).
The dataset lives in [`data/deals.json`](data/deals.json) and a PR only needs to touch that file.

## License

[MIT](LICENSE) for the code, [CC0](https://creativecommons.org/publicdomain/zero/1.0/) for the data.
""")

out = os.path.join(ROOT, "README.md")
with open(out, "w") as f:
    f.write("\n".join(lines).rstrip() + "\n")
print(f"wrote README.md with {len(deals)} deals")
