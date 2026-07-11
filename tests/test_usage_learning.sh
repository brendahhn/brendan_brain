#!/usr/bin/env bash
# V2 scenarios 16/18/19: model usage logging (no fabricated tokens), learning from
# repeated reactions (threshold candidates), interest change detected WITHOUT silently
# rewriting the profile. Plus the material-change gate stub path.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"

# --- usage logging (scenario 16)
python3 tools/log_usage.py --task synthetic-task --model sonnet --type research \
  --start 06:00 --end 06:20 --verdict "single lead sufficient" >/dev/null
grep -q "| synthetic-task | sonnet |" system/CAPACITY_LEDGER.md || { echo "FAIL: usage row missing"; exit 1; }
grep -qi "token" system/CAPACITY_LEDGER.md | grep -v "no token" && true
grep -qE "\| *[0-9]+ tokens" system/CAPACITY_LEDGER.md && { echo "FAIL: fabricated token numbers"; exit 1; }
python3 tools/log_usage.py --task synthetic-task-2 --model haiku --type extraction >/dev/null
[ "$(grep -c "^| 2" system/CAPACITY_LEDGER.md)" -ge 2 ] || { echo "FAIL: second row"; exit 1; }
# usefulness defaults to pending — never self-graded
grep "synthetic-task " system/CAPACITY_LEDGER.md | grep -q "pending" || { echo "FAIL: usefulness not pending"; exit 1; }

# --- learning gate: idle → stub (high threshold)
python3 tools/learning_report.py --week 2027-W03 --min-signals 999 >/dev/null
grep -q "nothing material" system/reviews/2027-W03-review.md || { echo "FAIL: gate stub missing"; exit 1; }

# --- repeated reactions → threshold candidate; mixed reactions → interest-change proposal
PROFILE_BEFORE=$(sha256sum preferences/INTEREST_PROFILE.md)
TODAY=$(date +%Y-%m-%d)
Y1=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)
cat >> preferences/PROPOSED_RULES.md <<EOF
- $TODAY | important | synthtopic-kelp | edition-test | body
- $Y1 | important | synthtopic-kelp | edition-test | body
- $TODAY | important | synthtopic-kelp | edition-test | body
- $TODAY | important | synthtopic-tacoma | edition-test | body
- $Y1 | not_useful | synthtopic-tacoma | edition-test | body
- $TODAY | not_useful | synthtopic-tacoma | edition-test | body
EOF
python3 tools/learning_report.py --week 2027-W04 --min-signals 5 >/dev/null
R=system/reviews/2027-W04-review.md
grep -q "synthtopic-kelp.*3 consistent signals" "$R" || { echo "FAIL: repeated-reaction candidate missed"; exit 1; }
grep -qi "synthtopic-tacoma.*interest" "$R" || { echo "FAIL: interest change not flagged"; exit 1; }
grep -qi "do NOT rewrite INTEREST_PROFILE silently" "$R" || { echo "FAIL: no-silent-rewrite instruction missing"; exit 1; }
# the profile itself was NOT touched (scenario 19's hard requirement)
[ "$PROFILE_BEFORE" = "$(sha256sum preferences/INTEREST_PROFILE.md)" ] || { echo "FAIL: profile silently rewritten"; exit 1; }
# reports are proposal-only: no CONFIRMED_RULES change either
git diff --name-only | grep -q "CONFIRMED_RULES" && { echo "FAIL: report touched confirmed rules"; exit 1; }
echo OK
