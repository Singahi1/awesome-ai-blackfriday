#!/usr/bin/env python3
"""Static build smoke tests — no browser required."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
source = json.loads((ROOT / "data" / "deals.source.json").read_text())
runtime = json.loads((ROOT / "data" / "deals.json").read_text())
assert runtime["meta"]["count"] == len(source["deals"])
assert runtime["deals"] == source["deals"]

expected = {
    "index.html": sum(d["lifecycle"] == "live" for d in source["deals"]),
    "black-friday/index.html": sum(d["campaign"] == source["meta"]["current_campaign"] and d["lifecycle"] in {"live", "announced"} for d in source["deals"]),
    "archive/index.html": sum(d["lifecycle"] in {"expired", "archived"} for d in source["deals"]),
}
for rel, count in expected.items():
    text = (ROOT / rel).read_text()
    actual = text.count('<article class="card')
    assert actual == count, f"{rel}: expected {count} static cards, found {actual}"
    assert not re.search(r"{{[A-Z_]+}}", text), f"{rel}: unresolved template placeholder"
    assert 'class="stretched"' in text, f"{rel}: missing clickable card overlay"
    assert 'data-snapshot="' in text, f"{rel}: missing snapshot date"

feed = (ROOT / "feed.xml").read_text()
assert feed.count("<item>") == min(50, expected["index.html"])
assert "Awesome AI Deals" in feed
sitemap = (ROOT / "sitemap.xml").read_text()
for path in ("", "black-friday/", "archive/"):
    assert f"https://singahi1.github.io/awesome-ai-blackfriday/{path}" in sitemap
assert "window.DEALS" in (ROOT / "data" / "deals.js").read_text()
assert "data/deals.source.json" in (ROOT / "README.md").read_text()
print(f"✓ static build smoke tests passed — {expected}")
