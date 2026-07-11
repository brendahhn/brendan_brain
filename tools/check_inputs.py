#!/usr/bin/env python3
"""Mechanical input gate for the morning editorial run (SCHEDULE_PLAN).
Reports which robot outboxes have a fresh block (today or yesterday) BEFORE the newspaper
is edited. Missing input = news to report ([FAIL] item), never something to fabricate or
silently skip, and never something to block on forever.

Usage: check_inputs.py [--date YYYY-MM-DD] [--require trading-robot[,more]]
Exit 0 normally; exit 1 only if a --require'd input is missing (for tests/gating)."""
import argparse, datetime, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, today

EXPECTED = ["jobs-robot", "footybot", "health-robot", "trading-robot"]  # cowork optional


def input_status(date):
    """[(name, fresh_bool, last_block_date_or_'')] for every from-*.md outbox."""
    yday = (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()
    inbox = os.path.join(ROOT, "queue", "inbox")
    out = []
    names = set(EXPECTED)
    if os.path.isdir(inbox):
        names |= {fn[5:-3] for fn in os.listdir(inbox)
                  if fn.startswith("from-") and fn.endswith(".md")}
    for name in sorted(names):
        p = os.path.join(inbox, f"from-{name}.md")
        dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", open(p, encoding="utf-8").read(),
                           re.M) if os.path.exists(p) else []
        last = max(dates) if dates else ""
        out.append((name, last in (date, yday), last))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=today())
    ap.add_argument("--require", default="")
    a = ap.parse_args()
    required = {r.strip() for r in a.require.split(",") if r.strip()}
    missing_required = False
    for name, fresh, last in input_status(a.date):
        tag = "REQUIRED " if name in required else ""
        if fresh:
            print(f"INPUT {name}: fresh ({last})")
        elif name in EXPECTED or name in required:
            print(f"INPUT {name}: {tag}MISSING (last block: {last or 'never'}) — report as "
                  f"[FAIL] item, do not fabricate, do not block publication")
            if name in required:
                missing_required = True
        else:
            print(f"INPUT {name}: no fresh block (optional inbox — nothing to report)")
    sys.exit(1 if missing_required else 0)


if __name__ == "__main__":
    main()
