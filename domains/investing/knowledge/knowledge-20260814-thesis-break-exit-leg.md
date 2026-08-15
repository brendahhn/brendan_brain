---
id: knowledge-20260814-thesis-break-exit-leg
title: When a thesis rests on a legal/regulatory mechanism, write an explicit "thesis-break" leg into the exit conditions at filing time — so a broken thesis can trigger a mechanical close the same run it's found, instead of waiting on a discretionary call plus a fresh quote
artifact_type: knowledge
domain: investing
confidence: medium
sensitivity: public
created_at: 2026-08-14
created_by: trading-robot
origin_repository: trading-notebook
derived_from: [inbox-trading-robot-20260814]
related: [knowledge-20260813-headline-label-is-not-self-verifying, prediction-20260802-auto-tariff-short]
topics: [epistemics, exit-conditions, risk-management, research-process, decoupled-findings]
---
A process-level lesson from the trading desk (RUN 31), a follow-on to the RUN 30 tariff/legal-text
lesson (`knowledge-20260813-headline-label-is-not-self-verifying`). Useful well beyond investing.

**The lesson:** when research finds a thesis is broken but the position can't be closed the same
moment (e.g. a price can't be verified that run), the gap between "verifiably wrong" and "actually
closed" is itself a real, ongoing source of exposure. For any thesis that rests on a
legal/regulatory/mechanical premise — the kind that can be *proven* false by reading the text
rather than waiting for the market — write an explicit **"thesis-break" leg** into the exit
conditions **at filing time**. Then a finding that the premise is false can trigger a mechanical
close the same run it's discovered, rather than sitting in limbo pending a discretionary judgment
call plus a lucky fresh quote.

**The concrete case:** the STLA/Stellantis paper short (`prediction-20260802-auto-tariff-short`)
was recorded BROKEN on 2026-08-13 when the tariff's own text was found to carve out exactly the
category the short bet on — but it could not be closed until RUN 31 (2026-08-14), and closed then
for a small realized loss (−$0.33). The days between "thesis confirmed dead" and "position closed"
were pure unhedged exposure that a pre-written thesis-break exit would have removed.

**Generalizes to:** any domain where a finding and the action it implies are temporally decoupled
— research says X is settled, but the mechanism to act on X runs on a different clock. The fix is
the same: pre-commit the trigger→action rule when you open the position/plan, so the action fires
mechanically on the finding instead of waiting on a fresh discretionary decision.

Proposed durable knowledge (medium confidence, not self-confirmed); a paper-desk process
observation, not investment advice.
