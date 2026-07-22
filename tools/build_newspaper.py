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
from brainlib import ROOT, iter_artifacts, today, SENSITIVE, is_active_watch

# Budgets + order redesigned per Brendan 2026-07-21 (D63): top-3 headlines first, investing
# condensed with a portfolio table, jobs as real listings, health in plain defensible English,
# footy shrunk (being retired), new challenge desk / tea / gym-oura sections.
BUDGETS = {"top_headlines": 120, "most_important": 150, "investing": 450, "jobs": 300,
           "health": 400, "challenge_desk": 220, "tea_business": 220, "gym_oura": 160,
           "fantasy_football": 140, "news": 300, "concierge": 250, "open_research": 400,
           "questions_and_system": 200}
# Sections the editor always fills by hand (never auto-collected) — emit a prompt, never drop.
EDITORIAL_SECTIONS = ("top_headlines", "most_important", "challenge_desk")
# robots whose missing output is NEWS (SCHEDULE_PLAN gate): section ← expected outbox
GATED_INPUTS = {"trading-robot": "investing", "jobs-robot": "jobs",
                "footybot": "fantasy_football", "health-robot": "health"}

# CONTENT-level medical/health scrub for ANY prose about to enter the paper (Chief Skeptic
# C1/M3, 2026-07-11): the sensitivity FIELD is not enough — a personal-tagged concierge task
# can carry health inference in its Findings prose or a health_alignment reason. This scans
# the actual text. Order matters: this is a leak wall, so it errs toward redaction.
MEDICAL = re.compile(
    r"health_alignment|strongly[_ ]aligned|generally[_ ]aligned|potentially[_ ]conflicting"
    # dose/biometric units only — NOT lb/kg, which are grocery weights in kitchen prose
    # (final merge-gate review D1: '2 lb chuck roast' redacted the whole cooking article;
    # body-weight in HEALTH exports is still caught by the robot-outbox scrub below)
    r"|\b\d+\s?(mg|mcg|bpm|mmol|mg/dl|iu)\b"
    r"|\b(ldl|hdl|a1c|hba1c|cholesterol|triglyceride|lipid panel|blood pressure|glucose"
    r"|hypertension|diabetes|diagnos(is|ed|e)|prescrib(ed|ption)|cardiologist|symptom"
    r"|dose|dosage|biometric|lab result|blood test)\b", re.I)


def trim(text, n):
    """Word-boundary truncation with a visible marker (QA defect #1, 2026-07-11 — raw
    slices cut mid-word with no indication content was dropped)."""
    if len(text) <= n:
        return text
    cut = text[:n]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + " […]"


def scrub_medical(summary, rel, section, sens):
    """Redact prose that reveals health state before it reaches the paper. Returns the
    (possibly redacted) summary. Health-section generic conclusions are allowed; every
    other section is scrubbed if medical content appears."""
    if sens in SENSITIVE:
        return (f"(sensitive {sens} content — see `{rel}` directly; only generic "
                f"conclusions may be quoted here by the editor)")
    if section != "health" and MEDICAL.search(summary):
        return (f"⚠️ HEALTH-LEAK REDACTION: `{rel}`'s findings contain health-derived "
                f"content that must not appear outside the health section (KITCHEN_PROFILE "
                f"bridge rule 3 / PUBLICATION_POLICY). Editor: write a generic, non-medical "
                f"line by hand if this belongs in the paper, or drop it. Nothing auto-quoted.")
    return summary


def collect_challenge_signals(date):
    """Challenge desk (D63): surface stale projects and stale open tasks so the editor can
    push back. Read-only heuristics; the editor writes the actual challenge prose."""
    sigs = []
    try:
        cutoff = (datetime.date.fromisoformat(date) - datetime.timedelta(days=10)).isoformat()
        for rel, fm, _ in iter_artifacts():
            at, st = fm.get("artifact_type"), str(fm.get("status", ""))
            upd = str(fm.get("updated_at") or fm.get("created_at") or "")
            if at == "task" and st in ("active", "open", "in_progress") and upd and upd < cutoff:
                sigs.append((fm.get("id"), f"stale task: {fm.get('title','?')}",
                             f"open since {upd}, untouched ≥10 days", rel))
    except Exception:
        pass
    return sigs


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
            sec = dom if dom in items else "open_research"
            summary = scrub_medical(summary, rel, sec, sens)
            items[sec].append((fm.get("id"), fm.get("title"), trim(summary, 2000), rel))
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
                    items[sec].append((fn, f"{dom} robot report {m.group(1)}", trim(b, 2500),
                                       f"queue/inbox/{fn}"))
    # input gate (SCHEDULE_PLAN): a robot with no fresh block is NEWS, not silence; a robot
    # whose only block is yesterday's is STALE, not current (Chief Skeptic M4)
    for aid, title, why, rel in collect_challenge_signals(date):
        items["challenge_desk"].append((aid, title, why, rel))
    from check_inputs import input_status
    for name, fresh, last, state in input_status(date):
        if name not in GATED_INPUTS:
            continue
        if state == "missing":
            items[GATED_INPUTS[name]].append(
                (f"gate-{name}", f"[FAIL] {name}: no output for this edition",
                 f"[FAIL] {name} produced no fresh block (last: {last or 'never'}) as of "
                 f"this draft. Reported honestly per SCHEDULE_PLAN — nothing fabricated. "
                 f"If it lands before the Publisher pass, the editor may pull it in.",
                 "system/SCHEDULE_PLAN.md"))
        elif state == "stale":
            items[GATED_INPUTS[name]].append(
                (f"stale-{name}", f"[STALE] {name}: today's run has not landed",
                 f"[STALE] The {name} content above is from {last} (yesterday); today's run "
                 f"had not produced a block as of this draft. Treat as [STALE], not current "
                 f"— re-verify before relying on it (SCHEDULE_PLAN, Chief Skeptic M4).",
                 "system/SCHEDULE_PLAN.md"))
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
# 🗞️ Brendan's Daily — {datetime.date.fromisoformat(a.date).strftime('%A, %B %-d, %Y')} (DRAFT)

