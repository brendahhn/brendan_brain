---
id: task-20260710-find-2002-2004-toyota-tacoma-2-4l-extra
title: Find 2002-2004 Toyota Tacoma 2.4L extra cab candidates
artifact_type: task
domain: vehicles
status: published
created_at: 2026-07-10
urgency: normal
depth: standard
effort_budget: 1_pass
publication_destination: newspaper
recurrence: none
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: vehicles/tacoma-2002-2004-2.4l-xtracab
deadline: 2026-07-11
word_budget: 300
---

## Request

Find a 2002-2004 Toyota Tacoma with the 2.4L engine and extra cab. Put results in tomorrow's newspaper. Ask useful questions immediately; continue with explicit assumptions; verify listings near publication; allow converting to a watch. [E2E ACCEPTANCE DEMO — listings below are SYNTHETIC]

## Constraints

2002-2004 only; 2.4L 4-cyl; extra cab (Xtracab); San Diego area preferred

## Assumptions

- ~~Budget ≤$15k~~ ANSWERED 2026-07-11: budget ≤$12k (q-20260710-tacoma-budget)
- ~~Either transmission~~ ANSWERED 2026-07-11: manual only
- <150k miles preferred; condition outranks odometer

## Questions

- q-20260710-tacoma-budget (material, non-blocking, asked 2026-07-10)
- DISCOVERED during research: frame-rust inspection standard — these trucks are in Toyota's
  historical frame-rust recall population; does Brendan want only trucks with documented
  frame inspection/treatment? (material, non-blocking; assumed yes-preferred)

## Research Log

> [dedupe 2026-07-10] Same request arrived again (origin: brendan_brain). Treated as +1 interest signal, not a new task.
- 2026-07-10 [sonnet lead, haiku dedup support] Retrieved prior prefs (domain-vehicles). SYNTHETIC-DEMO research pass: 3 candidate listings drafted; freshness check simulated near publication — candidate #2 marked inactive and dropped (stress scenario 10). Discovered frame-rust question filed. Staffing verdict: haiku support not needed at this volume — solo sonnet fine (cost discipline note).

## Findings

**SYNTHETIC DEMO DATA — not real listings.**
1. [SYNTHETIC] 2003 Tacoma Xtracab 2.4L 5-spd, 128k mi, $11,900, Escondido — frame inspected 2024, one owner. (as of 2026-07-10)
2. [SYNTHETIC] ~~2002 Tacoma Xtracab 2.4L auto, 142k mi, $9,800, Chula Vista~~ — listing went INACTIVE at pre-publication verification; dropped.
3. [SYNTHETIC] 2004 Tacoma Xtracab 2.4L 5-spd, 156k mi, $10,500, Oceanside — over mileage assumption; included as condition-first candidate; needs frame docs.

## Verification

Pre-publication freshness pass 2026-07-10 (simulated): #1 active, #2 inactive→dropped, #3 active. Sources would be recorded in sources/SOURCE_REGISTRY.md for real runs.
- 2026-07-11 [sonnet] Brendan answered q-20260710-tacoma-budget via edition annotation: $12k / manual / condition-first. Synthetic candidate #3 (auto) would now be excluded; candidate #1 (5-spd, $11.9k) fits. Recurring coverage moves to the watch task; this task -> published.
