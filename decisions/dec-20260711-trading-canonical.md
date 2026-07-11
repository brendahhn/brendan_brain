---
id: dec-20260711-trading-canonical
title: Canonical trading system is trading-notebook; health-notebook copy is noncanonical
artifact_type: decision
domain: investing
status: made
created_at: 2026-07-11
created_by: systems_architect
sensitivity: personal
related: [q-20260710-trading-dup]
topics: [trading, duplicate, canonical]
---
# Decision: trading duplicate resolved conservatively (V2 mandate §15)

1. **Canonical**: `brendahhn/trading-notebook` (the live robot, 4 recorded runs).
2. `health-notebook/trading/` is **noncanonical** — a frozen migration seed (RUN_COUNT 0).
3. **Nothing is deleted.** A separate archival/deletion proposal follows dependency
   verification; history stays intact per CLAUDE.md.
4. Required notice (cross-repo, ADDITIVE): place `health-notebook/trading/NONCANONICAL.md`
   stating "Frozen migration seed. The live trading system is brendahhn/trading-notebook.
   Do not run or edit robots from this folder; this repo's safe-bot-edits copy pointing
   here is stale — see the canonical repo." Plus a one-line pointer fix proposal for that
   repo's safe-bot-edits skill via the existing proposed-prompt-change mechanism (robot
   prompts/skills there are Brendan-authored — never edited silently, AUTONOMY #6/#7).
5. **Execution status**: BLOCKED in this session — `health-notebook` is not in the repo
   selection. The notice text above is ready to paste; any session with both repos (or the
   Health Robot's next brain-sync run reading this decision) applies it as an additive
   change and records the op. Until then, nothing active depends on the duplicate
   (verified 2026-07-10: RUN_COUNT 0, no routine points at it).
6. **This question stops resurfacing**: policy recorded here; the open question is now
   answered-by-policy (conservative default, option b→a path), flagged for Brendan's veto
   in the next edition rather than re-asked.