> _Morning edition. Evening runs (after 8pm PT) build the NEXT morning's paper, so an
> edition dated tomorrow is normal — it's the paper you'll read when you wake up._
>
> Editor per PUBLICATION_POLICY §Section rules (Brendan 2026-07-21): top-3 real headlines
> first; investing = trades + why + portfolio table + all-time vs SPY (no bot play-by-play);
> jobs = actual listings with apply links + why-fit; health in plain, defensible English;
> footy small; fill the challenge desk. Trim to budgets, then the Publisher checklist.
"""]
    order = ["top_headlines", "most_important", "investing", "jobs", "health",
             "challenge_desk", "tea_business", "gym_oura", "fantasy_football", "news",
             "concierge", "open_research", "questions_and_system"]
    PROMPTS = {
        "top_headlines": "_(editor: 3 one-line headlines — the biggest world/market news "
                         "from the robots' [FACT] items, most important first)_\n",
        "most_important": "_(editor selects 1-3 items from below and summarizes here)_\n",
        "challenge_desk": "_(editor: 1-3 honest pushbacks — stale projects, todos being "
                          "avoided, contradictions between stated priorities and behavior; "
                          "see CHALLENGE_DESK sources below)_\n",
    }
    empty = []
    for sec in order:
        got = items.get(sec, [])
        if not got and sec not in EDITORIAL_SECTIONS:
            empty.append(sec)
            continue
        lines.append(f"\n## {sec.replace('_', ' ').title()}  (budget ~{BUDGETS[sec]}w)\n")
        if sec in PROMPTS:
            lines.append(PROMPTS[sec])
        for aid, title, summary, rel in got:
            lines.append(f"### {title}\n<sub>source: [`{aid}`]({rel})</sub>\n\n{summary}\n")
    if empty:
        lines.append("\n---\n_Nothing meaningful today in: " +
                     ", ".join(e.replace('_', ' ') for e in empty) + "._\n")
    # system panel: LIVE watches only — shared eligibility with the watch runner
    # (brainlib.is_active_watch, production bug B: a cancelled synthetic watch once
    # surfaced here because this loop had its own weaker filter)
    sysex = []
    for rel, fm, _ in iter_artifacts():
        if is_active_watch(fm, rel):
            sysex.append(f"- Watch `{fm.get('id')}` — next run {fm.get('next_run') or 'due now'}")
    ops = os.path.join(ROOT, "system", "operations")
    if os.path.isdir(ops):
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "oplog.py"), "status"],
                           capture_output=True, text=True)
        if "0 unfinished" not in r.stdout:
            sysex.append("- ⚠️ Unfinished cross-repo operations: " + r.stdout.strip().replace("\n", "; "))
    if sysex:
        lines.append("\n## Watches & System\n" + "\n".join(sysex) + "\n")
    lines.append("\n---\n_**Labels**: [FACT] confirmed · [CONC] research conclusion · [OBS] "
                 "uncertain observation · [ASSUME] assumption · [PRED] prediction · [PREF] "
                 "preference · [RULE?] proposed rule · [RULE] confirmed rule · [Q] question · "
                 "[FAIL] failed/incomplete. Evidence tiers S/A/B/C from the robots ride along._\n")
    lines.append("\n---\n_Annotate inline: ⭐ important · 🙂 more like this · ❌ not useful · "
                 "or keywords on their own line: INCORRECT · CORRECTION · QUESTION: … · DEEPER "
                 "· WATCH · STOP COVERING · REMEMBER THIS: … · FORGET THIS: … · CHANGE "
                 "PREFERENCE: … · freeform after `>>`. Then run the brain-newspaper skill's "
                 "annotation flow (or `python3 tools/process_annotations.py --apply`)._\n")
    os.makedirs(os.path.dirname(draft), exist_ok=True)
    open(draft, "w", encoding="utf-8").write("\n".join(lines))
    n = sum(len(v) for v in items.values())
    print(f"draft written: newspaper/drafts/{a.date}.md ({n} candidate items, "
          f"{len(empty)} empty sections)")


if __name__ == "__main__":
    main()
