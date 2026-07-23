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
next_run: 
last_run: 
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
