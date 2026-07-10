#!/usr/bin/env bash
# RETRIEVAL_POLICY required behaviors, using SYNTHETIC fixtures only.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
mkdir -p timeline/2026/06 domains/vehicles/knowledge domains/health
# synthetic sensitive timeline observation (health)
cat > timeline/2026/06/2026-06-15-synthetic-itch.md <<'EOF'
---
id: tl-20260615-synthetic-itch
artifact_type: timeline
created_at: 2026-06-15
domain: health
sensitivity: health
entities: [skin, forearm]
topics: [itching, synthetic-fixture]
---
SYNTHETIC: Brendan mentioned itching on his forearm. No cause known. Not a diagnosis.
EOF
# vehicle preference knowledge
cat > domains/vehicles/knowledge/kn-20260701-tacoma-prefs.md <<'EOF'
---
id: kn-20260701-tacoma-prefs
artifact_type: knowledge
created_at: 2026-07-01
domain: vehicles
confidence: high
derived_from: [synthetic]
topics: [tacoma, extra-cab, 2.4l, manual, mileage]
entities: [toyota-tacoma]
---
SYNTHETIC: Prefers 2002-2004 Tacoma, 2.4L 4-cyl, extra cab, <150k miles, San Diego area.
EOF
python3 tools/build_index.py >/dev/null

# 1. later symptom retrieves earlier related observation (health-scoped)
python3 tools/brain_search.py "itching forearm" --domain health | grep -q tl-20260615 \
  || { echo "FAIL: health-scoped recall missed timeline event"; exit 1; }
# 2. vehicle query retrieves prior prefs
python3 tools/brain_search.py "tacoma extra cab engine" | grep -q kn-20260701-tacoma-prefs \
  || { echo "FAIL: vehicle prefs not retrieved"; exit 1; }
# 3. unrelated query does NOT retrieve sensitive health artifact
if python3 tools/brain_search.py "itching skin" 2>/dev/null | grep -q tl-20260615; then
  echo "FAIL: sensitive artifact leaked without domain scope"; exit 1; fi
# ...but the withholding is announced on stderr so the caller knows something exists
python3 tools/brain_search.py "itching skin" 2>&1 >/dev/null | grep -q "withheld" \
  || { echo "FAIL: no withheld notice"; exit 1; }
# 4. explicit override with reason works and is logged to stderr
python3 tools/brain_search.py "itching" --allow-sensitive "health task t-123" 2>/dev/null \
  | grep -q tl-20260615 || { echo "FAIL: justified override failed"; exit 1; }
# 5. fantasy query finds league facts (real, non-sensitive domain profile)
python3 tools/brain_search.py "yahoo half-ppr league draft" | grep -q domain-fantasy_football \
  || { echo "FAIL: fantasy facts not retrieved"; exit 1; }
echo OK
