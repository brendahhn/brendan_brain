<!-- version: 1.0.0 (2026-07-11) | status: provisional until 2026-08-15 (system/V2_LEDGER.md) -->
# Daily Schedule Plan (time-aware morning pipeline)

**Honesty first**: routine schedules live in Brendan's claude.ai routine configuration —
outside git, set by him in the UI. The platform gives no cross-routine coordination
primitive and no hard scheduler (LIMITATIONS #5): separate routines are separate sessions.
This plan is therefore **ordering INTENT with recommended clock times and mechanical
honesty gates**, not clock guarantees (arch-challenge response #9). Actual run durations
are UNKNOWN until the usage log accumulates rows — revisit the buffers after two weeks of
`log_usage.py` data.

## Recommended routine times (Pacific; Brendan sets these in the routines UI)
| Time (PT) | Routine | Notes |
|---|---|---|
| ~23:30 | FootyBot (existing) | unchanged |
| 02:00–05:00 | Jobs, Health, overnight concierge/kitchen deep passes | any order; finish before 06:00 |
| ~05:45 | (optional) Trading premarket prep | must complete before 06:30 |
| 06:30 | Trading opening analysis | market open 06:30 PT; exports its block to `queue/inbox/from-trading-robot.md` at run END |
| **07:05** | **Brendan OS editorial run** | 35-min buffer after trading start; runs the gate below |
| ~13:15 | (optional) Trading market-close review | updates the trading archive + a dated inbox block; NEVER delays or rewrites the morning paper — tomorrow's edition picks it up |

## The editorial gate (mechanical, in the 07:05 run)
1. `python3 tools/check_inputs.py --date <today>` — per-robot freshness.
2. Fresh trading block → include per PUBLICATION_POLICY. Missing → the Investing section
   carries a one-line `[FAIL]` item ("trading robot: no output as of 07:05 — reported, not
   fabricated"); build_newspaper.py inserts this automatically. The paper PUBLISHES anyway.
3. If trading lands late (e.g. 07:20 while editorial still open): the editor MAY pull it in
   before the Publisher pass; after publication it waits for tomorrow (editions are
   immutable audit trail).
4. Every missing/failed run appears in the edition — a silent gap is a policy violation
   (PUBLICATION_POLICY checklist 6).

## Failure modes, stated
- Trading routine slow/failed → paper ships at target time with the [FAIL] item. No retry
  loop inside the editorial run beyond one `check_inputs` re-check before the Publisher pass.
- Editorial routine itself fails → next session's oplog/status catches it; SYSTEM_HEALTH
  records the miss; no back-dated edition is fabricated.
- Cross-routine race (trading writing while editorial pulls) → git pull --rebase in the
  editorial run; inbox blocks are append-only dated so both sides survive.

## Verification status
Scheduling resolution: routines UI supports fixed times (Brendan's existing robots run at
fixed times daily); in-session waits use ScheduleWakeup (60s granularity, 1h max) — good
enough for the 07:05 buffer pattern; CronCreate minimum interval is hourly (fine: these are
daily). Durations: UNVERIFIED until usage-log data exists — buffers are estimates.
