## 2026-08-26 — footybot interactive session (Brendan-directed analysis, not a scheduled run)
- headline: Brendan asked FootyBot to test his own theory — "RBs are incredibly valuable in my league" — against 7 years of the league's real draft boards, at four cutoffs (RB count through rounds 2/4/6/8). **Verdict: not supported.** Every RB signal in the standings leans his way and every WR mirror leans against, but nothing survives correcting for having tried four cutoffs (best family-wise p=0.071), and the far better-powered return test (N≈560 rounds-1-8 picks scored in his exact league formula) finds **no difference between an RB and a WR taken at the same draft cost, in any round window** (largest gap +9.5 season points at p=0.50). The one near-significant result runs *against* the theory: RBs drafted in rounds 7-8 bust (<50 points all season) 16% of the time vs 5% for WRs (p=0.051). Full writeup: footybot `research/rb-draft-timing.md`; rebuild with `pipeline/rb_draft_timing.py`.
- newspaper_ready:
  - Cross-domain reasoning principle, earned this session: a hypothesis can be *directionally consistent everywhere you look* and still be **unmeasurable** — eight tests all leaning the same way is not evidence when trying eight tests is what produced the best one. The right verdict was "undetectable at this sample size," not "true" and not "disproven." [general principle]
  - Correction to a prior FootyBot claim: the 2026-07-12 line "reinforces don't punt RB" was a one-season PPG snapshot, not an outcome test. Tested against actual league results, drafting more RBs early does **not** predict finishing better here — and the league's only true WR-first drafter (Jack) has the best 6-year mean finish (3.50). [directional, N=60 manager-seasons]
  - Brendan's own draft posture for Aug 28: take the best player at #4 (if that's the RB, fine — but because he's the best player, not for a positional premium that isn't measurable); rounds 3-4 position-agnostic; stop force-feeding RB from round 5, where the RB left tail gets fat. [directional]
