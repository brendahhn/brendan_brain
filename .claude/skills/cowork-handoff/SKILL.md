---
name: cowork-handoff
description: >-
  End-of-session handoff from Cowork (or any interactive workspace session) into the
  Brendan Brain. Use at the end of meaningful Cowork work — document review, spreadsheet
  work, plans, presentations, menu/event design, business exploration — or when Brendan
  says "hand this off to the Brain", "save this session's results", "sync Cowork to the
  Brain". Produces one brain-sync-format outbox block; the Brain's normal triage absorbs it.
---
<!-- brendan-os-skill-version: 1.0.0 (2026-07-11) — canonical source: brendan_brain/.claude/skills/cowork-handoff -->
# cowork-handoff

**Division of labor (binding):** Claude Code owns system maintenance, automation, git,
routines, skills, testing, and canonical Brain updates. Cowork is the interactive knowledge
workspace (documents, spreadsheets, polished plans, presentations, folder organization,
business ideas, menus/events, finished knowledge work). **Cowork keeps NO permanent memory
of its own** — anything durable goes through this handoff into the Brain, once. Files stay
where Brendan keeps them; the Brain stores references + conclusions, not copies.

## When to hand off
At the natural end of work that produced anything durable. Skip (silently) for throwaway
sessions — a handoff with nothing in it is noise.

## The handoff block (brain-sync outbox format — same triage machinery as the robots)
Append ONE dated block to `queue/inbox/from-cowork.md` in the brendan_brain repo. If this
session cannot write to the repo, output the block as text for Brendan to paste (say so
plainly — never claim it was synced).

```
## YYYY-MM-DD — cowork session summary: <3-6 word topic>
- headline: <1-3 lines: what was produced/decided>
- newspaper_ready: <items Brendan would want surfaced, or "nothing meaningful">
- questions_for_brendan: <open questions with context to answer cold, or "none">
- proposed_durable_knowledge: <facts/conclusions worth Brain memory, each with confidence
  and why it's durable, or "none">
- decisions: <decisions Brendan made this session, verbatim intent, or "none">
- preferences_observed: <likes/dislikes/format reactions as EVIDENCE lines, or "none">
- queue_candidates: <follow-up research/tasks worth queueing: title + why + urgency, or "none">
- timeline_events: <dated personal events worth the timeline, with sensitivity, or "none">
- files_worth_preserving: <path/location + one-line what-it-is; REFERENCES, not copies, or "none">
- proposed_domain_or_skill_updates: <structure/skill ideas with evidence, or "none">
- sensitive_items: <anything health/private/financial needing special handling — NAME the
  handling need without quoting the sensitive content, or "none">
- run_status: complete | partial (<what's unfinished>)
```

Sub-fields beyond brain-sync's six are additive — the triage step reads them the same way
(each becomes a task / timeline entry / evidence line / question per MEMORY_POLICY).
Same-day idempotency: if a block with today's heading + same topic exists, REPLACE it.

## Import workflow (Brain side — runs in the next Brendan OS session/routine)
1. Daily-run triage picks up `from-cowork.md` blocks exactly like robot outboxes
   (mark `<!-- triaged YYYY-MM-DD -->` when done).
2. Sensitive_items rows route per PRIVACY_POLICY before anything else is filed.
3. preferences_observed rows append to preferences/PROPOSED_RULES.md evidence — thresholds
   unchanged (one session ≠ a rule).

## Reusable prompt (paste into any Cowork session at wrap-up)
> We're wrapping up. Produce a Brendan Brain handoff block per the cowork-handoff skill
> (brain-sync outbox format, dated today) covering: durable knowledge, decisions,
> preferences observed, open questions, queue candidates, timeline events, files worth
> preserving (references only), proposed domain/skill updates, and sensitive items needing
> special handling. Append it to queue/inbox/from-cowork.md in brendan_brain if you can
> write there; otherwise print it for me to paste. Do not store anything as your own
> permanent memory.
