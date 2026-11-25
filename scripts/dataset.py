#!/usr/bin/env python3
"""Generate the runtime dataset from the canonical, human-editable source.

Edit data/deals.source.json — never data/deals.json or data/deals.js directly.
This script emits both runtime artifacts and refreshes the computed deal count.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "deals.source.json"
JSON_OUT = ROOT / "data" / "deals.json"
JS_OUT = ROOT / "data" / "deals.js"

data = json.loads(SOURCE.read_text())
data["meta"]["count"] = len(data["deals"])

JSON_OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
JS_OUT.write_text(
    "/* generated from data/deals.source.json — do not edit */\nwindow.DEALS = "
    + json.dumps(data, indent=2, ensure_ascii=False)
    + ";\n"
)
print(f"wrote {len(data['deals'])} deals to data/deals.json and data/deals.js")
