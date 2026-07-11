---
id: audit-20260711-v2-finding-disposition
title: V2 reviewer finding disposition — every finding, repair, test, and rollback
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-11
created_by: systems_architect
related: [audit-20260711-v2-qa-sonnet, audit-20260711-v2-skeptic-opus]
topics: [audit, v2, repairs, disposition]
---
# V2 Finding Disposition (2026-07-11)

Severities: Critical / High / Medium / Low / Accepted risk / False positive.
Every repair was re-inspected in the final files and re-exercised by the named test.
Suite after all repairs: **19 PASS · 0 FAIL · 1 SKIP** (skill_sync cross-repo — sibling
repos absent in this session; skips are reported distinctly, never as passes).
Rollback for any single repair: `git revert` of the named commit; none is load-bearing
for V1 behavior.

| # | Finding (source) | Severity | Disposition | Repair | Test |
|---|---|---|---|---|---|
| C1 | Medical prose in Findings reaches the paper; leak test asserted a structural no-op (Skeptic) | **Critical** | Accepted | `scrub_medical()` content scan in build_newspaper (frontmatter AND prose; health-section-only allowance); leak-probe task added to the test asserting on PROSE with a required redaction notice | test_health_kitchen_bridge (C1 probe) — PASS |
| C2 | Fence sentinel spoofable by body content (Skeptic) | **Critical** | Accepted | FENCE regex neutralizes embedded markers pre-fencing + flag | test_injection_sanitize (spoof block) — PASS |
| M1 | Injection regexes bypassed by homoglyph/base64/split-lines/entities (Skeptic) | High | Accepted (bypass-resistant detection; residual risk documented) | NFKC normalization + base64 decode buffer + whitespace collapse; LIMITATIONS #21 states residual miss classes plainly | test_injection_sanitize (3 evasion regressions) — PASS |
| M2 | Connector fail-closed is prose, not mechanism (Skeptic) | High | Accepted (honesty) + Accepted risk (mechanism) | CONNECTOR_POLICY "Enforcement honesty" section + LIMITATIONS #22; mechanical option (settings.json deny rules for `mcp__Shopify__*`/`mcp__Intuit_QuickBooks__*`) documented for Brendan | policy text (no mechanical test possible in-session) |
| M3 | FOOD_GUIDANCE wall = weak keyword grep, no write-time gate (Skeptic) | High | Accepted | `check_food_guidance()` linter in validate_frontmatter --all (runs every daily bootstrap); broader medical-term list | verified live (bad row → 1 error; clean → 0) + runs inside every suite validation |
| M4 | Yesterday-only block reported "fresh"; stale content republished as current (Skeptic) | High | Accepted | three-state freshness (today/STALE/missing) in check_inputs; [STALE] notice auto-inserted in drafts; --require now demands TODAY | test_schedule_gate — PASS (fresh-today path); STALE path exercised live 2026-07-11 |
| QA1 | Mid-word truncation, no marker, both slice sites | High | Accepted | shared `trim()` word-boundary + " […]" at both sites | draft rebuild verified; covered by bridge/schedule tests that read drafts |
| QA2 | Pipe chars corrupt pantry/ledger tables | Medium | Accepted | `cell()` escaping in both writers | test_receipt_pantry + test_usage_learning — PASS |
| QA3 | Binary paste → raw traceback | Low | Accepted | clean error, nothing written | manual repro fixed (exit message, no traceback) |
| QA4 | Negative qty mangled silently | Low | Accepted | malformed lines skipped + reported | manual repro fixed |
| QA5 | Router conflict = list order, no hint | Medium | Accepted | last-stated-intent wins + CONFLICT hint; "don't save this" overlap fixed with lookbehind | test_intake_routing — PASS |
| QA6 | Sanitizer miss classes undocumented; exfil-markdown missed | Medium | Accepted | exfil patterns added (tracking-pixel/verbatim-echo); LIMITATIONS #21 | manual: QA's exact payload now exit 2; plain image exit 0 |
| m1 | Skill test claims 12-point coverage, tests 4 | Low | Accepted | comment states the honest mechanical subset; added referenced-tool-exists check | test_skill_quality — PASS |
| m2 | LEARNING_POLICY ±1-weight contradiction | Low | Accepted | weight moves are proposals like everything else | policy text |
| m3 | STOP COVERING auto-edit asymmetry undocumented | Low | Accepted (behavior is correct: explicit instruction) | documented as the one deliberate exception in LEARNING_POLICY | test_annotations already covers the behavior |
| m4 | PMC citation conflation in martial-arts demo | Low | Accepted | citation split to the two real papers | file inspected |
| m5 | Dead token assertion; weak checksum proof | Low | Accepted | real token-column assertions | test_usage_learning — PASS |
| QA7 | Concurrent mutation of the branch during QA | — | **Accepted risk** (process note) | reviews of a live branch are noted in reports; final suite ran on the final HEAD with the SHA recorded in the results file | run_all records tested SHA |
| Bug A | Prose/tutorial text parsed as annotations; reruns duplicated (production run) | **Critical** | Accepted | baseline-diff parsing (only post-publication lines) + --apply idempotency guard | test_annotation_regression — PASS (4 required proofs) |
| Bug B | Cancelled synthetic watch reached the paper; runner/builder disagreed (production run) | **Critical** | Accepted | shared `brainlib.is_active_watch` + `watch_is_due` (empty next_run ≠ due unless never-run) used by BOTH tools | test_watch_eligibility — PASS (each excluded status) |
| TZ | UTC dates vs PT user expectations (mandate §11) | High | Accepted | brainlib PT time policy (today/now_pt/editorial_date); all tools patched; schedule doc states policy | test_timezone — PASS (midnight/rollover/DST×2/market-open/naming) |

## Remaining accepted risks (stated, not hidden)
1. Connector blocking is policy + optional deny-rule, not platform enforcement (M2).
2. Sanitizer is a tripwire; novel encodings/phrasings can pass (M1/QA6) — the wall is the
   fence contract (external content is data), which is model behavior governed by policy.
3. "Still running" is mechanically indistinguishable from "missing" for the gate; the
   editor's one re-check before the Publisher pass is the mitigation (SCHEDULE_PLAN).
4. Cross-repo skill-sync drift check SKIPs in sessions without sibling repos.
