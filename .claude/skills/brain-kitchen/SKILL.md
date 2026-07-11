---
name: brain-kitchen
description: >-
  Kitchen & Food desk operations for Brendan OS: meal/menu planning, recipe research,
  pantry and receipt ingestion, shopping gap analysis, prep timing, cooking plans, and
  post-cook feedback. Use when Brendan mentions cooking, meals, recipes, groceries,
  receipts, pantry, menus, drinks, or desserts — e.g. "plan this menu", "research the best
  pot pie method", "here's my receipt", "what should I make with what I have", "we cooked
  it — here's how it went".
---
<!-- brendan-os-skill-version: 1.0.0 (2026-07-11) — canonical source: brendan_brain/.claude/skills/brain-kitchen -->
# brain-kitchen

Home: `domains/concierge/kitchen/` (KITCHEN_PROFILE.md = knowledge + BINDING bridge rules;
PANTRY.md + EQUIPMENT.md = live_state, edit in place). Route the request first
(brain-intake): same-day cook → mode 4; overnight research → mode 3/5; "keep ideas coming"
→ watch. Default `--publish file_only` — kitchen articles reach the paper only on request.

## Operations

**Ingest receipt/groceries** — Save paste to a temp file, run
`python3 tools/receipt_to_pantry.py --paste-file <f> [--receipt] --source "<store date>"`.
Confirm the parsed rows back to Brendan in one line; fix mis-parses with --add/--remove.
Photo pastes: transcribe to the paste format first, then ingest.

**Pantry update** — `--add "2 lb flour" [--expires ...]` / `--remove "flour"` / `--list`.
Cooking a plan consumes items: remove/decrement used rows the same day.

**Recipe research** — Per `system/BROWSER_RESEARCH_POLICY.md`: WebSearch, compare ≥3
credible sources per dish, SYNTHESIZE the method (never copy a recipe verbatim), cite
source URLs + access date, note where sources disagree. Check FOOD_GUIDANCE.md and set
`health_alignment` + one generic reason per bridge rules (KITCHEN_PROFILE — labels stay
OUT of the newspaper). Respect stated preferences over guidance, with a polite note.

**Menu design** — For each dish: method summary, active/passive time, advance-prep needs.
For the menu: execution order, oven/stove conflicts, a timed plan back-computed from
serving time, and a drink/dessert that fits the profile's fun rule.

**Shopping gap analysis** — Recipe ingredients minus PANTRY rows (confidence `confirmed`/
`likely` counts; `guess` → verify). Append gaps to PANTRY §Shopping with the plan's task id.

**Advance-prep reminders** — Every night-before step (dough rest, chilling, marinade)
becomes its OWN same-day task with a deadline (brain-intake mode 4) when the menu is
planned — never buried in plan text.

**Leftovers & waste** — When planning, check PANTRY for items expiring ≤5 days out and
prefer methods that use them; suggest a leftover use in the plan's last line.

**Post-cook feedback** — Create `domains/concierge/kitchen/outcomes/meal-YYYYMMDD-<slug>.md`
(knowledge; new file per cook): verdict, what worked/failed, changes for next time. Update
KITCHEN_PROFILE loved/disliked lists and log a preference-evidence line
(preferences/PROPOSED_RULES.md). Repeated signals promote per MEMORY_POLICY — propose,
never self-confirm.

## Hard rules
- NEVER read health-notebook or `sensitivity: health` artifacts from kitchen work; the
  bridge source is `domains/health/FOOD_GUIDANCE.md` ONLY, and `health_alignment` labels
  never leave kitchen artifacts (leak-gated by tests/test_health_kitchen_bridge.sh).
- Health guidance never diagnoses, never claims treatment, never becomes a permanent
  restriction without Brendan's confirmation.
- No purchases, orders, or bookings — plans and lists only (AUTONOMY_POLICY #3).
- Don't assume unlisted equipment; ask or provide alternatives.
- After writes: validate, rebuild indexes, commit (`concierge: ...`), push, verify.
