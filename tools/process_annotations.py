#!/usr/bin/env python3
"""Process Brendan's annotations on a published edition (annotations schema + MEMORY_POLICY).
Usage: process_annotations.py [--date YYYY-MM-DD] [--apply]
Scans newspaper/editions/<date>.md for reaction marks and `>>` lines. Without --apply:
prints the interpretation plan. With --apply: writes preference evidence to
preferences/PROPOSED_RULES.md, creates follow-up tasks via new_task.py mechanics, updates
INTEREST_PROFILE rejected topics ONLY on explicit 'stop covering' phrasing, and records an
annotation artifact. NEVER writes CONFIRMED_RULES.md (that requires Brendan/approval)."""
import argparse, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, today, slugify

REACT = {"⭐": "important", "🙂": "more_like_this", "❌": "not_useful"}
DEEP_RE = re.compile(r">>\s*(research (this )?(deeper|more)|go deep)", re.I)
STOP_RE = re.compile(r">>\s*(stop covering|don'?t show|do not show)", re.I)
WRONG_RE = re.compile(r">>\s*(wrong|incorrect|this was wrong)", re.I)
WATCH_RE = re.compile(r">>\s*(make|create).*(watch)", re.I)


def current_section_item(lines, i):
    for j in range(i, -1, -1):
        m = re.match(r"### (.+)", lines[j])
        if m:
            return m.group(1).strip()
        if re.match(r"## ", lines[j]):
            return re.sub(r"\s*\(budget.*", "", lines[j][3:]).strip()
    return "(edition-level)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=today())
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    p = os.path.join(ROOT, "newspaper", "editions", f"{a.date}.md")
    if not os.path.exists(p):
        sys.exit(f"no edition for {a.date}")
    lines = open(p, encoding="utf-8").read().splitlines()
    actions = []
    for i, line in enumerate(lines):
        # skip the annotation legend / instruction footer (arch review finding #5:
        # the legend contains all three marks and was generating phantom evidence)
        if "Annotate inline" in line or sum(m in line for m in REACT) >= 2:
            continue
        item = None
        for mark, kind in REACT.items():
            if mark in line:
                item = item or current_section_item(lines, i)
                actions.append(("evidence", kind, item, line.strip()[:160]))
        if line.strip().startswith(">>"):
            item = current_section_item(lines, i)
            note = line.strip()[2:].strip()
            if STOP_RE.match(line.strip()):
                actions.append(("stop_covering", "explicit", item, note))
            elif DEEP_RE.match(line.strip()):
                actions.append(("followup_task", "deep", item, note))
            elif WATCH_RE.match(line.strip()):
                actions.append(("create_watch", "explicit", item, note))
            elif WRONG_RE.match(line.strip()):
                actions.append(("correction", "flag", item, note))
            else:
                actions.append(("evidence", "comment", item, note))
    if not actions:
        print("no annotations found")
        return
    for act in actions:
        print(f"{'APPLY' if a.apply else 'PLAN '}: {act[0]:<14} [{act[1]}] on '{act[2]}' — {act[3]}")
    if not a.apply:
        print("\n(run with --apply to execute; one reaction becomes EVIDENCE, never a rule)")
        return
    ev_path = os.path.join(ROOT, "preferences", "PROPOSED_RULES.md")
    ev = open(ev_path, encoding="utf-8").read()
    new_ev = ""
    for kind, sub, item, note in actions:
        if kind in ("evidence", "correction", "stop_covering"):
            new_ev += f"- {a.date} | {sub} | {item} | edition-{a.date} | {note}\n"
        if kind == "correction":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "new_task.py"),
                            "--title", f"Correction check: {item}", "--domain", "general",
                            "--request", f"Brendan flagged as wrong on {a.date}: '{note}'. "
                            f"Re-verify the claim in edition {a.date} item '{item}'; if wrong, "
                            f"create a superseding artifact.", "--urgency", "high"], check=True)
        if kind == "followup_task":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "new_task.py"),
                            "--title", f"Deeper research: {item}", "--domain", "general",
                            "--request", f"Brendan asked to go deeper ({a.date}): '{note}' "
                            f"on edition item '{item}'.", "--depth", "deep",
                            "--publish", "newspaper"], check=True)
        if kind == "create_watch":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "new_task.py"),
                            "--title", f"Watch: {item}", "--domain", "general",
                            "--request", f"Brendan asked for a watch ({a.date}): '{note}'.",
                            "--recurrence", "watch", "--publish", "newspaper"], check=True)
        if kind == "stop_covering":
            ip = os.path.join(ROOT, "preferences", "INTEREST_PROFILE.md")
            t = open(ip, encoding="utf-8").read().replace(
                "Rejected topics (never resurface without instruction): (none yet)",
                f"Rejected topics (never resurface without instruction): {item} ({a.date})")
            if item not in t:
                t += f"\n- rejected: {item} ({a.date}, explicit)\n"
            open(ip, "w", encoding="utf-8").write(t)
    open(ev_path, "w", encoding="utf-8").write(
        ev.replace("(empty — populated by annotation processing)",
                   "(populated by annotation processing)") .rstrip() +
        ("\n" + new_ev if new_ev else "\n"))
    ann_dir = os.path.join(ROOT, "newspaper", "annotations")
    os.makedirs(ann_dir, exist_ok=True)
    ann = os.path.join(ann_dir, f"ann-{a.date}.md")
    open(ann, "w", encoding="utf-8").write(f"""---
id: ann-{a.date.replace('-', '')}
artifact_type: annotation
edition_id: edition-{a.date.replace('-', '')}
created_at: {a.date}
status: processed
---
# Annotations processed for {a.date}

""" + "\n".join(f"- {k} [{s}] '{i}': {n}" for k, s, i, n in actions) + "\n")
    print(f"\nprocessed {len(actions)} annotations -> {os.path.relpath(ann, ROOT)}")


if __name__ == "__main__":
    main()
