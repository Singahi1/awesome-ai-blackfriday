#!/usr/bin/env python3
"""Validate the canonical year-round deal source (schema v2)."""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "data" / "deals.source.json"
data = json.loads(PATH.read_text())
errors = []

LIFECYCLES = {"announced", "scheduled", "live", "expired", "archived"}
VERIFICATIONS = {"verified", "stale", "unverified", "conflicting", "reported", "announced", "standing"}
OFFER_TYPES = {"seasonal", "evergreen", "lifetime", "recurring", "partner", "perk", "referral", "student"}
EVIDENCE_TYPES = {"vendor_page", "vendor_terms", "vendor_email", "vendor_social", "tracker", "community"}
REQUIRED = [
    "id", "name", "category", "what", "deal", "lifecycle", "verification",
    "offer_type", "campaign", "regions", "currency", "tax_inclusive",
    "eligibility", "first_seen", "last_verified", "next_check", "valid_until",
    "evidence", "price_history", "useful", "url", "source", "sponsored",
    "tags", "renewal", "discount", "price_before", "price_after", "code", "ends_note",
]


def iso(value, where, field, nullable=True):
    if value is None and nullable:
        return
    if not isinstance(value, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        errors.append(f"{where}: {field} must be YYYY-MM-DD, got {value!r}")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{where}: {field} is not a real date: {value}")


def http(value, where, field):
    if not isinstance(value, str) or not re.match(r"^https?://", value):
        errors.append(f"{where}: {field} must be an http(s) URL")


if data.get("schema_version") != 2:
    errors.append("schema_version must be 2")
for field in ("title", "generated", "checked_window", "current_campaign", "upcoming_campaign"):
    if not data.get("meta", {}).get(field):
        errors.append(f"meta: missing {field}")
iso(data.get("meta", {}).get("generated"), "meta", "generated", nullable=False)

if not isinstance(data.get("deals"), list) or not data["deals"]:
    errors.append("deals must be a non-empty list")
seen_ids, seen_names = set(), set()
for i, d in enumerate(data.get("deals", [])):
    where = f"deals[{i}] ({d.get('name', '?')})"
    for field in REQUIRED:
        if field not in d:
            errors.append(f"{where}: missing {field}")
    if d.get("id") in seen_ids:
        errors.append(f"{where}: duplicate id {d.get('id')}")
    if d.get("name") in seen_names:
        errors.append(f"{where}: duplicate name {d.get('name')}")
    seen_ids.add(d.get("id")); seen_names.add(d.get("name"))
    if d.get("category") not in data.get("categories", []):
        errors.append(f"{where}: unknown category {d.get('category')!r}")
    if d.get("lifecycle") not in LIFECYCLES:
        errors.append(f"{where}: invalid lifecycle {d.get('lifecycle')!r}")
    if d.get("verification") not in VERIFICATIONS:
        errors.append(f"{where}: invalid verification {d.get('verification')!r}")
    if d.get("offer_type") not in OFFER_TYPES:
        errors.append(f"{where}: invalid offer_type {d.get('offer_type')!r}")
    if d.get("campaign") is not None and not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", d["campaign"]):
        errors.append(f"{where}: campaign must be a lowercase slug or null")
    if not isinstance(d.get("regions"), list) or any(not isinstance(r, str) or not r for r in d.get("regions", [])):
        errors.append(f"{where}: regions must be a list of non-empty strings")
    if d.get("currency") is not None and not re.match(r"^[A-Z]{3}$", d["currency"]):
        errors.append(f"{where}: currency must be a 3-letter ISO code or null")
    if d.get("tax_inclusive") is not None and not isinstance(d["tax_inclusive"], bool):
        errors.append(f"{where}: tax_inclusive must be boolean or null")
    for field in ("first_seen", "last_verified", "next_check", "valid_until"):
        iso(d.get(field), where, field)
    if d.get("last_verified") and d.get("first_seen") and d["first_seen"] > d["last_verified"]:
        errors.append(f"{where}: first_seen is after last_verified")
    if d.get("next_check") and d.get("last_verified") and d["next_check"] < d["last_verified"]:
        errors.append(f"{where}: next_check is before last_verified")
    if d.get("lifecycle") == "expired" and not d.get("valid_until"):
        errors.append(f"{where}: expired deals require valid_until")
    http(d.get("url"), where, "url"); http(d.get("source"), where, "source")
    evidence = d.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{where}: evidence must be a non-empty list")
    else:
        for j, e in enumerate(evidence):
            ew = f"{where}.evidence[{j}]"
            if e.get("type") not in EVIDENCE_TYPES:
                errors.append(f"{ew}: invalid evidence type {e.get('type')!r}")
            http(e.get("url"), ew, "url"); iso(e.get("checked_at"), ew, "checked_at", nullable=False)
            if not e.get("excerpt"):
                errors.append(f"{ew}: missing excerpt")
    if not isinstance(d.get("price_history"), list):
        errors.append(f"{where}: price_history must be a list")
    else:
        for j, h in enumerate(d["price_history"]):
            iso(h.get("observed_at"), f"{where}.price_history[{j}]", "observed_at", nullable=False)
    if not isinstance(d.get("useful"), (int, float)) or not 0 <= d["useful"] <= 100:
        errors.append(f"{where}: useful must be 0..100")
    if d.get("discount") is not None and (not isinstance(d["discount"], (int, float)) or not 0 < d["discount"] <= 100):
        errors.append(f"{where}: discount must be 0 < n <= 100 or null")
    if not isinstance(d.get("sponsored"), bool):
        errors.append(f"{where}: sponsored must be boolean")
    if d.get("sponsored") and d.get("offer_type") != "partner":
        errors.append(f"{where}: sponsored deals must use offer_type=partner")
    if not isinstance(d.get("tags"), list):
        errors.append(f"{where}: tags must be a list")

for section in ("no_deal", "watchlist", "always_on"):
    if not isinstance(data.get(section), list) or not data[section]:
        errors.append(f"{section} must be a non-empty list")
for i, n in enumerate(data.get("no_deal", [])):
    where = f"no_deal[{i}]"
    for field in ("name", "note", "url", "last_verified", "campaign", "evidence"):
        if field not in n:
            errors.append(f"{where}: missing {field}")
    http(n.get("url"), where, "url"); iso(n.get("last_verified"), where, "last_verified", nullable=False)
for i, w in enumerate(data.get("watchlist", [])):
    where = f"watchlist[{i}]"
    for field in ("name", "note", "url", "campaign", "lifecycle", "verification"):
        if field not in w:
            errors.append(f"{where}: missing {field}")
    http(w.get("url"), where, "url")
for i, a in enumerate(data.get("always_on", [])):
    where = f"always_on[{i}]"
    for field in ("name", "note", "url", "kind", "offer_type", "lifecycle", "verification"):
        if field not in a:
            errors.append(f"{where}: missing {field}")
    http(a.get("url"), where, "url")

if errors:
    print(f"✗ {len(errors)} problem(s) in data/deals.source.json\n")
    for e in errors:
        print("  -", e)
    sys.exit(1)

live = sum(d["lifecycle"] == "live" for d in data["deals"])
expired = sum(d["lifecycle"] == "expired" for d in data["deals"])
stale = sum(d["verification"] == "stale" for d in data["deals"])
print(f"✓ schema v2 valid — {len(data['deals'])} deals ({live} live, {expired} expired, {stale} stale), "
      f"{len(data['no_deal'])} no-deal rows, {len(data['watchlist'])} watched")
