#!/usr/bin/env python3
"""Detect sustained activity that may justify a new domain and DRAFT a proposal.
Signals used are ONLY ones the Brain actually collects (arch-challenge response #14):
per-topic artifact counts, task/question counts, and preference-evidence mentions.
Never creates the domain — output is a proposal artifact for Brendan/the daily run.

Usage: propose_domains.py [--threshold 3] [--dry-run]
Scans artifacts whose domain is 'general' (or missing) plus preference evidence lines;
clusters by topic; topics with >= threshold distinct artifacts and no existing domain get
a draft proposal in system/proposals/. Idempotent: skips topics with an open proposal."""
import argparse, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, iter_artifacts, today, slugify

PROPOSALS = os.path.join(ROOT, "system", "proposals")
STOP = {"general", "research", "question", "task", "brendan", "system", "news", "update"}


def existing_domains():
    d = os.path.join(ROOT, "domains")
    return {n for n in os.listdir(d) if os.path.isdir(os.path.join(d, n))} if os.path.isdir(d) else set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    domains = existing_domains()
    topic_hits = collections.defaultdict(set)   # topic -> set of artifact ids
    # only interest-bearing types signal a domain; system reports/ops/editions never do
    SIGNAL_TYPES = {"task", "watch", "question", "knowledge", "timeline", "prediction"}
    for rel, fm, _ in iter_artifacts():
        dom = fm.get("domain") or "general"
        if dom in domains and dom != "general":
            continue                              # already housed
        if fm.get("artifact_type") not in SIGNAL_TYPES:
            continue
        topics = fm.get("topics") or []
        if isinstance(topics, str):
            topics = [topics]
        for t in topics:
            t = t.strip().lower()
            if t and t not in STOP and t not in domains:
                topic_hits[t].add(fm.get("id"))
    # preference-evidence lines only ADD WEIGHT to a topic that artifacts already raised —
    # reactions alone never draft a proposal (and synthetic test lines never count)
    prop = os.path.join(ROOT, "preferences", "PROPOSED_RULES.md")
    if os.path.exists(prop):
        for line in open(prop, encoding="utf-8"):
            if "SYNTHETIC" in line:
                continue
            m = re.match(r"- \d{4}-\d{2}-\d{2} \| \w+ \| ([^|]+)\|", line)
            if m:
                cell = m.group(1).strip().lower()
                for topic in list(topic_hits):
                    if topic in cell:
                        topic_hits[topic].add("evidence: " + line.strip()[:50])
    open_props = set()
    if os.path.isdir(PROPOSALS):
        for fn in os.listdir(PROPOSALS):
            open_props.add(fn.split("domain-proposal-")[-1].rsplit(".md", 1)[0].split("-", 1)[-1])
    made = 0
    for topic, ids in sorted(topic_hits.items(), key=lambda kv: -len(kv[1])):
        if len(ids) < a.threshold:
            continue
        slug = slugify(topic)
        if any(slug in p or p in slug for p in open_props):
            print(f"SKIP {topic}: open proposal exists")
            continue
        if a.dry_run:
            print(f"WOULD PROPOSE domain '{slug}' — {len(ids)} artifacts: {sorted(ids)[:6]}")
            made += 1
            continue
        os.makedirs(PROPOSALS, exist_ok=True)
        pid = f"proposal-{today().replace('-', '')}-{slug}"
        path = os.path.join(PROPOSALS, f"domain-proposal-{today().replace('-', '')}-{slug}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"""---
id: {pid}
title: "Domain proposal: {topic}"
artifact_type: report
domain: general
sensitivity: personal
confidence: low
created_at: {today()}
created_by: propose_domains.py
topics: [domain-proposal, {slug}]
---
# Domain proposal: {topic}

DRAFT generated from real accumulation signals — a session must refine the placeholders,
then surface it in the newspaper questions section. DOMAIN_POLICY: Brendan's approval (or
the autonomy ladder) decides; casual questions never become domains.

- **Proposed name**: `{slug}`
- **Why it deserves a domain**: {len(ids)} artifacts/signals accumulated with no home:
{chr(10).join('  - ' + str(i) for i in sorted(ids)[:10])}
- **What would move/link**: (session: list the artifact paths above that would move)
- **Initial structure**: DOMAIN_PROFILE.md only (skeleton rule — no empty scaffolding)
- **Needs a routine?** (default no — justify against ROUTINE_REGISTRY cost)
- **Needs a skill?** (default no — SKILL_FOUNDRY criteria)
- **Needs an agent?** (default no — AGENT_REGISTRY 'no decorative personas')
- **Estimated maintenance cost**: (touches per week × model tier; be honest)
- **Provisional or permanent**: provisional (30-day review; dissolves back to tasks if idle)
""")
        print(f"PROPOSED {path}")
        made += 1
    print(f"{made} proposal(s) {'would be ' if a.dry_run else ''}drafted "
          f"(threshold {a.threshold}); existing domains untouched: {sorted(domains)}")


if __name__ == "__main__":
    main()
