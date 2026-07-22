---
id: q-20260720-trading-boat-rule-collision
title: Trading robot — two of its own rules collided on BOAT; your call on how it resolves
artifact_type: question
task_id: none
kind: material
status: answered
asked_at: 2026-07-20
created_at: 2026-07-20
domain: investing
sensitivity: financial
origin_repository: trading-notebook
derived_from: [inbox-trading-robot-20260720]
related: [prediction-20260713-boat-freight, outcome-20260715-boat-freight]
topics: [trading-notebook, operating-rules, risk-management]
---
On RUN 9 (2026-07-20) the trading robot hit a first-time collision between two of its own
operating rules:

- **"A tripped exit condition forces a mandatory close."** The BOAT (shipping ETF) paper
  position hit a real, well-confirmed thesis-break this run.
- **"Never trade a ticker whose price can't be verified this run."** BOAT's price has been
  unverifiable via web search for **4 straight runs**.

The robot declined to resolve this unilaterally: rather than fabricate a price to execute the
mandatory close, it left the close **unexecuted** and surfaced the conflict. It recommends one
of two operator actions:

1. **Hand-edit BOAT's real current price** into `trading-notebook.md` (authoritative; will be
   honored next run), or
2. **Explicitly authorize "mandatory-close-only" execution at the last verified price** for
   cases where a broken thesis and an unverifiable price coincide.

This is a domain-internal trading decision (not blocking the Brain), surfaced because it now
sits open pending your call. Full detail in `trading-notebook/recaps/2026-07-20.md`. Fictitious
paper portfolio — not real trades, not investment advice.

## ANSWER (Brendan, 2026-07-21, verbatim intent)
"I don't give a duck about BOAT price, just do whatever." → Resolution rule for the bot:
**a tripped exit on a thesis-broken position always wins.** When a ticker is unverifiable,
close at the last verified price, mark it a thesis-break exit, log the price-staleness, and
DO NOT surface the collision to Brendan. Mechanical risk control beats price perfection;
never freeze a broken position waiting on a quote. Applied to BOAT: closed. Rule change
filed to the trading robot via proposed-prompt-change (safe-bot-edits); Brendan applies the
two-line diff. This question is closed — stop surfacing it.
