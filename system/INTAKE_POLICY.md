<!-- version: 1.0.0 (2026-07-11) | status: provisional until 2026-08-15 (system/V2_LEDGER.md) -->
# Life Intake Policy (the Router)

Any Brain-enabled session that receives a request from Brendan routes it here BEFORE
creating artifacts. Routing is model judgment assisted by `tools/route_intake.py`
(deterministic phrase/override detection — run it first; it suggests, you decide).
Scope honesty: routing happens only in Brain-enabled sessions; there is no platform-wide
tap on all conversations (docs/LIMITATIONS.md #3).

## The six modes (Brendan-facing vocabulary)

| Mode | What happens | Mechanics (3 primitives × 2 switches) |
|---|---|---|
| 1. Immediate answer | answer in-session, write NOTHING | answer_now, capture=no, expand=no |
| 2. Immediate + memory | answer now, capture the durable part | answer_now, capture=yes (per MEMORY_POLICY class) |
| 3. Immediate + overnight expansion | best-effort answer now, deep pass tonight | answer_now + task (`--depth deep`), capture optional |
| 4. Same-day operational task | do/plan it before its deadline today | task (`--urgency high/urgent --deadline today`) |
| 5. Background research | queued research, surfaces when done | task (default flags; `--publish newspaper` only if he wants it in the paper) |
| 6. Ongoing watch | recurring check until stopped | watch (`--recurrence watch`) |

Every mode compiles to: **answer_now? · task/watch file? · capture-to-memory?** — reusing
existing `new_task.py` flags (urgency/depth/deadline/effort/publish/recurrence). No new
queue machinery.

## Decision factors (weigh all; any explicit override wins)
1. When does the information become useful? (before dinner ≠ tomorrow's paper)
2. Does delay reduce its value? (perishable → answer now, even roughly)
3. Needed depth (quick fact vs multi-source comparison).
4. Does the request reveal a durable preference? → also log evidence (PROPOSED_RULES).
5. Is clarification blocking? → ask NOW; else record assumption and proceed.
6. Can a useful preliminary answer be given immediately? (usually yes — give it)
7. Would a future article still add value after the quick answer? → mode 3.
8. Time-sensitive subject (listings, prices, events) → verify near use; consider watch.
9. Fits an existing domain? route there; else `domain: general` or concierge.
10. Might it justify a NEW domain? → note the signal; `tools/propose_domains.py` decides
    on accumulation, never on one question (DOMAIN_POLICY).

## Defaults when unstated
- One-off factual/tech question ("how do I free iPhone storage?") → mode 1. **Ephemeral:
  write nothing** — no timeline entry, no task, no preference note. A one-off question is
  not an interest signal.
- "Research X" with no deadline → mode 5, `--publish file_only` unless he says paper.
- Cooking/meal planning for a named day → mode 4 if today, else mode 3 with the kitchen
  desk (domains/concierge/).
- Anything with "keep watching / track / alert me when" → mode 6.

## Natural overrides (never require a form; phrases are examples, not syntax)
"Answer this now" → 1 · "quick answer and research it overnight" → 3 ·
"put this in tomorrow's paper" → 5 + `--publish newspaper` · "this is just a one-off" → 1 ·
"remember this" → 2 · "do not save this" → force capture=no (and delete nothing else) ·
"make this a watch" → 6 · "I need this before dinner" → 4.

## Telling Brendan (mandatory, one sentence, plain language)
State what you decided and how to override, e.g.: "Quick answer below; I've also queued a
deep overnight pass for tomorrow's paper — say 'skip the overnight' if you just wanted the
answer." Never silently queue, never silently capture.

## Ephemeral guarantee (tested)
Mode 1 leaves the repo byte-identical (no artifact, no evidence line, no index change).
If Brendan later says "actually remember that", capture then — from his words, not from a
hidden log.
