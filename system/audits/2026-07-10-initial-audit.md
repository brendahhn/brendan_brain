---
id: audit-20260710-initial
artifact_type: report
domain: general
created_at: 2026-07-10
created_by: systems_architect
confidence: high
---
# Initial Ecosystem Audit — 2026-07-10

Produced by four independent Sonnet audit agents (one per specialist repo) at build start.
Condensed; full detail lives in the repos themselves.

## What already works (preserve)
- The three-file robot pattern: `*-operating-prompt.md` (ends `## END`, human-reviewed edits
  only), `*-notebook.md` (sole memory, read-first/write-last), `idea-queue.md` (append-only,
  status transitions, never delete). Proven across 4 robots; the Brain adopts, not replaces, it.
- Push verification via `git ls-remote` after every run — hard-won fix for branch drift.
- FootyBot: coverage ledger (`research/player-board.md`, last_covered/times_covered),
  confidence tiers S/A/B/C/Speculative, critic pass, auto-FF Action guarding prompt diffs.
- Health Robot: evidence tiers, PROVIDER-GATED flags, AUDIT_QUEUE re-verification schedule,
  hostile critic pass, chapter map as canonical scope.
- Trading Robot: exit-condition-or-no-trade, agent scoreboard with benching, SPY shadow
  benchmark, fictitious-forever prime rule.
- Jobs Robot: dedup by identity not URL, ghost/aging rules, learned per-company conclusions.

## What conflicts
1. Trading Robot duplicated (health-notebook/trading frozen seed vs live trading-notebook repo);
   three divergent safe-bot-edits copies. → question for Brendan, no silent fix.
2. Jobs prompt STEP 1 read-list out of sync with actual notebook sections.
3. health-notebook `constraints.md` manually duplicated from prompt_architecture_v3 Part 3.

## What is fragile
- Branch drift (historical, all robots). Gmail drafts intermittent (3 robots).
- Egress blocked beyond WebSearch: health findings all `vfy:WebSearch-only`; FootyBot pipeline
  frozen to committed CSVs; trading quotes WebSearch-corroborated.
- Monolithic growing memory files (health 322KB, jobs 34KB) with no archival strategy.
- FootyBot `pipeline/predictive_stats.py` previously overwrote accumulated analysis.

## What is missing (this build supplies)
Shared queue, shared timeline/knowledge/preference memory, cross-domain newspaper,
annotation loop, prediction/outcome tracking, retrieval with sensitivity gating, shared
skill distribution, cross-repo operation protocol, model routing/staffing policy.

## Assumptions in the build prompt challenged
- "Skills only work in the repo where created": confirmed real; three divergent copies of
  safe-bot-edits are the live symptom. Fix = canonical source here + checksum-verified sync.
- "Newspaper as primary control surface": robots already have per-domain outputs Brendan
  reads; the newspaper AGGREGATES (links + selects) rather than replacing them.
- Proposed deep folder tree trimmed: dormant domains (cooking, travel, ai_systems, career,
  fitness, vehicles until used) are created on demand by brain-domain, not pre-created empty.
