#!/usr/bin/env python3
"""Append a per-task usage row to system/CAPACITY_LEDGER.md. OBSERVABLE fields only —
the platform exposes no token/quota API (LIMITATIONS #4) and this tool REFUSES invented
numbers by not having a tokens field at all (arch-challenge response #11).

Usage: log_usage.py --task <id-or-desc> --model <haiku|sonnet|opus|fable> --type <t>
       [--agents N] [--start HH:MM] [--end HH:MM] [--effort S|M|L]
       [--escalated no|yes:<trigger>] [--cheaper-ok yes|no|unsure]
       [--reviewer-changes none|minor|major] [--useful pending|yes|no|mixed]
       [--verdict "one line: was the staffing worth it?"]
--useful defaults to pending: usefulness is BRENDAN's reaction, recorded later by
annotation processing (process_annotations) or a session he reacts in — never self-graded
at write time. Monthly routing recommendations ride the weekly review when rows ≥ 8."""
import argparse, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, today, now_pt

LEDGER = os.path.join(ROOT, "system", "CAPACITY_LEDGER.md")
HEADER = ("| date | task | model | agents | start–end | type | effort | escalated | "
          "cheaper-ok? | reviewer-changes | useful? | verdict |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--model", required=True, choices=["haiku", "sonnet", "opus", "fable"])
    ap.add_argument("--type", required=True)
    ap.add_argument("--agents", default="1")
    ap.add_argument("--start", default="")
    ap.add_argument("--end", default=now_pt().strftime("%H:%M"))
    ap.add_argument("--effort", default="M", choices=["S", "M", "L"])
    ap.add_argument("--escalated", default="no")
    ap.add_argument("--cheaper-ok", dest="cheaper", default="unsure",
                    choices=["yes", "no", "unsure"])
    ap.add_argument("--reviewer-changes", dest="rev", default="none",
                    choices=["none", "minor", "major"])
    ap.add_argument("--useful", default="pending", choices=["pending", "yes", "no", "mixed"])
    ap.add_argument("--verdict", default="")
    a = ap.parse_args()
    text = open(LEDGER, encoding="utf-8").read()
    if HEADER not in text:
        text += f"""
## Usage log (V2 — observable fields only; no token numbers exist to record)

{HEADER}
|---|---|---|---|---|---|---|---|---|---|---|---|
"""
    def cell(x):  # pipes/newlines corrupt markdown tables (QA defect #2)
        return str(x).replace("|", "/").replace("\n", " ").strip()
    row = (f"| {today()} | {cell(a.task[:48])} | {a.model} | {cell(a.agents)} | "
           f"{cell(a.start)}–{cell(a.end)} | {cell(a.type)} | {a.effort} | "
           f"{cell(a.escalated)} | {a.cheaper} | {a.rev} | {a.useful} | "
           f"{cell(a.verdict[:80])} |")
    text = text.rstrip("\n") + "\n" + row + "\n"
    open(LEDGER, "w", encoding="utf-8").write(text)
    print(f"logged: {row}")


if __name__ == "__main__":
    main()
