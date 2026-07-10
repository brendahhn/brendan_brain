#!/usr/bin/env bash
# Scenarios: one repo pushes while another fails; a routine commits but fails to push;
# retry is idempotent; oplog makes partial state visible and recoverable.
set -euo pipefail
C1="$SCRATCH/clone1"
cd "$C1"
OP=$(python3 tools/oplog.py start partial-probe --repos brendan_brain,health-notebook)
# repo 1 (brendan_brain sandbox): succeeds
python3 tools/oplog.py set "$OP" brendan_brain committed >/dev/null
git add -A && git commit -qm "partial probe: brain side" && git push -q origin main
python3 tools/oplog.py set "$OP" brendan_brain verified >/dev/null
# repo 2: simulate push failure via unreachable remote
python3 tools/oplog.py set "$OP" health-notebook committed >/dev/null
git remote add deadend /nonexistent/path.git
if git push -q deadend main 2>/dev/null; then echo "expected failure"; exit 1; fi
python3 tools/oplog.py set "$OP" health-notebook failed >/dev/null
git add -A && git commit -qm "op: record partial failure" && git push -q origin main
# Detection: status must show PARTIAL/FAILED, not success
python3 tools/oplog.py status | grep -q "PARTIAL/FAILED" || { echo "partial state invisible"; exit 1; }
# Recovery: next session retries the failed leg; idempotent oplog start returns same id
OP2=$(python3 tools/oplog.py start partial-probe --repos brendan_brain,health-notebook)
[ "$OP" = "$OP2" ] || { echo "retry minted new op id ($OP2)"; exit 1; }
git remote set-url deadend "$SCRATCH/origin.git"
git push -q deadend main
python3 tools/oplog.py set "$OP" health-notebook verified >/dev/null
python3 tools/oplog.py status | grep -q "0 unfinished" || { echo "op not closed"; exit 1; }
echo OK
