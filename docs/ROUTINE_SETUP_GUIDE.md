<!-- version: 1.0.0 (2026-07-11) -->
# Routine Setup Guide — the manual steps only Brendan can do

The coding session cannot change routine configuration; these are UI actions at
claude.ai (Claude Code → Routines / scheduled sessions). Everything else is already
merged and tested.

## 1. Repository selections (each routine needs BOTH repos)
| Routine | Repositories to select |
|---|---|
| FootyBot | `brendahhn/FootyBot` + `brendahhn/brendan_brain` |
| Health Robot | `brendahhn/health-notebook` + `brendahhn/brendan_brain` |
| Trading Robot | `brendahhn/trading-notebook` + `brendahhn/brendan_brain` |
| Jobs Robot | `brendahhn/operator-notebook` + `brendahhn/brendan_brain` |
| Brendan Brain editorial | `brendahhn/brendan_brain` only |

Click steps per routine: open the routine → Settings/Configuration → Repositories (or
"Sources") → Add repository → pick `brendahhn/brendan_brain` → Save. (Each robot's
operating prompt already contains the guarded brain-sync steps — verified merged to every
robot's main 2026-07-10; they no-op harmlessly until the repo appears.)
**Success evidence**: the robot's next run CHANGELOG contains a brain-sync line and a new
dated block appears in `brendan_brain/queue/inbox/from-<robot>.md`.
**Failure looks like**: CHANGELOG says "brain-sync: brendan_brain not in session; skipped."
→ the repo selection didn't stick; redo the click steps.

## 2. Schedules (Pacific; SCHEDULE_PLAN targets — set in each routine's schedule field)
FootyBot ~23:30 · Health + Jobs anywhere 02:00–05:00 · Trading 06:30 ·
**Brendan Brain editorial 07:10** (publication lands ~07:25). Optional: Trading close
review ~13:15. These are initial targets; the usage log will tune them with evidence.

## 3. Editorial routine prompt
If the editorial routine doesn't yet use it, paste `system/DAILY_ROUTINE_PROMPT.md` as its
operating prompt (v1.1, 2026-07-11 — includes the input gate, cowork triage, usage log,
main-branch git behavior).

## 4. Connectors (optional, when wanted)
Enable Google Calendar / Google Drive for Brain sessions to unlock time-aware papers and
curated doc ingestion. Recommended mechanical guard until the Shopify/QuickBooks ownership
question is answered: add DENY rules for `mcp__Shopify__*` and `mcp__Intuit_QuickBooks__*`
in `.claude/settings.json` (a session can do this for you — say "add the connector deny
rules"). Banking stays disconnected. **Also answer**:
`newspaper/questions/q-20260711-shopify-ownership.md` (blocking).

## 5. Production rehearsal (after V2 merge + repo selections; ~30 min total)
Run each manually from the routines UI, in order, watching for the success evidence:
1. **Health** manual run → fresh dated block in `queue/inbox/from-health-robot.md`.
2. **FootyBot** manual run → block in `from-footybot.md`.
3. **Trading** manual run → block in `from-trading-robot.md`.
4. **Jobs** manual run → block in `from-jobs-robot.md`.
   (Each should also show its normal own-repo output; a robot that improvises because its
   prompt is missing is a FAIL — stop and check the routine's prompt configuration.)
5. **Brendan Brain editorial** manual run LAST. Success evidence, all mechanical:
   - `check_inputs` reports all four fresh (not STALE/MISSING);
   - old activation smoke blocks are ignored (they're `<!-- triaged -->`-marked and stale-dated);
   - zero duplicate annotation actions (`ALREADY PROCESSED` guard);
   - no synthetic/cancelled watch in the Watches & System panel;
   - ONE coherent edition in `newspaper/editions/<PT-date>.md`;
   - pushed to **main** with `git ls-remote` verification in the run log.
6. The run (or you) saves a dated rehearsal audit in `system/audits/` recording all of the
   above. The 2026-07-11 overnight run was a useful FAILURE test (missing access/capacity),
   not a rehearsal — the rehearsal happens after the merge + selections.
**If any step fails**: don't proceed to the next; the failed robot's CHANGELOG names the
cause (repo selection, prompt, or capacity), fix that one thing and rerun it.
