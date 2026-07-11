<!-- version: 1.0.0 (2026-07-10) -->
# Routine Registry

Schedules live in Brendan's routine configuration (external to git); cadences below are
inferred from repo evidence and may drift — verify against the routine UI when it matters.

| Routine | Repo | Cadence (inferred) | V2 recommended time (PT, SCHEDULE_PLAN) | Memory file | Output | Brain domain |
|---|---|---|---|---|---|---|
| Jobs Robot | operator-notebook | daily, morning | 02:00–05:00 window | jobs-notebook.md | Gmail draft briefing + notebook commit | jobs |
| FootyBot | FootyBot | nightly ~23:30 PT | ~23:30 (unchanged) | footybot-notebook.md | newsletters/YYYY-MM-DD.md + push notification | fantasy_football |
| Health Robot | health-notebook | ~daily; Sunday digest | 02:00–05:00 window | health-notebook.md | chapter file + Sunday Gmail draft | health |
| Trading Robot | trading-notebook | ~daily pre-market | 06:30 opening analysis (optional 05:45 premarket; optional ~13:15 close review, never delays the paper) | trading-notebook.md | recaps/YYYY-MM-DD.md + Gmail draft | investing |
| Brendan OS (this) | brendan_brain | on demand / scheduled | **07:05 editorial** (gate: tools/check_inputs.py) | the whole repo | newspaper editions, queue, Brain state | general |

Times are recommendations Brendan applies in the routines UI; the mechanical honesty gate
(missing robot → [FAIL] item, publish anyway) is what's actually enforced (SCHEDULE_PLAN).

## Integration status

| Routine | Reads Brain | Writes Brain | Mechanism | Status |
|---|---|---|---|---|
| Health Robot | implemented | implemented | BRAIN_INTEGRATION.md + brain-sync (claude/practical-heisenberg-akjb28, 33d1d48) | MERGED to main (32f35f7, PR #4) + prompt steps applied + post-merge round-trip verified (op-20260710-postmerge-roundtrips). Live once Brendan adds brendan_brain to the routine's repo selection |
| Jobs Robot | merged | merged | PR #2 → main 4ec80ed; prompt steps applied | pending only routine repo selection |
| FootyBot | merged | merged | PR #1 → main 506eabc; prompt steps applied | pending only routine repo selection |
| Trading Robot | merged | merged | PR #1 → main 0fe104e; prompt steps applied | pending only routine repo selection |

Each specialist repo gets: `BRAIN_INTEGRATION.md` (the read/write procedure),
`.claude/skills/brain-sync/` (synced canonical skill), and
`proposed-prompt-change.md` (exact two-line diff for Brendan to apply via safe-bot-edits —
robot prompts are never edited silently).
