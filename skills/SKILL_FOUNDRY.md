<!-- version: 1.0.0 (2026-07-11) | status: provisional until 2026-08-15 (system/V2_LEDGER.md) -->
# Skill Foundry

How repeated workflows graduate into canonical skills (`.claude/skills/` here, synced via
`tools/sync_skills.sh` — one canonical source, SKILL_REGISTRY unchanged as the inventory).
The foundry is a CHECKLIST, not a department (arch-challenge response #7): no skill ships
to satisfy this document.

## Graduation criteria (ALL must hold)
1. Used successfully MORE THAN ONCE (cite the task/run ids).
2. Inputs and outputs clearly definable.
3. Procedure stable (didn't materially change between uses).
4. Validation criteria exist (how does a run know it worked?).
5. Reuse reduces errors or cost vs re-deriving each time.

## Required skill anatomy (all 12, enforced by tests/test_skill_quality.sh)
1 purpose · 2 trigger description (the frontmatter `description` with concrete phrases) ·
3 inputs · 4 outputs · 5 steps · 6 tool permissions (commands it may run) · 7 model routing
(or "inherits MODEL_ROUTING_POLICY") · 8 validation · 9 failure behavior (what to do/say
when a step fails — honesty rules) · 10 examples (trigger phrases count) · 11 version
header (`brendan-os-skill-version`) · 12 evaluation fixtures (a test in tests/ or a named
fixture exercising the skill's mechanical parts).

## Candidate tracker (from the V2 spec; honest status)
| Candidate | Status | Where |
|---|---|---|
| Conversation→Brain extraction | SHIPPED (V1) | brain-ops capture |
| Receipt→pantry | SHIPPED 2026-07-11 | brain-kitchen + tools/receipt_to_pantry.py |
| Recipe research & timing plan | SHIPPED 2026-07-11 | brain-kitchen |
| Immediate-vs-queue routing | SHIPPED 2026-07-11 | brain-intake + tools/route_intake.py |
| Cowork Brain handoff | SHIPPED 2026-07-11 | cowork-handoff |
| Connector result sanitization | SHIPPED 2026-07-11 (tool+policy, not a skill — a skill adds nothing over `tools/sanitize_external.py`) | CONNECTOR_POLICY |
| Product comparison | candidate — 0 completed uses; graduate after 2 successful concierge product tasks | concierge charter covers it |
| Vehicle listing verification | candidate — 1 use (V1 Tacoma task); needs a 2nd | vehicles domain + BROWSER policy |
| Weekly learning review | SHIPPED as tool+policy (tools/learning_report.py); skill wrapper unnecessary | LEARNING_POLICY |
| Domain proposal | SHIPPED as tool (tools/propose_domains.py) inside brain-domain flow | DOMAIN_POLICY |
| Source verification | candidate — folded into BROWSER_RESEARCH_POLICY rules; separate skill only if verification steps stabilize across ≥2 domains | — |
| Newspaper article preparation | SHIPPED (V1) | brain-newspaper |

## Process
Weekly review (CONTINUOUS_IMPROVEMENT) checks the tracker: a candidate with 2+ logged
successful uses gets a graduation proposal (8-field format). New skills: write canonical
SKILL.md → registry row → sync manifest → test → `tools/sync_skills.sh` → verify --check.
Retirement mirrors STAFFING_POLICY (3 strikes of not-earning-its-keep → registry note).
