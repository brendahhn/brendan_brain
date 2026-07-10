#!/usr/bin/env python3
"""Create a queue task file, dedupe-aware and idempotent (CROSS_REPOSITORY_POLICY).
Usage: new_task.py --title "..." --domain vehicles --request "verbatim ask"
       [--urgency low|normal|high|urgent] [--depth quick|standard|deep]
       [--deadline YYYY-MM-DD] [--word-budget N] [--effort 1_pass|2_pass|until_strong]
       [--publish newspaper|file_only|none] [--recurrence none|daily|weekly|watch]
       [--origin repo] [--dedupe-key K] [--constraints "..."]
Prints the task path. If dedupe_key matches an open task, prints DUPLICATE + existing path
and appends a note to the existing task instead of creating a new one (exit 0)."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, iter_artifacts, today, slugify

OPEN = {"inbox", "triaged", "active", "waiting_for_brendan", "continuing_with_assumption",
        "scheduled", "verification", "ready_for_publication", "watching"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--request", required=True)
    ap.add_argument("--urgency", default="normal")
    ap.add_argument("--depth", default="standard")
    ap.add_argument("--deadline", default="")
    ap.add_argument("--word-budget", default="")
    ap.add_argument("--effort", default="1_pass")
    ap.add_argument("--publish", default="none")
    ap.add_argument("--recurrence", default="none")
    ap.add_argument("--origin", default="brendan_brain")
    ap.add_argument("--dedupe-key", default="")
    ap.add_argument("--constraints", default="")
    a = ap.parse_args()

    dk = a.dedupe_key or f"{a.domain}/{slugify(a.title)}"
    for rel, fm, _ in iter_artifacts():
        if fm.get("artifact_type") in ("task", "watch") and fm.get("dedupe_key") == dk \
                and str(fm.get("status")) in OPEN:
            p = os.path.join(ROOT, rel)
            with open(p, "a", encoding="utf-8") as f:
                f.write(f"\n> [dedupe {today()}] Same request arrived again "
                        f"(origin: {a.origin}). Treated as +1 interest signal, not a new task.\n")
            print(f"DUPLICATE {rel} (id={fm.get('id')})")
            return

    date = today().replace("-", "")
    slug = slugify(a.title)
    tid = f"task-{date}-{slug}"
    folder = "watches" if a.recurrence == "watch" else "inbox"
    status = "watching" if a.recurrence == "watch" else "inbox"
    path = os.path.join(ROOT, "queue", folder, f"{tid}.md")
    if os.path.exists(path):  # idempotent retry: same day, same slug
        print(f"EXISTS {os.path.relpath(path, ROOT)}")
        return
    fm = f"""---
id: {tid}
title: {a.title}
artifact_type: {"watch" if a.recurrence == "watch" else "task"}
domain: {a.domain}
status: {status}
created_at: {today()}
urgency: {a.urgency}
depth: {a.depth}
effort_budget: {a.effort}
publication_destination: {a.publish}
recurrence: {a.recurrence}
requires_brendan_answer: false
origin_repository: {a.origin}
dedupe_key: {dk}
"""
    if a.deadline:
        fm += f"deadline: {a.deadline}\n"
    if a.word_budget:
        fm += f"word_budget: {a.word_budget}\n"
    fm += "---\n"
    body = f"\n## Request\n\n{a.request}\n"
    if a.constraints:
        body += f"\n## Constraints\n\n{a.constraints}\n"
    body += "\n## Assumptions\n\n(none yet)\n\n## Questions\n\n(none yet)\n\n## Research Log\n"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(fm + body)
    print(os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
