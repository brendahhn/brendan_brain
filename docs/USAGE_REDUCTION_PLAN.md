<!-- Discovery deliverable addendum 2026-07-15 (Fable). Trigger: Brendan at ~50% weekly limit by Wednesday. -->
# Usage Reduction Plan

No token API exists (LIMITATIONS #4) — this plan uses structural cost drivers, not
fabricated counts. Cost ranking of current routines (by architecture, most→least):
1. **FootyBot weekly run** — 4 parallel lanes + reviewer ≈ 5 session-contexts per run.
2. **Brendan OS daily** — full repo bootstrap + triage + research + edition.
3. **Health robot** (~daily, single-lane chapter builds, heavy web research).
4. **Trading robot** (daily premarket, 4 desk agents but short).
5. Manual/discovery sessions (like this one — deep but occasional).

## Measures (in Brendan-decision order)
- **M1 FootyBot: pause now, resume ~2026-08-11** (2.5 weeks before the Aug 28 draft) in
  single-lane mode. Rationale: it's weekly+multi-lane (most expensive per run), Brendan
  rates output poorly, and its known accuracy problem is missing INPUTS (standing asks:
  Sleeper half-PPR ADP export, real 2024 standings, transaction logs) — pausing costs
  little now, and resuming WITH the data fixes "gets so much stuff wrong" cheaper than
  more runs. Don't delete the repo/memory — draft is still his #2 priority window.
- **M2 Robot lane caps**: all robots single-lane by default; multi-agent panels only on
  explicit escalation triggers. (FootyBot prompt change → safe-bot-edits approval.)
- **M3 Model floors down**: routines configured to Sonnet (never Opus as session model);
  Haiku subagents for scans/extraction; Opus only as fresh-context reviewer on
  consequential merges. (Matches MODEL_ROUTING_AFTER_FABLE.)
- **M4 Effort budgets enforced**: daily run keeps `1_pass` research budgets; deep passes
  only when a task explicitly says so; empty scans exit fast (already designed, D51).
- **M5 Read the paper on Personal OS, not in chat**: asking Claude "what's in my queue"
  costs a session; the Home cockpit costs one API row. (Phase 1 dependency.)
- **M6 Offload mechanical coding to Codex/GPT** (Brendan has both accounts): separate
  provider = separate limits; zero Claude tokens for implementation passes. Claude writes
  the task packet + reviews the PR (external-ai-handoff, D53 — PULLED FORWARD from Phase
  7 to Phase 1 by this plan). Codex works personal-os code tasks; Brain/system repos stay
  Claude-only (policy adherence untested for other models).
- **M7 Trading bot ROI**: keep daily (cheap, Brendan values it) but sharpen the mandate
  per D26 (alpha, not index-hugging) via proposed-prompt-change — better output per
  token, not more tokens.
- **M8 Schedule sanity**: keep total scheduled runs ≤3/day while limits bite
  (trading + health + brain; footy paused, jobs paused). Re-expand after Phase 1 ships
  and the paper shows what's actually worth its cost (usage ledger reviews).

## Weekly-limit arithmetic (structural)
Dropping FootyBot removes the most expensive run entirely; M2+M3 cut the remaining
robots' per-run cost roughly in half (single lane, Sonnet); M5+M6 move reading and
implementation off the Claude meter. Expected effect: comfortably under the weekly
ceiling with discovery/build sessions still possible. Verify against the routines UI's
actual behavior — no usage API exists to confirm numerically.
