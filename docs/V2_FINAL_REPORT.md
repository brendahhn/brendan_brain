<!-- version: 1.0.0 (2026-07-11) — release report for the V2 merge -->
# Brendan OS V2 — Final Report

## 1. Executive summary
V2 upgrades Brendan OS from a research/newspaper system into practical life operations:
natural-language request routing, a concierge domain with a working Kitchen desk, a
sanitized health→kitchen bridge, governed connectors, WebSearch-first research with
injection defenses, a Cowork handoff, evidence-gated learning, capacity instrumentation,
and a Pacific-time-aware morning pipeline. Built on branch
`claude/brendan-os-v2-operations-1rg97c`, challenged by a fresh Opus architect BEFORE
implementation (16 criticisms, all dispositioned), reviewed after implementation by a
fresh Sonnet QA operator and a fresh Opus Chief Skeptic (2 criticals + 4 majors found and
REPAIRED same-session), plus two real production bugs from the overnight run fixed with
regression suites. Final suite: **19 PASS · 0 FAIL · 1 honest SKIP**. Everything V2 is
provisional with retirement triggers (`system/V2_LEDGER.md`).

## 2. Architecture
Markdown remains the single source of truth; V2 adds: intake routing (INTAKE_POLICY →
6 Brendan-facing modes compiling to 3 primitives × 2 switches), one `concierge` domain
(desks as dormant charter rows, Kitchen active), one new mutable memory class
(`live_state` — pantry/equipment), a content-level medical scrub on everything entering
the paper, shared watch eligibility, baseline-diff annotation parsing, and a PT time
policy in `brainlib` used by every tool.

## 3-4. Files added / modified
See the PR diff (single source of truth). Highlights — added: 8 policies
(INTAKE/BROWSER_RESEARCH/CONNECTOR/LEARNING/CONTINUOUS_IMPROVEMENT/SCHEDULE_PLAN/
V2_LEDGER/SKILL_FOUNDRY), 3 skills (brain-intake, brain-kitchen, cowork-handoff), 8 tools
(route_intake, receipt_to_pantry, sanitize_external, propose_domains, learning_report,
log_usage, check_inputs + brainlib additions), 12 new test suites, concierge domain +
kitchen files, FOOD_GUIDANCE bridge source, 7 audit/report artifacts, 4 docs
(CONCIERGE_AND_V2_GUIDE, GIT_WORKFLOW, ROUTINE_SETUP_GUIDE, this report). Modified:
build_newspaper (concierge section, FAIL/STALE gates, medical scrub, trim), run_watches,
process_annotations (baseline parsing, idempotency), validate_frontmatter (live_state,
FOOD_GUIDANCE linter), new_task-adjacent schemas, MEMORY/DOMAIN/PUBLICATION/LEARNING
policies, ROUTINE_REGISTRY, DAILY_ROUTINE_PROMPT, run_all harness.

