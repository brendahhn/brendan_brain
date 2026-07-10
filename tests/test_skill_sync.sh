#!/usr/bin/env bash
# Scenarios: skill drift detection (a repo's copy diverges from canonical); version
# mismatch visibility. Runs against the REAL sibling repos read-only + a temp copy for the
# divergence check.
set -euo pipefail
cd "$BRAIN"
# all synced copies currently match canonical
./tools/sync_skills.sh --check | grep -q DIVERGED && { echo "unexpected divergence"; exit 1; }
# simulate divergence in a temp copy of one repo
TMP="$SCRATCH/skilldrift"; rm -rf "$TMP"; mkdir -p "$TMP"
cp -r ../health-notebook/.claude "$TMP/"
echo "rogue edit" >> "$TMP/.claude/skills/brain-sync/SKILL.md"
if diff -q .claude/skills/brain-sync/SKILL.md "$TMP/.claude/skills/brain-sync/SKILL.md" >/dev/null; then
  echo "diff should detect drift"; exit 1; fi
# canonical header present in canonical + synced copies (points editors home)
grep -q "canonical source: brendan_brain" .claude/skills/brain-sync/SKILL.md
grep -q "canonical source: brendan_brain" ../health-notebook/.claude/skills/brain-sync/SKILL.md
# interface version is declared in registry and skill headers agree
V=$(grep -o "interface version [0-9.]*" skills/SKILL_REGISTRY.md | head -1 | awk '{print $3}')
grep -q "brendan-os-skill-version: $V" .claude/skills/brain-sync/SKILL.md \
  || { echo "version mismatch registry=$V vs skill header"; exit 1; }
echo OK
