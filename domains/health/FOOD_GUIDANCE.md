---
id: health-food-guidance
title: Sanitized food guidance for the Kitchen desk (bridge source)
artifact_type: knowledge
domain: health
sensitivity: personal
confidence: low
derived_from: [domain-health]
created_at: 2026-07-11
updated_at: 2026-07-11
created_by: systems_architect
topics: [health, food, guidance, kitchen-bridge]
---
# Food Guidance — the ONLY health input the Kitchen desk may read

**Sanitization contract**: this file is deliberately `sensitivity: personal` (not `health`)
because it must contain NOTHING Brendan-specific-medical: no conditions, symptoms, labs,
doses, medications, or biometric values — ever. Generic, food-level guidance only
("favor X", "limit Y", "tolerates Z well"). The Health Robot (or a health-domain session)
updates it via the health sync flow; each row cites a health-repo artifact WITHOUT quoting
its sensitive content. If anything medical appears here, that is a sanitization failure —
remove it and fix the exporter (tests gate the newspaper side; this file is the wall).

Guidance is guidance, not prescription (KITCHEN_PROFILE bridge rules). Tentative research
NEVER becomes a standing restriction here without Brendan's confirmation.

## Current guidance rows

| # | guidance (generic food level) | strength | source (health-repo id, not quoted) | added |
|---|---|---|---|---|

*(empty — awaiting the Health Robot's first sanitized export. The health routine's
brain-sync run-end step may append rows that pass the sanitization contract above.
Until rows exist, Kitchen treats guidance as UNKNOWN and labels menus `unclear`.)*

## Explicit dietary constraints (Brendan-stated only)

*(none recorded — only Brendan's explicit words may add a row here)*
