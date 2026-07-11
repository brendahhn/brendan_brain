#!/usr/bin/env bash
# V2 scenario 10: dynamic cooking-adjacent domain proposal on accumulation;
# a single casual question proposes nothing.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"

mk() {  # id topic
cat > "queue/inbox/$1.md" <<EOF
---
id: $1
title: SYNTHETIC $1
artifact_type: task
domain: general
status: inbox
created_at: 2027-01-10
urgency: normal
depth: quick
effort_budget: 1_pass
publication_destination: none
recurrence: none
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: general/$1
topics: [$2]
---

## Request

SYNTHETIC accumulation fixture.

## Research Log
EOF
}

# one casual question → NO proposal
mk task-20270110-fermentation-a fermentation
python3 tools/propose_domains.py --dry-run | grep -q "fermentation" && { echo "FAIL: one question proposed a domain"; exit 1; }
# three artifacts on the topic → proposal drafted with required sections
mk task-20270110-fermentation-b fermentation
mk task-20270110-fermentation-c fermentation
python3 tools/propose_domains.py | grep -q "PROPOSED.*fermentation" || { echo "FAIL: 3 artifacts didn't propose"; exit 1; }
P=$(ls system/proposals/domain-proposal-*fermentation.md)
for want in "Proposed name" "Why it deserves a domain" "Initial structure" \
            "Needs a routine" "Needs a skill" "Needs an agent" "maintenance cost" \
            "Provisional or permanent"; do
  grep -qi "$want" "$P" || { echo "FAIL: proposal missing '$want'"; exit 1; }
done
# no domain folder was created — proposals never self-execute
[ -d domains/fermentation ] && { echo "FAIL: proposal self-executed a domain"; exit 1; }
# idempotent: second run skips
python3 tools/propose_domains.py | grep -q "SKIP fermentation" || { echo "FAIL: re-run not idempotent"; exit 1; }
echo OK
