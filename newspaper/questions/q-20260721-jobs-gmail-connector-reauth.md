---
id: q-20260721-jobs-gmail-connector-reauth
title: Jobs Robot — Gmail connector degraded 4 runs; can you reconnect it?
artifact_type: question
task_id: none
kind: material
status: open
asked_at: 2026-07-21
created_at: 2026-07-21
domain: jobs
sensitivity: personal
origin_repository: operator-notebook
derived_from: [inbox-jobs-robot-20260721]
topics: [gmail-connector, application-tracking, infrastructure]
---
The Gmail connector has now been degraded for **4 consecutive Jobs Robot runs** (across ~3
weeks): only the Trash/Spam label tools are exposed — no search, read, or draft. This blocks two
things the Robot otherwise does: application-status tracking (STEP 2 status scan) and delivering
application drafts by email (STEP 8). It won't self-heal.

Ask: can you manually reconnect / re-auth the Gmail connector?

While you're in the inbox, the Robot also suggests a manual look at the **Jun-11 application
cohort** (XiFin / Chromalloy / Kyocera / Eventeny) — now ~40 days out with no confirmable reply.
