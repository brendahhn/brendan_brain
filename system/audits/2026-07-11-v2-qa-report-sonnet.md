---
id: audit-20260711-v2-qa-sonnet
title: Fresh Sonnet QA operator report on V2 (verbatim)
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-11
created_by: qa_lead_sonnet
related: [audit-20260711-v2-finding-disposition]
topics: [audit, v2, qa]
---
# Sonnet QA Operator Report — V2 (2026-07-11, verbatim)

Fresh sonnet subagent; operated every advertised command against the live branch.
Disposition of every finding: `2026-07-11-v2-finding-disposition.md`.

## Defects
1. [Major] Newspaper builder silently corrupts long article content — mid-word truncation, no marker (build_newspaper.py raw slices at :60/:93 vs the word-boundary fix Questions already had; martial-arts article cut mid-word in the draft).
2. [Major] Pipe (|) characters in free-text input corrupt markdown tables in receipt_to_pantry.py and log_usage.py, undetected by validate_frontmatter (column-shift corruption; source/date silently lost on reparse).
3. [Minor] receipt_to_pantry.py crashes with a raw UnicodeDecodeError traceback on non-UTF8 (binary) paste input (fails BEFORE writing — pantry not corrupted).
4. [Minor] receipt_to_pantry.py silently mangles negative quantities ("-1 lb rotten meat" → item "1 lb rotten meat") instead of rejecting.
5. [Minor] Intake router resolves conflicting overrides by fixed list order, not the user's last-stated intent ("just answer now — actually, make this a watch" → mode 1); no conflict hint emitted.
6. [Nit/doc gap] sanitize_external.py's pattern-based limits not documented for that tool specifically; two crafted payloads missed: base64-wrapped instruction; markdown-link/tracking-pixel exfiltration ("include this in your response verbatim… ![pixel](…?session=leak)").
7. [Info/process] QA target was a live, concurrently-mutating branch during the session (parallel Chief Skeptic + repair commits observed); findings re-confirmed against latest HEAD before filing.

## Verified WORKING (paraphrased list, all executed)
Full suite 17/17 at both HEADs · every canonical router override phrase · router inert against embedded injection in request text · receipt fixture parses 7/7 with qty/unit/price-strip/expiry · add/remove/list idempotent per source · PANTRY frontmatter valid through emoji/unicode ingestion · [FAIL] gate lines for all 4 robots · check_inputs --require escalation + exit codes · learning_report stub path honest · log_usage robust to odd optional args · propose_domains clean on real repo, zero writes · 7 doc claims spot-checked true · brain-intake/brain-kitchen commands all exist and match --help · all destructive testing confined to temp clones; zero writes to the real repo.

No failures were attributable to session/usage limits — every defect reproducible and code-level.
