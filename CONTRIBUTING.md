# Contributing

The canonical, human-editable dataset is **`data/deals.source.json`**. Everything else is generated:

- `data/deals.json` and `data/deals.js`
- `README.md`
- `index.html`, `black-friday/index.html`, `archive/index.html`
- `feed.xml`, `sitemap.xml`, `robots.txt`

Never edit a generated file directly. A JSON-only or HTML-only PR will be overwritten by the next build.

## The bar for a listing

A deal is listed only when:

1. The vendor’s own pricing, promo or offer-terms page states it. Trackers are discovery sources, not proof.
2. The exact price or discount, eligible plan and billing period are recorded.
3. The deadline is copied from the vendor. If no date is printed, `valid_until` is `null` — never guess.
4. Renewal terms are recorded where the vendor prints them.
5. Region and currency are recorded when stated. Leave `regions` empty rather than guessing.
6. The evidence array contains the URL, check date, source type and a short excerpt.

A blocked or unavailable page means `verification: "stale"`, not `expired`.

## Schema v2 row

```json
{
  "id": "example-tool",
  "name": "Example Tool",
  "category": "AI Chat & Assistants",
  "what": "One-line description of what the tool does.",
  "deal": "40% off the first year of the Pro annual plan.",
  "discount": 40,
  "price_before": "$199/yr",
  "price_after": "$119.40/yr",
  "code": null,
  "valid_until": "2026-12-31",
  "ends_note": "Ends 23:59 PT on 31 December.",
  "renewal": "Renews at the regular annual price from year two.",
  "lifecycle": "live",
  "verification": "verified",
  "offer_type": "seasonal",
  "campaign": "christmas-2026",
  "regions": ["US"],
  "currency": "USD",
  "tax_inclusive": false,
  "eligibility": "New subscribers only.",
  "first_seen": "2026-11-25",
  "last_verified": "2026-11-25",
  "next_check": "2026-11-26",
  "evidence": [
    {
      "type": "vendor_terms",
      "url": "https://example.com/offer-terms",
      "checked_at": "2026-11-25",
      "excerpt": "40% off Pro annual through 31 December."
    }
  ],
  "price_history": [
    { "observed_at": "2026-11-25", "before": "$199/yr", "after": "$119.40/yr" }
  ],
  "useful": 72,
  "tags": ["annual"],
  "sponsored": false,
  "url": "https://example.com/pricing",
  "source": "https://example.com/offer-terms"
}
```

### Lifecycle

`announced` → `scheduled` → `live` → `expired` → `archived`

### Verification

`verified`, `stale`, `unverified`, `conflicting`, `reported`, `announced`, `standing`

### Offer types

`seasonal`, `evergreen`, `lifetime`, `recurring`, `partner`, `perk`, `referral`, `student`

## Before opening a PR

```bash
python3 scripts/dataset.py
python3 scripts/validate.py
python3 scripts/build_readme.py
python3 scripts/build_site.py
```

Commit the source change and every regenerated artifact in the same PR. CI fails if the generated diff is missing.

## Removing a dead deal

Set `lifecycle` to `expired`, keep `valid_until`, and retain the row for price history. Do not delete it. If a page merely fails to load, set `verification` to `stale` and leave the lifecycle unchanged.
