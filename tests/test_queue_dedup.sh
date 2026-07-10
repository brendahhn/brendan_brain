#!/usr/bin/env bash
# Scenarios: two conversations add the same research idea; a retry duplicates a task;
# QUEUE.md inconsistency detection.
set -euo pipefail
C1="$SCRATCH/clone1"
cd "$C1"
out1=$(python3 tools/new_task.py --title "Dedup probe: kelp farming" --domain news --request "probe A")
echo "first: $out1"
[[ "$out1" == queue/inbox/* ]] || { echo "expected new task"; exit 1; }
out2=$(python3 tools/new_task.py --title "Dedup probe: kelp farming" --domain news --request "probe B from another conversation")
echo "second: $out2"
[[ "$out2" == DUPLICATE* ]] || { echo "expected DUPLICATE"; exit 1; }
grep -q "dedupe 20" "$out1" || { echo "expected +1 interest note appended"; exit 1; }
# idempotent retry with identical dedupe key while task open
out3=$(python3 tools/new_task.py --title "Dedup probe: kelp farming" --domain news --request "probe A retry")
[[ "$out3" == DUPLICATE* ]] || { echo "retry created duplicate!"; exit 1; }
n=$(ls queue/inbox/ | grep -c kelp) ; [ "$n" -eq 1 ] || { echo "expected 1 file, got $n"; exit 1; }
# folder/status mismatch detection: corrupt the status without moving the file
sed -i 's/^status: inbox/status: active/' queue/inbox/task-*kelp*.md
if python3 tools/build_queue_dashboard.py; then echo "expected exit 2 on mismatch"; exit 1; fi
grep -q "Consistency warnings" QUEUE.md || { echo "warning missing from QUEUE.md"; exit 1; }
echo OK
