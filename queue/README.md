# Queue
One file per task (schema: system/SCHEMAS.md). Folders = lifecycle stages; `status`
frontmatter is authoritative. Create tasks with `python3 tools/new_task.py` (dedupe-aware).
Dashboard: QUEUE.md (generated — `python3 tools/build_queue_dashboard.py`).
`inbox/from-<robot>.md` files are append-only robot outbox drops, converted to tasks/
artifacts by the Chief of Staff during triage.
