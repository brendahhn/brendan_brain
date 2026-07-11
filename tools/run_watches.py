#!/usr/bin/env python3
"""Watch scheduler mechanics (QA finding #2 — watches previously could never fire).
Usage:
  run_watches.py due                 -> list watches due now (the session then researches them)
  run_watches.py mark <watch-id>     -> set last_run=today, next_run=today+interval
Intervals from `recurrence`: daily=1d, weekly=7d, watch=7d (default weekly).
A watch with no next_run is treated as DUE (never run yet)."""
import datetime, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, iter_artifacts, today, die, is_active_watch, watch_is_due, now_pt

INTERVALS = {"daily": 1, "weekly": 7, "watch": 7}


def watches(include_ineligible=False):
    # shared eligibility with the newspaper builder (brainlib.is_active_watch — bug B fix)
    for rel, fm, body in iter_artifacts():
        if is_active_watch(fm, rel) or \
                (include_ineligible and fm.get("artifact_type") == "watch"):
            yield rel, fm


def due():
    t, n = today(), 0
    for rel, fm in watches():
        if watch_is_due(fm, t):
            n += 1
            nr = str(fm.get("next_run", ""))
            print(f"DUE  {fm.get('id'):<50} {rel}  (next_run={nr or 'never ran'}, "
                  f"recurrence={fm.get('recurrence', 'watch')}, "
                  f"publish={fm.get('publish_policy', 'on_change')})")
    print(f"{n} watch(es) due. For each: research per the task body, append to its "
          f"Research Log, publish per publish_policy, then `run_watches.py mark <id>`.")


def mark(wid):
    for rel, fm in watches():
        if fm.get("id") == wid:
            p = os.path.join(ROOT, rel)
            text = open(p, encoding="utf-8").read()
            interval = INTERVALS.get(str(fm.get("recurrence", "watch")), 7)
            nxt = (now_pt().date() + datetime.timedelta(days=interval)).isoformat()
            lines = text.split("\n")
            fences = [i for i, l in enumerate(lines) if l.strip() == "---"]
            if len(fences) < 2:
                die(f"{rel}: no frontmatter fences")
            close = fences[1]
            for field, val in (("last_run", today()), ("next_run", nxt)):
                hit = [i for i in range(fences[0] + 1, close)
                       if lines[i].startswith(f"{field}:")]
                if hit:
                    lines[hit[0]] = f"{field}: {val}"
                else:
                    lines.insert(close, f"{field}: {val}")
                    close += 1
            open(p, "w", encoding="utf-8").write("\n".join(lines))
            print(f"{wid}: last_run={today()} next_run={nxt}")
            return
    die(f"no watch with id {wid}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("due", "mark"):
        die(__doc__)
    if sys.argv[1] == "due":
        due()
    else:
        mark(sys.argv[2])
