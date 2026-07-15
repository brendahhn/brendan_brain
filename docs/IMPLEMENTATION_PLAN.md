<!-- Discovery deliverable 2026-07-14 (Fable). Awaiting "Approved, build it." -->
# Implementation Plan — phased, reviewable, each phase independently shippable

Branch discipline: implementation on feature branches per phase; PR + independent review
(opus) + tests + privacy/secret scan; daily production routine never disrupted; rollback
note in every PR. Personal OS: backup before any schema change.

## Phase 0 — Prerequisites (Brendan) — BLOCKING
Network policy (supabase + commerce/full) · confirm no duplicate routine · (optional)
Gmail reconnect.

## Phase 1 — Secure the base + bridge foundation  [target: before 07-18, Fable-led]
1. Supabase: full export/backup, restore-verified. 2. Key rotation + RLS + password gate.
3. New tables (bridge spec) + agent_events idempotency. 4. Tea Stock save bug fixed +
verified in browser. 5. .claude/settings.json deny rules (QuickBooks, destructive bash,
env reads) in brendan_brain + personal-os; personal-os CLAUDE.md with data-safety rules.
6. personal-os-sync skill v1 (read scan + edition upsert + status strip write).
Acceptance: edition visible on Home (raw first pass); notes/todos scanned in a dry run;
no data loss; all robots unaffected.

## Phase 2 — Ops Router live [Sonnet build, Opus review]
ops-router skill inside daily run: tag map, FOR CLAUDE lifecycle, question answers,
feedback ingestion, agent-todo creation, empty fast-exit, failure flags.
Acceptance scenarios: fantasy note → FootyBot idea queue; "fix site X" note → paper site
task; FOR CLAUDE note ingested+deleted; untagged journal note untouched; empty run <5 min.

## Phase 3 — Home cockpit + site redesign [Builder sessions]
Newspaper-style Home (columns/widgets), question answer boxes, feedback box, brain status
strip, FOR CLAUDE category, UI/UX pass on all tabs, mobile-first, print view (stretch).

## Phase 4 — Tea business ops
Mark-fulfilled button + tea_fulfillments · BOM deductions · Tea Finance auto-append from
Shopify aggregates (backfill 14 orders) · ≤4-orders flags → paper Tea section · Stripe
switch support (Builder swaps Lovable button; keep order-notification path working) ·
sourcing scans once egress opens (verified links only).

## Phase 5 — Personal inventory
L-theanine weekday tick (0.5g Mon–Fri, shared jar with business stream) · home-batch
manual entry · actual vs projected display · recount reconciliation.

## Phase 6 — Oura autopilot + health wiring
Supabase pg_cron daily Oura pull · HealthBot reads Supabase (chooses its own fields) ·
Gym/Oura newspaper section · raw numbers never in git.

## Phase 7 — Multi-AI + skills
external-ai-handoff (paste-able packet/return format; Cowork uses cowork-handoff) ·
skill-scout with monthly AI-growth corner (D54) · newspaper sections Tea Business +
Gym/Oura formalized in BUDGETS.

## Phase 8 — Life after Fable (runs in parallel from day 1)
FABLE_ARCHITECTURE_HANDOFF maintained every session · MODEL_ROUTING_AFTER_FABLE active ·
evaluation fixtures for router + projector + bridge idempotency · completion gates.

## Acceptance scenarios (numbered, from the brief — the system isn't done until):
FootyBot note routing · site-fix loop · Euro logistics linkage · empty-run fast exit ·
Shopify order → projected deduction on fulfilled-mark · unmapped product → data error ·
low packaging → paper flag · sourcing compare with verified links · cart-stop honored ·
provider swap (Stripe) without inventory-engine rebuild · L-theanine weekday/weekend
behavior · recount reconcile · one-off leaves no memory · remember creates evidence ·
overnight research task · Cowork handoff absorbed · ChatGPT handoff absorbed · Scout
pitches + rejects · observer proposes only · Fable disappears, Opus continues · Home
cockpit shows editions/status/questions/feedback loop working.
