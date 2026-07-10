#!/usr/bin/env bash
# Scenario: two routines update the Brain simultaneously — different task files AND the
# same append-only inbox file. Second pusher must recover via rebase per
# CROSS_REPOSITORY_POLICY and end with both sides' content present.
set -euo pipefail
C1="$SCRATCH/clone1"; C2="$SCRATCH/clone2"

cd "$C1"
python3 tools/new_task.py --title "Concurrent A" --domain jobs --request "from routine A" >/dev/null
printf '## 2026-07-10 — jobs-robot run summary\n- headline: A\n' >> queue/inbox/from-jobs-robot.md
git add -A && git commit -qm "routine A" && git push -q origin main

cd "$C2"  # stale clone — did not pull
python3 tools/new_task.py --title "Concurrent B" --domain investing --request "from routine B" >/dev/null
printf '## 2026-07-10 — trading-robot run summary\n- headline: B\n' >> queue/inbox/from-trading-robot.md
git add -A && git commit -qm "routine B"
if git push -q origin main 2>/dev/null; then echo "expected push rejection"; exit 1; fi
git pull -q --rebase origin main   # recovery per policy
git push -q origin main

cd "$C1"; git pull -q origin main
[ -f queue/inbox/task-*concurrent-a*.md ] || ls queue/inbox/ | grep -qi concurrent-a || { echo "A task lost"; exit 1; }
ls queue/inbox/ | grep -qi concurrent-b || { echo "B task lost"; exit 1; }
grep -q "headline: A" queue/inbox/from-jobs-robot.md && grep -q "headline: B" queue/inbox/from-trading-robot.md \
  || { echo "inbox content lost"; exit 1; }
python3 tools/validate_frontmatter.py --all >/dev/null || { echo "validation broke"; exit 1; }
echo OK
