<!-- V2 subsystem ledger: everything shipped 2026-07-11 is PROVISIONAL (arch-challenge
     response #16). The weekly review checks this table; a subsystem with no acted-upon
     output by its review date auto-flags for removal (proposal, not silent deletion). -->
# V2 Subsystem Ledger

| Subsystem | Shipped | Review date | Retirement trigger | Rollback |
|---|---|---|---|---|
| Intake router (INTAKE_POLICY, brain-intake, route_intake.py) | 2026-07-11 | 2026-08-15 | Brendan overrides >50% of routings, or unused | delete skill+tool+policy; new_task.py flags remain |
| Concierge domain + desk charter | 2026-07-11 | 2026-08-15 | <3 concierge artifacts by review | dissolve to general (DOMAIN_POLICY provisional path) |
| Kitchen system (profile, pantry, brain-kitchen, receipt tool) | 2026-07-11 | 2026-08-15 | no pantry/plan use by review | archive kitchen/ folder; remove skill |
| Health→Kitchen bridge (FOOD_GUIDANCE) | 2026-07-11 | 2026-08-15 | health robot never populates it, or any leak incident (immediate) | empty the file; kitchen labels default `unclear` |
| BROWSER_RESEARCH_POLICY + sanitize_external.py | 2026-07-11 | 2026-08-15 | n/a (safety floor — retire only by replacement) | — |
| CONNECTOR_POLICY | 2026-07-11 | 2026-08-15 | n/a (safety floor) | — |
| cowork-handoff + from-cowork inbox | 2026-07-11 | 2026-08-15 | no handoff blocks by review | remove skill; keep any triaged content |
| Domain proposals (propose_domains.py) | 2026-07-11 | 2026-08-15 | only false-positive proposals | remove tool; manual ladder remains |
| Learning engine (LEARNING_POLICY, learning_report.py) | 2026-07-11 | 2026-08-15 | two consecutive stub-only months AND no proposals acted on | remove tool; evidence log remains |
| OCI charter | 2026-07-11 | 2026-08-15 | per its own §guardrail 5 | drop to on-failure-only |
| Skill Foundry checklist | 2026-07-11 | 2026-08-15 | no graduation in 60 days → fold into OCI review | delete file |
| Usage log (log_usage.py + ledger format) | 2026-07-11 | 2026-08-15 | rows unused by any review | revert ledger header |
| Schedule plan (SCHEDULE_PLAN) | 2026-07-11 | 2026-08-15 | Brendan doesn't adopt the routine times | doc remains as recommendation |
| Newspaper: concierge section + trading gate | 2026-07-11 | 2026-08-15 | section always empty → drop from BUDGETS | one-line revert in build_newspaper.py |
