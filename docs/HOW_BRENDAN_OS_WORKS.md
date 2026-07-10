<!-- version: 1.0.0 (2026-07-10) -->
# How Brendan OS Works

## Simple version
One GitHub repo (`brendan_brain`) is the shared memory. Your four robots keep their own
brains for their own subjects; this one holds what they share: your preferences, the
research queue, questions, predictions, and the newspaper. Claude sessions and scheduled
routines read and write it through skills; Git keeps every change auditable and reversible.

## The pieces, in detail

1. **The Markdown Brain.** Every piece of knowledge is one Markdown file with a metadata
   header (frontmatter — schemas in `system/SCHEMAS.md`, enforced by
   `tools/validate_frontmatter.py`). Dashboards (`QUEUE.md`, `BRAIN_MAP.md`,
   `system/INDEX.tsv`) are generated and never authoritative.
2. **GitHub** is the remote home: private repos, full history, no history rewriting on
   `main`. Corrections supersede (`supersedes`/`superseded_by`) — they never erase.
3. **The queue** (`queue/`): one file per task, lifecycle folders (inbox → active →
   completed…), dedupe by `dedupe_key` (asking twice = +1 interest signal, not a duplicate),
   created by `tools/new_task.py`.
4. **Timeline memory** (`timeline/YYYY/MM/`): dated raw observations with uncertainty
   preserved — an itch note stays an itch note, never becomes a diagnosis on its own.
5. **Durable knowledge** (`domains/<d>/knowledge/`): promoted only with evidence or your
   confirmation, always with provenance (`derived_from`).
6. **Sensitive memory**: `sensitivity: health/private/financial` plus fail-closed domain
   gating — health and investing artifacts are invisible to unrelated searches even if
   someone forgets the tag (`tools/brain_search.py`).
7. **Domains** (`domains/`): folders per interest, created on demand
   (`tools/new_domain.py`), never pre-created empty.
8. **Watches** (`queue/watches/`): recurring tasks with `next_run`;
   `tools/run_watches.py due|mark` drives the cycle; publish only on meaningful change.
9. **Specialist routines**: your four robots, untouched internally. Each merged prompt now
   has two guarded steps — BRAIN READ (start) and BRAIN WRITE (end) — that no-op when the
   Brain isn't in the session. Exports are one dated block per run in
   `queue/inbox/from-<robot>.md`; retries replace the same-day block.
10. **Model routing** (`system/MODEL_ROUTING_POLICY.md`): haiku for mechanical work,
    sonnet for most research and editing, opus for adversarial review and consequential
    health/money conclusions, fable for architecture. Escalation triggers are written down.
11. **Agent staffing** (`system/STAFFING_POLICY.md`): one sonnet lead by default; extra
    agents need a logged justification and get a logged worth-it verdict; three "no" verdicts
    retire a pattern.
12. **Retrieval**: `tools/brain_search.py` — metadata-weighted keyword search with the
    sensitivity gate; policy and upgrade triggers in `system/RETRIEVAL_POLICY.md`.
13. **Verification**: generation and review are separated. The newspaper needs an explicit
    Publisher verdict; consequential items get a fresh-context opus reviewer; robots keep
    their own critic passes. Agreement is not proof — checks need evidence.
14. **Newspaper creation** (`tools/build_newspaper.py` + the brain-newspaper skill):
    mechanical draft → Managing Editor selects/trims (importance over length, coverage
    ledger prevents repeats) → Publisher checklist → publish. Every item carries an
    epistemic label ([FACT]/[CONC]/[OBS]/[ASSUME]/[PRED]/[PREF]/[RULE?]/[RULE]/[Q]/[FAIL]).
15. **Annotation processing** (`tools/process_annotations.py`): your marks become evidence,
    tasks, watches, corrections, proposals — see
    `docs/READING_AND_ANNOTATING_THE_NEWSPAPER.md`.
16. **Proposed rules** (`preferences/PROPOSED_RULES.md`): evidence accumulates; promotion
    needs ≥3 consistent signals across ≥2 days OR your explicit instruction.
17. **Confirmed rules** (`preferences/CONFIRMED_RULES.md`): change behavior immediately;
    only you (or your explicit approval) put things here.
18. **Forgetting** (brain-forget skill): plan → your confirmation → delete + redact every
    derived copy + tombstone. Honest caveat: content stays in Git history unless you
    approve a history rewrite in a supervised session.
19. **Personal/work boundary** (`system/PRIVACY_POLICY.md`): no employer data in here,
    ever; a future work system clones the architecture with separate account/repos/memory.
20. **Failure recovery**: cross-repo operations tracked in `system/operations/` (partial
    failure is visible and resumable); pushes verified with `git ls-remote`; conflicts
    have per-file-class rules (CLAUDE.md); the whole thing is exercised by
    `tests/run_all.sh` (8 suites) and the 48-scenario matrix in `system/STRESS_TESTS.md`.

## The audit trail
Three independent fresh-context reviews (architecture, skeptic, QA) ran during the build;
every finding and its fix is in `system/audits/`. That habit continues: consequential
changes get fresh-context review, and the newspaper reports failures instead of hiding them.
