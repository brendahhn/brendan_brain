<!-- version: 1.0.0 (2026-07-11) -->
# V2 Acceptance Scenarios → automated tests vs demos

Per arch-challenge response #10, the 20 spec scenarios split honestly: **automated** =
deterministic offline test in `tests/run_all.sh` (synthetic data); **demo** = executed
once for real in the build session (WebSearch-bounded, artifacts labeled), NOT an
automated gate; **policy** = enforced by binding policy + review, no mechanical test
possible today.

| # | Scenario | Coverage |
|---|---|---|
| 1 | Cream puff & pot pie planning | **demo**: task-20260711-potpie-menu (queue) + kitchen plan artifact + newspaper section demo |
| 2 | Same-day cooking request | **automated** (routing: test_intake_routing mode 4) + **demo** flow documented in brain-kitchen |
| 3 | Receipt → pantry extraction | **automated**: test_receipt_pantry |
| 4 | Health guidance → recipe bridge | **automated**: test_health_kitchen_bridge (leak gate) |
| 5 | Martial arts research | **demo**: task + article in domains/concierge/ (real WebSearch pass) |
| 6 | Tacoma product & listing research | **demo (V1, done)**: completed task + active watch task-20260710-watch-vehicles-tacoma-search-90w |
| 7 | Immediate answer only | **automated**: test_intake_routing |
| 8 | Immediate answer + overnight research | **automated**: test_intake_routing |
| 9 | One-time tech question, no durable memory | **automated**: test_intake_routing (ephemeral guarantee) |
| 10 | Dynamic cooking domain proposal | **automated**: test_domain_proposal (synthetic fermentation topic) |
| 11 | Cowork Brain handoff | **automated**: test_cowork_handoff |
| 12 | Gmail connector result sanitization | **automated**: test_injection_sanitize (hostile_email fixture) |
| 13 | Shopify insight without customer PII | **automated** (PII scrub path: test_injection_sanitize) + **policy**: CONNECTOR_POLICY fail-closed pending q-20260711-shopify-ownership |
| 14 | Browser prompt injection | **automated**: test_injection_sanitize (hostile_recipe_page) |
| 15 | Browser freshness recheck | **automated (partial)**: access-date fencing in test_injection_sanitize; re-query near publication is **policy** (BROWSER_RESEARCH rule 6 + Publisher checklist 1) — no live browsing in this environment to test against |
| 16 | Model usage logging | **automated**: test_usage_learning |
| 17 | Skill proposal & creation | **automated**: test_skill_quality + foundry tracker |
| 18 | Learning from repeated newspaper reactions | **automated**: test_usage_learning (threshold candidates) |
| 19 | Interest change detected without silent profile rewrite | **automated**: test_usage_learning (profile checksum unchanged) |
| 20 | Trading run before Brain editorial | **automated**: test_schedule_gate |
