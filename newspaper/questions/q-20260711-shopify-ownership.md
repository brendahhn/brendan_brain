---
id: q-20260711-shopify-ownership
title: Shopify/QuickBooks — whose store and books are these?
artifact_type: question
task_id: none
kind: blocking
status: open
asked_at: 2026-07-11
created_at: 2026-07-11
domain: general
sensitivity: personal
topics: [connectors, shopify, quickbooks, work-boundary]
---
The org's connectors include a CONNECTED Shopify store admin (full surface: orders,
customers with PII, inventory, GraphQL writes) and a connected QuickBooks (authless —
possibly a sandbox/demo company).

**Blocking question**: Is the Shopify store (and QuickBooks company) yours personally, a
side business of yours, an employer's, or a demo/sandbox?

Until answered, CONNECTOR_POLICY blocks ALL Shopify/QuickBooks reads into the Brain
(PRIVACY_POLICY #4 work boundary + arch-challenge response #2). If it's your own business,
the plan is a separate `business` context/repo — not the personal concierge — with
aggregate-only products and customer PII never entering git.
