#!/usr/bin/env bash
# V2 scenario 4: health guidance → recipe bridge, leak-gated.
# health_alignment labels live in kitchen artifacts; they must NEVER reach the newspaper.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
D=2027-01-15   # collision-proof date

# synthetic sanitized guidance row (generic food level — the only legal content)
cat >> domains/health/FOOD_GUIDANCE.md <<'EOF'
| S1 | SYNTHETIC-TEST: favor synthetic-lentils | tentative | health-repo-ref-001 | 2027-01-14 |
EOF

# a kitchen menu task carrying an alignment label, ready for publication
mkdir -p queue/active
cat > queue/active/task-20270114-synthetic-menu.md <<EOF
---
id: task-20270114-synthetic-menu
title: SYNTHETIC-TEST kitchen menu plan
artifact_type: task
domain: concierge
status: ready_for_publication
created_at: 2027-01-14
urgency: normal
depth: quick
effort_budget: 1_pass
publication_destination: newspaper
recurrence: none
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: concierge/synthetic-menu-test
health_alignment: generally_aligned
health_alignment_reason: uses the synthetic encouraged list
---

## Request

SYNTHETIC-TEST menu request.

## Findings

A synthetic-lentil stew plan with crusty bread. Fun dessert follows the profile rule.
EOF

python3 tools/build_newspaper.py --date $D >/dev/null
DRAFT=newspaper/drafts/$D.md
# the menu item may appear (it asked for publication)...
grep -q "SYNTHETIC-TEST kitchen menu plan" "$DRAFT" || { echo "FAIL: kitchen item missing from draft"; exit 1; }
# ...but alignment labels and reasons must not (KITCHEN_PROFILE bridge rule 3)
grep -qiE "health_alignment|generally_aligned|strongly_aligned|potentially_conflicting" "$DRAFT" \
  && { echo "FAIL: alignment label leaked into newspaper draft"; exit 1; }
grep -qi "encouraged list" "$DRAFT" && { echo "FAIL: alignment reason leaked"; exit 1; }
# guidance file content itself must not be quoted into the paper either
grep -qi "synthetic-lentils" "$DRAFT" && { echo "FAIL: guidance row leaked into draft"; exit 1; }
# and the label survives where it belongs — the kitchen artifact
grep -q "health_alignment: generally_aligned" queue/active/task-20270114-synthetic-menu.md \
  || { echo "FAIL: label lost from kitchen artifact"; exit 1; }
# the bridge source's CONTENT rows must never carry medical markers (the contract prose
# above the table legitimately names the forbidden words — check table rows only)
grep "^|" domains/health/FOOD_GUIDANCE.md | grep -viE "^\| *#|^\|---| guidance .generic" \
  | grep -qiE "\b(diagnos|[0-9]+ ?(mg|mcg)\b|dose|symptom|lab result)" \
  && { echo "FAIL: medical content in FOOD_GUIDANCE rows"; exit 1; }
echo OK
