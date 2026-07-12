#!/usr/bin/env python3
"""routine_monitor.py — observability for the 4-window daily routine schedule.

WHY THIS EXISTS
The platform exposes NO token/quota API and NO per-run timing to a session
(docs/LIMITATIONS.md #4, #19; CAPACITY_LEDGER.md). So this tool records the
fields we CAN observe and treats them as PROXIES for allowance cost:

    runtime_min   wall-clock minutes (actual_finish - actual_start)
    tool_calls    number of tool invocations in the run
    web_searches  number of WebSearch calls
    files_read    number of file reads / large-context loads
    out_chars     characters of model output (token proxy: ~4 chars/token)

Token columns (in_tok/out_tok/total_tok) exist in the schema but stay BLANK
unless a real number is ever exposed. We never invent them.

The 5-hour usage WINDOW is account-wide: every message from every routine and
every manual chat draws from the same window if it lands inside it. This tool
models the window phase so it can flag drift, overlap, and a failed anchor.

SUBCOMMANDS
    log     append one run row (see --help for fields)
    stats   rolling mean/median/min/max/std + p75/p90/p95 per routine
    check   re-run the flag rules over the whole log and print alerts
    plan    given a routine's scheduled start, print the recommended
            downstream buffer times from accumulated data (or say "insufficient")

Stdlib only (repo rule). CSV lives at system/routine_runs.csv by default.
"""
import argparse, csv, os, sys, statistics, datetime
from zoneinfo import ZoneInfo

PACIFIC = ZoneInfo("America/Los_Angeles")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV = os.path.join(ROOT, "system", "routine_runs.csv")

FIELDS = [
    "date", "routine", "scheduled", "actual_start", "actual_finish",
    "runtime_min", "session_start", "expected_reset", "window_model",
    "in_tok", "out_tok", "total_tok", "out_chars",
    "tool_calls", "web_searches", "files_read", "errors",
    "allowance_remaining", "notes",
]

# --- flag thresholds (tune from data; conservative defaults) -----------------
LATE_START_MIN = 5.0        # actual_start later than scheduled by this many min
OUTLIER_SIGMA = 2.0         # runtime/proxy beyond mean +/- 2*std is an outlier
OVERLAP_GUARD_MIN = 3.0     # a run whose start is within N min BEFORE a reset
                            # risks landing in the wrong window
ANCHOR_ROUTINE = "anchor"   # name used for the 11:30 window-opener run


def parse_hhmm(s, ref_date):
    """'HH:MM' on ref_date (a date) -> aware PT datetime. '' -> None."""
    if not s:
        return None
    h, m = s.strip().split(":")
    return datetime.datetime(ref_date.year, ref_date.month, ref_date.day,
                             int(h), int(m), tzinfo=PACIFIC)


