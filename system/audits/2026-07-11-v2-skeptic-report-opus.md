---
id: audit-20260711-v2-skeptic-opus
title: Fresh Opus Chief Skeptic attack report on V2 (verbatim summary of findings + verdict)
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-11
created_by: chief_skeptic_opus
related: [audit-20260711-v2-finding-disposition]
topics: [audit, v2, skeptic, privacy, security]
---
# Opus Chief Skeptic Report — V2 (2026-07-11)

Fresh opus subagent, read-only, inspected files/history/tools and ran live bypass probes.
Full disposition: `2026-07-11-v2-finding-disposition.md`.

## CRITICAL
- **C1 — Health reasoning leaks into the newspaper through `## Findings` prose; the leak gate cannot see it.** build_newspaper copies Findings verbatim; redaction keyed only on the task's own `sensitivity` field; kitchen tasks are `personal` by design. PROVEN: a personal-tagged concierge task with "lipid panel showed LDL at 165 mg/dL and his cardiologist advised…" landed verbatim in a draft. The bridge test asserted on frontmatter tokens build_newspaper never copies — it tested a structural no-op.
- **C2 — Sanitizer fence spoofable by page content**: a literal `<<<END UNTRUSTED>>>` in the body closed the fence early, leaving hostile "SYSTEM:" text OUTSIDE the untrusted region, exit 0, no flag. The sanitizer actively helped the attacker.

## MAJOR
- **M1 — Injection detection trivially bypassable** (fullwidth-homoglyph, base64, split-across-lines, HTML entities all passed clean); fixtures only fed pre-matched ASCII; LIMITATIONS didn't say so for this tool. "Defenses built and tested" was OVERSTATED.
- **M2 — Connector "fail-closed/BLOCKED" is prose only**: no code references Shopify/QuickBooks or the blocking question; tools loadable in-session; honor system, weakly documented.
- **M3 — FOOD_GUIDANCE wall test is a weak keyword subset** (missed cholesterol/hypertension/LDL/blood-pressure-class terms); no write-time validation existed in production.
- **M4 — Freshness window (today OR yesterday) masks a robot that died today but ran yesterday**: reported "fresh", no [FAIL], yesterday's market note republished as current. Timezones: gate computed in UTC while SCHEDULE_PLAN speaks PT — absorbed by the 2-day window but undocumented; no month-boundary bug (verified).

## MINOR
- m1 — test_skill_quality tests 4 header greps, not the "12 anatomy points" its comment claimed (skill contents themselves verified honest — every cited flag exists).
- m2 — LEARNING_POLICY licensed "±1 weight moves on repeated evidence", contradicting its own proposal-only header (latent; no tool performs it).
- m3 — process_annotations DOES auto-edit INTEREST_PROFILE on explicit STOP COVERING (defensible; asymmetry was undocumented). Learning regex verified correct against the real evidence-log format.
- m4 — Martial-arts demo: two real stats conflated under one PMC id (both papers real, numbers accurate, epistemics honest — a mis-pinned citation, not fabrication).
- m5 — Dead assertion in test_usage_learning; scenario-19 checksum proves a structural no-op.

## Clean
Bloat/ledger audit clean: only kitchen/ exists under concierge; 8 desks are dormant rows; V2_LEDGER retirement rows complete; modified-not-new policies need no rows.

## Verdict table (as delivered)
"V2 implemented" TRUE · "Tested" OVERSTATED (C1/C2 untested no-ops) · "Demoed" TRUE ·
arch#1 leak-gating OVERSTATED→effectively FALSE · arch#2 fail-closed OVERSTATED ·
arch#3 proposal-only TRUE (m2 caveat) · arch#4 no-scaffolding TRUE · arch#8 injection OVERSTATED ·
arch#9/#20 schedule gate MOSTLY TRUE (M4) · arch#16 retirement TRUE · "all 16 honored" OVERSTATED (14 in substance).

Bottom line: design and documentation unusually honest, demos clean, but the two
safety-critical guarantees rested on model discipline, not the cited mechanisms —
C1 and C2 block "safe to activate" until fixed. (Both were fixed the same session —
see the disposition and repair commits.)
