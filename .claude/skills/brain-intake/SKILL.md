---
name: brain-intake
description: >-
  Route any natural-language request from Brendan into the right handling mode BEFORE
  creating artifacts: immediate answer, immediate+memory, immediate+overnight expansion,
  same-day task, background research, or ongoing watch. Use whenever Brendan asks a
  question, requests research, mentions a deadline ("before dinner"), or gives routing
  overrides like "answer this now", "put this in tomorrow's paper", "just a one-off",
  "remember this", "don't save this", "make this a watch".
---
<!-- brendan-os-skill-version: 1.0.0 (2026-07-11) — canonical source: brendan_brain/.claude/skills/brain-intake -->
# brain-intake

Policy: `system/INTAKE_POLICY.md` (read it; the 6 modes compile to answer_now?/task?/capture?).

## Procedure
1. `python3 tools/route_intake.py --request "<verbatim words>" --explain` — a deterministic
   SUGGESTION with override detection. You decide; the tool never overrules Brendan's words
   or your judgment about the 10 decision factors in the policy.
2. If a clarification is BLOCKING, ask it now. Otherwise state assumptions and proceed.
3. Execute the mode:
   - answer_now=y → answer in this session, best effort, with sources if researched.
   - task/watch → `python3 tools/new_task.py --title ... --domain <d> --request "<verbatim>"
     <FLAGS from step 1>` (kitchen/food → domain concierge; see DOMAIN_PROFILE desk table).
   - capture=y → brain-ops capture per MEMORY_POLICY class. capture=n → **write NOTHING**
     (no timeline, no evidence line — the ephemeral guarantee is tested). capture=ask →
     capture only if the content is a durable preference/decision/observation; a one-off
     question is not.
4. TELL Brendan the decision in ONE plain sentence including how to override
   (route_intake.py --explain prints a usable draft). Never silently queue or capture.
5. Overrides arriving later ("actually make it a watch", "don't save that") are executed
   immediately: mode change = move/edit the task per its schema; "don't save" for something
   already captured = brain-forget workflow (plan first — it may need Brendan confirmation).

## Guardrails
- Mode 1 (ephemeral) leaves the repo byte-identical. Verify with `git status --porcelain`
  if in doubt.
- A preference revealed inside ANY mode still gets an evidence line (that's capture of the
  preference, not of the question) — unless "don't save this" covered it.
- New-domain smell (repeated topic, no home): note it; `python3 tools/propose_domains.py`
  proposes on accumulated evidence. Never create a domain from one question.
