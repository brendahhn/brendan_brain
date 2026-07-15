<!-- Discovery deliverable 2026-07-14 (Fable). -->
# Personal OS ↔ Brain Bridge Spec (Phase 1)

## Security first (D12 — ships BEFORE bridge traffic)
1. Rotate the Supabase anon key (current one is public in git history).
2. Enable RLS on all tables; a simple shared-secret password gate: site prompts once,
   stores locally; requests carry it (Supabase JWT or header-checked edge functions).
3. Brain sessions get the secret via environment/settings — never committed.
4. Full data export (backup) BEFORE any schema change (D19). Verify restore once.

## New tables
`brain_editions(id=date, md, created_at)` · `brain_status(id, snapshot jsonb, ts)` ·
`brain_questions(id, question, status, answer, answered_at)` ·
`feedback(id, text, created_at, processed_at)` ·
`agent_events(id=op-id, kind, payload_hash, ts)` — idempotency ledger: every agent write
records here first; replays skip. · `tea_fulfillments(order_no, marked_at)` ·
plus `created_by` column (default 'brendan') on notes/todos/projects/events.

## Contracts
- Writes follow D13: create-only + check-done; deletes only FOR CLAUDE notes; everything
  else immutable to agents. Retry with backoff ×4; verify reads after writes.
- Editions: publish step upserts the edition row (one API call — no site rebuild).
- Site reads new tables on Home; question answer boxes update brain_questions;
  feedback box inserts feedback rows.

## Environment prerequisite (Brendan)
Network policy must allow *.supabase.co for Brain sessions/routines (D18).

## Tea Stock save bug (first Builder task, D14)
Diagnose live: probable missing table/column (`role`) in Supabase — confirm via REST once
egress opens, create/alter table, verify autosave path end-to-end in browser.
