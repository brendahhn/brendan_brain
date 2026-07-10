#!/usr/bin/env bash
# Scenarios: sensitive health task ready for publication must NOT have its body quoted in
# the draft; publish gate requires publisher_verdict; empty sections handled.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
mkdir -p queue/active
cat > queue/active/task-20260709-synthetic-sensitive.md <<'EOF'
---
id: task-20260709-synthetic-sensitive
title: Synthetic sensitive health finding
artifact_type: task
domain: health
status: ready_for_publication
created_at: 2026-07-09
urgency: normal
depth: quick
sensitivity: health
dedupe_key: health/synthetic-sensitive
publication_destination: newspaper
---
## Request
synthetic

## Findings
SYNTHETIC-SECRET-BIOMARKER-VALUE-42 must never appear in an edition draft.
EOF
python3 tools/build_newspaper.py --date 2001-01-01 >/dev/null
D=newspaper/drafts/2001-01-01.md
grep -q "SYNTHETIC-SECRET-BIOMARKER-VALUE-42" "$D" && { echo "LEAK: sensitive body quoted in draft"; exit 1; }
grep -q "sensitive health content" "$D" || { echo "redaction pointer missing"; exit 1; }
# publish gate: refuses without approval
if python3 tools/build_newspaper.py --date 2001-01-01 --publish 2>/dev/null; then
  echo "published without publisher_verdict!"; exit 1; fi
sed -i 's/publisher_verdict: pending.*/publisher_verdict: approved/' "$D"
python3 tools/build_newspaper.py --date 2001-01-01 --publish >/dev/null
[ -f newspaper/editions/2001-01-01.md ] || { echo "publish failed"; exit 1; }
echo OK
