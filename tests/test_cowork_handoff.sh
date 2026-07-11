#!/usr/bin/env bash
# V2 scenario 11: Cowork → Brain handoff block lands in the shared inbox, carries every
# required sub-field, is optional for the input gate, and flows into the newspaper draft.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
TODAY=$(date +%Y-%m-%d)

cat >> queue/inbox/from-cowork.md <<EOF

## $TODAY — cowork session summary: synthetic menu deck
- headline: SYNTHETIC — built a dinner-party planning deck
- newspaper_ready: nothing meaningful
- questions_for_brendan: none
- proposed_durable_knowledge: SYNTHETIC fact — Brendan's preferred deck format is one idea per slide (confidence: low; durable: repeated across 2 decks)
- decisions: none
- preferences_observed: - $TODAY | comment | deck format | cowork-session | one idea per slide
- queue_candidates: none
- timeline_events: none
- files_worth_preserving: ~/Decks/dinner-party-v2.key — final deck (reference only)
- proposed_domain_or_skill_updates: none
- sensitive_items: none
- run_status: complete
EOF

# block format: all required sub-fields present exactly once
for f in headline newspaper_ready questions_for_brendan proposed_durable_knowledge \
         decisions preferences_observed queue_candidates timeline_events \
         files_worth_preserving proposed_domain_or_skill_updates sensitive_items run_status; do
  grep -q "^- $f:" queue/inbox/from-cowork.md || { echo "FAIL: missing sub-field $f"; exit 1; }
done
# input gate treats cowork as OPTIONAL (no [FAIL] pressure)
python3 tools/check_inputs.py --date 2027-06-01 | grep "cowork" | grep -q "optional" || { echo "FAIL: cowork not optional in gate"; exit 1; }
# the daily-run pipeline sees the block (build_newspaper collects dated inbox blocks)
python3 tools/build_newspaper.py --date "$TODAY" >/dev/null
grep -q "cowork" "newspaper/drafts/$TODAY.md" || { echo "FAIL: handoff block not collected"; exit 1; }
# no competing memory: the handoff created no artifacts outside the inbox
git status --porcelain | grep -v "queue/inbox/from-cowork.md" | grep -v "newspaper/drafts" \
  | grep -q . && { echo "FAIL: handoff wrote outside the inbox"; exit 1; }
echo OK
