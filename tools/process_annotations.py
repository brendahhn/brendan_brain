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
# keyword annotations may appear bare on a line or after `>>` (docs: READING_AND_ANNOTATING)
KW = r"(?:>>\s*)?"
DEEP_RE = re.compile(KW + r"(DEEPER\b|research (this )?(deeper|more)|go deep)", re.I)
STOP_RE = re.compile(KW + r"(STOP COVERING|stop covering|don'?t show|do not show)")
WRONG_RE = re.compile(KW + r"(INCORRECT\b|CORRECTION\b|wrong|this was wrong)")
WATCH_RE = re.compile(KW + r"(WATCH\b|(make|create).*watch)", re.I)
QUESTION_RE = re.compile(KW + r"QUESTION[:\s]")
REMEMBER_RE = re.compile(KW + r"REMEMBER THIS[:\s]?")
FORGET_RE = re.compile(KW + r"FORGET THIS[:\s]?")
CHANGEPREF_RE = re.compile(KW + r"CHANGE PREFERENCE[:\s]?")


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
        s = line.strip()
        kw_hit = any(r.match(s) for r in (STOP_RE, DEEP_RE, WATCH_RE, WRONG_RE,
                                          QUESTION_RE, REMEMBER_RE, FORGET_RE, CHANGEPREF_RE))
        if s.startswith(">>") or kw_hit:
            item = current_section_item(lines, i)
            note = s[2:].strip() if s.startswith(">>") else s
            if STOP_RE.match(s):
                actions.append(("stop_covering", "explicit", item, note))
            elif FORGET_RE.match(s):
                actions.append(("forget_request", "explicit", item, note))
            elif REMEMBER_RE.match(s):
                actions.append(("remember", "explicit", item, note))
            elif CHANGEPREF_RE.match(s):
                actions.append(("change_preference", "explicit", item, note))
            elif QUESTION_RE.match(s):
                actions.append(("brendan_question", "explicit", item, note))
            elif DEEP_RE.match(s):
                actions.append(("followup_task", "deep", item, note))
            elif WATCH_RE.match(s):
                actions.append(("create_watch", "explicit", item, note))
            elif WRONG_RE.match(s):
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
    new_ev = ""
    for kind, sub, item, note in actions:
        if kind in ("evidence", "correction", "stop_covering", "remember", "change_preference"):
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
        if kind == "brendan_question":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "new_task.py"),
                            "--title", f"Answer Brendan's question: {item}", "--domain", "general",
                            "--request", f"Brendan asked in edition {a.date}: '{note}'. Answer "
                            f"from the Brain where possible; research if needed; publish the "
                            f"answer in the next edition.", "--urgency", "high",
                            "--publish", "newspaper"], check=True)
        if kind == "remember":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "new_task.py"),
                            "--title", f"Capture durable knowledge: {item}", "--domain", "general",
                            "--request", f"Brendan marked REMEMBER THIS in edition {a.date}: "
                            f"'{note}'. Write a knowledge artifact (SCHEMAS.md) with "
                            f"derived_from pointing at the edition item; correct domain + "
                            f"sensitivity.", "--urgency", "high"], check=True)
        if kind == "forget_request":
            subprocess.run([sys.executable, os.path.join(ROOT, "tools", "new_task.py"),
                            "--title", f"Forgetting request: {item}", "--domain", "general",
                            "--request", f"Brendan marked FORGET THIS in edition {a.date}: "
                            f"'{note}'. Run the brain-forget PLAN phase and present it to "
                            f"Brendan. NEVER execute deletion without his confirmation.",
                            "--urgency", "urgent"], check=True)
        if kind == "change_preference":
            ip = os.path.join(ROOT, "preferences", "PROPOSED_RULES.md")
            t = open(ip, encoding="utf-8").read()
            marker = "## Proposals awaiting evidence or approval"
            prop = (f"- PROPOSAL ({a.date}, explicit CHANGE PREFERENCE on '{item}'): {note} "
                    f"— awaiting Brendan's confirmation wording in the next edition.\n")
            t = t.replace(marker, marker + "\n" + prop) if marker in t else t + prop
            open(ip, "w", encoding="utf-8").write(t)
        if kind == "stop_covering":
            ip = os.path.join(ROOT, "preferences", "INTEREST_PROFILE.md")
            t = open(ip, encoding="utf-8").read().replace(
                "Rejected topics (never resurface without instruction): (none yet)",
                f"Rejected topics (never resurface without instruction): {item} ({a.date})")
            if item not in t:
                t += f"\n- rejected: {item} ({a.date}, explicit)\n"
            open(ip, "w", encoding="utf-8").write(t)
    # read AFTER the action loop — change_preference writes this file during the loop
    ev = open(ev_path, encoding="utf-8").read()
    ev = ev.replace("(empty — populated by annotation processing)",
                    "(populated by annotation processing)")
    marker = "## Proposals awaiting evidence or approval"
    if new_ev and marker in ev:  # insert under the Evidence log, not at file end
        ev = ev.replace(marker, new_ev + "\n" + marker)
    elif new_ev:
        ev = ev.rstrip() + "\n" + new_ev
    open(ev_path, "w", encoding="utf-8").write(ev)
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
