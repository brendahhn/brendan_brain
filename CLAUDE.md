<!-- version: 1.0.0 (2026-07-10) -->
# Brendan Brain — Operating Contract

This repository is the canonical shared memory and coordination layer for Brendan OS.
Every Claude session or routine that touches this repo MUST follow this contract.

## What this repo is

- **Canonical source of truth is Markdown.** Generated files (QUEUE.md, BRAIN_MAP.md, indexes)
  are rebuildable from the underlying Markdown and never authoritative.
- **Git is the audit trail.** Never rewrite history on `main`. Corrections supersede; they do not erase.
- **Specialist repos stay authoritative for their domain internals.** The Brain holds shared
  state: queue, timeline, preferences, cross-domain knowledge, newspaper, questions, predictions.
  `jobs-notebook.md`, `footybot-notebook.md`, `health-notebook.md`, `trading-notebook.md`
  remain the domain robots' own memory. The Brain is the exchange layer, not a replacement.

## Read this first, in this order

1. `BRAIN_MAP.md` — map of the repo (generated; run `python3 tools/build_brain_map.py` if stale)
2. `CURRENT_PRIORITIES.md` — what matters right now
3. `system/AUTONOMY_POLICY.md` — what you may do without asking
4. `system/PRIVACY_POLICY.md` — before touching anything with `sensitivity: private` or `health`
5. The domain folder relevant to your task (`domains/<domain>/DOMAIN_PROFILE.md`)

## Hard rules

1. **One file per artifact.** Tasks, timeline events, predictions, decisions, research reports
   each get their own file. Never append unrelated items to a shared file (exception:
   append-only inbox files under `queue/inbox/` and `system/operations/`).
2. **Frontmatter is mandatory** on artifacts. Schemas: `system/SCHEMAS.md`.
   Validate with `python3 tools/validate_frontmatter.py <file|--all>`.
3. **IDs are stable.** Format: `<type>-<YYYYMMDD>-<slug>` (e.g. `task-20260710-tacoma-4cyl`).
   Never reuse or renumber.
4. **Sensitive content stays scoped.** `sensitivity: health` or `private` artifacts must never
   be quoted in the newspaper, cross-domain outputs, commit messages, or logs unless the
   output is itself in that domain and the artifact is directly relevant. See PRIVACY_POLICY.
5. **Observations are not facts.** Raw timeline entries record what happened/was said, with
   uncertainty preserved. Promotion to durable knowledge requires evidence or Brendan's
   confirmation and is recorded via `supersedes`/`derived_from` links.
6. **One reaction is not a rule.** Reactions accumulate as preference evidence
   (`preferences/PROPOSED_RULES.md`); rules move to `CONFIRMED_RULES.md` only with repeated
   evidence or explicit instruction.
7. **Never claim success you didn't verify.** After pushing, verify with
   `git ls-remote origin <branch>` and record the op in `system/operations/` for
   cross-repo work. Partial failure must be reported as partial failure.
8. **Regenerate, don't hand-edit, generated files.** QUEUE.md and BRAIN_MAP.md carry a
   `GENERATED` header; edit the source files and rerun the tool.

## Git protocol for this repo

- Work on `main` (this repo is Brain-owned; routines commit directly).
- **Platform-pinned session branches (standing rule, Brendan-authorized 2026-07-14):**
  scheduled/cloud sessions are often pinned to an auto-generated `claude/*` branch. Routine
  operational commits (inbox blocks, triage, editions, health logs, index rebuilds) MUST
  still land on `main`: after committing, run
  `git pull --rebase origin main && git push origin HEAD:main`
  (also push the pinned branch if the harness requires it), then verify with
  `git ls-remote origin main`. This rule is the explicit permission those sessions need.
  It exists because 2026-07-02→07-14 runs stranded output on 26 session branches
  (system/audits/audit-20260714-stranded-run-branches.md). Architecture/discovery work is
  exempt — it stays branch-gated until approved.
- Pull with rebase before writing: `git pull --rebase origin main`.
- Commit scope: one logical change per commit; prefix with the area, e.g.
  `queue: add task-20260710-tacoma-4cyl` or `timeline: 2026-07-10 surf note`.
- On conflict: task files and timeline files are one-per-artifact so conflicts are rare;
  if QUEUE.md conflicts, take either side and regenerate. If an inbox file conflicts,
  keep BOTH sides (they are append-only). Never force-push.
- Cross-repo operations: follow `system/CROSS_REPOSITORY_POLICY.md` (operation IDs, per-repo
  status records, idempotent retries).

## Autonomy summary (full policy: system/AUTONOMY_POLICY.md)

Act freely: create/triage tasks, add timeline observations, file research, move task states,
draft newspaper, add questions, rebuild indexes, propose rules/preferences, create watches,
commit and push within granted scope, reversible reorganization (with audit note).
Ask Brendan first: deleting real knowledge or sensitive history, promoting weak evidence to a
confirmed rule, anything external (email, applications, trades, purchases, credentials),
moving data across the personal/work boundary, history rewriting.

## Skills

Canonical Brendan OS skills live in `.claude/skills/` here and are synced to specialist repos
with `tools/sync_skills.sh`. Never hand-edit a synced copy in a specialist repo; edit here
and re-sync. Registry: `skills/SKILL_REGISTRY.md`.
