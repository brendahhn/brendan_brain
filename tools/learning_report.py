#!/usr/bin/env python3
"""Draft the weekly Learning & Improvement report (LEARNING_POLICY / CONTINUOUS_IMPROVEMENT).
Mechanical evidence-gathering only — a session refines the draft; the report NEVER changes
behavior itself. Material-change gate: with fewer than --min-signals fresh signals in the
window, writes a one-line stub and exits 0 (no ritual reviews of an idle system).

Usage: learning_report.py [--week YYYY-Www] [--min-signals 5] [--days 7]
Signals gathered: preference-evidence lines in the window · annotations processed ·
new/changed artifacts · prediction outcomes scored · capacity ledger rows · repeated
topics in evidence (candidate rules) · interest-change hints (topics with opposite-sign
reactions). Output: system/reviews/<week>-review.md (refuses overwrite unless --force)."""
import argparse, os, re, sys, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brainlib import ROOT, iter_artifacts, today, now_pt

NEG = {"not_useful", "flag", "stop"}
POS = {"important", "more_like_this", "explicit"}


def main():
    ap = argparse.ArgumentParser()
    now = now_pt().date()
    ap.add_argument("--week", default=f"{now.isocalendar()[0]}-W{now.isocalendar()[1]:02d}")
    ap.add_argument("--min-signals", type=int, default=5)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    since = (now - datetime.timedelta(days=a.days)).isoformat()
    outdir = os.path.join(ROOT, "system", "reviews")
    out = os.path.join(outdir, f"{a.week}-review.md")
    if os.path.exists(out) and not a.force:
        sys.exit(f"REFUSED: {out} exists (reviews are part of the audit trail; --force to redo)")

    evidence, topics = [], collections.defaultdict(list)
    prop = os.path.join(ROOT, "preferences", "PROPOSED_RULES.md")
    if os.path.exists(prop):
        for line in open(prop, encoding="utf-8"):
            m = re.match(r"- (\d{4}-\d{2}-\d{2}) \| (\w+) \| ([^|]+)\|", line)
            if m and m.group(1) >= since and "SYNTHETIC" not in line:
                evidence.append(line.strip())
                topics[m.group(3).strip().lower()[:40]].append(m.group(2))
    fresh_artifacts = [(rel, fm) for rel, fm, _ in iter_artifacts()
                       if str(fm.get("created_at", ""))[:10] >= since]
    outcomes = [fm for _, fm in fresh_artifacts if fm.get("artifact_type") == "outcome"]
    annotations = [fm for _, fm in fresh_artifacts if fm.get("artifact_type") == "annotation"]
    ledger_rows = 0
    led = os.path.join(ROOT, "system", "CAPACITY_LEDGER.md")
    if os.path.exists(led):
        ledger_rows = sum(1 for l in open(led, encoding="utf-8")
                          if re.match(r"\| \d{4}-\d{2}-\d{2} ", l) and l[2:12] >= since)
    signals = len(evidence) + len(outcomes) + len(annotations) + ledger_rows

    os.makedirs(outdir, exist_ok=True)
    if signals < a.min_signals:
        open(out, "w", encoding="utf-8").write(
            f"# {a.week} review — nothing material\n\nGate: {signals} signal(s) since "
            f"{since} (< {a.min_signals}). No review run; this stub is the honest record.\n")
        print(f"stub written ({signals} signals < {a.min_signals}): {out}")
        return

    # repeated-reaction candidates (≥3 same-direction signals per MEMORY_POLICY)
    candidates, conflicts = [], []
    for t, sigs in topics.items():
        pos = sum(1 for s in sigs if s in POS)
        neg = sum(1 for s in sigs if s in NEG)
        if pos + neg >= 3 and (pos == 0 or neg == 0):
            candidates.append(f"- `{t}`: {pos + neg} consistent signals → check ≥2-day "
                              f"spread, then PROPOSE (never self-confirm)")
        elif pos and neg:
            conflicts.append(f"- `{t}`: mixed reactions ({pos}+/{neg}-) → possible interest "
                             f"CHANGE — draft a dated proposal + question; do NOT rewrite "
                             f"INTEREST_PROFILE silently")
    L = [f"""# {a.week} Learning & Improvement review (draft — session refines)

Window: {since} → {today()} · signals: {signals} (evidence {len(evidence)}, outcomes
{len(outcomes)}, annotations {len(annotations)}, ledger rows {ledger_rows})

## 1. Learned about Brendan (levels 1-2 — proposal-only)
""" + ("\n".join("- " + e for e in evidence) or "- (no fresh evidence)"), """
## 2. Rule-threshold candidates (MEMORY_POLICY: ≥3 signals, ≥2 days)
""" + ("\n".join(candidates) or "- none reached threshold"), """
## 3. Possible interest changes (propose, never rewrite)
""" + ("\n".join(conflicts) or "- none detected"), f"""
## 4. Own performance (levels 3-5 — observations only)
- Prediction outcomes scored this window: {len(outcomes)} (calibration notes: session fills from outcomes/)
- Capacity ledger rows: {ledger_rows} (staffing verdicts: session summarizes; 3-strike retirements?)
- Retrieval/search failures observed: (session fills from task logs)

## 5. Assumptions that changed
- (session fills, citing artifacts)

## 6-9. Proposed changes (each as an OCI 8-field proposal; MAX 3 open system-wide)
- (session drafts here or notes "none earned")

## 10. Experiments for the coming week
- (only from open proposals; each names its rollback)

---
_Gate honesty: this report observes; enactment goes through PROPOSED_RULES → Brendan
(LEARNING_POLICY). Consequential items → newspaper questions section._
"""]
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(f"draft review written: {out} ({signals} signals)")


if __name__ == "__main__":
    main()
