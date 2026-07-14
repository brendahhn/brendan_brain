---
id: audit-20260714-stranded-run-branches
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-14
updated_at: 2026-07-14
created_by: systems_architect
---
# Audit: stranded run branches across all repos (recovered 2026-07-14)

Brendan reported "a lot of runs and brendan brain stuff hasn't been pushing to main."
Confirmed and repaired. Root cause and recovery below.

## Root cause
Scheduled cloud sessions are pinned by the platform to an auto-generated `claude/*`
branch and instructed to push there; the repo contract ("work on main") loses. Every
routine run since ~2026-07-02 committed real production output to a throwaway branch
main never saw. Compounding effects observed:
- Editions 07-13 and 07-15 flagged "[FAIL] robot silence" while the robots' output sat
  on stranded branches — the system reported its own blindness as robot failure.
- FootyBot re-published "first daily newsletter" repeatedly (07-06, 07-07, 07-08) because
  each night's clone of main couldn't see the previous night's stranded newsletter.
- The Brendan OS daily run fired TWICE on 2026-07-14 (14:11 and 14:25 UTC, same base),
  producing near-duplicate artifact sets on two branches.
- 2026-07-11: the Health Robot's run launched with brendan_brain as its working repo
  (routine repo misconfiguration), found no `health-robot-prompt.md` (wrong repo), and
  created a stub `health-notebook.md` at the Brain root recording PROMPT VALIDATION
  FAILED. The stub is superseded by this audit and removed; the robot ran normally in
  its own repo on 07-12 and 07-13.

## Recovery (brendan_brain)
Merged into main, chronological order, conflicts resolved per CLAUDE.md rules
(inbox keep-both at block level; earliest true triage stamp wins; generated files
regenerated): exciting-ritchie-nci1c5 (07-10 first daily run), upbeat-mendel-uepa2z
(07-11 health failure record), keen-ritchie-ir0bkb (edition 07-12), charming-dijkstra-pqv8fm
(footybot inbox 07-12), keen-ritchie-wl6i80 (edition 07-13), routine-session-diagnostic-qbjsey
(07-12 diagnostic + routine_monitor.py), dazzling-tesla-cqbu6n (footybot inbox 07-14),
optimistic-bell-fl327o (trading inbox 07-14), keen-ritchie-xj24ht (07-14 daily run:
edition 2026-07-15, 4 predictions, 4 health knowledge candidates, triage stamps).

**Duplicate run NOT merged**: `claude/keen-ritchie-r2elmx` (the 14:25 double-fire) —
same triage + a parallel edition 2026-07-15 with differently-slugged duplicates of the
same 8 artifacts. Merging both would violate ID stability and duplicate predictions.
Branch left in place as evidence; safe to delete after review.

## Recovery (specialist repos)
Same procedure applied to production-run branches in FootyBot (9 branches: newsletters
07-02..07-09, 07-12 push-target note), health-notebook (run branches), trading-notebook
(RUN 7 2026-07-14). Feature-shaped branches (health obsidian-integration, trading-removal,
vigilant-ritchie prompt edits) were NOT auto-merged — listed for Brendan instead.
Per-repo results in the op record: op-20260714-stranded-branch-recovery.

## Prevention
CLAUDE.md git protocol amended (standing instruction, Brendan-authorized 2026-07-14):
routine sessions pinned to a `claude/*` branch must ALSO land routine operational commits
on main via `git pull --rebase origin main && git push origin HEAD:main`, then verify with
`git ls-remote origin main`. Same amendment proposed to each robot repo via its
BRAIN_INTEGRATION.md / proposed-prompt-change.md channel (robot prompts are never edited
silently — safe-bot-edits governs). Double-fire and wrong-repo-launch remain platform-side;
`tools/routine_monitor.py` (merged from the diagnostic branch) is the detection tool —
recommend Brendan checks the routines UI for a duplicated Brendan OS schedule entry and
each routine's repo selection.
