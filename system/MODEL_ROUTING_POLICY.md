<!-- version: 1.0.0 (2026-07-10) -->
# Model Routing Policy

Availability verified in this environment (2026-07-10): `haiku` (Haiku 4.5), `sonnet`
(Sonnet 5), `opus` (Opus 4.8), `fable` (Fable 5) via the Agent tool `model` parameter.
Scheduled routines inherit their session model; subagent overrides are how routing happens
in practice. If a requested tier is unavailable in some environment, fall back one tier UP
for consequential work, one tier DOWN for mechanical work, and log the substitution in the
task's research log.

## Tier assignments
| Tier | Use for | Never for |
|---|---|---|
| haiku | extraction, classification, dedup keys, formatting, date/entity checks, index maintenance, simple source triage | unsupported consequential conclusions (health/financial), adversarial review |
| sonnet | most research, synthesis, queue triage, newspaper editing, domain analysis, routine leadership, code changes | — |
| opus | adversarial review, conflicting evidence, consequential health/financial conclusions, contrarian calls, repeated failures, durable-rule proposals, stress tests | routine formatting/extraction |
| fable | architecture change, cross-domain coordination, major new capabilities, deep audits, long-horizon implementation | anything a cheaper tier reliably does |

## Escalation triggers (any one suffices)
evidence conflict · high confidence on thin evidence · recommendation contradicts credible
consensus · prior conclusion failed · Brendan asked for deep scrutiny · durable rule proposed
· 2+ failed attempts at the same step (escalate one tier, max opus for review / fable for
system repair).

## De-escalation
Well-specified, repetitive, verifiable-by-checklist work drops a tier. Batch mechanical work
to haiku instead of burning lead-model context.

## Recording
Every task's `## Research Log` entries name the model used (e.g. `2026-07-10 [sonnet] ...`).
Escalations record the trigger. Substantive tasks additionally log a row via
`python3 tools/log_usage.py` (V2 — observable fields only; usefulness starts `pending` and
is filled from Brendan's reactions, never self-graded). The weekly review summarizes rows
(≥8 rows → routing/schedule recommendations; 3-strike retirement per STAFFING_POLICY).
No token numbers exist on this platform; none are recorded (LIMITATIONS #4).
