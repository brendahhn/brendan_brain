---
id: tl-20260724-personal-os-notes-loss
artifact_type: timeline
created_at: 2026-07-24
domain: general
sensitivity: personal
entities: [personal-os, supabase]
verbatim: false
topics: [personal-os, data-loss, tea, infrastructure]
---
Brendan reported ("deeply alarming") that notes he wrote in the personal-os
website under a "BUY" category — tea and purchase notes he'd spent significant
time on — did not save and were gone. Cause: the app's Supabase writes were
fire-and-forget (failures silently console.warn'd, no retry, no local copy,
no user-facing error; failed loads masked by seed data). Fixed same day on
branch `claude/buy-section-notes-save-sxs6k1` of brendahhn/personal-os
(commit 8895da5): durable localStorage outbox with retry, local mirror
fallback, visible sync badge, delete guards, plus supabase/schema.sql for the
suspected DB-side rejection (integer id overflow / missing columns). The lost
notes themselves were not recoverable from the session container (Supabase
host unreachable from sandbox); recovery steps were given to Brendan to check
the notes and trash tables and Supabase backups directly.
