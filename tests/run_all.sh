#!/usr/bin/env bash
# Brendan OS test suite. Test WRITES happen in sandboxed clones under $SCRATCH; the only
# real-repo artifact is the intentional tests/results/run-*.md record. Never touches real
# remotes/GitHub. NOTE: sandboxes clone committed HEAD — commit your changes before
# trusting a run; uncommitted edits are NOT tested. Usage: tests/run_all.sh [test-name]
set -uo pipefail
BRAIN="$(cd "$(dirname "$0")/.." && pwd)"
SCRATCH="${BRAIN_TEST_SCRATCH:-$(mktemp -d)}"
export BRAIN SCRATCH
PASS=0; FAIL=0; SKIP=0; RESULTS="$BRAIN/tests/results/run-$(date +%Y%m%d-%H%M%S).md"
mkdir -p "$BRAIN/tests/results"
{ echo "# Test run $(date -Iseconds)"
  echo "tested commit: $(git -C "$BRAIN" rev-parse HEAD) (branch: $(git -C "$BRAIN" branch --show-current))"
  git -C "$BRAIN" status --porcelain | grep -q . && echo "⚠️ working tree had uncommitted changes — they were NOT tested (sandboxes clone HEAD)"
} > "$RESULTS"

fresh_sandbox() {  # bare "origin" + working clone, mirrors GitHub topology
  rm -rf "$SCRATCH/origin.git" "$SCRATCH/clone1" "$SCRATCH/clone2"
  git clone -q --bare "$BRAIN" "$SCRATCH/origin.git"
  # sandbox "main" = the CURRENT committed HEAD, whatever branch it's on — otherwise a
  # feature-branch session silently tests stale main (V2 fix, 2026-07-11)
  git -C "$SCRATCH/origin.git" update-ref refs/heads/main "$(git -C "$BRAIN" rev-parse HEAD)"
  git -C "$SCRATCH/origin.git" symbolic-ref HEAD refs/heads/main
  git clone -q -b main "$SCRATCH/origin.git" "$SCRATCH/clone1"
  git clone -q -b main "$SCRATCH/origin.git" "$SCRATCH/clone2"
  for c in clone1 clone2; do
    git -C "$SCRATCH/$c" config user.email test@test && git -C "$SCRATCH/$c" config user.name test
  done
}

run_test() {
  local name="$1"
  if [ $# -gt 1 ] && [ "$2" != "$name" ]; then return; fi
  fresh_sandbox
  if bash "$BRAIN/tests/$name.sh" >"$SCRATCH/$name.log" 2>&1; then
    # a skip is NOT a pass — tests that can't exercise their subject say "SKIP:" loudly
    if grep -q "^SKIP:" "$SCRATCH/$name.log"; then
      echo "SKIP $name ($(grep -m1 '^SKIP:' "$SCRATCH/$name.log" | cut -c6-80))"
      echo "- SKIP $name — $(grep -m1 '^SKIP:' "$SCRATCH/$name.log")" >> "$RESULTS"; SKIP=$((SKIP+1))
      return
    fi
    echo "PASS $name"; echo "- PASS $name" >> "$RESULTS"; PASS=$((PASS+1))
  else
    echo "FAIL $name (log follows)"; sed 's/^/    /' "$SCRATCH/$name.log" | tail -20
    echo "- FAIL $name" >> "$RESULTS"
    sed 's/^/      /' "$SCRATCH/$name.log" >> "$RESULTS"; FAIL=$((FAIL+1))
  fi
}

FILTER="${1:-}"
for t in test_queue_dedup test_concurrent_writes test_partial_failure test_retrieval \
         test_annotations test_newspaper_sensitivity test_forgetting test_skill_sync \
         test_intake_routing test_receipt_pantry test_health_kitchen_bridge \
         test_injection_sanitize test_domain_proposal test_usage_learning \
         test_cowork_handoff test_schedule_gate test_skill_quality \
         test_annotation_regression test_watch_eligibility test_timezone; do
  run_test "$t" $FILTER
done
echo "" >> "$RESULTS"; echo "PASS=$PASS FAIL=$FAIL SKIP=$SKIP" | tee -a "$RESULTS"
[ $FAIL -eq 0 ]
