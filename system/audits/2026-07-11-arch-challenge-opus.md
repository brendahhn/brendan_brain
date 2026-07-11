---
id: audit-20260711-arch-challenge-opus
title: Fresh Opus architecture challenge of the V2 spec (verbatim)
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-11
created_by: chief_skeptic_opus
related: [audit-20260711-arch-challenge-response]
topics: [audit, v2, architecture, review]
---
# Fresh Opus Architecture Challenge — V2 Spec (2026-07-11, verbatim)

Reviewer: fresh Opus subagent, no implementer context, inspected actual files.
Responses/verdicts: `2026-07-11-arch-challenge-response.md`.

# Fresh Opus Architecture Review — Brendan OS V2 Spec

Grounded in the actual repo (23 artifacts, 7 domains, 8 automated tests, 48 stress scenarios) and verified against files and the environment audit — not against the implementer's summaries. Ranked by severity. The goal is a leaner, safer build.

## TIER 1 — Safety / privacy / hard-policy contradictions

### 1. The Health↔Kitchen bridge is a live health-leak vector, and "alignment labels" themselves leak health status
- **Spec element:** #4 — kitchen reads "approved health food guidance"; emits alignment labels (strongly aligned … unclear); acceptance scenario publishes a food article to the newspaper.
- **Evidence:** `PRIVACY_POLICY.md` #3: "Brendan-specific values … never leave health-notebook"; `domains/health/DOMAIN_PROFILE.md`: the Brain health domain holds "ONLY … sanitized/generic research conclusions." A label like "this pot pie is *strongly aligned* with your health guidance," published in the newspaper, is a Brendan-specific health inference — it implies a condition/regimen — and the paper is the least-scoped surface. `AUTONOMY_POLICY.md` #4 makes crossing the personal boundary an ask-first action; a standing kitchen→health read pipe institutionalizes that crossing.
- **Recommendation:** Do not let alignment labels reach the newspaper or any non-health artifact. Kitchen may consume only *generic* guidance already sanitized into `domains/health/` (never health-notebook), and alignment must render as a neutral kitchen-internal flag, never a published phrase that reveals health state. Add a test analogous to `test_newspaper_sensitivity.sh` that fails if a food/kitchen artifact carries a health-derived label into publication. Build the bridge *read-only, one-directional, sanitized-source-only,* or defer it.

