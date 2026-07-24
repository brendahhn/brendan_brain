---
id: tl-20260724-personal-os-second-loss-never-deployed
artifact_type: timeline
created_at: 2026-07-24
domain: general
sensitivity: personal
entities: [personal-os, vercel]
verbatim: false
related: [tl-20260724-personal-os-notes-loss, tl-20260724-personal-os-notes-mostly-recovered]
topics: [personal-os, data-loss, deployment, process-failure]
---
Brendan lost a second batch of notes (a rebuilt tea section) the night after the
durability fix was written. Root cause was NOT the new code: the fix was pushed
to branch claude/buy-section-notes-save-sxs6k1 and never merged, so
personal-os main was still the original fire-and-forget code (2cb79e8) and the
site he typed into had none of it. Compounding factor discovered here: Brendan
ships this app by MANUALLY PASTING code, so any fix left on a branch reaches
production only if he copies it. Process lesson: for this repo a fix is not
"done" until it is on main and he has confirmed the deployed page shows it.
Resolution: merged to main (cc0f8c0) with his explicit approval; added an
explicit SAVE button (his request: "do we need a big ass save button?"), a
beforeunload guard for sign-out, and quota-safe outbox persistence. Deploy is
now self-verifying — the SAVE button is visible only in the fixed build.
