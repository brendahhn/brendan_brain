---
id: know-20260713-tea-physical-inventory
artifact_type: knowledge
domain: tea-business
sensitivity: personal
confidence: high
derived_from: [brendan-photo-2026-07-14]
created_at: 2026-07-14
updated_at: 2026-07-14
created_by: systems_architect
---
# Physical inventory count — taken by Brendan night of 2026-07-13

Header on his sheet: "Margin for error" — counts are approximate, not exact.

| Item | Count (as written) | Normalized |
|---|---|---|
| Chamomile | 306.8g + 1 lb | ≈760.4 g |
| Lemon balm | 239.5 | 239.5 g |
| Glycine | 2.2 lb minus 90 g | ≈908 g |
| Taurine | 201 | 201 g |
| L-Theanine | 18 | 18 g |
| Stickers | 37 | 37 |
| Cards | 34 | 34 |
| Big muslin bags | 8 | 8 |
| Mini scoops | 28 | 28 |
| Tea bags | 74 | 74 |
| Boxes | 36 | 36 |
| Powder tins | 11 | 11 |
| Tea (herb) tins | 8 | 8 |

## Orders-left math (BOM per know-20260714-tea-bom; flag rule: ≤4 orders)
Loose ceiling ≈ **3 orders** (L-theanine 18/6=3; taurine 201/60=3.35).
Tea-bag ceiling ≈ **2 orders** (tea bags 74/30=2.4). Muslin 8, lemon balm ≈7.9 next-lowest.
**FLAGGED at count time: tea bags (2), L-theanine (3), taurine (3)** — all ≤4.
Sales skew 13:1 toward tea-bag orders (Shopify aggregate 2026-07-14), so the tea-bag
ceiling is the binding one.

## Unfulfilled backlog at count time (order numbers only — no customer data in git)
Shopify #1013 (1 item, paid 2026-07-09) and #1014 (2 items, paid 2026-07-14) are not yet
fulfilled; all other orders (#1001–#1012) fulfilled per Brendan. NOTE: Shopify's own
fulfillment field is unmaintained (all 14 show UNFULFILLED) — Brendan's word + future
Personal OS "mark fulfilled" button are the truth, never Shopify status.

## AMENDMENT 2026-07-14 (Brendan): count was AFTER #1013 was packed; #1014 (2 tea-bag
orders) was packed after the count → subtract 2 tea-bag orders from every number above.
Current effective stock and orders-left:
| Item | Now | Orders left |
|---|---|---|
| Tea bags | ~14 | **0** 🔴 cannot fulfill another tea-bag order |
| L-Theanine | ~6 g | **1** 🔴 (and it's the shared personal jar: ~2.4 weeks of nightly
use OR one order — not both) |
| Taurine | ~81 g | **1** 🔴 |
| Muslin bags | ~6 | 6 |
| Chamomile ~670 g · Lemon balm ~180 g · Glycine ~728 g | | 14 / 6 / 8 |
No fulfillment backlog remains (#1013, #1014 both packed).
**Reorder NOW list: tea bags, L-theanine, taurine** — sourcing task bumped to urgent.
