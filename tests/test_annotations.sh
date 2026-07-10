#!/usr/bin/env bash
# Scenarios: annotations create followups/evidence; one reaction does NOT become a rule;
# explicit "stop covering" works; correction spawns high-urgency task; ambiguous ❌ stays evidence.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
D=2026-07-09
mkdir -p newspaper/editions
cat > newspaper/editions/$D.md <<'EOF'
---
id: edition-20260709
artifact_type: edition
created_at: 2026-07-09
status: published
publisher_verdict: approved
---
# Test edition

## News  (budget ~400w)

### Synthetic story about kelp farming
Body text. ⭐
>> research this deeper

### Synthetic story about pickleball
Body. ❌

### Synthetic claim about ferry schedules
Body.
>> wrong — the ferry stopped running in 2024

### Synthetic story about tide pools
>> stop covering this
EOF
python3 tools/process_annotations.py --date $D | grep -q "PLAN" || { echo "plan mode failed"; exit 1; }
python3 tools/process_annotations.py --date $D --apply >/dev/null
# evidence recorded
grep -q "kelp" preferences/PROPOSED_RULES.md || { echo "evidence missing"; exit 1; }
# one ❌ did NOT create a confirmed rule or rejected topic
grep -qi "pickleball" preferences/CONFIRMED_RULES.md && { echo "reaction became rule!"; exit 1; }
grep -qi "pickleball" preferences/INTEREST_PROFILE.md && { echo "single X rejected topic!"; exit 1; }
# deep-research follow-up task created
ls queue/inbox/ | grep -qi "deeper-research" || { echo "no follow-up task"; exit 1; }
# correction task created with high urgency
grep -rl "urgency: high" queue/inbox/ | xargs grep -li "correction" >/dev/null || { echo "no correction task"; exit 1; }
# explicit stop covering → rejected topic recorded
grep -qi "tide pools" preferences/INTEREST_PROFILE.md || { echo "stop-covering not recorded"; exit 1; }
# annotation artifact exists and validates
ls newspaper/annotations/ann-$D.md >/dev/null
python3 tools/validate_frontmatter.py --all >/dev/null
echo OK

# regression (arch review #5): the edition footer legend must not create phantom evidence
grep -c "| edition-$D |" preferences/PROPOSED_RULES.md > /tmp/evcount || true
python3 - <<'PY'
import re
ev = open('preferences/PROPOSED_RULES.md').read()
# exactly the annotations we made: kelp star, kelp comment? (>> deeper is a task not evidence),
# pickleball X, ferry correction, tidepools stop = evidence lines expected: kelp(⭐), pickleball(❌), ferry(correction), tidepools(stop) = 4
n = len(re.findall(r'^- 2026-07-09 \|', ev, re.M))
assert n == 4, f"expected 4 evidence lines, got {n} (legend phantom or missing)"
PY
echo OK-legend
