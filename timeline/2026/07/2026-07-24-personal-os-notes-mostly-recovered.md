---
id: tl-20260724-personal-os-notes-mostly-recovered
artifact_type: timeline
created_at: 2026-07-24
domain: general
sensitivity: personal
entities: [personal-os, supabase]
verbatim: false
supersedes: tl-20260724-personal-os-notes-loss
topics: [personal-os, data-loss, recovery]
---
Correction to tl-20260724-personal-os-notes-loss: Brendan exported the Supabase
notes table and most "lost" notes are intact — the 7/24 BUY note (47 bullets),
Ella Health (34 bullets incl. the give-birth-abroad line), WFH setup (Logitech
MX Keys S). Confirmed missing (never persisted): Assam-tea bullets, a 7/24
L-theanine note, a 24 Bottles item. Loss pattern = tail-end writes dropped by
the old fire-and-forget saver (integer-id-overflow theory ruled out; saved ids
reach 1.78e15). Audit pass shipped same day (personal-os d419006): memoized
rendering, faster retry pump, checked-in Playwright smoke/stress suites (13
green). A prior symptom report existed in his 6/22 note "OS Fixes (to Claude)":
"nothing on the tea stock tab ever saves."
