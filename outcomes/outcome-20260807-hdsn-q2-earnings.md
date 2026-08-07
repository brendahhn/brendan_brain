---
id: outcome-20260807-hdsn-q2-earnings
artifact_type: outcome
prediction_id: prediction-20260729-hdsn-q2-earnings
domain: investing
result: incorrect
scored_at: 2026-08-07
created_at: 2026-08-07
created_by: brain-daily-run
sensitivity: financial
derived_from: [inbox-trading-robot-20260807]
---
Scored early (nominal horizon 2026-08-19). The binary catalyst the thesis depended on — HDSN's
Q2 2026 earnings print — has now occurred and resolved decisively, so the prediction is no longer
uncertain and is scored now. Paper/fictitious thesis, not investment advice.

The prediction (2026-07-29): HDSN (Hudson Technologies) "closes above $8.50, or pops >15% on its
Q2 2026 earnings print, within days to a few weeks of the report."

**Resolved — incorrect.** Neither success condition was met. Per the trading-robot 2026-08-07
run, the Q2 print delivered a real ~30% EPS miss vs. consensus, which tripped the paper
position's own written exit condition (an EPS-miss-vs-consensus-of-more-than-15% leg). The
fictitious position was mandatorily closed for a realized loss of **-$13.36** — the largest
single loss in the bot's history — the opposite of the predicted >15% pop / close above $8.50.

Process caveat recorded by the desk itself: the position was closed one day later than the
condition's plain text required, because a prior run's summary of the exit condition read as
stricter (an AND with an unwritten "guidance walked back" clause) than what was actually filed
(an OR). The generalizable lesson the desk flagged — verify against original source text, not a
prior summary of it, and write multi-clause self-checked rules with unambiguous AND/OR grouping —
is surfaced in today's edition as a cross-routine process note. It does not change the scoring:
the thesis is falsified on the merits.
