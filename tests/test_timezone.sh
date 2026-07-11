#!/usr/bin/env bash
# V2 time policy (mandate §11): user-facing dates are America/Los_Angeles; editorial-date
# attribution; UTC rollover; DST boundaries; newspaper naming.
set -euo pipefail
C1="$SCRATCH/clone1"; cd "$C1"

python3 - <<'EOF'
import sys, datetime
sys.path.insert(0, "tools")
from brainlib import PACIFIC, editorial_date, today, now_pt
from zoneinfo import ZoneInfo
UTC = ZoneInfo("UTC")

def at(s):  # aware UTC instant
    return datetime.datetime.fromisoformat(s).replace(tzinfo=UTC)

# UTC date rollover: 04:30Z on Jul 12 is 21:30 PT on Jul 11 → PT date differs from UTC date
inst = at("2026-07-12T04:30:00")
assert inst.astimezone(PACIFIC).date().isoformat() == "2026-07-11", "PT conversion wrong"
# ...and 21:30 PT is past the 20:00 editorial cutoff → belongs to the Jul 12 edition
assert editorial_date(inst) == "2026-07-12", f"overnight attribution: {editorial_date(inst)}"

# midnight PT: 00:10 PT belongs to the SAME day's edition
inst = at("2026-07-12T07:10:00")   # 00:10 PT Jul 12
assert editorial_date(inst) == "2026-07-12", "midnight PT attribution"

# late-but-before-cutoff afternoon result stays on its own day
inst = at("2026-07-11T21:00:00")   # 14:00 PT Jul 11
assert editorial_date(inst) == "2026-07-11", "same-day attribution"

# DST: spring forward (2026-03-08 02:00 PST→PDT). 09:59Z = 01:59 PST; 10:01Z = 03:01 PDT.
a = at("2026-03-08T09:59:00").astimezone(PACIFIC)
b = at("2026-03-08T10:01:00").astimezone(PACIFIC)
assert a.utcoffset().total_seconds() == -8*3600, "PST offset"
assert b.utcoffset().total_seconds() == -7*3600, "PDT offset"
assert a.date() == b.date(), "DST jump must not change the calendar date"

# DST: fall back (2026-11-01). 08:30Z = 01:30 PDT; 09:30Z = 01:30 PST — same date either way.
c = at("2026-11-01T08:30:00").astimezone(PACIFIC)
d = at("2026-11-01T09:30:00").astimezone(PACIFIC)
assert c.date() == d.date() == datetime.date(2026, 11, 1), "fall-back date stable"

# market-open framing: 06:30 PT is 13:30Z in PDT — a run at 13:30Z lands on the same PT date
inst = at("2026-07-11T13:30:00")
assert inst.astimezone(PACIFIC).hour == 6, "market-open hour mapping"
assert editorial_date(inst) == "2026-07-11", "market-open edition date"

# today() is PT: consistent with now_pt()
assert today() == now_pt().date().isoformat()
print("timezone assertions OK")
EOF

# newspaper naming: builder default date == PT today (file name check, no publish)
D=$(python3 -c "import sys; sys.path.insert(0,'tools'); from brainlib import today; print(today())")
python3 tools/build_newspaper.py >/dev/null
[ -f "newspaper/drafts/$D.md" ] || { echo "FAIL: draft not named by PT date"; exit 1; }
echo OK
