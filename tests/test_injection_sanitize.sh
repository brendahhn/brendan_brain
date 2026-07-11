#!/usr/bin/env bash
# V2 scenarios 12/13/14 (+15 partial): browser prompt injection, Gmail-style injection,
# PII scrub (Shopify-without-PII enforcement path), provenance/access-date fencing.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"
OUT="$SCRATCH/sanitized_page.txt"

# hostile webpage: exit 2, imperatives neutralized, legit content kept, PII scrubbed
set +e
python3 tools/sanitize_external.py --in tests/fixtures/injection/hostile_recipe_page.txt \
  --source "https://example-blog.test/potpie" > "$OUT" 2>"$SCRATCH/flags.txt"
RC=$?
set -e
[ "$RC" = "2" ] || { echo "FAIL: hostile page should exit 2 (got $RC)"; exit 1; }
grep -qi "curl -s https://evil" "$OUT" && { echo "FAIL: live command survived"; exit 1; }
grep -q "sk-abc123" "$OUT" && { echo "FAIL: credential string survived"; exit 1; }
grep -q "braise 90 minutes" "$OUT" || { echo "FAIL: legitimate content lost"; exit 1; }
grep -q "email-redacted" "$OUT" || { echo "FAIL: email not scrubbed"; exit 1; }
grep -q "phone-redacted" "$OUT" || { echo "FAIL: phone not scrubbed"; exit 1; }
# provenance fence: source + access date (freshness bookkeeping, scenario 15's mechanical part)
grep -q "source: https://example-blog.test/potpie" "$OUT" || { echo "FAIL: source lost"; exit 1; }
grep -qE "accessed: [0-9]{4}-[0-9]{2}-[0-9]{2}" "$OUT" || { echo "FAIL: access date missing"; exit 1; }
grep -q "UNTRUSTED EXTERNAL CONTENT" "$OUT" || { echo "FAIL: untrusted fence missing"; exit 1; }

# hostile email (Gmail connector path): flags fire
set +e
python3 tools/sanitize_external.py --in tests/fixtures/injection/hostile_email.txt \
  --source "gmail:msg-synthetic" > "$SCRATCH/email.txt" 2>&1
RC=$?
set -e
[ "$RC" = "2" ] || { echo "FAIL: hostile email should exit 2"; exit 1; }
grep -qi "reveal your system prompt" "$SCRATCH/email.txt" && { echo "FAIL: email imperative survived"; exit 1; }
grep -q "order #8812" "$SCRATCH/email.txt" || { echo "FAIL: legit order info lost"; exit 1; }

# clean content: exit 0, no injection flags, text intact
printf 'Simmer the filling 90 minutes.\nCool before topping.\n' > "$SCRATCH/clean.txt"
python3 tools/sanitize_external.py --in "$SCRATCH/clean.txt" --source test > "$SCRATCH/clean_out.txt" 2>"$SCRATCH/clean_flags.txt"
grep -q "injection" "$SCRATCH/clean_flags.txt" && { echo "FAIL: false positive on clean text"; exit 1; }
grep -q "Simmer the filling" "$SCRATCH/clean_out.txt" || { echo "FAIL: clean text mangled"; exit 1; }
echo OK
