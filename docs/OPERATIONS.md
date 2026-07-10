<!-- version: 1.0.0 (2026-07-10) -->
# Operations Manual

## Session bootstrap (any Brendan OS session in this repo)
1. `git pull --rebase origin main`
2. Read CLAUDE.md → CURRENT_PRIORITIES.md → BRAIN_MAP.md (regenerate if stale)
3. `python3 tools/oplog.py status` — resume any unfinished cross-repo operation FIRST
4. `python3 tools/validate_frontmatter.py --all` — repair before adding

## Daily Brendan OS run (scheduled or manual), in order
1. Bootstrap (above). 2. Triage `queue/inbox/` (Chief of Staff role). Scope: only the
`predictions`, `proposed_durable_knowledge`, and `questions_for_brendan` sub-fields of each
outbox block become artifacts (predictions/ per the template in predictions/README.md,
domain knowledge/, newspaper/questions/) — `newspaper_ready` content is ingested directly
by build_newspaper, do NOT duplicate it. IDEMPOTENCY: after triaging a block, append
`<!-- triaged YYYY-MM-DD -->` to its heading line; skip any block already marked. Assign
desk/model/urgency per MODEL_ROUTING_POLICY.
3. Advance active tasks within capacity (CAPACITY_LEDGER policy; record staffing verdicts).
4. Run watches: `python3 tools/run_watches.py due`, research each due watch per its task body, publish per its publish_policy, then `run_watches.py mark <id>`. 5. Score any predictions
whose horizon passed → `outcomes/`. 6. Build + edit + publish the newspaper
(brain-newspaper skill). 7. Process yesterday's annotations if unprocessed. 8. Regenerate
indexes, validate, commit (area-prefixed), push, VERIFY ls-remote. 9. Update
system/SYSTEM_HEALTH.md (failures are news). 10. Notify Brendan with 3-5 headlines.

## Installing skills
- Cloud routines: skills load from each repo's `.claude/skills/` automatically. Sync after
  editing canonical: `tools/sync_skills.sh` (then commit each repo — use oplog, pushes are
  not atomic). Verify: `tools/sync_skills.sh --check`.
- Local machine: `ln -s ~/path/to/brendan_brain/.claude/skills/brain-ops ~/.claude/skills/`
  (repeat per skill) for user-scoped availability.

## Common operations
| Want | Run |
|---|---|
| New task | `python3 tools/new_task.py --title ... --domain ... --request ...` |
| Search memory | `python3 tools/brain_search.py "terms" [--domain d]` |
| Queue dashboard | `python3 tools/build_queue_dashboard.py` then read QUEUE.md |
| New domain | `python3 tools/new_domain.py slug --title ... --reason ...` |
| Newspaper | `python3 tools/build_newspaper.py [--date D]`, edit draft, set verdict, `--publish` |
| Annotations | `python3 tools/process_annotations.py --date D [--apply]` |
| Cross-repo op | `python3 tools/oplog.py start <slug> --repos a,b` → `set` → `status` |
| Full test suite | `tests/run_all.sh` (sandboxed; never touches real repos/remotes) |

## Git rules (summary; full: CLAUDE.md)
Brain: work on `main`, pull-rebase first, never force-push, verify pushes.
Specialist repos: integration surface only (BRAIN_INTEGRATION.md, synced skills, outbox);
prompts/notebooks are the robots' — propose diffs, never edit silently.

## Recovery playbook
- Push failed → retry 2/4/8/16s → still failing: mark op `failed`, report PARTIAL, stop.
- Rebase conflict → per-file-class rules in CLAUDE.md; regenerate generated files.
- QUEUE.md warnings (exit 2) → fix status/folder mismatch (`git mv` or fix frontmatter).
- Duplicate open dedupe_key (validator error) → merge task bodies, keep both histories,
  supersede one id.
- Unfinished op from a dead session → `oplog.py status`, finish or mark failed honestly.
