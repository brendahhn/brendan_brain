#!/usr/bin/env bash
# V2 scenario 17: skill proposal & creation quality. Every V2 skill satisfies the
# SKILL_FOUNDRY anatomy's mechanical parts; the foundry tracker + graduation criteria exist.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"

for s in brain-intake brain-kitchen cowork-handoff; do
  F=".claude/skills/$s/SKILL.md"
  [ -f "$F" ] || { echo "FAIL: $F missing"; exit 1; }
  grep -q "brendan-os-skill-version:" "$F" || { echo "FAIL: $s version header"; exit 1; }
  grep -q "canonical source: brendan_brain" "$F" || { echo "FAIL: $s canonical pointer"; exit 1; }
  grep -q "^description:" "$F" || { echo "FAIL: $s trigger description"; exit 1; }
  grep -q "$s" skills/SKILL_REGISTRY.md || { echo "FAIL: $s not in registry"; exit 1; }
done
# foundry: graduation criteria + candidate tracker + honest statuses
grep -q "Graduation criteria" skills/SKILL_FOUNDRY.md || { echo "FAIL: criteria missing"; exit 1; }
grep -q "Candidate tracker" skills/SKILL_FOUNDRY.md || { echo "FAIL: tracker missing"; exit 1; }
grep -qi "candidate — " skills/SKILL_FOUNDRY.md || { echo "FAIL: no honest not-yet-shipped rows"; exit 1; }
# every V2 subsystem has a retirement trigger (arch-challenge #16)
for sub in "Intake router" "Kitchen system" "cowork-handoff" "Learning engine" "OCI"; do
  grep -qi "$sub" system/V2_LEDGER.md || { echo "FAIL: $sub not in V2 ledger"; exit 1; }
done
echo OK
