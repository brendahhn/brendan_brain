<!-- version: 1.0.0 (2026-07-10) -->
# Memory & Privacy

## Simple version
Everything the system remembers is a file you can read. Health and money artifacts are
invisible outside their own domains. Nothing sensitive goes in the newspaper beyond
generic conclusions. Forgetting is real but honest: Git history keeps deleted content
unless you approve a history rewrite.

## What gets remembered, where
| Kind | Where | Rule |
|---|---|---|
| Raw observations ("mentioned X on date Y") | `timeline/` | uncertainty preserved; never auto-promoted to fact |
| Facts & conclusions | `domains/<d>/knowledge/` | need evidence or your confirmation, with provenance |
| Tasks, watches, questions | `queue/`, `newspaper/questions/` | operational state |
| Predictions & how they turned out | `predictions/`, `outcomes/` | originals never rewritten |
| Your preferences & rules | `preferences/` | evidence → proposed → confirmed (by you) |
| Robot summaries | `queue/inbox/from-*.md` | sanitized by contract |

## Sensitivity levels
`personal` (default) · `private` · `health` · `financial` · `public`. Health and investing
artifacts are gated **by domain**, not just by tag — a missing tag cannot leak them
(tested: `tests/test_retrieval.sh`). Overriding the gate requires a written reason that
gets logged.

## What the newspaper may carry
Generic research conclusions and decision-needed items only. Never your labs, doses,
symptoms, biometrics, or personal context — those live in `health-notebook` and the paper
links there. A pattern-scrub withholds any health export containing numeric dose/biometric
values, visibly flagged.

## Forgetting, honestly
Say "forget …" → the brain-forget skill finds every copy (artifact, indexes, robot outbox
blocks, editions, evidence lines) and shows you a PLAN: what normal deletion removes, and
the fact that **Git history keeps the content in every clone** unless you separately
approve a history rewrite (a supervised, irreversible step). After your confirmation:
delete + redact derived copies + tombstone recording THAT something was removed, never WHAT.
For truly radioactive information: don't put it in Git at all.

## The work boundary (the one rule with no undo)
No employer data enters this repo or any personal repo — no internal docs, datasets,
customer info, financials, unreleased plans. A future work system clones this architecture
with a separate account, separate repos, separate memory. The validator rejects artifacts
claiming an origin outside the personal manifest, but the real guardrail is you: if in
doubt, it stays out.

## Your levers
- Edit or delete any file — it's your repo (prefer supersede over silent edits to history).
- `python3 tools/brain_search.py "topic" --domain health` — see exactly what's retrievable.
- Every skill logs sensitive-access reasons; audits live in `system/audits/`.
