<!-- version: 1.1.0 (2026-07-11) — V2 -->
# START HERE

> **V2 (2026-07-11)**: Brendan OS now also runs practical daily life — just talk to it
> ("plan this menu", "research overnight", "keep an eye on…", "don't save this"). New-user
> tour: `docs/CONCIERGE_AND_V2_GUIDE.md`. Your one-time setup steps:
> `docs/ROUTINE_SETUP_GUIDE.md`. Git rules: `docs/GIT_WORKFLOW.md`.

## The short version

**Brendan OS is a shared memory and a morning newspaper for all your Claude robots.**

- **The Brain lives at** `github.com/brendahhn/brendan_brain` (this repo). Everything it
  knows is a Markdown file you can open, edit, or delete.
- **Your robots stay where they are**: FootyBot (`brendahhn/FootyBot`), Health Robot
  (`brendahhn/health-notebook`), Trading Robot (`brendahhn/trading-notebook`), Jobs Robot
  (`brendahhn/operator-notebook`). They work exactly like before — plus, when the Brain is
  present, they read your shared preferences at the start of a run and drop a short summary
  into the Brain at the end.
- **Information moves in one simple loop**: robots and conversations write into the Brain →
  the daily run picks the best of it into a newspaper → you react on the newspaper → your
  reactions change what happens next.

## What happens when…

- **You add an idea** ("add researching X to my queue"): a task file appears in `queue/`,
  Claude asks any useful questions immediately, and research proceeds — using stated
  assumptions if you don't answer.
- **Research hits a question**: it's written into the task and shows up in the next
  newspaper under "Questions For Brendan." Work continues on assumptions unless the
  question truly blocks it.
- **The newspaper appears** (`newspaper/editions/YYYY-MM-DD.md`): only things worth your
  attention — sections with nothing meaningful say so in one line.
- **You annotate it** (⭐ 🙂 ❌, or keywords like DEEPER / WATCH / STOP COVERING /
  QUESTION: / REMEMBER THIS: / FORGET THIS: / CHANGE PREFERENCE: / INCORRECT): the next
  run turns those into follow-up research, watches, corrections, and preference evidence.
  **One reaction never becomes a permanent rule** — rules need repeated evidence or your
  explicit say-so.

## What Claude remembers vs. doesn't

- **Remembers** (because it's in this repo): queue tasks, timeline observations you asked
  to capture, research findings, your preferences and rules, predictions and outcomes,
  questions and answers.
- **Does NOT automatically remember**: anything from conversations that don't have this
  repo attached, or things you mention casually that you didn't ask to keep. If you want
  it kept, say "remember this" or "add this to the Brain."

## Every morning (2 minutes)

Open the newest file in `newspaper/editions/` on GitHub. Read it. React inline. Commit.

## When something looks wrong

Say to Claude (in a session with this repo): "something looks wrong — check system
status." It will run `tools/oplog.py status`, the test suite, and read
`system/SYSTEM_HEALTH.md`. Also see `docs/TROUBLESHOOTING.md`.

## The five most useful things you can say

1. "**Add this to my research queue**: … — put it in tomorrow's newspaper, ask me
   questions if needed."
2. "**What's waiting for me?**"
3. "**What does the Brain know about** …?"
4. "**Make this a weekly watch.**"
5. "**Remember this:** …" (or "**Forget** that observation about …")

## ⚡ Flip the switch (the only 2 things I could not do for you)

Everything is merged and tested, but two settings live in the claude.ai routines screen,
which no tool in a coding session can reach — that's why these are yours:

**1. Give your four robots the Brain (once, ~2 min).**
- Open **claude.ai → your scheduled tasks/routines list** (where you created FootyBot,
  Health Robot, Trading Robot, Jobs Robot).
- For **each** of the four routines: open it → **repository selection** → **add
  `brendahhn/brendan_brain`** alongside its existing repo → save.
- Why you: routine configurations are only editable in that UI, not from any session.
- Verify: after each robot's next scheduled run, its repo's notebook CHANGELOG mentions
  brain-sync, and `brendan_brain/queue/inbox/from-<robot>.md` has a new dated block.
  (If a robot runs without the Brain attached, nothing breaks — the steps no-op.)

**2. Create the daily Brendan OS routine (once, ~2 min).**
- Same screen → **new scheduled task/routine** → repositories: **`brendahhn/brendan_brain`**
  (adding the four robot repos too is optional but lets the daily run double-check them) →
  schedule: **daily, ~6:00 AM Pacific** (after the robots' overnight runs) → prompt: paste
  the contents of **`system/DAILY_ROUTINE_PROMPT.md`**.
- Verify: tomorrow there's a new file in `newspaper/editions/` and you got a notification
  with 3-5 headlines.
