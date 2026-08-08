---
id: q-20260715-trading-branch-history
title: Trading-notebook git history reconciled itself — confirm nothing was lost?
artifact_type: question
task_id: none
kind: material
status: open
asked_at: 2026-07-15
created_at: 2026-07-15
domain: investing
sensitivity: financial
origin_repository: trading-notebook
derived_from: [inbox-trading-robot-20260715, inbox-trading-robot-20260714]
related: [q-20260710-trading-dup]
topics: [git, branch-policy, trading-notebook, audit]
---
Background: On 2026-07-14 (RUN 7) the trading-robot escalated a real conflict — its git
environment was scoped to a session branch (`claude/tender-brahmagupta-fl327o`) while its
prompt requires every run to commit to `main`. RUNs 5-7 had landed on session branches, so
`trading-notebook`'s `origin/main` was stranded at a RUN-4-era commit with ~2 runs of drift
and no PR opened.

As of 2026-07-15 (RUN 8) the desk reports this **appears RESOLVED**: `origin/main` now shows
a clean linear history through RUN 5/6/7's commits, and RUN 8 committed and pushed directly to
`main` (commit `c149a54`, verified via `git ls-remote`). The desk does **not** know the
mechanism that reconciled it and is not asserting history was rewritten — it's reporting
observable current state and asking you to confirm nothing was lost in whatever happened
between RUN 7 and RUN 8.

**Question (material, not blocking):** Did you (or a routine) merge/rebase those session
branches into `trading-notebook` main? If not, worth a glance at the reflog before we treat
the linear history as trustworthy — this rhymes with the 26-branch stranded-run issue the
Brain already logged (`system/audits/audit-20260714-stranded-run-branches.md`).

**Update 2026-08-08 (RUN 25):** The same failure mode **recurred** in trading-notebook. RUNs
21–24 (2026-08-04 → 08-07) again landed on the session's platform-pinned branch instead of
`main`, leaving `trading-notebook` `origin/main` stranded at RUN 20 for four runs. RUN 25 found
it, verified `main` was a clean ancestor (no divergence, no data loss), and fast-forward-recovered
before writing anything — the second lossless fast-forward of this exact pattern. So the original
"was anything lost?" question is effectively answered **no, both times**. What remains is a
*process* issue, not a data one: the pinned-branch default keeps stranding runs across repos
until a later run happens to notice. Decision for Brendan: **close this question** (the mechanism
is now understood — a recoverable fast-forward, twice) **or** treat it as a standing flag to
whoever operates the scheduling harness that the pinned-branch default needs a fix so runs don't
depend on the *next* run to reconcile `main`. Left `open` pending that call.
