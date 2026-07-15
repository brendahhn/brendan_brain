<!-- Discovery deliverable 2026-07-14 (Fable). Sources: AUTONOMY_POLICY, D1-D55. -->
# Permission Matrix

| Action | Autonomous? | Notes |
|---|---|---|
| Brain artifacts/tasks/watches/domains/indexes | ✅ | domain auto-create allowed w/ paper announcement (D23) |
| Routine ops commits → brendan_brain main | ✅ | standing rule D9; ls-remote verify |
| Robot repo commits (their own runs) | ✅ | robot's own memory; prompts NEVER silently edited (safe-bot-edits) |
| Personal OS: create todos/events/projects; refresh Log; check todos done | ✅ | D13; agent-created marked as such |
| Personal OS: delete ANY data | 🚫 except FOR CLAUDE-category notes after ingestion (D21/D55) | trash-first everywhere else; never wipe |
| Supabase schema changes | ⚠️ backup + migration note first (D19) | "stuff not saving" history |
| Website code: fix/feature on branch + PR | ✅ branch+PR | merge needs green verify; deploy = Vercel auto on main merge |
| Website: merge to main | ⚠️ low-risk fixes after verification OK; redesigns need Brendan look | D14 mandate given, still show him |
| Shopify reads (orders/products/aggregates) | ✅ read-only | customer PII NEVER in git (order numbers only) |
| Shopify writes | 🚫 ask | inventory/fulfillment fields ignored anyway (D39) |
| Gmail read/label | ✅ when tools exist | bodies never dumped to git |
| Gmail drafts | only to brendanhamor@gmail.com (D3); no tool today | |
| Gmail SEND / any message send | 🚫 NEVER | permanent |
| Purchases / carts | 🚫 NEVER order; ingredients: not even cart (D42); non-ingredient cart-prep in interactive session OK, always stop before checkout | permanent |
| Real trades / banking / job applications | 🚫 NEVER / NEVER / NEVER | trading paper-only (D26) |
| QuickBooks | 🚫 DENIED — mechanical deny rules ship in Phase 1 | Brendan: irrelevant |
| Third-party skill install | 🚫 ask; quarantine pilot first (D54) | Scout pitches only |
| Forgetting/deleting Brain history | 🚫 ask (brain-forget flow) | |
| Employer/work data | 🚫 never enters the system | |
| New connector or re-scoping | 🚫 ask | |
