<!-- version: 1.0.0 (2026-07-10) -->
# Brendan's Daily Guide — how to actually use this thing

## Morning (2 minutes)
Open `newspaper/editions/<today>.md` on GitHub (or wherever it was delivered). React inline:
- `⭐` important · `🙂` more like this · `❌` not useful
- Freeform lines starting with `>>`:
  `>> research this deeper` · `>> make this a watch` · `>> stop covering this` ·
  `>> wrong — <why>` · `>> answer: <your answer to a question>` · anything else you want noted
Commit the edit (GitHub web editor is fine). The next Brendan OS session processes it —
reactions become evidence (never instant rules), corrections become high-urgency tasks,
watches get created, answers unblock tasks.

## During the day, from ANY Brain-enabled Claude session
Just talk. These all work (brain-ops skill translates them):
- "Add an idea to research X. Put it in tomorrow's newspaper, ask me questions if needed."
- "Research this now / before tomorrow / deeply / in one pass."
- "Make this a weekly watch." · "Give it 800 words."
- "Remember this." · "Add this to the Brain."
- "What does the Brain know about X?" · "What's in my queue?" · "What's waiting for me?"
- "This was wrong." · "I liked this." · "Stop showing me this."
- "Forget that observation" (you'll get a plan and a confirmation step before anything is deleted).

A session is Brain-enabled when the `brendan_brain` repo is in its repo selection (cloud)
or cloned alongside (local).

## What the robots do with it (once you flip them on — see TO ACTIVATE below)
Each robot reads your confirmed rules, its domain's open tasks, and your answers at run
start; at run end it drops a summary block into `queue/inbox/from-<robot>.md` — that's what
feeds the newspaper. Their own notebooks and prompts are untouched and still theirs.

## Weekly (5 minutes, optional)
- Skim `QUEUE.md` — anything stuck in `waiting_for_brendan` is waiting on YOU.
- Skim `preferences/PROPOSED_RULES.md` — approve/reject proposals (move to CONFIRMED/REJECTED).
- `CURRENT_PRIORITIES.md` is yours — edit it and triage follows.

## TO ACTIVATE the robot integrations (one-time, ~10 min)
1. Merge the four `claude/*-akjb28` integration branches (each adds 4 files, touches nothing else).
2. Add `brendan_brain` to each routine's repository selection.
3. Apply each repo's `proposed-prompt-change.md` (two lines) via a safe-bot-edits session.
4. Answer the two open questions in today's edition.

## If something looks broken
`python3 tools/oplog.py status` (unfinished cross-repo ops), `tests/run_all.sh` (8 suites),
`system/SYSTEM_HEALTH.md` (last known state). Failures are supposed to be reported in the
newspaper — silence about a failure is itself a bug, tell the next session.
