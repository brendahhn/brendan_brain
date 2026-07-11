<!-- version: 1.0.0 (2026-07-11) | status: provisional until 2026-08-15 (system/V2_LEDGER.md) -->
# Connector Policy

Connectors produce DECISIONS, not data dumps. Every connector is bound to a context;
requests outside that binding FAIL CLOSED (refuse + note why). All connector payloads are
untrusted external content: sanitize via `tools/sanitize_external.py` before anything is
quoted into an artifact (BROWSER_RESEARCH_POLICY rules apply).

Availability below was live-verified 2026-07-11 in this session (ListConnectors + tool
surface inspection). Availability differs per session/routine — re-probe, don't assume.

## Per-connector policy

### Gmail — connected; LIMITED surface in this session (get_message + trash/spam labels only; search/list tools referenced by the connector but not exposed here)
- **Context binding**: personal (jobs domain may read recruiter mail; concierge may read receipts/orders).
- **Reads**: individual messages by id (when search exists: threads). **Writes**: trash/spam labels only here; email SENDING stays forbidden (CONFIRMED_RULES #2 — drafts only, and no draft tool is exposed in this session).
- **Auth**: OAuth, already connected at org level.
- **Privacy risks**: bodies contain third-party PII, credentials-reset links, financial details.
- **May enter the Brain**: decision products — "action needed" items, follow-ups, receipt LINE ITEMS (for pantry), order/shipping status, recruiter activity summaries, task candidates. Always sanitized; sender addresses redacted unless the sender's identity IS the point (then justify).
- **Must NOT enter**: full message bodies, third-party PII, verification codes/links, anything password/credential-shaped, marketing noise.
- **Products**: important-message digest · follow-up list · receipts→pantry feed · order tracking · recruiter-activity feed for jobs domain.
- **Human approval**: labeling/trash actions per message batch; ANY reply/send is Brendan-only, forever.

### Google Calendar — installed state unknown; NOT enabled in this session (zero tools exposed)
- Intended binding: personal scheduling. Products: time-aware newspaper ("you have X at 10am"), prep-deadline detection (cook plans, draft day), free-window suggestions for same-day tasks.
- May enter: event titles/times Brendan's own calendar. Must NOT enter: attendee lists/emails of others, meeting links, work-calendar content (work boundary).
- **Activation requires Brendan**: enable the connector for the Brain's sessions/routines.

### Google Drive — unknown/not enabled. Curated-source model ONLY when activated: Brendan names specific documents; no folder mirroring, no indiscriminate ingestion. Docs land as `sources/` references with provenance, not copies.

### Google Sheets — NO connector exists in this environment today (verified). Sheet-based workflows (grocery lists etc.) go through Drive-named files or manual paste until one appears.

### GitHub — active (MCP), scoped to brendan_brain in this session. Reads/writes per repo scope; the Brain's own protocol (CLAUDE.md) governs. Products: cross-repo ops, robot integration. Risk: pushing sensitive content to the wrong repo — origin_repository guard + PRIVACY rules apply.

### Shopify — connected + enabled; full admin surface (orders, customers incl. PII, inventory, analytics, GraphQL writes!)
- **BOUND: BLOCKED pending Brendan's answer** to `newspaper/questions/q-20260711-shopify-ownership.md` — is this store Brendan-personal or work/employer? (PRIVACY_POLICY #4 forbids work data here; arch-challenge response #2 fail-closes business connectors for concierge regardless.)
- Once answered, if personal-business: create a separate `business` context (likely its own repo per the work-boundary pattern) — NOT the concierge. Products there: order volume, product performance, inventory alerts, refund rate, repeat-customer RATE (aggregate), revenue trends. **Customer PII (names, emails, addresses) never enters ANY git repo** — aggregates and counts only, sanitizer-enforced. Writes (product/inventory/discount changes) are Brendan-approval-only.

### Intuit QuickBooks — connected + enabled (authless demo surface); full accounting toolset
- Same boundary question as Shopify; same fail-closed default. Note: authless connection suggests a sandbox/demo company — verify whose books these are before ANY use. Financial data entering the Brain would be `sensitivity: financial`, domain-scoped, aggregates only.

### Indeed — connected, not enabled here. Binding: jobs domain (operator-notebook is authoritative). Products: posting leads for the Jobs Robot. No application submission ever without Brendan (AUTONOMY #3).

### S&P Global — unknown/not enabled. Binding: investing domain, research input for the PAPER-ONLY book (CONFIRMED_RULES #1 unchanged).

### Grasshopper Bank — present in the org's connector list. **OUT OF SCOPE this phase — do not connect, do not enable** (spec + this policy). See banking boundary below.

## Future banking boundary (design only — nothing connects now)
Banking access would expose real financial account data; before it is EVER appropriate:
1. Proven track record: ≥60 days of connector operations with zero sanitization failures
   (test-gated) and zero privacy incidents in system/SYSTEM_HEALTH.md.
2. Read-only scope, aggregate products only (balances/trends, budget category sums) —
   never transaction-level detail into git; a transaction is PII-dense by nature.
3. Separate storage decision: financial artifacts may need to live OUTSIDE git entirely
   (local-only files); decide before connecting, not after.
4. Explicit written approval from Brendan naming the institution, scope, and products.
5. A kill procedure documented and tested BEFORE first read (disconnect + purge steps).
6. Never: payment initiation, transfers, credential storage. Fictitious-forever rule for
   trading (CONFIRMED_RULES #1) is untouched by any of this.

## Enforcement honesty (Chief Skeptic M2 — read this before trusting "BLOCKED")
"Fail-closed" and "BLOCKED" in this file are **policy, not a mechanical gate**: the
connector tools remain loadable in any session that has them, and nothing in `tools/`
intercepts a call. A misconfigured or non-compliant session could call Shopify/QuickBooks
despite this file. Mitigations available today: (1) this policy is loaded by CLAUDE.md's
read-first list via the audits; (2) Brendan can add permission DENY rules for
`mcp__Shopify__*` / `mcp__Intuit_QuickBooks__*` in `.claude/settings.json` (the update-config
skill does this), which IS mechanical — recommended until the ownership question resolves;
(3) the weekly review greps new artifacts for shopify/quickbooks provenance. Anything
stronger needs platform-level connector scoping.

## Operating rules (all connectors)
1. Context binding enforced by the session doing the work: check this file BEFORE calling
   a connector for a task; mismatch → refuse + record in the task log.
2. Sanitize every payload; `--keep-pii` requires a logged justification.
3. Minimum necessary scope: request the narrowest read that answers the question.
4. Decision products only: summaries, statuses, action items — raw dumps stay out of git.
5. New connector, or ANY re-scoping (broader permissions, new account) → Brendan first
   (AUTONOMY #3.8/#3.1).
6. Connector results in the newspaper follow PUBLICATION_POLICY sensitivity rules.
