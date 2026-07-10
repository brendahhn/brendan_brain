---
name: brain-newspaper
description: >-
  Build, edit, and publish Brendan's morning newspaper, and process his annotations on it.
  Use when asked to "make/publish the newspaper", "what's in today's edition", "process my
  annotations/reactions", or when a scheduled Brendan OS run reaches publication time.
---
<!-- brendan-os-skill-version: 1.0.0 (2026-07-10) — canonical source: brendan_brain/.claude/skills/brain-newspaper -->
# brain-newspaper

Roles: you act as Managing Editor on the draft, then as Publisher (fresh eyes — reread
sources, don't trust your own draft) on the checklist. If any item is consequential
(health/financial claims, contrarian calls), spawn an opus reviewer for the Publisher pass
(MODEL_ROUTING_POLICY).

## Publish flow
1. `python3 tools/build_newspaper.py` → mechanical draft in `newspaper/drafts/<date>.md`.
2. EDIT as Managing Editor per `system/PUBLICATION_POLICY.md`: select (importance >
   novelty > length), trim to budgets ±20%, fill "Most Important" (1-3 items), apply
   `preferences/PRESENTATION_PREFERENCES.md` edition overrides, check
   `newspaper/coverage_ledger.md` — no repeats without meaningful change; update the ledger
   for every item you keep. Re-verify time-sensitive claims (listings, prices) or mark
   "as of <date>". Sensitive items: generic conclusions only + repo link.
3. Publisher checklist (PUBLICATION_POLICY): record answers in `checklist_notes`
   frontmatter; set `publisher_verdict: approved`.
4. `python3 tools/build_newspaper.py --publish` → moves to editions/. Commit, push, verify.
5. Notify Brendan: 3-5 headlines max.

## Annotation flow
`python3 tools/process_annotations.py --date <edition-date>` (plan) then `--apply`.
Then review what it created: corrections get high urgency; check whether accumulated
evidence in PROPOSED_RULES.md crosses the MEMORY_POLICY threshold (≥3 signals, ≥2 days) —
if so, write a proposal (not a confirmed rule) and surface it in the next edition's
questions section. Ambiguous annotations (e.g. a bare ❌ that could mean "bad article" or
"stop the topic") → treat as one evidence signal AND add a clarifying question to the next
edition; never guess a permanent meaning.
