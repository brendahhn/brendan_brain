#!/usr/bin/env bash
# V2 scenario 3: receipt → pantry extraction. Parsing, noise exclusion, idempotency,
# schema validity, and removal.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"

python3 tools/receipt_to_pantry.py --paste-file tests/fixtures/synthetic_receipt.txt \
  --receipt --source "vons 2026-07-10" >/dev/null
N=$(python3 tools/receipt_to_pantry.py --list | tail -1)
[ "$N" = "7 items" ] || { echo "FAIL: expected 7 items, got: $N"; exit 1; }
# store header and totals never become items
python3 tools/receipt_to_pantry.py --list | grep -qi "vons store" && { echo "FAIL: store header leaked"; exit 1; }
python3 tools/receipt_to_pantry.py --list | grep -qi "subtotal" && { echo "FAIL: totals leaked"; exit 1; }
# quantities and units parsed
python3 tools/receipt_to_pantry.py --list | grep -q "chuck roast | 2 | lb" || { echo "FAIL: qty/unit parse"; exit 1; }
# perishables get a best-effort expiry
python3 tools/receipt_to_pantry.py --list | grep "strawberries" | grep -qE "2026-[0-9]{2}-[0-9]{2}" || { echo "FAIL: no expiry guess for strawberries"; exit 1; }
# idempotent re-ingest of the same source
python3 tools/receipt_to_pantry.py --paste-file tests/fixtures/synthetic_receipt.txt \
  --receipt --source "vons 2026-07-10" >/dev/null
N2=$(python3 tools/receipt_to_pantry.py --list | tail -1)
[ "$N2" = "7 items" ] || { echo "FAIL: re-ingest duplicated rows: $N2"; exit 1; }
# live_state file still validates
python3 tools/validate_frontmatter.py domains/concierge/kitchen/PANTRY.md >/dev/null || { echo "FAIL: pantry invalid"; exit 1; }
# removal (used up while cooking)
python3 tools/receipt_to_pantry.py --remove "chuck roast" >/dev/null
python3 tools/receipt_to_pantry.py --list | grep -q "chuck roast" && { echo "FAIL: remove didn't"; exit 1; }
echo OK
