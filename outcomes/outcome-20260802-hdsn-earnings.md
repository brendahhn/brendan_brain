---
id: outcome-20260802-hdsn-earnings
artifact_type: outcome
prediction_id: prediction-20260712-hdsn-earnings
domain: investing
result: incorrect
scored_at: 2026-08-02
created_at: 2026-08-02
created_by: brain-daily-run
sensitivity: financial
derived_from: [inbox-trading-robot-20260802, inbox-trading-robot-20260801, inbox-trading-robot-20260731]
---
Scored on the 2026-08-02 horizon. Paper/fictitious thesis, not investment advice.

The prediction (2026-07-12): HDSN (Hudson Technologies) "closes above $8.50, or pops >15% on
the 2026-07-29 earnings print, within 2-3 weeks of 2026-07-12."

**Resolved — incorrect (with a material caveat).** By the 2026-08-02 horizon neither success
condition was met:
- The price leg (a close above $8.50) was not reached. The paper position spent the window in
  decline (reported ~10% below entry around 2026-07-21) and its price was repeatedly flagged as
  hard-to-verify in later runs; no run recorded a close above $8.50.
- The earnings leg (a >15% pop on the 2026-07-29 print) never became testable: the prediction's
  premise that HDSN reports on 2026-07-29 was **factually wrong**. Trading-robot runs on 07-31
  and 08-01 independently caught and discarded search-summary hallucinations claiming the
  earnings had already released, and re-dated the real Q2 print to **~2026-08-05** — after this
  prediction's horizon. So the catalyst the pop-leg depended on had not occurred by the score
  date.

The honest read: the prediction is falsified as written (neither disjunct true by 08-02), but a
core input — the earnings date — was contaminated, which is itself the recurring dated-headline
hygiene pattern the desk keeps flagging. The live earnings catalyst is now carried forward by
the desk as an ~Aug 5 2026 print; no separate prediction artifact has been filed for it yet
(the 08-01 outbox tracks it as an open, unresolved thesis with a ~4-day horizon). If Brendan
wants the Aug-5 catalyst scored, a fresh prediction should be filed at the next trading run.
