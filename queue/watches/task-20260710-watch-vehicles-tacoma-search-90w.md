---
id: task-20260710-watch-vehicles-tacoma-search-90w
title: Watch: Vehicles — Tacoma search  (~90w)
artifact_type: watch
domain: general
status: watching
created_at: 2026-07-10
urgency: normal
depth: standard
effort_budget: 1_pass
publication_destination: newspaper
recurrence: watch
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: general/watch-vehicles-tacoma-search-90w
last_run: 2026-08-11
next_run: 2026-08-18
---

## Request

Brendan asked for a watch (2026-07-11): 'make this a watch — check listings weekly'.

## Assumptions

(none yet)

## Questions

(none yet)

## Research Log

### 2026-07-20 (weekly pass; was due 2026-07-17)
Criteria: 2002-2004 Tacoma, 2.4L 4-cyl, Xtracab, manual only, ≤$12k, condition-first
(<150k mi preferred). WebSearch pass returned only marketplace index pages (Edmunds,
Cars.com, CarGurus, eBay) and transmission-parts listings — no individual live listing
with a verifiable price/URL/mileage. Live per-listing inventory on those sites is
JS-rendered and unreachable from a scheduled WebSearch-only run (same egress limit noted
across other robots). **No change to report** → nothing published (publish_policy=on_change).
To actually surface listings, Brendan would need to run a filtered CarGurus/Cars.com search
locally (or paste results into the Brain). next_run advanced to 2026-07-27.

### 2026-07-27 (weekly pass; due today)
Criteria unchanged: 2002-2004 Tacoma, 2.4L 4-cyl, Xtracab, manual only, ≤$12k, condition-first
(<150k mi preferred). WebSearch pass again returned only marketplace index/aggregator pages
(Edmunds, Cars.com, CARFAX, eBay, Tacoma World forum) plus a factory-service-manual thread —
no individual live listing with a verifiable price/URL/mileage, and no SoCal-filtered result.
Same structural egress limit as prior weeks (per-listing inventory is JS-rendered, unreachable
from a WebSearch-only scheduled run). **No change to report** → nothing published
(publish_policy=on_change). This is now the 3rd consecutive dry pass from the same cause; the
reliable unblock remains Brendan running a filtered Cars.com/CarGurus search locally (or pasting
listings into the Brain). next_run advances to 2026-08-03.

### 2026-08-04 (weekly pass; was due 2026-08-03, no run fired 08-03)
Criteria unchanged: 2002-2004 Tacoma, 2.4L 4-cyl, Xtracab, manual only, ≤$12k, condition-first
(<150k mi preferred). WebSearch pass again returned only marketplace index/aggregator pages
(Edmunds, Cars.com, Carsforsale, JDPower, craigslist SF-bay) — the one individual auction hit
(Cars & Bids 2002 Xtracab) is a **V6**, not the 4-cyl target, and not SoCal. No individual live
4-cyl/manual listing with a verifiable price/URL/mileage in the SoCal window. Same structural
egress limit as prior weeks (per-listing inventory is JS-rendered, unreachable from a
WebSearch-only scheduled run). **No change to report** → nothing published
(publish_policy=on_change). 4th consecutive dry pass from the same cause; the reliable unblock
remains Brendan running a filtered Cars.com/CarGurus search locally (or pasting listings into the
Brain). next_run advances to 2026-08-11.

### 2026-08-11 (weekly pass; due today)
Criteria unchanged: 2002-2004 Tacoma, 2.4L 4-cyl, Xtracab, manual only, ≤$12k, condition-first
(<150k mi preferred). WebSearch pass again returned only marketplace index/aggregator pages
(Edmunds, Cars.com, Carsforsale, JDPower, KBB) plus Tacoma World forum threads — no individual
live SoCal 4-cyl/manual listing with a verifiable price/URL/mileage. The one concrete forum hit
(2002 Xtracab 2.4L 5spd 2wd, $3,600) is **360k miles** — far over the <150k-mi condition
preference — and not confirmed SoCal, so it fails criteria. Same structural egress limit as prior
weeks (per-listing inventory is JS-rendered, unreachable from a WebSearch-only scheduled run).
**No change to report** → nothing published (publish_policy=on_change). This is now the 5th
consecutive dry pass from the same cause; the reliable unblock remains Brendan running a filtered
Cars.com/CarGurus search locally (or pasting listings into the Brain). next_run advances to
2026-08-18.
