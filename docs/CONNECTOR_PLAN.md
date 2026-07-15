<!-- Discovery deliverable 2026-07-14 (Fable). -->
# Connector Plan

| Connector | State (verified 07-14) | Plan |
|---|---|---|
| Supabase (REST, not an MCP connector) | blocked by network policy | Brendan allows *.supabase.co → becomes the bridge backbone |
| Shopify | full admin surface live | READ-ONLY use (orders aggregate, product facts); writes ask-first; exit to Stripe Payment Links by 07-31 (task published) — after exit, poll Stripe read-only equivalent or email notifications |
| Gmail | get_message + trash/spam labels ONLY; no search/list/draft | design dormant (D33); Brendan may reconnect connector to refresh scopes; re-probe every session; drafts only-to-self whenever tool returns |
| Google Calendar | no tools | NOT NEEDED — Personal OS calendar is the real one (D34) |
| QuickBooks | connected (authless demo?) | DENY mechanically in settings (Phase 1); never used |
| Oura | via Supabase edge fn (site) | pg_cron daily pull server-side (no tokens); Oura Web retires Sept — API path already correct |
| Amazon | none | browser-based research only; ingredients never carted (D42); needs open egress |
| GitHub MCP | live, 5 repos | unchanged; operator-notebook out of this session's scope |
| Web egress | commerce sites all 403 (policy) | Brendan: trusted/full network for research environment, else sourcing scans stay honest-but-empty |
