<!-- THE continuity document. Fable 5 access ends 2026-07-18. Opus: start here. -->
# Fable → Opus Architecture Handoff

## Who you are now
You are the **architecture lead** for Brendan OS (role: Systems Architect,
agents/AGENT_REGISTRY.md) running on Opus. Fable designed V1/V2 and ran the 2026-07-14
discovery; you continue — you do not re-litigate settled decisions (docs/DECISION_LOG.md
D1–D55) unless evidence breaks them. Brendan approves architecture changes; the approval
phrase for the build plan is exactly: **Approved, build it.**

## Read in order
1. docs/GOAL_CONTRACT.md (what winning means; once-daily ceiling is HARD)
2. docs/DECISION_LOG.md (D1–D55 — the interview IS the requirements)
3. docs/IMPLEMENTATION_PLAN.md (phases; check which are done vs pending)
4. docs/SOURCE_OF_TRUTH.md + docs/PERMISSION_MATRIX.md (never violate)
5. docs/discovery/CURRENT_STATE_AUDIT.md (system state as of 07-14)
6. system/ policies (AUTONOMY, PRIVACY, CONNECTOR, MODEL_ROUTING + docs/MODEL_ROUTING_AFTER_FABLE.md)

## The five things most likely to bite you
1. **Session branches**: platform pins sessions to claude/* branches; routine ops MUST
   also land on main (CLAUDE.md standing rule, D9). 26 branches stranded before the fix.
   Always `git ls-remote` verify. Architecture work stays branch-gated until approved.
2. **Personal OS data is sacred** (D13/D19): agents create/check, never delete (except
   FOR CLAUDE notes), backup before schema changes. The site historically "didn't save"
   — verify persistence end-to-end in a browser after any site change.
3. **Verified links/prices only** (D43): Brendan received hallucinated links before.
   WebFetch-blocked ⇒ label figures inferred or don't present them. The 07-15 sourcing
   run's honesty is the template.
4. **Customer PII never enters git** — order numbers only. Health raw numbers never in
   git. Sensitivity rules are hard rule 4.
5. **Once daily, no interrupts** (D2). Urgent = Brendan opens a session manually.

## Delegation method (works; keep it)
Recon minimal → spec with acceptance tests → Sonnet builds in isolated context/worktree →
you review diff+evidence → Opus fresh-context review for consequential merges (you = both
lead and reviewer now: use FRESH sessions for review, never review your own context) →
release gates per docs/IMPLEMENTATION_PLAN preamble. Haiku for scans/classification.
Don't force delegation on serial debugging.

## State at handoff (updated 2026-07-15 — FINAL Fable session)
Brendan paused the project 2026-07-15 → 2026-07-20 (job case study; conserving weekly
limit). Fable access ends 07-18, so **Opus leads the build from Monday 2026-07-20**.
If Brendan has said "Approved, build it" by then: start Phase 1 exactly per
IMPLEMENTATION_PLAN (check Phase 0 prerequisites first — network policy!). If not,
ask him once, plainly, then wait.

## State at handoff (2026-07-14 late)
- Interview COMPLETE (7 rounds, D1–D55). Pre-build docs written (this package).
- Brendan has NOT yet said "Approved, build it." Do not start Phase 1 until he does.
- Production healthy: all repos' mains recovered + verified; daily run publishing
  (edition 2026-07-16 live); jobs robot PAUSED by Brendan (report "paused", never FAIL).
- Blockers on Brendan: network policy (supabase + commerce), duplicate-routine check,
  Euro trip details, supplier cost baseline, Stripe account creation, reorder confirm
  (tea bags/L-theanine/taurine were critical on 07-14).
- Shopify exit decision published (Stripe Payment Links, act by 07-31).
- Watch: first daily run after any CLAUDE.md/policy change; annotation false-positive
  pattern (SYSTEM_HEALTH 07-12) — don't --apply annotations without dry-run review.

## Risks & mitigations
Open Supabase until Phase 1 (rotate keys FIRST); connector surfaces change without
notice (re-probe, never assume; Gmail lost draft tools ~06-25); double-fire routines
(idempotency ledger + dedupe keys); model unavailability (fallback table); scale (61→
hundreds of artifacts: archival triggers in STRESS_TESTS #27).

## Testing & release
tools/ suite + tests/ fixtures must stay green on main. Every phase: acceptance
scenarios from IMPLEMENTATION_PLAN + browser verification for site work + privacy scan
(grep for emails/names/keys) before push. Rollback: every PR names its revert; Supabase
changes need a tested restore path. Never claim unverified success (hard rule 7).
