---
id: q-20260819-cmgh-egress-unblock
title: CMGH journal-article task is blocked ~3 weeks on web egress — open the allowlist or paste the text?
artifact_type: question
task_id: task-20260723-read-summarize-the-cmgh-journal-article
kind: material
status: open
asked_at: 2026-08-19
created_at: 2026-08-19
domain: health
sensitivity: personal
origin_repository: health-notebook
derived_from: [inbox-health-robot-20260819]
topics: [cmgh, blocked-task, egress, sandbox, unblock]
---
The task "read & summarize the CMGH journal article"
(`task-20260723-read-summarize-the-cmgh-journal-article`) has been stuck since it was queued
(target was Mon 2026-07-27 — now ~3 weeks overdue). The request is one specific article at a fixed URL
(`https://www.cmghjournal.org/article/S2352-345X(26)00103-7/fulltext`).

The blocker is environmental, not effort: the health-robot's sandbox blocks all outbound WebFetch
(egress allowlist — only WebSearch works), and the 2026 in-press article is **not yet indexed**, so it
can't be resolved by title/author search either. The health robot correctly **refused to guess** rather
than hallucinate a source match. The Brain routine confirmed on 2026-08-19 that its own sandbox is
**also egress-blocked for `cmghjournal.org`** — so neither agent can fetch it.

Two ways to unblock (either works):
1. **Open the environment's web-egress allowlist** so `cmghjournal.org` can be fetched (the same one-time
   fix flagged in the health-notebook SANDBOX_CAPABILITIES), or
2. **Paste the article's title or text** and the health robot will review it next run.

Until then the task stays `active`, honestly blocked. Low urgency, but it won't self-heal.
