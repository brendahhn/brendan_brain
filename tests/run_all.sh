#!/usr/bin/env bash
# Brendan OS test suite. Test WRITES happen in sandboxed clones under $SCRATCH; the only
# real-repo artifact is the intentional tests/results/run-*.md record. Never touches real
# remotes/GitHub. NOTE: sandboxes clone committed HEAD — commit your changes before
# trusting a run; uncommitted edits are NOT tested. Usage: tests/run_all.sh [test-name]
set -uo pipefail
BRAIN="$(cd "$(dirname "$0")/.." && pwd)"
SCRATCH="${BRAIN_TEST_SCRATCH:-$(mktemp -d)}"
export BRAIN SCRATCH
PASS=0; FAIL=0; RESULTS="$BRAIN/tests/results/run-$(date +%Y%m%d-%H%M%S).md"
mkdir -p "$BRAIN/tests/results"
echo "# Test run $(date -Iseconds)" > "$RESULTS"

fresh_sandbox() {  # bare "origin" + working clone, mirrors GitHub topology
  rm -rf "$SCRATCH/origin.git" "$SCRATCH/clone1" "$SCRATCH/clone2"
  git clone -q --bare "$BRAIN" "$SCRATCH/origin.git"
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
    echo "PASS $name"; echo "- PASS $name" >> "$RESULTS"; PASS=$((PASS+1))
  else
    echo "FAIL $name (log follows)"; sed 's/^/    /' "$SCRATCH/$name.log" | tail -20
    echo "- FAIL $name" >> "$RESULTS"
    sed 's/^/      /' "$SCRATCH/$name.log" >> "$RESULTS"; FAIL=$((FAIL+1))
  fi
}

FILTER="${1:-}"
for t in test_queue_dedup test_concurrent_writes test_partial_failure test_retrieval \
         test_annotations test_newspaper_sensitivity test_forgetting test_skill_sync; do
  run_test "$t" $FILTER
done
echo "" >> "$RESULTS"; echo "PASS=$PASS FAIL=$FAIL" | tee -a "$RESULTS"
[ $FAIL -eq 0 ]
