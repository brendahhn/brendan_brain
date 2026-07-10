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
   --allow-sensitive "forgetting request <date>"` plus a raw `grep -ril <terms> .`
   sweep of EVERYTHING — no `--include=*.md` filter: generated files like
   `system/INDEX.tsv` are not Markdown and must be caught (search can miss; grep is the
   backstop).
2. Find derived copies: generated files (INDEX.tsv, QUEUE.md, BRAIN_MAP.md), editions,
   annotations, superseding artifacts, robot outbox blocks, and any `derived_from` chains.
3. Report to Brendan, explicitly split:
   - Removable normally: delete files + rebuild generated files (content leaves the working
     tree but REMAINS IN GIT HISTORY — say this plainly).
   - Requires history rewriting: `git filter-repo`-style rewrite + force-push — irreversible,
     breaks clones, needs his separate explicit go-ahead. Never done autonomously.
4. STOP and wait for confirmation of exactly which option.

## Phase 2 — Execute (only after explicit confirmation)
1. `git rm` the artifacts; rebuild INDEX.tsv, QUEUE.md, BRAIN_MAP.md.
2. REDACT every derived copy Phase 1 found — this is where forgetting usually fails:
   robot outbox blocks (`queue/inbox/from-*.md`), published editions, annotation records,
   and `preferences/PROPOSED_RULES.md` evidence lines that quote the content. Replace the
   quoted content in place with `[forgotten <date>, <op-id>]` — privacy outranks
   edition immutability here, and the tombstone records that an edit happened. Artifacts
   `derived_from` the deleted one either get deleted too (Brendan's call in Phase 1) or
   re-pointed with the provenance line redacted.
3. Final sweep: `grep -ril <terms> .` (everything, not just .md) must come back empty
   outside .git/ — if it doesn't, you are not done.
4. Write a tombstone `system/operations/op-<date>-forget-<slug>.md` recording THAT a
   deletion happened, the artifact IDs (not content), which derived copies were redacted,
   scope chosen, and what remains in git history. Nothing else references the content
   again — do not re-derive it from memory of this conversation.
5. Commit (`forget: <ids>`), push, verify. History rewriting, if chosen, is a separate
   Brendan-supervised session.
