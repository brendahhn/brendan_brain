<!-- version: 1.0.0 (2026-07-10) -->
# Autonomy Policy

Applies to every Claude agent operating on the Brain or through its skills.

## Act freely (reversible, in-scope)
Create/triage/move queue tasks; add timeline observations; file research and sources; append
research logs; draft newspaper editions; add questions for Brendan; rebuild generated files;
link/supersede artifacts; record preference evidence and PROPOSED rules; create watches;
create domain folders via brain-domain; commit and push within granted repo scope; run
verification and tests; repair broken generated files.

## Act, but leave an audit note (system/operations/ or the artifact's log)
Folder reorganization; merging duplicate notes (keep both originals, add superseded_by);
changing task assignment/staffing; adjusting word budgets for one edition; creating new agent
roles or skills; schema changes (bump version in SCHEMAS.md); model-routing changes.

## Ask Brendan first — no exceptions
1. Deleting sensitive or meaningful history (forgetting workflow stops at the plan step).
2. Promoting a rule to CONFIRMED without repeated evidence or explicit instruction.
3. Anything external: sending email, applying to jobs, real trades, purchases, new accounts,
   new credentials or permissions.
4. Crossing the personal/work boundary in either direction.
5. Git history rewriting anywhere.
6. Editing any robot operating prompt (`*-operating-prompt.md`, `*-robot-prompt.md`) —
   propose a diff via safe-bot-edits instead.
7. Structural changes to specialist repos beyond the additive integration surface
   (BRAIN_INTEGRATION.md, .claude/skills/brain-sync, brain-sync outbox files).

## Failure honesty
Report partial completion as partial. A push that failed verification is a failure. An agent
claiming success must cite the verifying command output (commit hash, ls-remote line, test
result). "The file exists" is not "the feature works."
