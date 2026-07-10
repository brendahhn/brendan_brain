<!-- version: 1.0.0 (2026-07-10) -->
# Reading & Annotating the Newspaper

## Simple version
Open the newest file in `newspaper/editions/` (GitHub web is fine). Read. Type reactions
directly under the items they're about. Commit. The next daily run does the rest.

## The labels you'll see on every item
[FACT] confirmed · [CONC] research conclusion · [OBS] uncertain observation · [ASSUME]
assumption in force · [PRED] prediction · [PREF] preference · [RULE?] proposed rule ·
[RULE] confirmed rule · [Q] question for you · [FAIL] failed/incomplete (never hidden).
Robots' evidence tiers (S/A/B/C/Speculative) appear inside items.

## Your annotation vocabulary
Put these on their own line under the item (or after `>>`):

| Mark | What happens next run |
|---|---|
| ⭐ | "important" evidence → more of this, sooner |
| 🙂 | "more like this" evidence |
| ❌ | "not useful" evidence (one ❌ ≠ banned topic) |
| `INCORRECT …` or `CORRECTION …` | high-urgency re-verification task; if wrong, a superseding correction (history kept) |
| `QUESTION: …` | becomes a queue task; answered in a future edition |
| `DEEPER` | deep follow-up research task on that item |
| `WATCH` | recurring watch created on that topic |
| `STOP COVERING` | topic goes on the rejected list immediately (explicit = instant) |
| `REMEMBER THIS: …` | capture task → durable knowledge with provenance |
| `FORGET THIS: …` | forgetting request task — you get a PLAN first; nothing is deleted without your confirmation |
| `CHANGE PREFERENCE: …` | written up as a proposed rule for your confirmation |
| `>> anything else` | freeform note → recorded as evidence/context |

## The safety rails
- One reaction is **evidence**, never a rule. Rules need ≥3 consistent signals across ≥2
  days, or your explicit instruction ("always/never/stop").
- An ambiguous ❌ triggers a clarifying question in the next edition, not a guess.
- Reactions attach to the nearest `###` item heading — react under the right item.

## Processing manually (optional)
`python3 tools/process_annotations.py --date <edition-date>` shows the plan;
add `--apply` to execute. The daily routine does this automatically.
