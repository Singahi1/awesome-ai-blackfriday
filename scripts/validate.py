#!/usr/bin/env python3
"""Validate data/deals.json — fails CI on malformed rows, dead structure or stale metadata."""
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "deals.json")

errors = []
data = json.load(open(PATH))

REQUIRED = ["id", "name", "category", "what", "deal", "status", "url", "source", "verified"]
STATUSES = {"live", "standing", "perk", "upcoming", "expired", "announced"}

if not isinstance(data.get("deals"), list) or not data["deals"]:
    errors.append("deals must be a non-empty list")

seen = set()
for i, d in enumerate(data.get("deals", [])):
    where = f"deals[{i}] ({d.get('name', '?')})"
    for f in REQUIRED:
        if not d.get(f):
            errors.append(f"{where}: missing {f}")
    if d.get("id") in seen:
        errors.append(f"{where}: duplicate id {d.get('id')}")
    seen.add(d.get("id"))
    if d.get("category") not in data.get("categories", []):
        errors.append(f"{where}: unknown category {d.get('category')!r}")
    if d.get("status") not in STATUSES:
        errors.append(f"{where}: bad status {d.get('status')!r}")
    for f in ("url", "source"):
        if d.get(f) and not re.match(r"^https?://", d[f]):
            errors.append(f"{where}: {f} is not an http(s) URL")
    for f in ("verified", "ends"):
        v = d.get(f)
        if v is not None and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(v)):
            errors.append(f"{where}: {f} must be YYYY-MM-DD, got {v!r}")
        elif v:
            try:
                date.fromisoformat(v)
            except ValueError:
                errors.append(f"{where}: {f} is not a real date: {v}")
    if d.get("discount") is not None:
        if not isinstance(d["discount"], (int, float)) or not 0 < d["discount"] <= 100:
            errors.append(f"{where}: discount must be 0 < n <= 100")

for s in ("no_deal", "watchlist", "always_on"):
    if not isinstance(data.get(s), list) or not data[s]:
        errors.append(f"{s} must be a non-empty list")

if errors:
    print(f"✗ {len(errors)} problem(s) in data/deals.json\n")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print(f"✓ data/deals.json valid — {len(data['deals'])} deals, "
      f"{len(data['no_deal'])} no-deal rows, {len(data['watchlist'])} watched")
