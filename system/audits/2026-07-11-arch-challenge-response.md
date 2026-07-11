---
id: audit-20260711-arch-challenge-response
title: Fable responses to the fresh Opus V2 architecture challenge
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-11
created_by: systems_architect
related: [audit-20260711-v2-preimplementation]
topics: [audit, v2, architecture, review]
---
# Fable → Opus Architecture Challenge: Formal Responses (2026-07-11)

A fresh Opus reviewer inspected the actual repo and environment and raised 16 criticisms
of the V2 spec. Verdicts below govern the build. Full review text preserved in
`2026-07-11-arch-challenge-opus.md`.

| # | Criticism (short) | Verdict | Binding resolution |
|---|---|---|---|
| 1 | Health↔Kitchen alignment labels leak health status into the newspaper | **ACCEPT (modified)** | Kitchen reads ONLY sanitized generic guidance in `domains/health/FOOD_GUIDANCE.md` (never health-notebook). `health_alignment` labels + short generic reasons live in kitchen artifacts (`file_only`) and NEVER in newspaper text, cross-domain output, or commit messages. Leak gate added to tests. |
| 2 | Shopify/QuickBooks are business surfaces; wiring them into the personal concierge crosses the personal/work boundary | **ACCEPT (modified)** | Connector policy binds every connector to a context; business connectors are FAIL-CLOSED for concierge/personal domains. Whether the Shopify store is Brendan-personal or work is UNKNOWN → filed as a blocking question; zero Shopify/QuickBooks data enters the Brain until he answers. Kitchen receipt path is manual paste. |
| 3 | 6-level Learning Engine grants self-modification V1 deliberately withholds | **ACCEPT (modified)** | All 6 levels get RECORDED as evidence; only levels 1–2 (output format, preferences) may generate proposals, and every learned change is proposal-only through the existing PROPOSED_RULES/decision machinery — nothing auto-applies. Meta-learning = observations in the review, never enactment. |
| 4 | 8-desk pre-scaffold violates "no empty domains / no decorative personas" | **ACCEPT (modified)** | One `domains/concierge/` domain. All 8 desks DEFINED compactly (spec requires their 10 fields) in the domain profile, but only Kitchen is ACTIVE; the rest are `dormant` rows that activate at ≥3 artifacts (existing DOMAIN_POLICY ladder). No desk folders, no desk agents until evidence. |
| 5 | Pantry is a mutable memory class the memory model lacks — competing live state | **ACCEPT** | New memory class added deliberately: "live operational state" (PANTRY.md etc.): last-write-wins, git history as audit trail, explicitly exempt from supersede-chains, regenerable views allowed. MEMORY_POLICY + SCHEMAS bumped once, minimally. |
| 6 | 14 kitchen categories strain the schema; receipt ingestion has no automated source | **ACCEPT** | No new artifact types for kitchen knowledge — categories become sections of a few files + ordinary knowledge/task artifacts. Ingestion is MANUAL-PASTE-FIRST (`tools/receipt_to_pantry.py` parses pasted text; deterministic, offline-testable). Documented honestly. |
| 7 | OCI + Learning Report + Foundry + monthly capacity recs = standing bureaucracy | **ACCEPT (modified)** | One weekly review RUN (Sonnet) produces one file with Learning + Improvement sections, gated on material change (below threshold → one line, stop). Opus adversarial review is event-triggered (real failure, Brendan request) or ~6-weekly, whichever later. Fable only for multi-department failures. Max 3 open experiments. Every V2 subsystem ships provisional with a retirement trigger (see #16). |
| 8 | Browser layer is inert here; DOM injection defenses/freshness rechecks presuppose blocked access | **ACCEPT (modified)** | Policy is written WebSearch-first with a mandatory capability probe and honest degradation. DOM workflows are documented as conditional (permissive env / local session) — not exercised here. Injection defenses ARE built and tested offline: `tools/sanitize_external.py` treats ALL external text (web, connector) as data; adversarial fixtures run in CI. Freshness = re-query + as-of dating. |
| 9 | Schedule assumes cron precision / cross-routine chaining that doesn't exist | **ACCEPT** | Schedule expressed as ordering INTENT with recommended UI times + buffers. Editorial run consumes whatever trading output exists; absence is reported as [FAIL] news (existing pattern), never waited on indefinitely, never fabricated. `tools/check_inputs.py` makes the gate mechanical. |
| 10 | Flagship acceptance tests can't pass here if they depend on live browsing | **ACCEPT** | 20 scenarios split: deterministic offline tests join `tests/run_all.sh`; research-dependent scenarios are DEMOS (WebSearch-bounded, labeled, real artifacts produced this session where possible) and are never counted as automated gates. Mapping table records which is which. |
| 11 | Capacity analytics built on usage data that doesn't exist | **ACCEPT (modified)** | Per-task usage log keeps only OBSERVABLE fields (model, agents, times, type, effort, escalation-justified, cheaper-model-possible, reviewer changes, usefulness when Brendan reacts). No token columns; "actual usage" stays absent until a platform API exists. Routing recommendations ride the gated review, not a standing monthly engine. |
| 12 | 6-way router over-encodes existing task flags; "immediate" presumes a live surface | **MODIFY (partial reject)** | The 6 modes stay as Brendan-facing vocabulary — they are his real cases (quick answer + overnight expansion; one-off no-memory). Implementation compiles them to 3 primitives (answer-now / task / watch) × 2 switches (capture? expand-overnight?), reusing new_task.py flags. Router operates only in Brain-enabled sessions — stated in the policy. Reject only the reduction of the vocabulary itself. |
| 13 | Daily food articles = padded output; no food section exists | **ACCEPT** | Kitchen default `publication_destination: file_only`. Newspaper gets an OPTIONAL `concierge` section (budget 300w) that appears only when a task explicitly requests publication (as the pot-pie scenario does) or Brendan reacts asking for it. |
| 14 | Domain signal detection relies on signals not collected | **ACCEPT** | `tools/propose_domains.py` uses only signals that exist: per-topic artifact/task/question counts and annotation reactions. "Saved docs"/"engagement telemetry" dropped until such stores exist. Provisional-vs-permanent = status flag on domain_profile. |
| 15 | Cowork handoff risks a third memory tier / parallel schema | **ACCEPT** | Handoff output IS a brain-sync-format outbox block appended to `queue/inbox/from-cowork.md` (same triage machinery as the robots). The 10 spec categories are subsection headings inside that one block format. No new schema, no Cowork-side memory. |
| 16 | No retirement trigger on V2's own additions | **ACCEPT** | Every V2 subsystem ships `status: provisional` with an explicit retirement trigger and review date (30–45 days) recorded in `system/V2_LEDGER.md`. No acted-upon output in the window → auto-flag for removal in the weekly review. |

## Net build plan (amended)
Ship now: intake router (6-mode vocabulary → 3+2 mechanics) · one concierge domain with
Kitchen active · manual-first kitchen tooling + sanitized health bridge with leak gate ·
WebSearch-first research/browser policy + offline injection tests · connector governance
with domain binding and fail-closed business connectors · Cowork handoff on brain-sync
format · domain proposal tool on real signals · learning engine (record 6, enact ≤2,
proposal-only) with gated weekly review shared with OCI · lightweight usage log ·
ordering-intent schedule with mechanical input gate · deterministic test suite + labeled
demos (pot pie, Muay Thai) · everything provisional with retirement triggers.
Not built: desk folders/agents beyond Kitchen · token analytics · DOM automation here ·
standing separate OCI/Learning/Foundry rituals · autonomous workflow/meta learning ·
banking (boundary doc only).
