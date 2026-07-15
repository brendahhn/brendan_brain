<!-- Discovery deliverable 2026-07-14 (Fable). -->
# Source of Truth Rules

| Data | Truth lives in | Mirrors/consumers |
|---|---|---|
| Notes, todos, projects, calendar, gym, daily log | Personal OS Supabase | Brain reads via bridge; captures durable parts as artifacts |
| Newspaper edition | brendan_brain git (newspaper/editions/) | Supabase copy for display — regenerable |
| Brain knowledge/queue/preferences/predictions | brendan_brain git (markdown) | QUEUE.md/BRAIN_MAP.md generated |
| Tea BOM + rules | domains/tea-business/bom-20260714.md (until Tea tab save-fix ships, then Supabase recipe with Brain snapshot mirror) | inventory projector |
| Tea inventory counts | Brendan's physical counts → Personal OS Tea Stock (post-fix) | Brain snapshots on change |
| Order events | Shopify (read-only; notifications + checkout only) | deductions fire on BRENDAN's fulfilled-mark, never Shopify status |
| Tea revenue | Tea Finance tab (manual + Shopify auto-append, aggregate only) | Brain aggregates |
| Robot domain internals | each robot's own repo (notebook files) | Brain gets outbox blocks only |
| Oura | Oura API → Supabase (edge function, daily cron) | HealthBot reads; raw numbers never in git |
| Schedules/routines/connectors/network policy | claude.ai platform UI (Brendan-only) | ROUTINE_REGISTRY documents, never controls |

Conflict rule: the truth column wins; mirrors regenerate; generated files never hand-edited.
Supersede, never erase (git history is the audit trail).
