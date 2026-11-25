#!/usr/bin/env python3
"""Print a Markdown freshness queue without changing any deal data."""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "deals.source.json").read_text())
today = date.today()


def parse(value):
    return date.fromisoformat(value) if value else None


due = []
ending = []
for d in data["deals"]:
    if d.get("lifecycle") not in {"live", "announced"}:
        continue
    next_check = parse(d.get("next_check"))
    until = parse(d.get("valid_until"))
    if d.get("verification") == "stale" or (next_check and next_check <= today):
        due.append(d)
    if until and today <= until <= today + timedelta(days=7):
        ending.append(d)

print(f"# Freshness queue — {today.isoformat()}\n")
print(f"**{len(due)} offers need re-checking.** A failed fetch means stale, not expired.\n")
if due:
    print("| Tool | Lifecycle | Last verified | Next check | Ends | Source |")
    print("| --- | --- | --- | --- | --- | --- |")
    for d in sorted(due, key=lambda x: (x.get("next_check") or "9999", x["name"])):
        print(f"| [{d['name']}]({d['url']}) | {d['lifecycle']} | {d.get('last_verified') or '—'} | {d.get('next_check') or '—'} | {d.get('valid_until') or '—'} | [evidence]({d['source']}) |")
print("\n## Ending in the next 7 days\n")
if ending:
    for d in sorted(ending, key=lambda x: x["valid_until"]):
        print(f"- **{d['name']}** — {d['valid_until']} — {d['deal']}")
else:
    print("None.")
