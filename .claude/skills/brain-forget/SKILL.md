---
name: brain-forget
description: >-
  Forgetting workflow for the Brendan Brain. Use when Brendan asks to forget, delete, or
  remove something from memory ("forget this", "delete that observation", "remove this from
  the Brain"). NEVER execute destructive steps without his explicit confirmation in the
  same conversation.
---
<!-- brendan-os-skill-version: 1.0.0 (2026-07-10) — canonical source: brendan_brain/.claude/skills/brain-forget -->
# brain-forget

## Phase 1 — Plan (always safe, do immediately)
1. Find every relevant artifact: `python3 tools/brain_search.py "<terms>"
   --allow-sensitive "forgetting request <date>"` plus a raw `grep -ril` sweep (search can
   miss; grep is the backstop).
2. Find derived copies: generated files (INDEX.tsv, QUEUE.md, BRAIN_MAP.md), editions,
   annotations, superseding artifacts, robot outbox blocks, and any `derived_from` chains.
3. Report to Brendan, explicitly split:
   - Removable normally: delete files + rebuild generated files (content leaves the working
     tree but REMAINS IN GIT HISTORY — say this plainly).
   - Requires history rewriting: `git filter-repo`-style rewrite + force-push — irreversible,
     breaks clones, needs his separate explicit go-ahead. Never done autonomously.
4. STOP and wait for confirmation of exactly which option.

## Phase 2 — Execute (only after explicit confirmation)
1. `git rm` the artifacts; rebuild INDEX.tsv, QUEUE.md, BRAIN_MAP.md; grep the whole repo
   again for the content to catch stale summaries (prevents reintroduction from generated
   files).
2. Write a tombstone `system/operations/op-<date>-forget-<slug>.md` recording THAT a
   deletion happened, the artifact IDs (not content), scope chosen, and what remains in
   git history. Nothing else references the content again — do not re-derive it from
   memory of this conversation.
3. Commit (`forget: <ids>`), push, verify. History rewriting, if chosen, is a separate
   Brendan-supervised session.
