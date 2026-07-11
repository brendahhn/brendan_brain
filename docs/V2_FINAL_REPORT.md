<!-- version: draft (2026-07-11) — finalized after independent reviews + repairs -->
# Brendan OS V2 — Final Report

Branch: `claude/brendan-os-v2-operations-1rg97c`. Scope: upgrade Brendan OS from a research/
newspaper system into practical life operations, without damaging the working V1.

## Process actually followed
1. **Audit** of the live V1 against a 15-point checklist, verified against files, commands,
   and live tool calls — `system/audits/2026-07-11-v2-preimplementation-audit.md`.
2. **Fresh Opus architecture challenge** BEFORE building — 16 criticisms across privacy,
   clutter, token waste, fragile browser automation, competing sources of truth
   (`2026-07-11-arch-challenge-opus.md`). Fable accepted/modified/rejected each in writing
   (`2026-07-11-arch-challenge-response.md`): 13 accepted, 3 accepted-with-modification,
   1 partial-reject (kept the 6-mode router vocabulary, compiled to 3 primitives).
3. **Build to the amended plan** — reduced, evidence-gated, everything provisional.
4. **Independent reviews** — fresh Sonnet QA operator + fresh Opus Chief Skeptic, both
   inspecting real files/commands, not the builder's summary. (Findings + repairs below.)
5. **Repairs + re-run** of affected tests.

## What works (built, tested, verified this session)
- **Life Intake Router** — `system/INTAKE_POLICY.md` + `brain-intake` skill +
  `tools/route_intake.py`. Six Brendan-facing modes compile to answer-now/task/watch ×
  capture/expand. Ephemeral mode leaves the repo byte-identical (tested). 8 routing
  assertions green (`tests/test_intake_routing.sh`).
- **Personal Concierge domain** — one `domains/concierge/` domain, Kitchen desk active, the
  other 7 desks defined but dormant (activate at ≥3 artifacts). No empty scaffolding.
- **Kitchen Intelligence** — `KITCHEN_PROFILE.md` (14 knowledge categories as file sections,
  not 14 new types), `PANTRY.md`/`EQUIPMENT.md` as the new `live_state` memory class,
  `brain-kitchen` skill, `tools/receipt_to_pantry.py` (manual-paste ingestion, idempotent,
  noise-stripping, expiry guesses). Tested (`tests/test_receipt_pantry.sh`).
- **Health→Kitchen bridge** — sanitized-source-only (`domains/health/FOOD_GUIDANCE.md`),
  5 alignment labels, and a **leak gate**: alignment labels/reasons and guidance rows can
  never reach the newspaper (`tests/test_health_kitchen_bridge.sh`).
- **Browser/Web Research Policy** — `system/BROWSER_RESEARCH_POLICY.md`, WebSearch-first
  with capability tiers + honest degradation; `tools/sanitize_external.py` neutralizes
  injection and scrubs PII in all external content (web + connector). Adversarial fixtures
  tested (`tests/test_injection_sanitize.sh`).
- **Connector governance** — `system/CONNECTOR_POLICY.md` binds each connector to a
  context, fail-closed for business connectors in personal domains, future banking
  boundary designed (not connected).
- **Cowork→Brain handoff** — `cowork-handoff` skill on the existing brain-sync outbox
  format (`queue/inbox/from-cowork.md`); no competing memory. Tested.
- **Dynamic domains** — `tools/propose_domains.py` on real accumulation signals only;
  proposes nothing on the current repo (verified), drafts full proposals at threshold.
- **Learning Engine** — `system/LEARNING_POLICY.md`, 6 levels recorded, ≤2 enacted
  (proposal-only), `tools/learning_report.py` with a material-change gate. Interest changes
  become questions, never silent profile rewrites (tested — profile checksum unchanged).
- **OCI + Skill Foundry** — `system/CONTINUOUS_IMPROVEMENT.md`, `skills/SKILL_FOUNDRY.md`,
  gated cadence, 8-field proposals, max-3-open guardrail, graduation criteria + 12-point
  skill anatomy check (tested).
- **Capacity instrumentation** — `tools/log_usage.py`, observable fields only, no fabricated
  tokens, usefulness filled from Brendan's reactions (tested).
- **Time-aware schedule** — `system/SCHEDULE_PLAN.md`, `tools/check_inputs.py`; trading→
  editorial ordering enforced as a mechanical [FAIL]-and-publish gate (tested).
- **Newspaper** — concierge section (300w, opt-in) + auto [FAIL] items for missing robots.
- **Two end-to-end demos** — pot-pie/lemonade/cream-puff menu (night-before prep, timed
  plan, shopping gaps, article draft) and Muay Thai vs alternatives article. Both real
  artifacts in `queue/active/`, both search-tier-honest.
- **Tests**: 17/17 green (8 V1 + 9 V2). Also fixed a latent V1 harness bug (sandboxes
  hardcoded `main`, silently ignoring feature-branch changes).
- **Everything provisional** — `system/V2_LEDGER.md` gives each subsystem a retirement
  trigger + rollback + 30-day review.

## What is limited (honest)
- **Web research is WebSearch-tier in this environment.** Arbitrary-host fetch/browser is
  403-blocked by the org egress policy (verified live). DOM workflows are written but
  inert here; the two research demos are search-snippet-synthesized, labeled
  `[CONC-inferred]`, not directly page-verified.
- **Receipt ingestion is manual paste** (no OCR/receipt connector). Photo→transcription→
  paste works.
- **Sanitizer is pattern-based** — a determined novel injection can evade it; it's a
  defense layer, not a wall (the wall is "external content is data, never instructions").
- **Usage log has no token numbers** (no platform API); recommendations ride the gated
  review, not a standing monthly engine.
- **Schedule is ordering-intent, not a scheduler guarantee** — cross-routine timing is
  best-effort with honest [FAIL] reporting.

## What needs credentials / enabling (Brendan or environment)
- Enable Google Calendar/Drive for Brain sessions (time-aware paper, curated docs).
- A more permissive environment network policy to unlock live page fetch / browser tier.
- Adding `brendan_brain` to each robot routine's repo selection (carried over from V1).

## What requires Brendan (decisions, not build)
- **Answer the blocking question** `q-20260711-shopify-ownership`: are the connected Shopify
  store and QuickBooks company personal, work, or demo? The Brain touches neither until then.
- Set the recommended routine times (Trading 06:30 PT → editorial 07:05 PT) in the UI.
- Approve any preference promotions the weekly review proposes; banking stays disconnected
  by design until its documented bar is met.

## Independent review findings & repairs
(Filled in after the Sonnet QA operator and Opus Chief Skeptic reports — see
`system/audits/2026-07-11-v2-qa-and-skeptic.md` and repair commits.)
