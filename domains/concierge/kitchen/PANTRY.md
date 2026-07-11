---
id: pantry-live
title: Pantry & shopping — live state
artifact_type: live_state
domain: concierge
sensitivity: personal
created_at: 2026-07-11
updated_at: 2026-07-11
created_by: systems_architect
topics: [kitchen, pantry, shopping, ingredients]
---
# Pantry (live state — edit in place; git history is the audit trail)

Maintained by `tools/receipt_to_pantry.py` and direct edits. Confidence: `confirmed`
(Brendan stated/receipt), `likely` (inferred from purchase, may be used up), `guess`.
`expires` is best-effort (blank = shelf-stable or unknown). Rows at qty 0 are removed,
not zeroed.

## Inventory

| item | qty | unit | confidence | expires | source | updated |
|---|---|---|---|---|---|---|

*(empty until Brendan's first paste — plans must treat pantry as unknown and say so)*

## Shopping needs

*(gap analysis appends here: `- [ ] item — for <plan/task id>`)*
