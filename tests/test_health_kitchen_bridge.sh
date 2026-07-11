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

A hearty stew plan with crusty bread — brown 2 lb chuck, braise, rest overnight.
Fun dessert follows the profile rule.
EOF

# SEPARATE leak vector (Chief Skeptic C1): medical inference in the Findings PROSE of a
# personal-tagged concierge task — NOT in frontmatter, which build_newspaper never copies.
cat > queue/active/task-20270114-leak-probe.md <<EOF
---
id: task-20270114-leak-probe
title: SYNTHETIC-TEST leak probe menu
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
dedupe_key: concierge/leak-probe-test
---

## Findings

Low-saturated-fat pot pie chosen because Brendan's recent lipid panel showed LDL at
165 mg/dL and his cardiologist advised cutting saturated fat.
EOF

python3 tools/build_newspaper.py --date $D >/dev/null
DRAFT=newspaper/drafts/$D.md
# the menu item may appear (it asked for publication)...
grep -q "SYNTHETIC-TEST kitchen menu plan" "$DRAFT" || { echo "FAIL: kitchen item missing from draft"; exit 1; }
# ...WITH its grocery-weight prose intact — food weights are not medical values
# (merge-gate D1 regression: '2 lb' must not trigger the health scrub)
grep -q "brown 2 lb chuck" "$DRAFT" || { echo "FAIL: grocery weight over-redacted (D1)"; exit 1; }
# ...but alignment labels and reasons must not (KITCHEN_PROFILE bridge rule 3), whether in
# frontmatter OR copied from the Findings prose
grep -qiE "health_alignment|generally_aligned|strongly_aligned|potentially_conflicting" "$DRAFT" \
  && { echo "FAIL: alignment label leaked into newspaper draft"; exit 1; }
grep -qi "encouraged list" "$DRAFT" && { echo "FAIL: alignment reason leaked from prose"; exit 1; }
# guidance file content itself must not be quoted into the paper either
grep -qi "synthetic-lentils" "$DRAFT" && { echo "FAIL: guidance row leaked into draft"; exit 1; }
# the C1 leak probe: NONE of its medical prose may reach the draft; a redaction notice must
grep -qiE "lipid panel|ldl|165 mg/dl|cardiologist|saturated fat" "$DRAFT" \
  && { echo "FAIL: medical prose leaked into newspaper draft (C1)"; exit 1; }
grep -q "HEALTH-LEAK REDACTION" "$DRAFT" || { echo "FAIL: leak probe not redacted with a notice"; exit 1; }
# and the label survives where it belongs — the kitchen artifact
grep -q "health_alignment: generally_aligned" queue/active/task-20270114-synthetic-menu.md \
  || { echo "FAIL: label lost from kitchen artifact"; exit 1; }
# the bridge source's CONTENT rows must never carry medical markers (the contract prose
# above the table legitimately names the forbidden words — check table rows only)
grep "^|" domains/health/FOOD_GUIDANCE.md | grep -viE "^\| *#|^\|---| guidance .generic" \
  | grep -qiE "\b(diagnos|[0-9]+ ?(mg|mcg)\b|dose|symptom|lab result)" \
  && { echo "FAIL: medical content in FOOD_GUIDANCE rows"; exit 1; }
echo OK
