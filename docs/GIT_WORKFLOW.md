<!-- version: 1.0.0 (2026-07-11) -->
# Git Workflow — daily work vs feature work

## Daily operations → `main`, directly
Newspapers, queue updates, watch runs, annotation processing, index rebuilds, timeline
entries, health/system logs, ordinary memory updates.

The daily sequence (also in system/DAILY_ROUTINE_PROMPT.md):
1. `git checkout main && git pull --rebase origin main` BEFORE writing.
2. Do the work; commit with area-prefixed messages (`newspaper: …`, `queue: …`).
3. `git push origin main` (retry 2/4/8/16s on network errors only).
4. **Verify**: `git ls-remote origin main` matches local HEAD. Unverified push = failure.
5. If branch protection blocks main: report the exact restriction and STOP — never
   silently publish the newspaper to a side branch.
6. Never create a feature branch for ordinary daily output.

## Feature branches → major changes only
Architecture, schemas, tools, skills, significant policy changes, large connector
integrations, risky migrations. Pattern: `claude/<topic>-<suffix>` branch → full test
suite green → PR into main → independent review of the final diff → merge → post-merge
verification on fresh main (V2's own release is the template:
`system/audits/2026-07-11-*` series).

## Conflict rules (unchanged from CLAUDE.md)
One-file-per-artifact keeps conflicts rare; generated files regenerate (take either side);
append-only inboxes keep BOTH sides; never force-push; never rewrite history on main.
