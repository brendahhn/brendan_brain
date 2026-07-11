#!/usr/bin/env bash
# Production bug B regression (2026-07-11): cancelled/completed/failed/archived/expired/
# synthetic watches must appear in NEITHER the watch runner NOR the newspaper; the two use
# one shared eligibility function. Missing next_run ≠ automatically due.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
D=2027-05-01

mkw() {  # id status folder [extra-frontmatter-line]
mkdir -p "queue/$3"
cat > "queue/$3/$1.md" <<EOF
---
id: $1
title: ${4:-Real watch on $1}
artifact_type: watch
domain: general
status: $2
created_at: 2027-04-20
urgency: normal
depth: quick
effort_budget: 1_pass
publication_destination: none
recurrence: watch
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: general/$1
next_run: 2026-01-05
last_run: 2026-01-01
publish_policy: on_change
---

## Request

Watch fixture for eligibility test.
EOF
}

mkw watch-20270420-live-alpha watching watches
mkw watch-20270420-cancelled cancelled failed
mkw watch-20270420-failed failed failed
mkw watch-20270420-done completed completed
mkw watch-20270420-synth watching watches "SYNTHETIC-TEST watch that must never surface"

# archived/expired statuses aren't folder-mapped; place under active for the filter check
mkdir -p queue/active
sed 's/status: watching/status: archived/; s/watch-20270420-live-alpha/watch-20270420-arch/g' \
  queue/watches/watch-20270420-live-alpha.md > queue/active/watch-20270420-arch.md || true

# runner: only the live real watch is due
OUT=$(python3 tools/run_watches.py due)
echo "$OUT" | grep -q "watch-20270420-live-alpha" || { echo "FAIL: live watch not due"; exit 1; }
for bad in cancelled failed done synth arch; do
  echo "$OUT" | grep -q "watch-20270420-$bad" && { echo "FAIL: runner included $bad watch"; exit 1; }
done

# newspaper: system panel lists ONLY the live real watch (plus V1 tacoma watch)
python3 tools/build_newspaper.py --date $D >/dev/null
DRAFT=newspaper/drafts/$D.md
grep -q "watch-20270420-live-alpha" "$DRAFT" || { echo "FAIL: live watch missing from paper"; exit 1; }
for bad in cancelled failed done synth arch; do
  grep -q "watch-20270420-$bad" "$DRAFT" && { echo "FAIL: $bad watch leaked into newspaper"; exit 1; }
done
grep -qi "SYNTHETIC-TEST watch" "$DRAFT" && { echo "FAIL: synthetic watch title leaked"; exit 1; }

# missing next_run: due only when never run; malformed (has last_run, empty next_run) is NOT due
sed -i 's/^next_run: .*/next_run: /' queue/watches/watch-20270420-live-alpha.md
OUT=$(python3 tools/run_watches.py due)
echo "$OUT" | grep -q "watch-20270420-live-alpha" && { echo "FAIL: malformed empty next_run treated as due"; exit 1; }
sed -i 's/^last_run: .*/last_run: /' queue/watches/watch-20270420-live-alpha.md
python3 tools/run_watches.py due | grep -q "watch-20270420-live-alpha" || { echo "FAIL: never-run watch should be due"; exit 1; }
echo OK
