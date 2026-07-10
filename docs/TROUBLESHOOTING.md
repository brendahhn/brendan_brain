<!-- version: 1.0.0 (2026-07-10) -->
# Troubleshooting

## Simple version
Say to Claude (with this repo attached): **"check system status."** It runs the checks
below and tells you what's wrong. This page is for when you want to look yourself.

## Quick diagnosis table
| Symptom | Check | Fix |
|---|---|---|
| No newspaper this morning | Did the daily routine run? claude.ai routines screen → run history | Re-run it, or in any session: "build and publish today's paper" |
| A robot's section says [FAIL]/missing | `queue/inbox/from-<robot>.md` — is there a dated block? Robot repo's notebook CHANGELOG | If the robot ran but no block: its routine is missing `brendan_brain` in repo selection (START_HERE step 1) |
| "Unfinished operation" warnings | `python3 tools/oplog.py status` | Follow the op file's repo states; finish or mark failed honestly |
| QUEUE.md looks wrong | `python3 tools/build_queue_dashboard.py` (exit 2 = mismatches listed) | Fix the listed status/folder mismatches (`git mv` or edit `status:`) |
| Validation errors | `python3 tools/validate_frontmatter.py --all` | Each error names file + missing field; fix per system/SCHEMAS.md |
| Duplicate tasks after concurrent runs | Same command — flags OPEN DUPLICATE dedupe_keys | Merge task bodies, keep both histories, supersede one id |
| Search can't find something you know exists | Is it sensitive? Add `--domain health` (etc.) or `--allow-sensitive "reason"` | Working as designed — the gate fails closed |
| Push failed / branch weirdness | `git ls-remote origin main` vs `git rev-parse HEAD` | Retry (2/4/8/16s), rebase-pull first; never force-push |
| A test fails | `tests/run_all.sh <test-name>`; log in tests/results/ | Fix before trusting the affected feature; commit BEFORE re-running (the harness tests committed HEAD) |
| Gmail draft missing | Known intermittent issue (predates Brendan OS) | The repo file is the durable copy; push notifications carry headlines |
| Everything is on fire | `system/SYSTEM_HEALTH.md` (last known state) + `system/audits/` | Ask a session: "run a full health check and repair what's safe" |

## Verify the whole system in one line
`cd brendan_brain && python3 tools/validate_frontmatter.py --all && python3 tools/oplog.py status && tests/run_all.sh`
(Expect: 0 errors, 0 unfinished, PASS=8.)

## Getting help from Claude
Any session with this repo can self-diagnose: the skills, policies, and this file are all
it needs. Describe the symptom in plain words; don't pre-diagnose.