## 5-8. System classification (mandate §5 vocabulary)
| System | Status |
|---|---|
| Life Intake Router | Implemented & verified (tested; live in any Brain-enabled session) |
| Personal Concierge | Implemented & verified (Kitchen active; 7 desks dormant by design) |
| Kitchen Intelligence | Implemented & verified; ingestion manual-paste (no OCR source exists) |
| Health→Kitchen bridge | Implemented & verified (leak-gated, write-time linter); **awaiting first real guidance rows from the Health Robot** |
| Browser Research Policy + injection defense | Implemented & verified offline; live DOM tier **blocked by environment network policy** |
| Connector policy | Implemented (policy); Shopify/QuickBooks **blocked pending Brendan's ownership answer**; Calendar/Drive **blocked by connector enablement** |
| Cowork handoff | Implemented & verified (synthetic); first real handoff pending Brendan using it |
| Dynamic domains | Implemented & verified |
| Learning Engine | Implemented & verified (proposal-only; gate honest) |
| OCI + Skill Foundry | Implemented (charters + gated cadence; first real cycle pending live weeks) |
| Capacity instrumentation | Implemented & verified (observable fields only) |
| Newspaper builder V2 | Implemented & verified (concierge section, FAIL/STALE, scrub, trim) |
| Schedule & freshness gates | Implemented & verified (ordering-intent + mechanical gate; clock times need Brendan's UI action) |
| Model routing / agent registry / privacy / retrieval / op ledger / indexes / validation / V1 features | V1, intact — full V1 suite still green; V2 additions validated |
| Kitchen + martial-arts demos | Implemented, **synthetic-tier research** (WebSearch-only, labeled [CONC-inferred]) |
| Trading duplicate | Decision recorded (dec-20260711-trading-canonical); cross-repo notice **blocked** (health-notebook not in session) |

## 9. Connector truth table (live-verified this session)
Gmail: connected+enabled, LIMITED surface here (get_message + trash/spam labels; no
search/list/draft tools exposed) — read/summarize per policy; drafts only when asked;
never auto-send (no send tool exists here anyway). Calendar/Drive: not enabled, zero
tools — read-for-planning policy written, awaiting enablement. Sheets: no connector
exists. GitHub: MCP, scoped to brendan_brain. Shopify: connected+enabled, full admin
surface — POLICY-BLOCKED pending q-20260711-shopify-ownership; read-only start + no
customer PII in git when unblocked. QuickBooks: connected (authless — likely sandbox) —
same block, read-only until approved. Indeed: connected, disabled here (jobs domain).
S&P Global: not enabled (investing, paper-only). Grasshopper Bank: NOT connected, out of
scope by design; boundary bar documented in CONNECTOR_POLICY. None of the Google/commerce
connectors was live-tested beyond surface inspection — no supported call was needed or
made; claims are scoped accordingly. Enforcement honesty: blocking is policy + optional
settings deny-rules, not platform mechanism (LIMITATIONS #22).

## 10. Browser truth table (live-verified)
This cloud session/routine environment: Chromium ✓ (binaries), playwright-core installs ✓,
launch ✓, **arbitrary egress ✗ (CONNECT 403 policy)**, WebSearch ✓, WebFetch ✗ (same 403),
login persistence ✗, click/interact — works locally against allowed hosts only,
authenticated sites ✗. Local desktop Claude Code: expected full browser (not probeable
from here — stated as expectation, not fact). Scheduled routine environment: same policy
class as this session unless Brendan selects a permissive network policy. Injection
protection: sanitizer (normalize/decode/fence) + fence contract + adversarial tests.
Critical browser-clicking workflows must NOT be scheduled until a scheduled run proves
them (SCHEDULE_PLAN / BROWSER_RESEARCH_POLICY probes).

## 11. Privacy boundaries
5-level sensitivity intact; V2 adds: content-level medical scrub on ALL newspaper prose
(not just tagged artifacts), FOOD_GUIDANCE write-time linter, alignment labels confined to
kitchen artifacts, connector PII scrubbing, work-boundary fail-closed for business
connectors. Leak paths found by the Skeptic (C1) are repaired and regression-tested.

## 12-15. Learning / domains / foundry / capacity behavior
Learning: 6 levels recorded, ≤2 enacted, everything proposal-only; weekly report gated on
material change; interest changes become questions, never rewrites (tested). Domains:
proposals from real accumulation signals only; provisional status; nothing self-executes
(tested). Foundry: graduation criteria + honest candidate tracker; mechanical-subset
quality test. Capacity: per-task observable rows; usefulness stays `pending` until
Brendan reacts; no token numbers exist and none are recorded.

## 16-17. Demonstrations
Kitchen (pot pie / strawberry Brazilian lemonade / strawberry cream puffs):
`queue/active/task-20260711-menu-research-beef-pot-pie-strawberry.md` — inventory
(pantry empty, stated), shopping gaps (in PANTRY §Shopping), night-before prep, cook-day
timed plan, technique synthesis from ~10 sources (cited, not copied), health_alignment
`unclear` (no guidance rows yet) kept out of the article, newspaper article draft ready,
post-meal feedback + leftover/waste flows defined in brain-kitchen. Martial arts:
`queue/active/task-20260711-martial-arts-selection-muay-thai-pads.md` — all 20 mandated
elements verified present (why Muay Thai; boxing/BJJ/wrestling/MMA/kickboxing each cut
with reasons; injuries; surfing compatibility flagged as inference where unsourced; no
sparring; pads/bag/footwork/clinch; gym criteria; 8-12-week entry plan; revision
triggers; honest tier-1 confidence; real sources spot-checked by the Skeptic; explicit
not-medical-clearance). Citation conflation found in review → fixed.

## 18-20. Tests
20 suites in `tests/run_all.sh` (8 V1 + 12 V2, incl. regression suites
test_annotation_regression, test_watch_eligibility, test_timezone). Final run on the
final feature HEAD: **19 PASS, 0 FAIL, 1 SKIP** (test_skill_sync — sibling repos not in
this session; skips are reported distinctly and never counted as passes; results record
the tested SHA). Scenario→test mapping incl. what is demo-only:
`tests/V2_ACCEPTANCE_MAP.md`.

## 21-23. Reviews & repairs
Pre-implementation Opus architecture challenge: 16 criticisms →
`system/audits/2026-07-11-arch-challenge-{opus,response}.md`. Post-implementation:
Sonnet QA (`2026-07-11-v2-qa-report-sonnet.md`) and Opus Chief Skeptic
(`2026-07-11-v2-skeptic-report-opus.md`). Every finding dispositioned with severity,
repair, test, and rollback: `2026-07-11-v2-finding-disposition.md` — 2 criticals (health
prose leak, fence spoof) + 2 production criticals (annotation prose parsing, watch
leakage) + 4 highs all REPAIRED and re-tested; nothing critical/high remains open.

## 24-25. Remaining limitations & accepted risks
docs/LIMITATIONS.md #14-22 (egress, Gmail surface, manual ingestion, sanitizer tripwire,
connector policy-not-mechanism, best-effort timing, no token data, search-tier demos) +
the 4 accepted risks in the disposition file.

## 26. Rollback
Whole release: revert the merge commit on main (`git revert -m 1 <merge-sha>`) — V1
behavior is untouched by V2 files (V1 suite green throughout). Single subsystem: each has
a rollback line in `system/V2_LEDGER.md`; single repair: revert its named commit.
Never rewrite history.

## 27. Daily behavior on main
docs/GIT_WORKFLOW.md — daily output commits directly to main with pull-rebase before and
ls-remote verification after; feature branches only for major work; branch-protection
blocks are reported, never worked around.

## 28-29. Routine configuration + production rehearsal
docs/ROUTINE_SETUP_GUIDE.md — exact repo selections per routine, schedule targets
(06:30 trading → 07:10 editorial → ~07:25 paper), click steps, success/failure evidence,
and the 6-step rehearsal sequence with mechanical checks. The 2026-07-11 overnight run
was a failure test, not a rehearsal.

## 30. Brendan-required actions (complete list)
1. Merge-time: none — handled in this session (PR → review → merge → post-merge checks).
2. Add `brendan_brain` to each robot routine's repository selection (guide §1).
3. Set/confirm routine schedules (guide §2) and the editorial routine's prompt (§3).
4. Answer `q-20260711-shopify-ownership` (blocking for any commerce connector use).
5. Optionally enable Calendar/Drive; optionally add the Shopify/QuickBooks deny rules (§4).
6. Run the production rehearsal (§5) and annotate the first real edition — the learning
   loop starts with your reactions.
