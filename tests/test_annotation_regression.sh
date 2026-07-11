#!/usr/bin/env bash
# Production bug A regression (2026-07-11): article prose and tutorial examples must never
# parse as annotations; processed annotations must never reapply; genuine post-publication
# annotations process exactly once.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
D=2027-04-01

# a PUBLISHED edition whose PROSE contains every trap: a star, the word WATCH, keyword
# tutorial examples — all part of the committed baseline
mkdir -p newspaper/editions
cat > newspaper/editions/$D.md <<'EOF'
---
id: edition-20270401
artifact_type: edition
created_at: 2027-04-01
status: published
publisher_verdict: approved
---
# Test edition

## News  (budget ~400w)

### Synthetic article about annotation tutorials
This article explains reactions: a ⭐ means important. Writing WATCH on a line creates
a watch. You could write REMEMBER THIS: something worth keeping.
DEEPER
WATCH
⭐ this is a prose example, not a reaction

### Synthetic article about tide charts
Plain body text with no annotations at all.
EOF
git add newspaper/editions/$D.md && git commit -qm "publish test edition"

# 1+2: prose star / prose WATCH / tutorial keywords → ZERO annotations
OUT=$(python3 tools/process_annotations.py --date $D)
echo "$OUT" | grep -q "no annotations found" || { echo "FAIL: prose parsed as annotations:"; echo "$OUT"; exit 1; }
EV_BEFORE=$(sha256sum preferences/PROPOSED_RULES.md)
python3 tools/process_annotations.py --date $D --apply >/dev/null
[ "$EV_BEFORE" = "$(sha256sum preferences/PROPOSED_RULES.md)" ] || { echo "FAIL: prose created preference evidence"; exit 1; }
ls queue/watches/ 2>/dev/null | grep -qi "annotation-tutorials\|tide" && { echo "FAIL: prose WATCH created a watch"; exit 1; }

# 3: genuine post-publication annotations (added AFTER the commit) process once
cat >> newspaper/editions/$D.md <<'EOF'
⭐
>> research the tide chart methodology deeper
EOF
python3 tools/process_annotations.py --date $D | grep -q "evidence" || { echo "FAIL: genuine annotation not detected"; exit 1; }
python3 tools/process_annotations.py --date $D --apply >/dev/null
grep -q "tide charts" preferences/PROPOSED_RULES.md || { echo "FAIL: genuine evidence not recorded"; exit 1; }
N1=$(grep -c "edition-$D" preferences/PROPOSED_RULES.md || true)

# 4: re-running --apply is a guarded no-op — zero duplicate actions
OUT2=$(python3 tools/process_annotations.py --date $D --apply)
echo "$OUT2" | grep -q "ALREADY PROCESSED" || { echo "FAIL: rerun not guarded"; exit 1; }
N2=$(grep -c "edition-$D" preferences/PROPOSED_RULES.md || true)
[ "$N1" = "$N2" ] || { echo "FAIL: rerun duplicated evidence ($N1 -> $N2)"; exit 1; }
echo OK
