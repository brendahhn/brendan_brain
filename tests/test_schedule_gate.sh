#!/usr/bin/env bash
# V2 scenario 20: trading runs before the Brain editorial run — mechanically enforced as
# an input gate: missing trading output becomes a [FAIL] item in Investing; a fresh block
# clears it; publication is never blocked.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
D=2027-03-02   # collision-proof future date; committed inbox blocks are stale by then

# stale inbox → trading gate fails when required, and the draft reports [FAIL]
set +e
python3 tools/check_inputs.py --date $D --require trading-robot >/dev/null
RC=$?
set -e
[ "$RC" = "1" ] || { echo "FAIL: --require trading should exit 1 on stale inbox"; exit 1; }
python3 tools/build_newspaper.py --date $D >/dev/null
grep -q "\[FAIL\] trading-robot" "newspaper/drafts/$D.md" || { echo "FAIL: no [FAIL] item for missing trading"; exit 1; }
# publication is not blocked: the draft exists and is editable
[ -f "newspaper/drafts/$D.md" ] || { echo "FAIL: draft not produced"; exit 1; }
rm "newspaper/drafts/$D.md"

# fresh trading block (as if the 06:30 run completed) → gate clears, no FAIL item
cat >> queue/inbox/from-trading-robot.md <<EOF

## $D — trading robot run summary
- headline: SYNTHETIC opening analysis complete
- newspaper_ready: SYNTHETIC market note (tier B)
- questions_for_brendan: none
- proposed_durable_knowledge: none
- predictions: none
- run_status: success
EOF
python3 tools/check_inputs.py --date $D --require trading-robot >/dev/null || { echo "FAIL: fresh block should pass gate"; exit 1; }
python3 tools/build_newspaper.py --date $D >/dev/null
grep -q "\[FAIL\] trading-robot" "newspaper/drafts/$D.md" && { echo "FAIL: FAIL item despite fresh block"; exit 1; }
grep -q "SYNTHETIC opening analysis" "newspaper/drafts/$D.md" || { echo "FAIL: trading content not collected"; exit 1; }
echo OK
