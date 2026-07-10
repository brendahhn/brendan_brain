<!-- version: 1.0.0 (2026-07-10) -->
# Adding Research

## Simple version
In any Claude session that has `brendan_brain` attached, just say what you want:
> "Add an idea to research four-cylinder Tacomas. Put it in tomorrow's newspaper and ask
> me questions if needed."

Claude (via the brain-ops skill) creates the task, asks intake questions right away,
records assumptions for anything you don't answer, and research proceeds.

## What your words turn into
| You say | The task gets |
|---|---|
| "research this now" | `urgency: urgent` (preempts other work) |
| "before tomorrow morning" | `deadline: <date>` + newspaper destination |
| "quick answer" | `depth: quick`, one pass |
| "go deep" / "until the evidence is strong" | `depth: deep`, `effort: until_strong` |
| "one research pass only" | `effort_budget: 1_pass` |
| "give it 500 words" | `word_budget: 500` |
| "make it a weekly watch" | a watch with `next_run` maintained by the scheduler |
| "don't put it in the paper" | `publication_destination: file_only` |

## Duplicates are fine
Ask for the same thing twice (even from different conversations) and the system finds the
existing task by its `dedupe_key`, notes "+1 interest," and does NOT create a duplicate.

## Questions and assumptions
- **Blocking** question → task waits for you (shows in QUEUE.md + every newspaper).
- **Material but not blocking** → research continues on a WRITTEN assumption; the question
  rides in the paper until you answer (annotate `>> answer: …` right on it).
- Discovered mid-research questions work the same way — they never silently die.

## Doing it by hand (works from the GitHub web editor too)
Create a file in `queue/inbox/` following the template in `system/SCHEMAS.md`, or run:
`python3 tools/new_task.py --title "..." --domain vehicles --request "..." [flags]`
Then: `python3 tools/build_queue_dashboard.py` to refresh QUEUE.md.