def reset_time(start_dt, model):
    """Expected reset for a window opened at start_dt.
    model='exact' : start + 5h (window anchored to first-message timestamp).
    model='hour'  : floor to top of hour, + 5h (rounded-to-hour hypothesis).
    Both are hypotheses until week-1 evidence picks one (see the audit)."""
    if model == "hour":
        start_dt = start_dt.replace(minute=0, second=0, microsecond=0)
    return start_dt + datetime.timedelta(hours=5)


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_header_if_missing(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def cmd_log(a):
    save_header_if_missing(a.csv)
    d = datetime.date.today() if not a.date else \
        datetime.date.fromisoformat(a.date)
    start = parse_hhmm(a.actual_start, d)
    finish = parse_hhmm(a.actual_finish, d)
    runtime = ""
    if start and finish:
        if finish < start:                       # ran past midnight
            finish += datetime.timedelta(days=1)
        runtime = round((finish - start).total_seconds() / 60.0, 1)
    sess = parse_hhmm(a.session_start, d) or start
    reset = reset_time(sess, a.window_model) if sess else None
    row = {
        "date": d.isoformat(), "routine": a.routine, "scheduled": a.scheduled,
        "actual_start": a.actual_start, "actual_finish": a.actual_finish,
        "runtime_min": runtime,
        "session_start": sess.strftime("%H:%M") if sess else "",
        "expected_reset": reset.strftime("%H:%M") if reset else "",
        "window_model": a.window_model,
        "in_tok": a.in_tok, "out_tok": a.out_tok, "total_tok": a.total_tok,
        "out_chars": a.out_chars, "tool_calls": a.tool_calls,
        "web_searches": a.web_searches, "files_read": a.files_read,
        "errors": a.errors, "allowance_remaining": a.allowance_remaining,
        "notes": a.notes,
    }
    with open(a.csv, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(row)
    print("logged:", row["date"], row["routine"], f"{runtime}min")
    for msg in flags_for_row(row, a.scheduled):
        print("  FLAG:", msg)


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def flags_for_row(row, scheduled):
    out = []
    sched = row.get("scheduled") or scheduled
    st = row.get("actual_start")
    if sched and st:
        d = datetime.date.fromisoformat(row["date"])
        s0, s1 = parse_hhmm(sched, d), parse_hhmm(st, d)
        if s0 and s1 and (s1 - s0).total_seconds() / 60.0 > LATE_START_MIN:
            out.append(f"late start: {st} vs scheduled {sched}")
    if row.get("errors") and row["errors"] not in ("", "0", "none", "None"):
        out.append(f"errors recorded: {row['errors']}")
    if row.get("routine") == ANCHOR_ROUTINE and not st:
        out.append("anchor run has no actual_start — MISSING ANCHOR")
    return out


def _series(rows, routine, key):
    vals = []
    for r in rows:
        if r.get("routine") != routine:
            continue
        v = _f(r.get(key))
        if v is not None:
            vals.append(v)
    return vals


def pct(vals, p):
    """pth percentile, linear interpolation; safe on tiny samples."""
    if not vals:
        return None
    s = sorted(vals)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 1)


def describe(vals):
    if not vals:
        return None
    return {
        "n": len(vals), "mean": round(statistics.mean(vals), 1),
        "median": round(statistics.median(vals), 1),
        "min": min(vals), "max": max(vals),
        "std": round(statistics.pstdev(vals), 1) if len(vals) > 1 else 0.0,
        "p75": pct(vals, 75), "p90": pct(vals, 90), "p95": pct(vals, 95),
    }


def cmd_stats(a):
    rows = load(a.csv)
    if not rows:
        print("no data yet — log some runs first.")
        return
    routines = a.routine and [a.routine] or sorted({r["routine"] for r in rows})
    for rt in routines:
        print(f"\n=== {rt} ===")
        for key in ("runtime_min", "out_chars", "tool_calls",
                    "web_searches", "total_tok"):
            d = describe(_series(rows, rt, key))
            if d:
                print(f"  {key:12} n={d['n']:>3}  mean={d['mean']:<7} "
                      f"med={d['median']:<7} min={d['min']:<6} max={d['max']:<6} "
                      f"std={d['std']:<6} p75={d['p75']:<6} p90={d['p90']:<6} "
                      f"p95={d['p95']}")
            else:
                print(f"  {key:12} (no numeric data)")


def cmd_check(a):
    rows = load(a.csv)
    if not rows:
        print("no data yet.")
        return
    n_alerts = 0
    # per-row flags
    for r in rows:
        for msg in flags_for_row(r, r.get("scheduled", "")):
            print(f"[{r['date']} {r['routine']}] {msg}")
            n_alerts += 1
    # outliers vs each routine's own history
    for rt in sorted({r["routine"] for r in rows}):
        for key in ("runtime_min", "out_chars", "tool_calls"):
            vals = _series(rows, rt, key)
            d = describe(vals)
            if not d or d["n"] < 4 or d["std"] == 0:
                continue
            for r in rows:
                if r.get("routine") != rt:
                    continue
                v = _f(r.get(key))
                if v is not None and abs(v - d["mean"]) > OUTLIER_SIGMA * d["std"]:
                    print(f"[{r['date']} {rt}] {key} outlier: {v} "
                          f"(mean {d['mean']} +/- {d['std']})")
                    n_alerts += 1
    # window-phase checks: overlap risk + reset drift
    for r in rows:
        st = r.get("actual_start")
        rs = r.get("expected_reset")
        sc = r.get("scheduled")
        if st and rs:
            d0 = datetime.date.fromisoformat(r["date"])
            s = parse_hhmm(st, d0)
            reset = parse_hhmm(rs, d0)
            # a run that OPENS a window very close after a prior reset is fine;
            # flag a run whose scheduled time sits BEFORE its own logged reset
            # by < guard (i.e. the prior window may still be open -> shared).
            if sc:
                scd = parse_hhmm(sc, d0)
                if scd and reset and 0 <= (reset - scd).total_seconds()/60.0 < OVERLAP_GUARD_MIN:
                    print(f"[{r['date']} {r['routine']}] OVERLAP RISK: scheduled "
                          f"{sc} is <{OVERLAP_GUARD_MIN}min before reset {rs}")
                    n_alerts += 1
    print(f"\n{n_alerts} alert(s).")


def cmd_plan(a):
    """Recommend downstream start = scheduled + high-pct runtime + buffer.
    Uses the *upstream* routine's runtime distribution."""
    rows = load(a.csv)
    vals = _series(rows, a.routine, "runtime_min")
    d = describe(vals)
    if not d or d["n"] < 5:
        print(f"insufficient data for {a.routine} "
              f"(have {d['n'] if d else 0} runs; need >=5). "
              f"Use the interim conservative buffer until then.")
        return
    sched = a.scheduled
    d0 = datetime.date.today()
    base = parse_hhmm(sched, d0)
    print(f"{a.routine}: n={d['n']} runtime mean={d['mean']} p90={d['p90']} "
          f"p95={d['p95']} max={d['max']} min")
    for label, run_len in (("p90", d["p90"]), ("p95", d["p95"]), ("max", d["max"])):
        for buf in (2, 3, 5, 10):
            t = base + datetime.timedelta(minutes=run_len + buf)
            print(f"  downstream start if using {label}({run_len}) + {buf}min buffer: "
                  f"{t.strftime('%H:%M')}")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", default=DEFAULT_CSV)
    sub = p.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("log", help="append one run row")
    lg.add_argument("--routine", required=True,
                    help="stockbot|brendan-brain|anchor|healthbot|footybot|manual")
    lg.add_argument("--scheduled", default="", help="HH:MM scheduled trigger")
    lg.add_argument("--actual-start", dest="actual_start", default="", help="HH:MM")
    lg.add_argument("--actual-finish", dest="actual_finish", default="", help="HH:MM")
    lg.add_argument("--session-start", dest="session_start", default="",
                    help="HH:MM the account window this run belongs to opened "
                         "(defaults to actual-start)")
    lg.add_argument("--window-model", dest="window_model", default="exact",
                    choices=["exact", "hour"],
                    help="reset hypothesis: 'exact'=start+5h, 'hour'=floor-hour+5h")
    lg.add_argument("--in-tok", dest="in_tok", default="")
    lg.add_argument("--out-tok", dest="out_tok", default="")
    lg.add_argument("--total-tok", dest="total_tok", default="")
    lg.add_argument("--out-chars", dest="out_chars", default="",
                    help="chars of model output (token proxy)")
    lg.add_argument("--tool-calls", dest="tool_calls", default="")
    lg.add_argument("--web-searches", dest="web_searches", default="")
    lg.add_argument("--files-read", dest="files_read", default="")
    lg.add_argument("--errors", default="")
    lg.add_argument("--allowance-remaining", dest="allowance_remaining", default="",
                    help="subjective: full|high|mid|low|hit-limit")
    lg.add_argument("--notes", default="")
    lg.add_argument("--date", default="", help="YYYY-MM-DD (default today PT)")
    lg.set_defaults(func=cmd_log)

    st = sub.add_parser("stats", help="rolling distribution per routine")
    st.add_argument("--routine", default="")
    st.set_defaults(func=cmd_stats)

    ck = sub.add_parser("check", help="run all flag rules over the log")
    ck.set_defaults(func=cmd_check)

    pl = sub.add_parser("plan", help="recommend downstream buffer from data")
    pl.add_argument("--routine", required=True, help="the UPSTREAM routine")
    pl.add_argument("--scheduled", required=True, help="upstream scheduled HH:MM")
    pl.set_defaults(func=cmd_plan)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
