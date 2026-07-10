---
id: q-20260710-trading-dup
artifact_type: question
title: Retire the frozen trading/ copy inside health-notebook?
kind: material
status: open
created_at: 2026-07-10
domain: investing
asked_at: 2026-07-10
---
# Question for Brendan

The Trading Robot exists twice: the live one in `trading-notebook` (4 recorded runs) and a
frozen seed copy in `health-notebook/trading/` (RUN_COUNT 0, added by PR #2, later migrated).
Three copies of the safe-bot-edits skill disagree about which is home; the health-notebook
copy points at the dead one, so a session started there could edit the wrong robot.

**Options:** (a) delete `health-notebook/trading/` and fix that repo's safe-bot-edits skill
to point at trading-notebook; (b) keep it but add a DEPRECATED marker; (c) it's intentional
— tell us why and we'll record it.

Nothing has been changed pending your answer (per no-silent-fix policy).
