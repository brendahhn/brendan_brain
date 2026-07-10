#!/usr/bin/env bash
# Forgetting workflow on SYNTHETIC data in a sandbox clone: plan finds all copies,
# execution removes them from working tree + generated files, tombstone records the event
# without the content, and honesty about git history is enforced.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
MARK="FORGETME""-CONTENT"   # concatenated so this script never contains the literal marker
mkdir -p timeline/2026/07
cat > timeline/2026/07/2026-07-05-synthetic-forget-me.md <<'EOF'
---
id: tl-20260705-synthetic-forget-me
artifact_type: timeline
created_at: 2026-07-05
domain: health
sensitivity: private
topics: [forgetme-marker]
---
SYNTHETIC-${MARK}: an embarrassing synthetic observation.
EOF
# inject the runtime-built marker (heredoc above is quoted, so do it here) and PROVE the
# fixture contains it before deletion — guards against this assertion going vacuous
sed -i "s/SYNTHETIC-\${MARK}/SYNTHETIC-$MARK/" timeline/2026/07/2026-07-05-synthetic-forget-me.md
grep -q "$MARK" timeline/2026/07/2026-07-05-synthetic-forget-me.md || { echo "fixture missing marker"; exit 1; }
python3 tools/build_index.py >/dev/null
git add -A && git commit -qm "fixture: forgettable" && git push -q origin main
# PLAN: locate every copy (artifact + index)
HITS=$(grep -ril "forgetme" --exclude-dir=.git --exclude-dir=tests . | sort)
echo "$HITS" | grep -q "timeline/2026/07" || { echo "plan missed artifact"; exit 1; }
echo "$HITS" | grep -q "INDEX.tsv" || { echo "plan missed generated index"; exit 1; }
# EXECUTE (simulating Brendan's confirmation)
git rm -q timeline/2026/07/2026-07-05-synthetic-forget-me.md
python3 tools/build_index.py >/dev/null && python3 tools/build_queue_dashboard.py >/dev/null || true
grep -riq "$MARK" --exclude-dir=.git --exclude-dir=tests . && { echo "content survived deletion"; exit 1; }
# tombstone: records THAT, not WHAT
mkdir -p system/operations
cat > system/operations/op-20260710-forget-synthetic.md <<'EOF'
---
id: op-20260710-forget-synthetic
artifact_type: operation
started_at: 2026-07-10T12:00:00
repos:
  brendan_brain: verified
---
# Forget operation
Deleted artifact id tl-20260705-synthetic-forget-me (content not recorded here).
Scope: working tree + generated indexes. REMAINS IN GIT HISTORY — history rewrite was
offered and declined in this synthetic test.
EOF
git add -A && git commit -qm "forget: tl-20260705-synthetic-forget-me" && git push -q origin main
# honesty check: content IS still in history (expected; the workflow must say so)
[ -n "$(git log --all --oneline -- timeline/2026/07/2026-07-05-synthetic-forget-me.md)" ] \
  || { echo "history claim wrong"; exit 1; }
# and it is NOT retrievable by search anymore
python3 tools/brain_search.py "forgetme" --allow-sensitive test 2>/dev/null | grep -q tl-20260705 \
  && { echo "still retrievable"; exit 1; }
echo OK
