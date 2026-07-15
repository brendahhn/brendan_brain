<!-- Discovery deliverable 2026-07-14 (Fable). -->
# Ops Router Spec (runs INSIDE the daily Brendan OS routine — D51)

## Position in the daily run
bootstrap → **OPS ROUTER** → triage → research → tea projector → edition → verify-push.

## Scan set (haiku-tier where possible)
1. Supabase notes: `updated_at > last_scan` (watermark in system/, plus per-item
   `agent_events` dedupe). Full bullet trees. 2. todos (same). 3. brain_questions answers.
4. feedback box rows. 5. Shopify orders since watermark (read-only). 6. queue/inbox/from-*
   blocks (existing triage). 7. Brendan's fulfillment marks (tea_fulfillments rows).

## Routing order (first match wins)
1. FOR CLAUDE category/all-caps → parse as instruction to the system → execute routing it
   describes → delete the note (sole delete permission, D21/D55).
2. Category tag map: footybot→FootyBot idea queue · health→HealthBot idea queue ·
   tea→tea-business desk · (extendable; Brendan edits map by re-tagging, D22).
3. brain-intake modes (existing INTAKE_POLICY): answer-tomorrow / remember / research /
   watch / same-day(→ never scheduled; only manual sessions) / one-off.
4. Website-ish ("fix the site…") → site task list → appears in paper; Builder is manual (D24).
5. Needs-Brendan → agent-created todo in Personal OS (D52).
6. No match / pure journal content → leave alone, no capture, no noise.

## Feedback learning
Feedback rows → annotation vocabulary → preference evidence; routing corrections logged;
>50% override rate on a rule = auto-flag (existing V2 ledger discipline).

## Empty behavior
Nothing new anywhere → one health line in SYSTEM_HEALTH, publish edition from whatever
robots sent, exit. No manufactured work.

## Failure surfacing
Scan/write failures → edition failure flags + brain_status row; partial failure reported
as partial (hard rule 7). Idempotent retries next day via watermarks + agent_events.
