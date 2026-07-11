<!-- version: 1.0.0 (2026-07-11) | status: provisional until 2026-08-15 (system/V2_LEDGER.md) -->
# Learning Policy (the Learning Engine)

The system learns at six levels, but with a hard asymmetry (arch-challenge response #3):
**all six levels are RECORDED as evidence; only levels 1–2 may generate behavior-change
proposals; NOTHING consequential auto-applies.** The enactment path for every learned
change is the existing machinery: evidence → `preferences/PROPOSED_RULES.md` →
MEMORY_POLICY thresholds → Brendan's approval → CONFIRMED_RULES. The weekly report
observes; it does not change behavior by itself.

## The six levels
| # | Level | What gets recorded | Where | May propose changes? |
|---|---|---|---|---|
| 1 | Output | preferred length/structure/tone/format; repeated edits to drafts; rejected formats | evidence log + PRESENTATION_PREFERENCES | YES (proposal-only) |
| 2 | Preference | likes/dislikes/constraints/interest shifts | evidence log + INTEREST_PROFILE weights (weights may move ±1 on repeated evidence; topic ADD/REMOVE needs approval) | YES (proposal-only) |
| 3 | Research | which sources/methods/depths produced useful findings (usefulness = Brendan's reaction or task outcome) | task Research Logs + SOURCE_RELIABILITY.md | observations only |
| 4 | Workflow | schedule fit, question strategies (blocking-vs-assume outcomes), depth calibration | weekly report + CAPACITY_LEDGER | observations only |
| 5 | Prediction | calibration from predictions/ vs outcomes/; recurring error types | outcomes/ scoring + weekly report | observations only |
| 6 | Meta | whether departments/prompts/skills/models/system should change | weekly report → CONTINUOUS_IMPROVEMENT proposals | via OCI proposals to Brendan ONLY |

## Learned-change record (mandatory fields — no silent learning)
Any change proposed (levels 1–2) or executed (after approval) is recorded as a `decision`
artifact in `decisions/` with: **evidence** (artifact ids / evidence-log lines) ·
**confidence** · **date_range** of the evidence · **exceptions** (where the change doesn't
apply) · **reversibility** (how to undo) · **approved_by** (`brendan` | `threshold+brendan` —
never blank on an executed change) · **success_measure** (what reaction/metric would show
it worked, checked in a later report). Never silently alter a consequential preference;
detected interest CHANGES (e.g. Tacoma interest fading) become a dated proposal + question,
not a profile rewrite — the old profile line stays until Brendan confirms.

## Weekly Learning & Improvement Report (one run, gated)
`python3 tools/learning_report.py [--week YYYY-Www]` drafts
`system/reviews/YYYY-Www-review.md`; a Sonnet session refines it. **Material-change gate**:
below thresholds (see tool) it writes a one-line "nothing material" stub and STOPS —
no ritual reviews of an idle system. Contents when material:
1. What the system learned about Brendan (levels 1–2 evidence, incl. repeated edits/reactions)
2. What it learned about its own performance (levels 3–5)
3. Assumptions that changed (with the evidence)
4. Repeated edits or reactions (verbatim counts)
5–9. Proposed prompt / skill / schedule / domain / agent changes (each as an OCI 8-field
   proposal — see CONTINUOUS_IMPROVEMENT.md; max 3 open at once)
10. Experiments for the coming week (only from open proposals; each has a rollback)
Consequential proposals surface in the newspaper's questions section for Brendan.
