#!/usr/bin/env python3
"""Sensitivity-gated retrieval over the Brain (RETRIEVAL_POLICY.md).
Usage: brain_search.py "query terms" [--domain D] [--type T] [--since YYYY-MM-DD]
       [--allow-sensitive REASON] [-n N]
Sensitive artifacts (health/private/financial) are returned ONLY if --domain matches the
artifact's domain, or --allow-sensitive REASON is given (reason echoed to stderr so callers
must log it)."""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import iter_artifacts, SENSITIVE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--domain")
    ap.add_argument("--type", dest="atype")
    ap.add_argument("--since")
    ap.add_argument("--allow-sensitive", dest="allow", metavar="REASON")
    ap.add_argument("-n", type=int, default=10)
    a = ap.parse_args()
    terms = [t.lower() for t in re.findall(r"\w+", a.query) if len(t) > 1]
    # light stemming for recall: also match singular forms (arch review finding #8)
    terms = list({t[:-1] if len(t) > 3 and t.endswith("s") else t for t in terms})
    if a.allow:
        print(f"SENSITIVE ACCESS GRANTED — reason: {a.allow} (log this in your task/artifact)",
              file=sys.stderr)
    results, blocked = [], 0
    for rel, fm, body in iter_artifacts():
        dom = fm.get("domain", "")
        sens = fm.get("sensitivity", "personal") or "personal"
        # FAIL CLOSED: health/financial DOMAINS are sensitive regardless of the field
        # (arch review 2026-07-10 finding #3 — a missing sensitivity line must not leak)
        if dom == "health" and sens not in ("health", "private"):
            sens = "health"
        if dom == "investing" and sens == "personal":
            sens = "financial"
        if a.atype and fm.get("artifact_type") != a.atype:
            continue
        if a.domain and dom != a.domain:
            continue
        if a.since and str(fm.get("created_at", ""))[:10] < a.since:
            continue
        meta = " ".join([str(fm.get("title", "")),
                         " ".join(fm.get("topics", []) if isinstance(fm.get("topics"), list) else []),
                         " ".join(fm.get("entities", []) if isinstance(fm.get("entities"), list) else []),
                         dom]).lower()
        blo = body.lower()
        score = sum(3 for t in terms if t in meta) + sum(1 for t in terms if t in blo)
        if score <= 0:
            continue
        if sens in SENSITIVE and not (a.domain and a.domain == dom) and not a.allow:
            blocked += 1
            continue
        score += 1 if (a.domain and dom == a.domain) else 0
        results.append((score, str(fm.get("created_at", "")), fm.get("id"), rel,
                        str(fm.get("title", ""))[:70], sens))
    # score desc, then recency desc (arch review finding #8: old double-sort left ties oldest-first)
    results.sort(key=lambda r: (r[0], r[1]), reverse=True)
    for score, dt, aid, rel, title, sens in results[:a.n]:
        print(f"{score:>3}  {aid:<38} {rel:<55} [{sens}] {title}")
    if blocked:
        print(f"note: {blocked} sensitive artifact(s) matched but were withheld "
              f"(pass --domain <their domain> or --allow-sensitive REASON)", file=sys.stderr)
    if not results:
        print("no matches")


if __name__ == "__main__":
    main()