### 2. Shopify + QuickBooks are business/work connectors; wiring them into a *personal* concierge violates the personal/work boundary and risks PII in git
- **Spec element:** #2/#3/#7 — concierge desks (Purchases, Kitchen) with connector access; "receipt/grocery ingestion"; "Shopify without customer PII into GitHub."
- **Evidence:** `PRIVACY_POLICY.md` #4: "no employer data enters this repo." Audit §10: Shopify exposes `list-customers`, `list-orders`, analytics; QuickBooks is full business accounting. These are commerce/financial *business* surfaces, not Brendan's personal grocery history. `AUTONOMY_POLICY.md` #4 forbids crossing the boundary without asking. The spec's own "without customer PII" caveat concedes the hazard but still routes a work connector into a personal-life domain.
- **Recommendation:** Keep business connectors (Shopify, QuickBooks) out of the personal concierge entirely — they belong to a future work-system clone (per PRIVACY #4). The concierge's only commerce data path is manual entry (Brendan pastes a receipt). Write the per-connector policy to *bind each connector to a domain* and fail closed if a personal-domain task requests a business connector. This also removes the "PII into GitHub" problem by construction.

### 3. The 6-level Learning Engine grants self-modification authority that V1 policy deliberately withholds
- **Spec element:** #10 — learning at output/preference/research/workflow/prediction/**meta** levels, with learned-change records and autonomous application.
- **Evidence:** `MEMORY_POLICY.md`: the *only* promotion path today is preference→rule at "≥3 consistent signals across ≥2 distinct days … One reaction NEVER confirms a rule," and even that needs Brendan's approval. Audit §8 states plainly: "NO structured learning above preferences … This is the V2 gap." `AUTONOMY_POLICY.md` #2 makes rule promotion ask-first. On a 1-user, 1-day-old system with 23 artifacts, "workflow" and "meta" learning (the system changing how it works, autonomously) is pure overreach and directly contradicts the ask-first guardrail.
- **Recommendation:** Ship levels 1–2 only (output-format and preference learning), reusing the existing evidence-log + threshold machinery. Every "learned change" is a **proposal in `preferences/PROPOSED_RULES.md`**, never auto-applied; workflow/prediction/meta learning is *recorded as evidence*, not enacted. Drop "meta-learning" from V2. The weekly report can *observe*; it may not *change behavior*.

## TIER 2 — Structural strain / competing sources of truth / clutter

### 4. Pre-scaffolding an 8-desk Concierge department directly violates the "no empty domains" rule
- **Spec element:** #2 — up to 8 desks, each with ~9 standing config fields (scope, model, escalation, memory access, privacy, publication, completion, cost).
- **Evidence:** `DOMAIN_POLICY.md`: "Do not pre-create empty domains"; a domain earns creation at "≥3 artifacts accumulated"; skeleton rule: "no empty scaffolding clutter." `AGENT_REGISTRY.md`: "No decorative personas … A role exists only if it has distinct inputs, outputs, and a completion standard." Zero concierge/kitchen artifacts exist today (verified: only the audit mentions the words).
- **Recommendation:** Create **one** `domains/concierge/` with a profile, and let desks materialize as thin overlays *only when ≥3 artifacts accumulate for that desk* — exactly the existing desk pattern (`AGENT_REGISTRY.md`: "Desks = domain profile overlays, not standing roles"). Kitchen is the one desk with real demand; build it. The other 7 are a config table masquerading as capability.

### 5. Kitchen pantry state is a new *mutable* memory class the memory model doesn't have — and a competing source of truth
- **Spec element:** #3 — pantry with confidence/expiry, cooking calendar, shopping list, prep timing: all live, constantly-changing state.
- **Evidence:** `MEMORY_POLICY.md`'s classes are timeline (immutable), durable knowledge (supersede-only, "Never edit old conclusions in place" per `SCHEMAS.md`), queue (operational), preferences. A pantry that decrements as you cook fits none: it's neither append-only nor supersede-chained. `CLAUDE.md` Hard Rule #1 is one-file-per-artifact; a mutating pantry inventory breaks that. This is a second live-state store alongside the queue.
- **Recommendation:** Model pantry as **operational state in the queue family** (like watches), not knowledge — a single regenerable inventory file explicitly exempted from the supersede rule, with git as the audit trail. Add exactly one memory-class row to `MEMORY_POLICY.md` ("live inventory: last-write-wins, git-audited") rather than smuggling mutable state into `knowledge/`. Keep the 14 "categories" as *sections of a few files*, not 14 artifact types.

### 6. 14 kitchen categories + ingestion strain the 13-type schema, and ingestion has no data source in this environment
- **Spec element:** #3 — receipt/grocery/pantry ingestion; 14 knowledge categories.
- **Evidence:** `SCHEMAS.md` defines 13 artifact types; audit §2 confirms. There is **no OCR, no Sheets connector, no Drive** (audit §10), and arbitrary-host egress is 403-blocked (audit §9). The only commerce connectors are business ones (see #2). So "receipt ingestion" has no automated input path — it's manual paste only.
- **Recommendation:** Don't mint 14 new types; express kitchen knowledge within the existing `knowledge` type plus the one live-inventory class. State honestly in the kitchen doc that ingestion is **manual-entry-first** until a personal receipt source exists; don't build parsers for data that can't arrive. Bump `SCHEMAS.md` version once, minimally.

### 7. OCI + Skill Foundry + Learning Report + monthly capacity recs is standing bureaucracy — the exact "endless redesign" the spec claims to guard against
- **Spec element:** #10/#11/#12/#13 — weekly Sonnet review, periodic Opus adversarial review, Fable architecture reviews, 10-section weekly Learning Report, 8-field improvement proposals, monthly capacity recommendations, 12-field skill template.
- **Evidence:** `AGENT_REGISTRY.md`: roles "are prompts + policies, not daemons," with a 3-strike retirement rule. `STAFFING_POLICY.md`: "No decorative personas"; multi-agent work must record "did the extra staffing improve the result?" The system today has 23 artifacts and one real edition (~430 words). A weekly Opus/Fable review cadence over that surface is a self-licking process; it will generate proposals about a system barely exercised. This is the token-waste and decorative-bureaucracy failure mode.
- **Recommendation:** Collapse OCI + Learning Report into **one monthly, Sonnet-authored "System Review"** that runs *only if there is material change to review* (gate on: ≥N new artifacts or a logged failure). Reserve Opus/Fable for triggered events (a real failure, Brendan's request), not a calendar. Skill Foundry = the graduation *criteria* checklist only; no standing 12-field template ritual until a 2nd skill actually graduates. Make every one of these earn its existence with the same 3-strike retirement rule already on the books.

## TIER 3 — Environment can't honor it / fragile

### 8. The browser layer is largely inert in this environment; injection defenses and freshness-rechecks presuppose DOM access that's 403-blocked
- **Spec element:** #5 — browser policies/workflows, prompt-injection defenses, provenance, freshness rechecks, adversarial tests; #6 Muay Thai end-to-end.
- **Evidence:** Audit §9 (verified live): "arbitrary-host egress is DENIED … CONNECT 403 (curl, Playwright, and WebFetch all blocked) … WebSearch WORKS." `LIMITATIONS.md` §7: "Egress in routine sandboxes is WebSearch-only." So live DOM automation, page-level injection surfaces, and "recheck the listing page" freshness passes don't run here.
- **Recommendation:** Rename this to a **Research Policy (WebSearch-first)**. Build: source-provenance recording, freshness via *re-query* (not re-DOM), and a *capability probe* that degrades honestly (the audit's own conclusion). Keep prompt-injection *principle* (external content is data, not instructions — already stress scenario #41) but drop DOM-injection tooling until Brendan selects a permissive network policy. Do not write "adversarial browser tests" that can't execute; write WebSearch adversarial tests.

### 9. The time-aware schedule assumes cron precision and cross-routine chaining the platform doesn't provide
- **Spec element:** #14 — overnight → premarket before 6:30 → trading 6:30 → editorial ~7:05 with buffer → publish after inputs.
- **Evidence:** `LIMITATIONS.md` #5: "No hard scheduler … the Brain can only prioritize within a session." Audit §12: "CronCreate minimum interval hourly … ScheduleWakeup granularity 60s *within a session*." Routine schedules live in Brendan's UI, external to git (`ROUTINE_REGISTRY.md`). A 7:05 editorial that *waits on* a separate 6:30 trading routine's output is a cross-routine timing dependency with no coordination primitive — the trading routine and the Brain routine are different sessions.
- **Recommendation:** Express the schedule as **ordering intent, not clock guarantees.** Either (a) the morning Brain run reads whatever trading output *already exists in the Brain* and reports `[FAIL]` if absent (the existing "a robot that didn't run is news" pattern), or (b) fold premarket+editorial into one longer Brain session that internally waits via ScheduleWakeup. Do not promise a 7:05 publish that depends on a 6:30 sibling routine landing on time. Document it as best-effort with honest failure reporting.

### 10. Several flagship acceptance tests can't actually pass here — they depend on blocked live browsing
- **Spec element:** #3 (pot-pie overnight *research*), #6 (Muay Thai *end-to-end research*), #15 (20 acceptance tests).
- **Evidence:** Both scenarios require multi-source web research; egress is 403 (audit §9). Existing tests (`tests/run_all.sh`) are stdlib-only, offline, synthetic-fixture — that's *why* they pass. A "beef pot pie overnight research → newspaper article" test either uses WebSearch (shallow, non-deterministic) or synthetic data (then it's not an acceptance test of research).
- **Recommendation:** Split the 20 into **deterministic offline tests** (routing decisions, schema validation, privacy gating, pantry-state transitions, handoff extraction) that join `run_all.sh`, versus **manual demo scenarios** clearly labeled non-automated and WebSearch-bounded (like the existing SYNTHETIC Tacoma demo). Don't inflate the count by listing scenarios the environment can't execute as if they're passing gates.

### 11. Capacity instrumentation builds monthly recommendations on usage data that doesn't exist
- **Spec element:** #13 — per-task records incl. "usage-if-available," reviewer changes, cheaper-model-possible; monthly recommendations; "never fabricate token numbers."
- **Evidence:** `LIMITATIONS.md` #4: "No account usage/quota API … conservative manual ledger … not real usage data." `CAPACITY_LEDGER.md` header repeats this. So "usage-if-available" is *never available*; the monthly recommendation engine runs on effort-estimate proxies.
- **Recommendation:** Keep the *lightweight* per-task fields already implied by `MODEL_ROUTING_POLICY.md` (model used, escalation trigger, one-line staffing verdict — this exists in the Tacoma log). Drop the token/usage columns and the *monthly recommendation* until a usage API exists; a periodic human-readable "was staffing worth it" scan (already the 3-strike retirement mechanism) is sufficient. Don't build analytics on numbers you've forbidden yourself to fabricate.

## TIER 4 — Over-engineering / token waste

### 12. The 6-way Intake Router over-encodes what `new_task.py` flags already express, and "immediate answer" presumes a real-time surface that doesn't exist
- **Spec element:** #1 — six categories including "immediate answer" and "immediate+overnight expansion."
- **Evidence:** `SCHEMAS.md` task frontmatter already carries `urgency`, `depth (quick|standard|deep)`, `recurrence (none|daily|weekly|watch)`, `effort_budget` — most of the 6-way space. `LIMITATIONS.md` #3: "No universal conversation capture … only in Brain-enabled sessions." "Immediate answer" implies live chat, but Brendan OS is scheduled-routine + on-demand; there is no always-on intake.
- **Recommendation:** Reduce to **3 outcomes**: answer-now (in-session, optionally captured), queue-it (maps to existing urgency/depth flags), watch-it (existing watch). "Overnight expansion" is just `depth: deep` + a scheduled slot — don't make it a first-class category. State that routing operates only in Brain-enabled sessions.

### 13. Daily "overnight expansion → published food article" is the padded output Brendan explicitly hates, and there's no newspaper food section for it
- **Spec element:** #3 acceptance scenario — a dinner request becomes overnight research → newspaper article.
- **Evidence:** `BRENDAN_PROFILE.md`: "values verification discipline, hates repetition and padded output." `PUBLICATION_POLICY.md` lists 8 fixed sections — none is food/kitchen; the real edition ran ~430 words total. Turning "what's for dinner" into a research report + published article is exactly the inflation the paper's word budgets and "length is not rewarded" rule fight.
- **Recommendation:** Kitchen output default = a **terse plan/answer artifact**, `publication_destination: file_only`. It reaches the newspaper only when Brendan reacts positively or asks — surfaced through the existing `open_research` or a serendipity slot, not a standing daily food column. Expansion is opt-in, not the default behavior.

### 14. Dynamic domain "signal detection" relies on signals the system doesn't collect
- **Spec element:** #9 — detect via "repeated questions, saved docs, queue tasks, engagement."
- **Evidence:** There is no document store ("saved docs") and no engagement telemetry in this repo; retrieval is keyword-level (`LIMITATIONS.md` #10). The grounded signals that *do* exist are queue-task count and repeated topics — which is precisely the existing `DOMAIN_POLICY.md` ladder ("≥3 artifacts accumulated").
- **Recommendation:** Base detection on the signals that exist (artifact/task/question counts per topic, annotation reactions). Drop "saved docs" and "engagement." This is a small enhancement to `brain-domain`, not a new subsystem; keep provisional-vs-permanent as a status flag on the domain profile.

### 15. The Cowork handoff's 10-category extraction risks becoming the third memory tier it's trying to avoid
- **Spec element:** #8 — Cowork = interactive workspace, Brain = canonical memory, "no competing memory," with a 10-category standard extraction.
- **Evidence:** The principle is correct and matches `CLAUDE.md` ("The Brain is the exchange layer"). But three tiers already exist (specialist notebooks, Brain, now Cowork). A heavyweight 10-field extraction ritual on every handoff invites drift and duplicate capture if the mapping isn't mechanical.
- **Recommendation:** Reuse the **existing `brain-sync` outbox contract** (predictions/knowledge/questions blocks, dedupe_key, triaged markers) rather than inventing a parallel 10-category schema. Cowork writes into the *same* inbox format the robots use; the Brain's existing triage absorbs it. One handoff format, not two. This keeps "no competing memory" true in implementation, not just in the doc.

### 16. New standing overhead has no retirement trigger wired in — it will accrete
- **Spec element:** cumulative — router, 8 desks, learning engine, OCI, foundry, capacity ledger, handoff, all landing at once on top of V1.
- **Evidence:** `STAFFING_POLICY.md` and `AGENT_REGISTRY.md` already define a 3-strike retirement rule and "did it earn its cost" verdicts — but the V2 spec adds ~8 standing subsystems without applying that discipline to *itself*.
- **Recommendation:** Every V2 subsystem ships with an explicit **retirement/rollback trigger and a "provisional" status** for 30 days (the spec already invented "provisional vs permanent" for domains — apply it system-wide). If a subsystem produces no acted-upon output in its trial window, it auto-flags for removal. This is the single most important guardrail: it converts the whole build from irreversible scaffolding into reversible experiments.

## Overall verdict

**Build reduced, in three layers, gated by evidence — do not build as specified.** The genuinely valuable, low-risk, grounded pieces are: the connector-governance policies with domain-binding (#7 in spec, but with business connectors *excluded* from the personal concierge and banking already correctly out of scope), a **single** Kitchen desk under one concierge domain with manual-first ingestion, a WebSearch-first Research Policy that degrades honestly, a 3-way intake router that reuses existing task flags, and the Cowork handoff *if* it rides the existing brain-sync outbox format. Those are worth shipping now. Build **reduced**: the Learning Engine (levels 1–2, proposal-only), the schedule (as ordering-intent with honest failure reporting), and capacity instrumentation (lightweight per-task verdicts, no fabricated usage analytics). **Do not build** as specified: the 8-desk pre-scaffold, the 14-type kitchen schema, the standing OCI/Learning-Report/Foundry bureaucracy, autonomous workflow/meta-learning, DOM-level browser automation, and any acceptance test that depends on blocked egress. The two things that must not ship in *any* form without hard gating are the health→kitchen label pipeline reaching publication (a privacy leak) and business connectors feeding the personal concierge (a boundary violation). The spec's own instincts — provisional-vs-permanent, anti-endless-redesign, 3-strike retirement — are the cure; the fix is to apply them to V2 itself, so the build lands as a set of reversible, evidence-gated experiments rather than a doubling of standing infrastructure on a system that has produced exactly one real newspaper edition.
