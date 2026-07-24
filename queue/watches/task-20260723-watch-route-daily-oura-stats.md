---
id: task-20260723-watch-route-daily-oura-stats
title: Watch: route daily Oura stats
artifact_type: watch
domain: health
sensitivity: health
status: watching
created_at: 2026-07-23
urgency: normal
depth: standard
effort_budget: 1_pass
publication_destination: none
recurrence: watch
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: health/watch-route-daily-oura-stats
next_run: 2026-07-31
last_run: 2026-07-24
publish_policy: on_change
---

## Request

Route daily oura stats.

## Constraints

Pull the raw metrics that matter each day, not the composite Readiness score: nighttime RMSSD (HRV), sleeping RHR, body-temp deviation, total sleep time, deep, REM, sleep-onset latency, respiratory rate. Flag deviations vs the 30-day baseline per the Early-Warning Dashboard (Protocol Master §12/§13). Terse daily line, escalate only on threshold breaches.

## Assumptions

(none yet)

## Questions

(none yet)

## Research Log

- 2026-07-24 [sonnet] First scheduled run. BLOCKED: no Oura data source is wired into the Brain — no Oura connector/API is configured in this environment (CONNECTOR_POLICY has no Oura entry; no oura data file exists in-repo). The routine cannot pull nighttime RMSSD/RHR/temp-deviation/sleep-stage metrics without a connection. No change to publish (publish_policy: on_change). ACTION NEEDED FROM BRENDAN: connect Oura (API token / export path) so this watch can route daily stats; until then it will report BLOCKED each run rather than fabricate numbers.
