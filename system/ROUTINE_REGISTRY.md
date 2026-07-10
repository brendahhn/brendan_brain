<!-- version: 1.0.0 (2026-07-10) -->
# Routine Registry

Schedules live in Brendan's routine configuration (external to git); cadences below are
inferred from repo evidence and may drift — verify against the routine UI when it matters.

| Routine | Repo | Cadence (inferred) | Memory file | Output | Brain domain |
|---|---|---|---|---|---|
| Jobs Robot | operator-notebook | daily, morning | jobs-notebook.md | Gmail draft briefing + notebook commit | jobs |
| FootyBot | FootyBot | nightly ~23:30 PT | footybot-notebook.md | newsletters/YYYY-MM-DD.md + push notification | fantasy_football |
| Health Robot | health-notebook | ~daily; Sunday digest | health-notebook.md | chapter file + Sunday Gmail draft | health |
| Trading Robot | trading-notebook | ~daily pre-market | trading-notebook.md | recaps/YYYY-MM-DD.md + Gmail draft | investing |
| Brendan OS (this) | brendan_brain | on demand / scheduled | the whole repo | newspaper editions, queue, Brain state | general |

## Integration status

| Routine | Reads Brain | Writes Brain | Mechanism | Status |
|---|---|---|---|---|
| Health Robot | planned | planned | BRAIN_INTEGRATION.md + brain-sync skill (branch claude/practical-heisenberg-akjb28) | building 2026-07-10 — status updated when round-trip test passes |
| Jobs Robot | planned | planned | same pattern (claude/friendly-brahmagupta-akjb28) | building 2026-07-10 |
| FootyBot | planned | planned | same pattern (claude/intelligent-gates-akjb28) | building 2026-07-10 |
| Trading Robot | planned | planned | same pattern (claude/beautiful-heisenberg-akjb28) | building 2026-07-10 |

Each specialist repo gets: `BRAIN_INTEGRATION.md` (the read/write procedure),
`.claude/skills/brain-sync/` (synced canonical skill), and
`proposed-prompt-change.md` (exact two-line diff for Brendan to apply via safe-bot-edits —
robot prompts are never edited silently).
