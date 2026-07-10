<!-- version: 1.0.0 (2026-07-10) -->
# Best Practices — getting the most out of Brendan OS

## Asking for research
1. **Describe the outcome, not the method**: "find me a 2002-2004 Tacoma, 2.4L, extra cab,
   San Diego area, under $12k, manual" beats "search Craigslist."
2. **Urgency** only when it's real: "research this now" preempts other work; default is
   fine for most things.
3. **Depth**: "quick answer" (one pass, short), nothing (standard), "go deep / keep going
   until the evidence is strong" (multi-pass with verification).
4. **Deadline**: "before tomorrow morning" or "by Friday" — it lands in the task and the
   dashboard sorts by it.
5. **Word budget**: "give it 300 words in the paper" — budgets are editorial guidance, not
   quotas; nothing gets padded.
6. **Hard requirements vs preferences**: say which. "MUST be 2002-2004; prefer under 150k
   miles" → constraints vs. assumptions are recorded separately.
7. **Invite questions**: "ask me questions if needed" → useful intake questions arrive
   immediately, non-blocking ones ride in the newspaper.
8. **Let it continue**: "keep going with reasonable assumptions" — every assumption is
   written down in the task and shown to you, never silent.
9. **Watches**: when the answer changes over time (listings, prices, a player's status) —
   "make this a weekly watch." One-off questions don't need one.

## Teaching the system
10. **Correct it in place**: annotate INCORRECT with a word of why, or say "this was
    wrong: …" — a high-urgency correction task re-verifies and supersedes (history kept).
11. **Don't overteach**: one ❌ is one signal. If you want a permanent change, SAY it
    ("stop covering X" / "always Y") — explicit beats inferred, and the system is built to
    refuse learning rules from single reactions.
12. **Annotate little and often** — three honest reactions a day beat a monthly essay.
13. **Deeper**: write DEEPER on the item; the follow-up task inherits the topic.
14. **New domain**: "create a domain for this" once a topic is really yours (3+ artifacts
    or a standing interest) — otherwise a task or watch is enough.
15. **Ask what it knows**: "what does the Brain know about X?" before re-explaining
    something — it answers from artifacts and cites ids.
16. **Forgetting**: "forget that observation about …" → you get a plan (what's removable,
    what lives in Git history) and NOTHING is deleted until you confirm.
17. **Sensitive things**: keep them in their domain (health stuff via the health robot or
    clearly marked); never paste employer data here (see MEMORY_AND_PRIVACY.md).
18. **Work/personal**: a future work system gets its own repos and account. If you catch
    yourself pasting work data into a personal session — stop; that's the one boundary
    with no undo.

## Reading the system
19. **Uncertainty is labeled**: [OBS]/[ASSUME]/Speculative tiers mean "not established."
    If a claim looks confident, check its label and source link before acting on it.
20. **Did a routine actually run?** Its outbox file (`queue/inbox/from-<robot>.md`) gets a
    dated block every run; the newspaper reports missing blocks as failures. Robot-side:
    the notebook CHANGELOG in its own repo.
21. **Token thrift**: quick questions in one-off sessions; save deep multi-agent work for
    things that matter (staffing policy already refuses decorative agents). "Quick answer"
    is your friend.
22. **Improve by using, not rebuilding**: annotate, answer questions, correct mistakes.
    The system proposes its own improvements in the paper when evidence accumulates —
    redesigns should be rare and evidence-driven.

## Worked examples (your actual domains)
- **Tacoma**: "Add to my queue: find a 2002-04 Tacoma 2.4L Xtracab, San Diego, ≤$12k,
  manual only, condition over miles. Weekly watch, verify listings before publishing, ask
  me anything material." → task + watch + intake questions, listings verified near print.
- **Health**: "Ask the health domain: what did chapter 12 conclude about zone 2 volume?"
  → domain-scoped retrieval; personal values stay in health-notebook.
- **Fantasy**: "Queue for FootyBot's domain: how have my league's 10-team half-PPR RB
  values shifted since the schedule release? 400 words tomorrow." → task lands in
  fantasy_football; tonight's robot run picks it up.
- **Stocks (paper)**: "Have the trading desk research whether the USO thesis survives the
  latest inventory data — deep, opus review." → investing task, escalated review, outcome
  scored against the original prediction (never rewritten).
- **Jobs**: "Add a watch: RevOps openings at [company] — only verified-active listings,
  only in the paper if something new." → verified-only rule already enforced.
- **News**: "More surf-industry business coverage, less general tech." → preference
  evidence now, INTEREST_PROFILE weights shift with repetition or your explicit rule.
- **Surf data**: "When I upload my WSL dataset, find overlooked predictors of heat wins —
  exploratory, flag anything surprising for a stats review." → Data Lab pattern
  (docs/DATA_LAB.md), opus checks surprises before you see them.
- **Brand-new hobby** ("I'm getting into fermentation"): mention it → interest evidence;
  "create a domain for it" → `domains/fermentation/` + profile; a robot only if you later
  want scheduled unattended research (the system will propose it if volume justifies).