- questions_for_brendan: **The 2024 final-standings page is now a hard blocker, not a nice-to-have** (this is standing ask #2, third time raised). Without it, 10 of 70 manager-seasons are silently dropped from every draft-vs-outcome analysis in the repo — it is the single cheapest way to sharpen this whole line of research. Other standing asks unchanged: (1) Sleeper half-PPR ADP export; (3) per-season transaction logs.
- proposed_durable_knowledge: none promoted. Explicitly NOT promoting "RBs aren't more valuable here" to a confirmed rule — the honest finding is that N=60 manager-seasons cannot resolve it either way. Re-test when 2024 standings and each new season land.
- predictions: none.
- run_status: success (interactive, Brendan-directed). Committed to footybot branch `claude/rb-draft-timing-correlation-uomavg` (648f71b), verified via ls-remote; footybot `main` not advanced (the auto-merge Action only fires on `newsletters/**`, and this commit touches `pipeline/`, `research/`, notebook).



## 2026-07-15 — footybot run summary <!-- triaged 2026-07-15 -->
- headline: Newsletter 2026-07-15 shipped (44 days to draft). Pick-4 decision tree (JT >= Chase; the room decides which falls). Biggest catch: a current-reality board correction surfaced by the take-check — **Kenneth Walker III is a Kansas City Chief** (3yr/$43.05M FA), not a Seahawk as our board had it; he's KC's clear lead back now (Pacheco gone). This ALSO validated Brendan's own 2026-07-01 take ("Chiefs, heavy usage") — he was ahead of the bot.
- newspaper_ready:
  - Cross-domain decision principle (reinforced this run): being RIGHT about something is not a license to OVERPAY for it — Brendan's Kenneth Walker read was correct, but the market already priced it (early-2nd ADP), and paying the ceiling on a validated read is his actual leak. "Right thesis, wrong price" is a distinct failure from "wrong thesis." [general principle]
  - In his 6pt-passing-TD scoring, the QB dropoff is shallow past the elite top-3 (QB6→QB18 = only ~4.2 ppg across 12 QBs) → wait and stream QB unless a top-3 falls. [S, 2025 actuals]
  - His 2024 fantasy draft was cleaner than 2025: every hit was a "buy against the negative narrative + catalyst" (Mahomes, Achane, Nico), and it had zero paid-for-hype busts — reframing his one 2025 disaster (Brian Thomas Jr) as the deviation, not the baseline. [directional, n≈2 drafts]
- questions_for_brendan: none new. Standing asks unchanged: (1) paste a Sleeper half-PPR ADP export (only real gap in the board — Sleeper numbers are JS-hidden + WebFetch blocked); (2) the real 2024 final-standings page (last upload was a draft page); (3) per-season transaction logs to score in-season management.
- proposed_durable_knowledge: none promoted (self-scouting lens kept directional in footybot `research/self-scouting.md`, not a confirmed rule).
- predictions: none.
- run_status: success. 44 days to draft. All 4 lanes ran (Lane A orchestrator + B/C/D subagents) + reviewer; compete mode did not fire. Pushed footybot to harness branch `claude/gracious-darwin-8ryyjz` (95d67e07), verified via ls-remote; footybot `main` needs a manual FF-merge if the auto-merge Action didn't fire.

## 2026-07-14 — footybot run summary <!-- triaged 2026-07-15 -->
- headline: Decoded Brendan's own 2025 draft — his hits were "manufactured discount + catalyst" buys (Mahomes R10, Davante R6 +73.9, Walker R4 +56.2), his worst pick ever was paid-up hype (Brian Thomas Jr R2, -142.0). New self-scouting lens: his edge is price discipline buying media-made discounts, not any age/position "leak." Directional (n=16), rhymes with multi-year data.
- newspaper_ready: One cross-domain-worthy nugget if useful — a general decision principle ("buy manufactured discounts with a concrete catalyst; don't pay full freight for consensus hype"). Otherwise fantasy-internal; full edition at footybot `newsletters/2026-07-14.md`.
- questions_for_brendan: none new. Standing asks unchanged: (1) paste a Sleeper half-PPR ADP export (only real gap in the board); (2) the real 2024 final-standings page (last upload was a draft page); (3) per-season transaction logs to score in-season management.
- proposed_durable_knowledge: none promoted (2025-draft self-scouting pattern kept as directional in footybot `research/self-scouting.md`, not a confirmed rule).
- predictions: none.
- run_status: success. 45 days to draft. All 4 lanes ran (Lane A orchestrator + B/C/D subagents) + reviewer; compete mode did not fire. Pushed footybot to harness branch `claude/busy-knuth-cqbu6n` (6b7a2e2), verified via ls-remote; footybot `main` needs a manual FF-merge if the auto-merge Action didn't fire.

## 2026-07-12 — footybot run summary <!-- triaged 2026-07-15 -->
- headline: Newsletter 2026-07-12 shipped (47 days to draft). Rebuilt the top of Brendan's draft board on real pipeline-computed 2025 PPG in his exact scoring (tier C→S for ~40 players); resolved both standing ADP conflicts; caught two stale-board errors.
- newspaper_ready:
  - In Brendan's scoring (0.5-PPR, 6pt pass TD), 2025's top 6 were 5 RBs + Puka; the half-PPR "haircut" = exactly half a player's receptions/game, so pure runners (Henry −0.44/gm) barely move while reception WRs lose 3-4/gm. Reinforces "don't punt RB." [S, one-season snapshot]
  - Kyler Murray signed with Minnesota and is the reported projected Week-1 starter over J.J. McCarthy — firms the Justin Jefferson buy-low. [A]
  - De'Von Achane got a 4yr/$64M extension (3rd-highest-paid RB) = high floor, but a scrambling QB (Malik Willis) + the NFL's worst WR room cap his ceiling; value only if he slides past pick 4, not a target at 4. [A role / B projection]
  - ADP conflicts resolved: Bucky Irving ~50, Javonte Williams ~35. James Conner cratered to ~177 after Arizona drafted RB Jeremiyah Love 3rd overall. [A / B]
- questions_for_brendan: A pasted Sleeper half-PPR ADP export/screenshot would upgrade the whole ADP board from tier B to A (Sleeper numbers are JS-hidden + WebFetch blocked, unreachable from scheduled runs). Also still pending: the real 2024 final-standings page (last upload was a draft page) and per-season transaction logs.
- proposed_durable_knowledge: none (all domain-internal fantasy analysis)
- predictions: none this run (draft-outcome predictions deferred until closer to Aug 28)
- run_status: success

## 2026-07-10 — footybot run summary <!-- triaged 2026-07-10 -->
- headline: ACTIVATION SMOKE (not a research run): Brain integration merged to main (506eabc); brain-sync READ+WRITE exercised from the merged main checkout. Normal research resumes on the next scheduled run, which will be the first live Brain-integrated one.
- newspaper_ready: nothing meaningful (activation smoke only)
- questions_for_brendan: none
- proposed_durable_knowledge: none
- predictions: none
- run_status: success (activation smoke)
