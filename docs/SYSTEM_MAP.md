<!-- Discovery deliverable 2026-07-14 (Fable). -->
# System Map

```
                     ┌──────────────────────────────────────────┐
  Brendan (phone) ──▶│ PERSONAL OS  (personal-os repo → Vercel) │
                     │ Home cockpit · Notes · Todos · Projects  │
                     │ Calendar · Gym · Log/Data(Oura) · Tea ×2 │
                     └───────────────┬──────────────────────────┘
                                     │ Supabase REST (bridge; pw-gated after Phase 1)
                     ┌───────────────▼──────────────────────────┐
                     │ SUPABASE  kgztnportoondvwicfqb           │
                     │ notes/todos/projects/events/gym/logs     │
                     │ + NEW: brain_editions · brain_status ·   │
                     │ brain_questions(+answers) · feedback ·   │
                     │ agent_events (idempotency ledger)        │
                     │ + pg_cron: daily Oura pull (edge fn)     │
                     └───────────────▲──────────────────────────┘
                                     │ read scan + writes (D13 rules)
┌────────────────────────────────────┴─────────────────────────────┐
│ BRENDAN BRAIN daily routine (once/day; Ops Router inside, D51)   │
│ scan → route (intake modes + tag map + FOR CLAUDE) → research →  │
│ tea projector → edition (git + Supabase) → verify main push      │
└──┬──────────────┬──────────────┬──────────────┬──────────────────┘
   │ outbox/inbox │              │              │ read-only
┌──▼───┐ ┌────────▼──┐ ┌─────────▼──┐ ┌─────────▼─────────┐
│Footy │ │ HealthBot │ │ TradingBot │ │ Shopify (orders)  │
│ Bot  │ │ (+Oura via│ │ paper-only │ │ Gmail (dormant)   │
└──────┘ │ Supabase) │ └────────────┘ │ QuickBooks:DENIED │
JobsBot  └───────────┘                └───────────────────┘
(paused)
Cowork / ChatGPT / Codex ──"handoff block" paste──▶ queue/inbox/from-*.md
Website Builder: manual session, event = site task in paper (D24)
Skill Scout: monthly AI-growth pitch in the paper; never installs (D54)
```
Roles: Fable=architect (to 07-18) → Opus. Sonnet=builder/research. Haiku=scans/routing.
