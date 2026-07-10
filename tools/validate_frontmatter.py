#!/usr/bin/env python3
"""Validate artifact frontmatter against system/SCHEMAS.md rules.
Usage: validate_frontmatter.py [--all | file...]   Exit 1 on any error."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import (ROOT, ARTIFACT_TYPES, SENSITIVITIES, TASK_STATUSES, FOLDER_STATUS,
                      parse_frontmatter, iter_artifacts)

REQUIRED_BASE = ["id", "artifact_type", "created_at"]
REQUIRED_BY_TYPE = {
    "task": ["title", "domain", "status", "urgency", "depth", "dedupe_key"],
    "timeline": ["sensitivity"],
    "knowledge": ["domain", "confidence"],
    "prediction": ["domain", "confidence", "horizon"],
    "outcome": ["result"],
    "watch": ["title", "domain", "status", "recurrence"],
    "question": ["kind", "status"],
    "annotation": ["edition_id", "status"],
    "operation": ["repos", "started_at"],
    "domain_profile": ["domain", "status"],
}
MANIFEST_REPOS = {"brendan_brain", "operator-notebook", "FootyBot", "footybot",
                  "health-notebook", "trading-notebook"}


def check(rel, fm):
    errs = []
    at = fm.get("artifact_type", "")
    for f in REQUIRED_BASE + REQUIRED_BY_TYPE.get(at, []):
        if f == "created_at" and fm.get("started_at"):
            continue
        if not fm.get(f):
            errs.append(f"missing required field '{f}'")
    if at and at not in ARTIFACT_TYPES:
        errs.append(f"unknown artifact_type '{at}'")
    sens = fm.get("sensitivity")
    if sens and sens not in SENSITIVITIES:
        errs.append(f"unknown sensitivity '{sens}'")
    orig = fm.get("origin_repository")
    if orig and orig not in MANIFEST_REPOS:
        errs.append(f"origin_repository '{orig}' not in repository manifest (work-boundary guard)")
    if at in ("task", "watch"):
        st = fm.get("status", "")
        if st not in TASK_STATUSES:
            errs.append(f"invalid task status '{st}'")
        parts = rel.split(os.sep)
        if len(parts) >= 2 and parts[0] == "queue" and parts[1] in FOLDER_STATUS:
            if st not in FOLDER_STATUS[parts[1]]:
                errs.append(f"status '{st}' inconsistent with folder queue/{parts[1]}/")
    return errs


def main():
    args = sys.argv[1:]
    targets = []
    if not args or args == ["--all"]:
        targets = [(rel, fm) for rel, fm, _ in iter_artifacts()]
    else:
        for a in args:
            p = a if os.path.isabs(a) else os.path.join(ROOT, a)
            fm, _ = parse_frontmatter(open(p, encoding="utf-8").read())
            if not fm.get("id"):
                print(f"{a}: no frontmatter/id found", file=sys.stderr)
                sys.exit(1)
            targets.append((os.path.relpath(p, ROOT), fm))
    seen, bad = {}, 0
    for rel, fm in targets:
        errs = check(rel, fm)
        i = fm.get("id")
        if i in seen:
            errs.append(f"duplicate id (also in {seen[i]})")
        seen[i] = rel
        for e in errs:
            print(f"{rel}: {e}", file=sys.stderr)
            bad += 1
    print(f"validated {len(targets)} artifacts, {bad} errors")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
