---
id: domain-concierge
title: Personal Concierge — practical life operations
artifact_type: domain_profile
domain: concierge
status: active
domain_status: provisional        # provisional until 2026-08-15; see system/V2_LEDGER.md
created_at: 2026-07-11
created_by: systems_architect
sensitivity: personal
topics: [concierge, kitchen, food, purchases, fitness, travel, home, weekend, technology]
---
# Personal Concierge Department

Practical daily-life operations: one-time questions, same-day planning, overnight research,
and watches about food, purchases, activities, gear, trips, and home life. Requests enter
via `system/INTAKE_POLICY.md` (brain-intake). This is ONE domain; desks below are thin
overlays (AGENT_REGISTRY desk pattern), not folders, agents, or routines.

**Default output is terse and `file_only`.** Concierge items reach the newspaper only when
the task explicitly requests it or Brendan asks (arch-challenge response #13).

## Desk charter
Common to every desk unless a row overrides it — **Default model**: sonnet lead (haiku for
extraction/normalization; opus only via MODEL_ROUTING escalation triggers). **Inputs**:
Brendan's words via intake; WebSearch per system/BROWSER_RESEARCH_POLICY.md; manual pastes.
**Outputs**: task findings, terse plan artifacts, knowledge files in this domain.
**Memory access**: this domain + preferences/ + non-sensitive general; NEVER health-notebook
(kitchen reads only `domains/health/FOOD_GUIDANCE.md`); no business connectors
(system/CONNECTOR_POLICY.md binds connectors to contexts — fail closed). **Privacy**:
`personal` default; purchases/finance amounts stay `financial`-tagged and domain-scoped.
**Publication criteria**: only on explicit request; concierge newspaper section budget 300w.
**Completion standard**: the stated need is met (answer given / plan usable / gap list
actionable), sources cited for researched claims, honest [FAIL] if blocked. **Cost limit**:
1 sonnet pass (`effort_budget: 1_pass`) unless the task says otherwise; escalation logged.

| Desk | Scope | Status | Activation |
|---|---|---|---|
| Kitchen & Food | meal/menu planning, recipes, pantry, shopping gaps, prep timing, post-cook feedback | **ACTIVE** — see `kitchen/` + brain-kitchen skill | active now (real demand: pot-pie menu) |
| Purchases & Products | product comparisons, price checks, owner sentiment, buy/wait calls | dormant | ≥3 artifacts on purchase questions |
| Vehicles | LINK — lives in `domains/vehicles/` (Tacoma watch etc.); desk = that domain's profile | linked | already active as its own domain |
| Fitness & Activities | training options, martial arts, scheduling around surf, gear | dormant (martial-arts task runs here under general concierge rules) | ≥3 artifacts |
| Personal Technology | device questions, storage, backups, app choices — mostly mode-1 ephemeral | dormant | ≥3 non-ephemeral artifacts |
| Weekend Planning | local events, conditions, short outings | dormant | ≥3 artifacts |
| Travel & Logistics | trips, bookings research (never booking without approval) | dormant | ≥3 artifacts |
| Home & Storage | organization, storage solutions, household maintenance | dormant | ≥3 artifacts |

Dormant means: requests still get handled under the common charter above (nothing is
refused); the desk row just gains no standing structure until the DOMAIN_POLICY ladder
(≥3 artifacts) is met — then note activation here with the evidence.

## Escalation rules (all desks)
Health/money-consequential conclusion → opus review (MODEL_ROUTING). Purchase execution,
bookings, messages, anything external → **Brendan only** (AUTONOMY_POLICY #3). Kitchen items
touching health guidance → bridge rules in `kitchen/KITCHEN_PROFILE.md`, leak-gated.

## Active questions
(none)
