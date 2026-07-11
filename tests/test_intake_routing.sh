#!/usr/bin/env bash
# V2 scenarios 7/8/9: immediate-answer-only, immediate+overnight, ephemeral tech question.
# Router override phrases map to the right modes; mode-1 leaves the repo byte-identical.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"

r() { python3 tools/route_intake.py --request "$1"; }

# scenario 7: immediate answer only
r "Answer this now: what's the tallest mountain in California?" | grep -q "MODE=1 " || { echo "FAIL: 'answer now' != mode 1"; exit 1; }
# scenario 9: one-off personal tech question → ephemeral, no memory
OUT=$(r "How do I free up iPhone storage? Just a one-off question.")
echo "$OUT" | grep -q "MODE=1 .*CAPTURE=n" || { echo "FAIL: one-off tech question should be ephemeral"; exit 1; }
# scenario 8: immediate + overnight expansion
r "Give me the quick answer and research it overnight" | grep -q "MODE=3 .*TASK=task.*EXPAND=y" || { echo "FAIL: overnight expansion"; exit 1; }
# paper request routes publication
r "Research pot pie methods overnight and put this in tomorrow's paper" | grep -q -- "--publish newspaper" || { echo "FAIL: paper override"; exit 1; }
# watch
r "Make this a watch: Tacoma listings under 12k" | grep -q "MODE=6 .*TASK=watch" || { echo "FAIL: watch"; exit 1; }
# same-day deadline
r "I need a shopping list before dinner" | grep -q "MODE=4 " || { echo "FAIL: before dinner != same-day"; exit 1; }
# remember→memory; don't-save wins over everything
r "Remember this: I love strawberry desserts" | grep -q "MODE=2 .*CAPTURE=y" || { echo "FAIL: remember"; exit 1; }
r "Don't save this, but what do you think of my resume?" | grep -q "CAPTURE=n" || { echo "FAIL: don't-save override"; exit 1; }

# ephemeral guarantee: routing itself writes NOTHING (repo stays clean)
[ -z "$(git status --porcelain)" ] || { echo "FAIL: router dirtied the repo"; git status --porcelain; exit 1; }
echo OK
