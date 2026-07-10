#!/usr/bin/env python3
"""Assemble a newspaper DRAFT (Managing Editor mechanics; editorial judgment happens in the
session that reviews/edits the draft before publishing — see PUBLICATION_POLICY.md).
Usage: build_newspaper.py [--date YYYY-MM-DD] [--publish]
Collects: ready_for_publication tasks, robot outbox files (queue/inbox/from-*.md dated
today/yesterday), open questions, unfinished operations, proposed rules awaiting approval.
Writes newspaper/drafts/<date>.md; --publish moves it to editions/ after the Publisher
checklist fields are filled in the draft frontmatter."""
import argparse, os, re, shutil, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, iter_artifacts, today, SENSITIVE

BUDGETS = {"most_important": 150, "investing": 1000, "fantasy_football": 500, "health": 500,
           "jobs": 300, "news": 400, "open_research": 500, "questions_and_system": 200}


def collect(date):
    items = {k: [] for k in BUDGETS}
    for rel, fm, body in iter_artifacts():
        at, dom, st = fm.get("artifact_type"), fm.get("domain", ""), str(fm.get("status", ""))
        sens = fm.get("sensitivity", "personal")
        # publication_destination gates collection (QA finding #6): file_only/none tasks
        # complete without a newspaper appearance
        if at in ("task", "watch") and st == "ready_for_publication" \
                and fm.get("publication_destination", "none") == "newspaper":
            m = re.search(r"## Findings\n(.*?)(\n## |\Z)", body, re.S)
            summary = (m.group(1).strip() if m else "(findings section missing)")
            if sens in SENSITIVE:
                summary = f"(sensitive {sens} content — see `{rel}` directly; only generic " \
                          f"conclusions may be quoted here by the editor)"
            sec = dom if dom in items else "open_research"
            items[sec].append((fm.get("id"), fm.get("title"), summary[:2000], rel))
        if at == "question" and st == "open":
            q = body.strip()
            if len(q) > 500:
                q = q[:500].rsplit(" ", 1)[0] + " […]"  # word boundary (QA finding #7)
            items["questions_and_system"].append(
                (fm.get("id"), fm.get("title", "(question)"), q, rel))
    # robot outboxes from the last 2 days
    inbox = os.path.join(ROOT, "queue", "inbox")
    if os.path.isdir(inbox):
        for fn in sorted(os.listdir(inbox)):
            if fn.startswith("from-") and fn.endswith(".md"):
                p = os.path.join(inbox, fn)
                text = open(p, encoding="utf-8").read()
                dom = fn.replace("from-", "").split(".")[0].split("-2")[0].replace(".md", "")
                dom = {"jobs-robot": "jobs", "footybot": "fantasy_football",
                       "health-robot": "health", "trading-robot": "investing"}.get(dom, dom)
                sec = dom if dom in items else "news"
                # include every dated block from today or yesterday (arch review finding #6:
                # last-block-only dropped robots that ran yesterday but not today)
                yday = (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()
                for block in re.split(r"\n(?=## \d{4}-)", text):
                    b = block.strip()
                    m = re.match(r"## (\d{4}-\d{2}-\d{2})", b)
                    if not m or m.group(1) not in (date[:10], yday):
                        continue
                    # health outbox scrub (arch review finding #12): flag numeric medical
                    # values that the sanitization rules say must never be exported
                    if "health" in fn and re.search(
                            r"\d+\s?(mg|mcg|kg|lb|bpm|mmol|mg/dl|iu)\b", b, re.I):
                        b = ("⚠️ SANITIZATION FLAG: this health export contains numeric "
                             f"dose/biometric-like values and was withheld from the draft. "
                             f"Review `queue/inbox/{fn}` directly and fix the robot's export.")
                    items[sec].append((fn, f"{dom} robot report {m.group(1)}", b[:2500],
                                       f"queue/inbox/{fn}"))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=today())
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    draft = os.path.join(ROOT, "newspaper", "drafts", f"{a.date}.md")
    edition = os.path.join(ROOT, "newspaper", "editions", f"{a.date}.md")
    if a.publish:
        if not os.path.exists(draft):
            sys.exit(f"no draft for {a.date}")
        if os.path.exists(edition) and not a.force:
            sys.exit(f"REFUSED: newspaper/editions/{a.date}.md already exists — a published "
                     f"edition is part of the audit trail (QA finding #1). Use --force only "
                     f"if you truly mean to supersede it, after committing the original.")
        text = open(draft, encoding="utf-8").read()
        if "publisher_verdict: approved" not in text:
            sys.exit("draft not approved: set `publisher_verdict: approved` in frontmatter "
                     "after completing the Publisher checklist (PUBLICATION_POLICY.md)")
        text = text.replace("status: draft", "status: published", 1)
        text = text.replace(" (DRAFT)", "", 1)
        os.makedirs(os.path.dirname(edition), exist_ok=True)
        open(edition, "w", encoding="utf-8").write(text)
        os.remove(draft)
        print(f"published newspaper/editions/{a.date}.md")
        return
    items = collect(a.date)
    lines = [f"""---
id: edition-{a.date.replace('-', '')}
artifact_type: edition
created_at: {a.date}
status: draft
publisher_verdict: pending   # set to `approved` after the Publisher checklist
checklist_notes: ""
---
# 🗞️ Brendan's Daily — {a.date} (DRAFT)

> Editor: trim to budgets, drop empty sections, check coverage_ledger.md for repeats,
> re-verify time-sensitive claims, then complete the Publisher checklist.
"""]
    order = ["most_important", "health", "fantasy_football", "investing", "jobs", "news",
             "open_research", "questions_and_system"]
    empty = []
    for sec in order:
        got = items.get(sec, [])
        if not got and sec != "most_important":
            empty.append(sec)
            continue
        lines.append(f"\n## {sec.replace('_', ' ').title()}  (budget ~{BUDGETS[sec]}w)\n")
        if sec == "most_important":
            lines.append("_(editor selects 1-3 items from below and summarizes here)_\n")
        for aid, title, summary, rel in got:
            lines.append(f"### {title}\n<sub>source: [`{aid}`]({rel})</sub>\n\n{summary}\n")
    if empty:
        lines.append("\n---\n_Nothing meaningful today in: " +
                     ", ".join(e.replace('_', ' ') for e in empty) + "._\n")
    lines.append("\n---\n_Annotate inline: ⭐ important · 🙂 more like this · ❌ not useful · "
                 "lines starting with `>>` are freeform notes. Then run the brain-annotations "
                 "skill (or `python3 tools/process_annotations.py`)._\n")
    os.makedirs(os.path.dirname(draft), exist_ok=True)
    open(draft, "w", encoding="utf-8").write("\n".join(lines))
    n = sum(len(v) for v in items.values())
    print(f"draft written: newspaper/drafts/{a.date}.md ({n} candidate items, "
          f"{len(empty)} empty sections)")


if __name__ == "__main__":
    main()
