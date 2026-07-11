<!-- version: 1.0.0 (2026-07-11) | status: provisional until 2026-08-15 (system/V2_LEDGER.md) -->
# Office of Continuous Improvement (OCI)

Not a research department and not a daemon: a charter + a review cadence + a proposal
format. Its job is pressure-testing the system itself; it may NOT redesign anything —
it proposes, Brendan (or the autonomy ladder for trivially-reversible items) disposes.

## Scope (what reviews look for)
Repeated mistakes · stale assumptions · duplicated work across desks/robots · predicted-vs-
actual outcome gaps · agents/roles not earning their cost (3-strike retirement,
STAFFING_POLICY) · prompt quality · skill quality (foundry criteria) · retrieval failures ·
publication usefulness (annotations/coverage ledger) · missed opportunities (things Brendan
asked twice, watches that never fire usefully).

## Cadence (deliberately lean — arch-challenge response #7)
| Review | Model | Trigger | Output |
|---|---|---|---|
| Weekly review | sonnet | `tools/learning_report.py` gate passes (≥5 fresh signals); otherwise a one-line stub | `system/reviews/<week>-review.md` (shared with the Learning report — ONE run) |
| Adversarial review | opus (fresh context) | a real failure, Brendan's request, or ≥6 weeks since last — whichever comes FIRST, and only if the weekly gate passed at least twice since the last one | attack report in `system/audits/` |
| Architecture review | fable | failures spanning ≥2 departments, or major capability change | audit + repair plan |

## Improvement proposal format (all 8 fields mandatory)
`## PROPOSAL: <title>` in the review file (or its own decision artifact if executed):
**problem** · **evidence** (artifact ids, counts — no vibes) · **proposed change** ·
**expected benefit** · **cost** (build + ongoing tokens/attention) · **risk** ·
**test plan** · **rollback plan**.

## Anti-endless-redesign guardrails (binding)
1. **Max 3 open proposals/experiments system-wide.** A 4th waits for a slot.
2. A subsystem changed in the last 30 days is off-limits without new failure evidence.
3. Every proposal names its rollback BEFORE approval; no rollback → no proposal.
4. Reviews of an idle system don't happen (the gate) — silence is recorded, not padded.
5. OCI itself is provisional (V2_LEDGER): if two consecutive months of reviews produce no
   acted-upon proposal, OCI's cadence drops to on-failure-only.
