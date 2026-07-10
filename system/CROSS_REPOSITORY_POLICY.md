<!-- version: 1.0.0 (2026-07-10) -->
# Cross-Repository Coordination Policy

The system spans independent repos with independent histories. Multi-repo commits are NOT
atomic. This protocol makes partial failure visible, recoverable, and idempotent.

## Operation records
Any change touching 2+ repos gets an operation file `system/operations/op-YYYYMMDD-<slug>.md`
(schema: SCHEMAS.md `operation`), created BEFORE pushing anything:

```yaml
---
id: op-20260710-example
artifact_type: operation
started_at: 2026-07-10T08:00:00Z
repos:
  brendan_brain: planned      # planned|committed|pushed|verified|failed
  health-notebook: planned
---
```

Protocol per repo, in order: commit → push (retry 4x, backoff 2/4/8/16s) → verify with
`git ls-remote origin <branch>` matching local HEAD → update the op record → commit the op
record update in the Brain. If any repo ends `failed`, the op is PARTIAL: say so in any
report, and the next session in that repo checks `system/operations/` for unfinished ops
(status not all `verified`) and resumes.

## Idempotency
- Task creation dedupes on `dedupe_key` (tools/new_task.py) — a retry finds the existing file
  and updates it instead of duplicating.
- Robot outbox writes append dated blocks (`## YYYY-MM-DD — <robot> run summary`) to
  `queue/inbox/from-<robot>.md`. A retry REPLACES the same-day block (the robot checks for
  an existing heading first) rather than appending a duplicate. This single-file contract
  is THE outbox mechanism; build_newspaper.py reads all blocks from the last 2 days.
- Timeline files are date+slug keyed; identical retries collide on filename and are no-ops.

## Interface versioning
The Brain↔robot interface version lives in `skills/SKILL_REGISTRY.md` and in each synced
skill's header comment. brain-sync (in a robot repo) checks its own version against
`../brendan_brain/skills/SKILL_REGISTRY.md`; on major mismatch it writes a warning to its
outbox instead of guessing at the new format.

## Conflict recovery (Brain repo)
`git pull --rebase` before writing. If rebase conflicts: artifact files → keep both/yours
(one file per artifact makes true conflicts rare); generated files (QUEUE.md, BRAIN_MAP.md)
→ take either side, regenerate, commit; append-only inbox/outbox files → merge keeping both
sides. Never force-push. Tested in tests/test_concurrent_writes.sh.
