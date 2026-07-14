<!-- Discovery decision log — grows during the interview; graduates to docs/DECISION_LOG.md on approval. -->
# Brendan OS Discovery — Decision Log

Format: ID · decision · source · date. "Inferred default" = Fable's recommendation Brendan
didn't override; he can reverse any of these by saying so.

## Round 1 — Vision and daily experience (2026-07-14)

- **D1 · Morning surface**: The daily output must be easily readable OUTSIDE Claude.
  Personal OS is preferred if it can be done simply; Gmail acceptable as fallback.
  Brendan is not picky about the surface, is worried about token cost, and wants
  **printability** down the road. → Plan: newspaper stays canonical in git; publish step
  additionally writes the edition to Supabase (one cheap API row, no site rebuild, no
  meaningful token cost); Personal OS renders it + a print-friendly view later.
  (Brendan, R1; delivery mechanism = inferred default)
- **D2 · Cadence ceiling**: Nothing is more urgent than the daily run. **Max one run per
  day per routine; no intraday alerts, no real-time interrupts.** Proactive findings go in
  the next paper. This deletes all "immediate Gmail alert" ideas from the roadmap
  (inventory alerts etc. become newspaper items). (Brendan, R1, explicit)
- **D3 · Never-do additions**: All prior boundaries confirmed (no purchases, no sending,
  no banking, no customer PII in git, no employer data). Added: **email drafts may only
  ever be addressed to brendanhamor@gmail.com** — never draft to anyone else. (Brendan, R1)
- **D4 · Memory density**: Confirmed "decisions, preferences, projects, confirmed facts —
  not a transcript." Notes containing question batches (e.g. health questions) should be
  **decomposed into the relevant queues** (Brain research queue / robot idea queues) for
  eventual research. Brendan offered to add timelines per item; default: not required —
  router infers, deadline optional, 7-day default SLA (D6). (Brendan, R1)
- **D5 · Intake defaults for the bridge**: **Todos: always read by the router.** Notes:
  read every new note if token-cheap (haiku-tier triage); `@claude` in a note acts as an
  explicit route-me marker/override. Open: category exclusions (e.g. `love`, `health`) —
  Round 2. (Brendan, R1; @claude semantics = inferred default)
- **D6 · Uncertainty & SLA**: Plain-language confidence tiers (existing practice) are fine.
  **Unstated-deadline research: surface results within ~7 days**, treated as
  lower-than-deadline priority. (Brendan, R1)
- **D7 · Perfect day shape**: Overnight routines → one tailored morning paper (health
  summary prominent; idea-queue items get real breakdowns). Anything captured during the
  day is actioned next cycle, never same-day. Brendan expects to add routines over time.
  (Brendan, R1)
- **D8 · Noticing license**: Broad. The system may notice and suggest anything —
  stale projects ("whatever happened to X?"), trends across Oura/log/gym, cross-domain
  contradictions — **suggestions are explicitly welcomed**, channeled through the daily
  paper only (per D2). (Brendan, R1)

## Operational decisions made during Round 1 (production repair, Brendan-directed)

- **D9 · Push-to-main standing rule**: Routine sessions pinned to platform `claude/*`
  branches must land routine operational commits on main (CLAUDE.md amendment,
  2026-07-14). Source: Brendan — "runs haven't been pushing to main, fix that."
  Recovery: op-20260714-stranded-branch-recovery (all 4 repos verified).
- **D10 · Duplicate daily run 2026-07-14**: keen-ritchie-r2elmx (14:25 double-fire) NOT
  merged — duplicate artifacts. Brendan should check the routines UI for a duplicated
  Brendan OS schedule entry. (Fable, evidence-based; flagged to Brendan)
