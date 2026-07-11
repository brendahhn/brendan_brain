---
id: kitchen-profile
title: Kitchen & Food desk — profile and knowledge
artifact_type: knowledge
domain: concierge
sensitivity: personal
confidence: medium
derived_from: [audit-20260711-v2-preimplementation]
created_at: 2026-07-11
updated_at: 2026-07-11
created_by: systems_architect
topics: [kitchen, food, cooking, recipes, meals, pantry]
---
# Kitchen & Food Desk

Operating skill: `brain-kitchen`. Live pantry/shopping state: `PANTRY.md` (live_state).
Equipment: `EQUIPMENT.md`. Cooking outcomes: one knowledge artifact per cooked meal in
`outcomes/` here (never overwrite — a repeat cook gets a new file). Everything below is
additive; contested entries get a question, not a rewrite.

## Food preferences (evidence-linked; update via annotation/feedback flow)
- Enjoys hearty comfort food done well (pot pie), fun drinks and desserts (Brazilian
  lemonade, cream puffs) — evidence: 2026-07-11 menu request.
- (accumulating — see preferences/PROPOSED_RULES.md evidence log for signals)

## Rejected foods and textures (never suggest without asking)
- (none recorded yet — populate ONLY from Brendan's words or repeated feedback)

## Meals & recipes he LOVED
- (post-cook feedback populates this — each entry links its outcome artifact)

## Meals & recipes he DISLIKED
- (post-cook feedback; keep the reason: flavor, texture, effort, timing)

## Health food guidance (BRIDGE — read rules below)
The ONLY health input this desk may read is `domains/health/FOOD_GUIDANCE.md` (sanitized,
generic, maintained via health-domain sync). NEVER read health-notebook, timeline health
entries, or any `sensitivity: health` artifact from kitchen work.

### Bridge rules (arch-challenge response #1 — binding, leak-gated by tests)
1. Guidance is GUIDANCE, not medical certainty. No diagnosing, no "this recipe treats X",
   no converting tentative research into permanent restrictions.
2. Recipes/menus get a `health_alignment` field: `strongly_aligned | generally_aligned |
   neutral | potentially_conflicting | unclear` + one generic reason (e.g. "uses the
   encouraged-fats list") — never a condition, symptom, metric, or medication.
3. `health_alignment` and its reason live ONLY in kitchen artifacts (`file_only` default).
   They never appear in the newspaper, commit messages, cross-domain output, or logs.
   A published cooking article may say "see the kitchen plan for guidance fit" at most.
4. Brendan's expressed food preferences WIN over guidance; note the tension politely in
   the kitchen artifact ("indulgent pick — balanced elsewhere in the week") and move on.
5. Fun stays fun: guidance shapes the week, not every dish.

## Kitchen equipment
See `EQUIPMENT.md` (live_state). Unknown until Brendan confirms — plans must not assume
gear he hasn't listed (ask or offer alternatives).

## Shopping needs
Live list in `PANTRY.md` §Shopping. Gap analysis = recipe ingredients minus pantry rows
at usable confidence.

## Time-sensitive preparation
Prep steps that must happen the night before (dough rest, marinade, chilling) become
same-day tasks with deadlines via brain-intake mode 4, created when the menu is planned —
not buried in the plan text.

## Cooking calendar
Planned cooks = queue tasks (`domain: concierge`, kitchen topics) with deadlines. The queue
IS the calendar; no parallel calendar file.

## Recipe outcomes
`outcomes/meal-YYYYMMDD-<slug>.md` (knowledge): what was cooked, source method links,
what worked/failed, Brendan's verdict, what to change next time.

## Useful techniques (accumulates from research + outcomes)
- (populated by research tasks; each entry cites its source)

## Favorite menu progressions
- (populated from loved-meal combinations; e.g. hearty main → bright drink → rich dessert
  worked on 2026-07 menu — pending post-cook confirmation)

## Fun drinks & desserts
- Strawberry Brazilian lemonade, strawberry cream puffs (requested 2026-07-11; outcomes
  pending).

## Ingestion (manual-first — honest about sources)
No OCR/receipt connector exists in this environment. Paths that work today:
1. **Receipt/grocery paste** → `python3 tools/receipt_to_pantry.py --paste-file <f>
   --source "<store YYYY-MM-DD>"` (idempotent per source tag).
2. **Quick pantry edits** → edit PANTRY.md directly (live_state allows it) or
   `receipt_to_pantry.py --add "2 lb flour"` / `--remove "flour"`.
3. Photos of receipts: Brendan can paste a photo into a Brain-enabled session; the session
   transcribes to the paste format, then runs the tool (the transcription is the model's,
   the ledger row cites it).
Copyright rule: research SYNTHESIZES methods and cites sources; never copy a full recipe
text into the Brain.
