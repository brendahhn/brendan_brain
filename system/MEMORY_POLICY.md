<!-- version: 1.0.0 (2026-07-10) -->
# Memory Policy

## Memory classes → locations
| Class | Location | Rule |
|---|---|---|
| Raw timeline | `timeline/YYYY/MM/` | Dated observations, uncertainty preserved, never auto-promoted |
| Durable knowledge | `domains/<d>/knowledge/`, root profile files | Requires evidence or Brendan confirmation; provenance via `derived_from` |
| Active operational state | `queue/`, `newspaper/questions/`, op records | Generated QUEUE.md mirrors it |
| Research archive | `domains/<d>/research/` | Completed reports with sources |
| Predictions/outcomes | `predictions/`, `outcomes/` | Score every prediction when horizon passes |
| Preference evidence | `preferences/PROPOSED_RULES.md` evidence log | Reactions accumulate; see thresholds below |
| Confirmed rules | `preferences/CONFIRMED_RULES.md` | Changes behavior immediately |
| Rejected rules | `preferences/REJECTED_RULES.md` | Never re-propose without new evidence |
| Sensitive memory | in-domain, `sensitivity:` tagged | PRIVACY_POLICY governs |
| Live operational state (V2) | `live_state` artifacts (e.g. kitchen PANTRY.md) | The one mutable class: in-place last-write-wins edits, git-audited, exempt from supersede chains; physical-state facts only, never conclusions |

## Capture triage (what a session should write down)
- Explicit "remember this / add to Brain / queue this" → capture immediately, verbatim intent.
- Dated personal observation (health symptom, surf session, life event) → timeline file,
  marked with appropriate sensitivity, no interpretation.
- Preference signal (liked/disliked/corrected) → evidence entry in PROPOSED_RULES.md.
- Decision, prediction, new interest, priority change → respective artifact.
- Conversational filler → do NOT capture.

## Promotion thresholds
- Observation → knowledge: multi-occurrence or Brendan confirmation; new file with
  `derived_from` listing the timeline ids; original stays raw.
- Preference evidence → CONFIRMED rule: ≥3 consistent signals across ≥2 distinct days, OR
  explicit instruction ("always/never/stop showing me"), OR Brendan approves a proposal.
  One reaction NEVER confirms a rule.
- Corrections supersede: new artifact with `supersedes`; old artifact gets `superseded_by`
  and stays in place. History is never silently rewritten.

## Growth control
One file per artifact; monthly timeline folders; generated indexes rebuildable at any time.
When a folder exceeds ~200 files, the Archivist proposes (does not silently execute) an
archival scheme in a system/operations note.
