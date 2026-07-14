<!-- Discovery artifact — branch claude/brendan-os-discovery-963n2h. Not on main until approved. -->
# Brendan OS — Current State Audit (2026-07-14, Fable)

Audit performed before the discovery interview so Brendan is never asked what the repos
already answer. Everything below was verified directly in this session.

## 1. What exists and works

### Brendan Brain (`brendahhn/brendan_brain`) — substantially built, V1+V2
- 49 validated artifacts; schemas, frontmatter validation, generated indexes.
- **Intake router already exists** (`system/INTAKE_POLICY.md`, `brain-intake` skill,
  `tools/route_intake.py`): 6 modes (immediate / immediate+memory / immediate+overnight /
  same-day task / background research / watch), natural-language overrides, ephemeral
  guarantee tested. This IS the "Life Intake Router" — it routes requests *inside*
  Brain-enabled sessions. What does NOT exist: a scheduled scanner of external surfaces
  (Personal OS notes/todos, Gmail, Shopify) — the "Ops Router" gap.
- **Model routing policy exists** (`system/MODEL_ROUTING_POLICY.md`): haiku/sonnet/opus/fable
  tiers, escalation triggers, per-task logging. Close to the required fallback table; needs
  only an explicit "after Fable" section (architecture_lead: fable→opus).
- Newspaper system live (first real edition 2026-07-11, ~07:25 PT target), annotations
  vocabulary, publication policy, capacity ledger, learning engine, kitchen desk,
  concierge domain, forgetting workflow, cross-repo op ledger.
- Agent registry (11 roles incl. Chief Skeptic/QA), staffing policy, stress tests
  (suite 19 pass / 0 fail / 1 skip on main at last audit).
