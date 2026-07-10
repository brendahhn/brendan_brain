<!-- version: 1.0.0 (2026-07-10) -->
---
id: manifest-20260710
artifact_type: knowledge
domain: general
confidence: confirmed
created_at: 2026-07-10
created_by: systems_architect
---
# Repository Manifest

Repositories selected in the routine configuration. This is the complete accessible
workspace; nothing else may be read or written.

| Repo | Role | Default branch | Robot writes to | State (2026-07-10) |
|---|---|---|---|---|
| `brendahhn/brendan_brain` | Coordination repo (this one) | `main` (created by this build) | `main` | New — built 2026-07-10 |
| `brendahhn/operator-notebook` | Jobs Robot (JoBot) + dormant stocks stub | `main` | `main` | Active; Gmail degraded 3 runs |
| `brendahhn/FootyBot` | Fantasy football robot | `main` | `claude/**` → auto-FF to `main` via Action | Active; 8 newsletters shipped |
| `brendahhn/health-notebook` | Health Research Robot (+ frozen trading/ copy) | `main` | `main` | Active; Ch16/36 complete |
| `brendahhn/trading-notebook` | Trading Robot (paper, fictitious forever) | `main` | `main` | Active; 4 runs |

## Cross-repo layout assumption

Cloud routines that include multiple repos get sibling clones (e.g. `/home/user/<repo>`).
Brain integration in specialist repos locates the Brain at `../brendan_brain` and degrades
gracefully (skip, log a note) when absent. **To enable integration for a routine, Brendan must
add `brendan_brain` to that routine's repository selection.** This is the platform-supported
mechanism; there is no remote-fetch fallback (robots' egress is largely blocked).

## Known conflicts (recorded, not silently fixed)

1. **Trading Robot duplication.** `health-notebook/trading/` holds a frozen seed copy
   (RUN_COUNT 0, commit c04264e) of the robot that actually runs in `trading-notebook`
   (4 recorded runs). Three divergent copies of the `safe-bot-edits` skill disagree about
   where the Trading Robot lives. → Question for Brendan: `newspaper/questions/q-20260710-trading-dup.md`.
2. **Jobs prompt drift.** `jobs-operating-prompt.md` STEP 1 read-list omits sections that now
   exist in the notebook (STANDING DIRECTIVES, WATCHLIST INTEL). Recorded; prompt edits are
   Brendan-reviewed only.
3. **Gmail delivery** is degraded/intermittent across Jobs, FootyBot, Trading robots. The Brain
   treats Gmail drafts as best-effort; repo files are the durable channel.

## Inaccessible / referenced-but-absent

- No separate "surf dataset" or WSL analytics repo is selected; WSL analytics live inside
  Jobs Robot context and Brendan's mentions. Data Lab ships with synthetic fixtures until a
  dataset repo is selected. (Limitation, recorded in docs/LIMITATIONS.md.)
- No employer/work repositories are selected. Correct per the personal/work boundary.
