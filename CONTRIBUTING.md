# Contributing

The whole list is one file: [`data/deals.json`](data/deals.json). A contribution is a PR that edits that file — the site and the README are generated from it.

## The bar for a listing

A deal goes in only if **all** of these are true:

1. **The vendor's own page states it.** A pricing page, a `/black-friday` landing page, or published offer terms. Coupon aggregators, newsletters and "exclusive code" blog posts don't count on their own.
2. **You include the URL you read it on**, in `source`.
3. **You include the date you read it**, in `verified` (`YYYY-MM-DD`).
4. **You state what it renews at**, if the vendor prints it. A first-month price with a steep renewal is a coupon, not a deal — say so.
5. **It is a real discount**, not a standing annual-billing rate dressed up as seasonal. Those belong in `always_on`.

If the vendor has *no* offer, that's also a useful contribution: add it to `no_deal` with the date you checked. The no-deal table is the part readers trust most.

## Row format

```json
{
  "id": "elevenlabs",
  "name": "ElevenLabs",
  "category": "Voice & Audio",
  "what": "Text-to-speech, voice cloning, dubbing, music and agents",
  "deal": "Up to 55% off the first year — Creator $99 (was $220)",
  "discount": 55,
  "price_before": "$220/yr",
  "price_after": "$99/yr",
  "code": null,
  "ends": "2026-12-01",
  "ends_note": "11:59 PM ET",
  "renewal": "Renews at the regular annual price from year two",
  "status": "live",
  "audience": "New and upgrading subscribers",
  "tags": ["annual", "editor-pick"],
  "url": "https://elevenlabs.io/pricing",
  "source": "https://elevenlabs.io/black-friday-promo",
  "verified": "2026-11-21"
}
```

### Fields

| Field | Notes |
| --- | --- |
| `category` | One of the strings in `categories`. Don't invent new ones in a PR — open an issue. |
| `discount` | Integer percentage for sorting, or `null` when the offer isn't a percentage (credits, bundles, perks). |
| `ends` | `YYYY-MM-DD`, or `null` when the vendor prints no end date. Never guess a date. |
| `ends_note` | Deadline detail (timezone, "countdown only", terms window). |
| `status` | `live`, `standing`, `perk`, `upcoming`, `expired`. |
| `tags` | Free-form: `lifetime`, `annual`, `student`, `offline`, `flash`, `bundle`, `editor-pick`… |

## Before you open the PR

```bash
python3 scripts/validate.py     # schema, ids, dates, categories
python3 scripts/build_readme.py # regenerate README.md
```

Both must pass, and the README must be regenerated in the same PR. CI runs the validator.

## Removing a dead deal

Deals end. If a code stops working or a page drops the offer, either set `"status": "expired"` or delete the row and add a line to `no_deal`. Don't leave a dead code in the list — that's worse than an empty row.