- 9 skills canonical in `.claude/skills/`, checksum-synced to specialist repos.
- Open questions to Brendan: Tacoma budget, trading dup, **Shopify ownership (now answered
  per discovery brief: Brendan's personal tea business — unblocks CONNECTOR_POLICY)**.
- Active queue: 2 tasks + 1 watch (Tacoma, next run 2026-07-17). Inboxes receiving real
  robot blocks (health 07-12/13, trading 07-12/13).

### Specialist repos — integrated, pending routine repo-selection
- FootyBot, health-notebook, trading-notebook: `BRAIN_INTEGRATION.md` + synced `brain-sync`
  merged to main; round-trips verified. Jobs Robot (operator-notebook) same status but that
  repo is NOT in this session's scope.
- health-notebook also contains `trading/` remnants; trading-notebook is its own repo.
- Remaining activation is platform-gated: Brendan must add `brendan_brain` to each
  routine's repo selection in the claude.ai UI (docs/START_HERE.md).

### Personal OS (`brendahhn/personal-os`) — live SPA, no Brain connection
- Vite + React 18, **single file** `src/App.jsx` (849 lines, minified-style). No router,
  no tests, no lint, no CI, no vercel.json in-repo (deploy config lives on Vercel's side;
  commit history is all "Update App.jsx" — likely edited via GitHub/Claude web).
- **Backend: Supabase** (project `kgztnportoondvwicfqb`) via REST from the browser.
  Tables: notes, todos, projects, events, daily_logs, gym, app_settings, trash,
  tea_inventory (+ finance table), Oura edge function (`clever-endpoint`).
- **No authentication**: the anon key is hardcoded in the client and RLS appears open —
  anyone with the URL+key can read/write. Acceptable risk so far but must be a conscious
  decision (see interview R2). Key is public-by-design for Supabase anon, but no user
  scoping exists.
- Tabs: Home, Log (mood/sleep sliders), Gym, Notes (bullet trees, categories), Todos
  (priority urgent/week/month/longterm), Projects (active/later/far), Data, Calendar,
  Trash (soft delete), Tea Finance (category ledger, testing walled off), Tea Inventory.
- **Tea Inventory already has a real BOM**: 13 roles (chamomile 45g, lemon balm 30g,
  L-theanine 6g, glycine 90g, taurine 60g + tins/bags/muslin/stickers/scooper/card/box)
  with per-order loose/bag consumption, "orders left" ceilings, add-stock with unit
  conversion. One product (a sleep-tea blend), two SKU forms: loose + bag.
  NOTE: personal L-theanine (0.5 g/weekday rule) is a SEPARATE stream from the 6 g/order
  business use — design must not conflate them.
- **Bridge feasibility**: Supabase REST is callable from any Claude session with the same
  anon key (it's in the public repo already) — a Brain↔OS bridge needs no new
  infrastructure, "only" contract + idempotency + privacy rules.

### Connectors (live-verified this session)
- **Gmail**: connected but LIMITED surface here — `get_message` + sensitive-label tools
  only; NO search/list ⇒ inbox scanning is not possible with today's exposed tools.
  Round 4 answers must respect this until the surface grows.
- **Google Calendar**: zero tools exposed. Not usable today.
- **Shopify**: full admin surface incl. writes and customer PII. Was policy-BLOCKED on
  ownership; now unblocked as Brendan's personal tea business → read-only start,
  PII-never-in-git, per existing CONNECTOR_POLICY plan.
- **QuickBooks**: connected (authless/demo-looking). Brendan says EXCLUDE. Recommend
  permission deny-rules as the mechanical enforcement.
- **Amazon**: no connector exists. Sourcing/cart work would be browser-driven
  (BROWSER_RESEARCH_POLICY exists; routine sandboxes are WebSearch-only egress —
  cart prep likely interactive-session-only).
- **GitHub MCP**: full, scoped to the 5 repos of this session.

## 2. Known failures / debt (from SYSTEM_HEALTH + LIMITATIONS)
- Robot Gmail drafts intermittent (predates Brain).
- Routine sandbox egress is WebSearch-only → source-verification backlog in health.
- No usage/quota API → manual capacity ledger only; no token counts recordable.
- Skill sync is session-borne; drift detectable, not self-healing.
- Retrieval is keyword-level; semantic recall deferred (evidence-first).
- Personal OS: zero tests, zero CI, one-file architecture, open-write database,
  fat-finger risk on `confirm()`-only deletes (soft-delete trash mitigates).
- V2 subsystems are provisional until 2026-08-15 with auto-flag retirement triggers.

## 3. The actual gap list (what the target architecture adds)
1. **Personal OS ↔ Brain bridge** (event contract, notes/todos sync, return path) — nothing exists.
2. **Ops Router as a scheduled scanner** of OS notes/todos, robot inboxes (exists), Gmail
   (blocked on connector surface), Shopify — INTAKE_POLICY covers classification; the
   scanner+trigger loop doesn't exist.
3. **Shopify read-only integration** + provider-neutral commerce adapter + BOM projection
   (the BOM itself already lives in Personal OS — decide source of truth).
4. **Personal L-theanine deterministic inventory** (0.5 g weekdays) — new, small.
5. **Website Builder** flow (issue→branch→fix→verify→PR) — new.
6. **External-AI handoff format** — cowork-handoff exists; generalize.
7. **Skill Scout / Workflow Observer** — SKILL_FOUNDRY.md is the seed; scouting is new.
8. **Fable→Opus handoff docs + model fallback formalization** — routing policy exists;
   handoff doc is new and is the highest-continuity deliverable before 2026-07-18.
9. Gmail/Calendar routines — **blocked on connector surface**, design-only for now.

## 4. Contradictions & risks to resolve in the interview
- Newspaper (exists, morning artifact in git) vs Personal OS (the intended cockpit):
  which is the primary morning surface, and does the paper render in the OS?
- Tea BOM source of truth: Personal OS Supabase (live, Brendan-edited) vs Brain markdown
  (auditable). Two truths will diverge.
- CLAUDE.md says Brain routines commit to main; discovery work is branch-gated by the
  task contract — architecture work stays on this branch until "Approved, build it."
- Personal OS has no auth: connecting agents that WRITE to it raises the stakes of the
  open database. Decide: accept, or add minimal auth first.
- `health-notebook/trading/` remnants vs separate trading-notebook repo (cleanup candidate).
- QuickBooks connected but excluded → add mechanical deny rules, not just policy text.
