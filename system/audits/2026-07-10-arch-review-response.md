---
id: audit-20260710-arch-response
artifact_type: report
domain: general
sensitivity: personal
created_at: 2026-07-10
created_by: systems_architect
confidence: high
---
# Response to Opus Architecture Review — 2026-07-10

A fresh-context Opus reviewer challenged the architecture (15 findings). Disposition of
each, per the independent-assurance protocol (accept & repair / partially accept / reject
with evidence / record as limitation):

| # | Finding | Disposition |
|---|---|---|
| 1 | Integration dark on robots' `main` | **Accepted as known constraint, not a defect.** This build may not push to robots' `main` (Brendan-reviewed branches only, per his scope grant). Activation requires Brendan: merge the 4 `claude/*` branches AND add brendan_brain to each routine's repo selection. Stated in ROUTINE_REGISTRY, each BRAIN_INTEGRATION.md, docs/LIMITATIONS.md, and the final report. Round-trip was proven from the working tree in-session. |
| 2 | "Tested" claims preceded tests | **Accepted & repaired.** Review raced the build (tests were written ~30 min after the policies). All 8 suites now exist and pass (tests/results/); policy texts corrected to real filenames. Lesson recorded: never write "tested" before the test exists, even as forward reference. |
| 3 | Sensitivity fails open | **Accepted & repaired.** brain_search now fails closed by DOMAIN (health/investing) regardless of the field; SCHEMAS + validator require `sensitivity` on knowledge/timeline/report. Covered in test_retrieval.sh. |
| 4 | Cross-clone concurrent writes | **Accepted & repaired (detection), limitation (prevention).** validate_frontmatter now errors on two OPEN tasks sharing a dedupe_key (post-merge detection); test_concurrent_writes.sh covers same-file races. True cross-clone prevention is impossible without a coordination server — recorded limitation; recovery is the designed path. |
| 5 | Legend creates phantom evidence | **Accepted & repaired.** Legend/multi-mark lines skipped; regression test added (exactly 4 evidence lines from the fixture edition). |
| 6 | Outbox specified 3 ways | **Accepted & repaired.** Single contract now everywhere: `queue/inbox/from-<robot>.md`, dated `## YYYY-MM-DD` blocks, same-day replace on retry; build_newspaper reads ALL blocks from the last 2 days (not last-block-only). |
| 7 | INDEX.tsv decorative | **Partially accepted.** Search still walks files (correct at 15 artifacts; policy documents the ~5k revisit threshold honestly). The index remains the browsing/metadata surface. Deferred with evidence per nonnegotiable principle 6. |
| 8 | Sort bug + thin recall | **Accepted & repaired.** Single sort (score desc, recency desc); light plural stemming. Alias maps deferred until retrieval tests show recall failures. |
| 9 | Validator gaps | **Accepted & repaired.** Orphan .md detection in artifact dirs; REQUIRED_BY_TYPE aligned to SCHEMAS (report/decision/edition/knowledge); origin_repository required on tasks. |
| 10 | oplog not self-persisting | **Accepted & repaired.** start/set now auto-commit the op record (local commit survives a failed push of the operation itself). |
| 11 | Generated files committed → churn | **Rejected in part, mitigated.** QUEUE.md/BRAIN_MAP.md stay committed — Brendan reads them on GitHub, which is half their purpose. Conflict cost is bounded by the regenerate-on-conflict rule (CLAUDE.md) and tested. INDEX.tsv kept for the same reason. Revisit if churn proves painful. |
| 12 | Health sanitization unenforced | **Accepted & repaired (minimal).** build_newspaper scrubs health outbox blocks containing numeric dose/biometric patterns and withholds them with a visible flag. Deeper linting recorded as a next improvement. |
| 13 | pycache committed | **Accepted & repaired** (.gitignore + removal). Independently caught by test_concurrent_writes. |
| 14 | BRAIN_INTEGRATION.md missing in 3 repos | **Rejected with evidence.** All four repos have it; pushed before the review concluded (operator-notebook 05a050a, FootyBot 80f88bf, trading-notebook 1412be5, health-notebook 33d1d48 — verified via ls-remote). The review snapshot predated those pushes. |
| 15 | "Universal capture" overclaimed | **Accepted.** docs/LIMITATIONS.md words capture scope honestly: capture happens in Brain-enabled sessions/routines that invoke the skills; there is no platform-wide conversation tap. |

Verification: full suite rerun after repairs — 8/8 PASS at the time of that run
(tests/results/run-20260710-034458.md). CORRECTION (Chief Skeptic, later on 2026-07-10):
that run predated committing tests/test_forgetting.sh, which contained a self-referential
marker and failed 7/8 once committed. Repaired (runtime-built marker + tests/ excluded from
sweeps + positive fixture assertion); suite green again on committed HEAD. The reviewer's
concurrent-session collision with this build (its finding #4 narrative) was itself a live
demonstration of the recovery path: mixed commit unwound, files recovered, history intact.
