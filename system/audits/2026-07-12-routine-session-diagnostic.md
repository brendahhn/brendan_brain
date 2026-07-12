<!-- version: 1.0.0 (2026-07-12) | author: diagnostic session | status: provisional -->
# Routine + 5‑Hour Session Diagnostic and Stress Test

Scope: full audit of Brendan's proposed 4‑session daily routine schedule
(StockBot → Brendan Brain → 11:30 anchor → HealthBot → FootyBot), the timing
logic behind it, per‑routine cost diagnostics, a 16‑scenario stress test, a
monitoring system, and a final recommended operating schedule.

**Reading guide / honesty contract.** Every claim below is tagged:
`[CONFIRMED]` = documented platform behavior or verified in this repo;
`[LIKELY]` = strong inference, not directly inspectable here;
`[UNVERIFIED]` = assumption that materially affects the design and MUST be
measured. I could **not** inspect a live usage meter, token counts, or run
durations — this environment has **no account‑usage API** (repo
`docs/LIMITATIONS.md` #4, #19; confirmed again below). Where a number was
requested and no data exists, I say so and give the collection method instead
of inventing it.

---

## 0. The single most important correction up front

Two different things are both being called "session," and conflating them is
the root of most of the risk in this plan:

- **Usage window** — the 5‑hour, **account‑wide** allowance clock. Every
  message from *any* routine or manual chat draws from the *same* window if it
  lands inside it. `[CONFIRMED — this is the "5‑hour session" you mean]`
- **Routine/conversation** — one chat thread. Each scheduled routine is a
  **separate conversation** with its own fresh context. `[CONFIRMED in repo:
  SCHEDULE_PLAN.md — "separate routines are separate sessions… no cross‑routine
  coordination primitive."]`

Consequence you had right: StockBot and Brendan Brain, if both fire between
06:30 and 11:30, **share one usage window** — their costs add up against the
same 5‑hour allowance. `[LIKELY/CONFIRMED]`

Consequence you had wrong (or at least unstated): Brendan Brain does **not**
run "in the same session" as StockBot in the conversation sense. It is a second
conversation that **cannot see** whether StockBot finished. Sequencing them by
clock time alone is fragile; the repo already built a better mechanism for this
(the freshness gate, `tools/check_inputs.py`) — see §3 and §7.

---

## 1. Timing logic analysis

### 1.1 How the window actually behaves

`[CONFIRMED — documented Anthropic behavior]`
- Usage limits reset on a rolling **5‑hour** window.
- A window **opens with your first message** after the previous window has
  ended, and runs 5 hours. Your core understanding is **correct**.
- Limits are **account‑wide** (shared across all chats, projects, and
  routines), and there is a separate **weekly** limit sitting on top of the
  5‑hour one.

`[UNVERIFIED — and this is the decisive unknown]` **Does the window anchor to
the exact first‑message timestamp, or round to the top of the hour?** The two
hypotheses give opposite verdicts on your knife‑edge schedule:

| Hypothesis | Window opened by a 06:30 first message | Margin at your :30 boundaries |
|---|---|---|
| **Exact** — reset = first_msg + 5h | resets at **11:30 + jitter** | **~zero.** Any positive start jitter pushes the reset *past* the next :30 trigger |
| **Hour‑rounded** — reset = floor(hour) + 5h | opens "11:00", resets 11:00 | **~30 min.** Every :30 trigger lands safely after the reset |

I cannot resolve this from inside a session (no usage API). **This is
data‑collection item #1** (§ "Next data"). The recommended schedule in §7 is
built to survive **either** answer, so you are not blocked on it — but if you
ever want to trust the plain :30 times, you must confirm this first.

### 1.2 Does 4 × 5h + a 4h gap make a repeatable 24h loop?

`[CONFIRMED — arithmetic]` Yes. 4 windows × 5h = 20h active + 4h inactive =
24h. Four is also the **theoretical maximum** number of *fresh full* windows
per day: a 5th non‑overlapping 5‑hour window would need 25h and would bleed
past the next day's 06:30, de‑phasing the loop. **Your design already hits the
usage ceiling** — there is no schedule that legally extracts a 5th fresh
allowance while repeating at fixed daily times. Good instinct.

The 4‑hour night gap is not wasted slack — it is the **re‑phasing mechanism**.
Any timing drift that accumulates during the day is erased overnight because
nothing is sent from ~02:30 to 06:30, so the 06:30 window always opens clean.

### 1.3 Is the 11:30 anchor necessary for a fresh HealthBot at 16:30?

`[CONFIRMED by mechanics]` **No — not for HealthBot's freshness.** By 16:30 the
06:30 window (which closed at 11:30) is long gone. Whether or not the anchor
fired, if you send nothing else midday, HealthBot at 16:30 opens a fresh window
regardless. The night gap + fixed HealthBot time already guarantee that.

**What the anchor actually buys you** (two distinct things):
1. **The 4th window's allowance.** Without the anchor, and with no midday use,
   you only ever *open* 3 windows/day (morning, HealthBot, FootyBot) — the
   11:30–16:30 window is never claimed. The anchor is what secures the 4th
   fresh allowance so you can do interactive work midday on a clean quota. This
   is the entire "maximize usage" goal.
2. **Phase‑pinning.** If you use Claude ad‑hoc at, say, 13:00 with *no* anchor,
   that message opens the midday window at 13:00 → it resets at 18:00 → and
   HealthBot at 16:30 falls **inside** it (not fresh) and the whole afternoon
   phase drifts to :00. The anchor, fired at 11:30, forces the midday window to
   be 11:30–16:30 so any midday use is safely contained and HealthBot at 16:30
   still opens clean.

**Skeptical takeaway:** the anchor is worth keeping, but not for the reason
stated. It is a *usage‑maximizer and phase‑lock*, not a *HealthBot guarantee*.
If you never touch Claude between 11:30 and 16:30, it only ever opens a window
you then leave empty.

### 1.4 What if the anchor fires late (or not at all)?

- **Late anchor (e.g. 11:45).** The midday window simply opens at 11:45 and
  resets 16:45. Under the **exact** hypothesis, HealthBot at 16:30 then lands
  *inside* the midday window (16:30 < 16:45) → HealthBot is **not** fresh and
  the afternoon phase shifts to :45. Under **hour‑rounding**, 11:45 rounds to
  "11:00"/reset 16:00 → HealthBot at 16:30 is fine. So a late anchor is only
  dangerous under the exact hypothesis, and only if it slips past ~16:30 minus
  HealthBot's start. **A late anchor is self‑correcting overnight regardless.**
- **Anchor fails entirely.** Degrades to the no‑anchor case (§1.3): you lose
  *that day's* midday window; HealthBot and FootyBot are unaffected; the loop
  is intact by the next morning. **Cost of a missed anchor = one midday window,
  one day. No drift.**

### 1.5 Does a message just *before* a reset shift the next window?

`[LIKELY, exact hypothesis]` No, provided a message *after* the reset follows.
A message at 11:29 sits in the 06:30 window and does nothing to the phase; the
next message after 11:30 opens the new window. The danger is not a pre‑reset
message — it is a **first post‑reset message that lands at an unintended
time** (that is what floats the phase). This is exactly why the anchor exists:
to be the *intended* first post‑reset message.

### 1.6 Does routine runtime matter, or only the first‑message time?

`[CONFIRMED by mechanics]` For **window phase**, only the **first‑message
time** matters. A routine that runs 40 minutes emits many turns, all inside the
window it opened; the window does not extend. Runtime matters for exactly two
other things:
1. **Intra‑window collision** — StockBot's finish time vs. when Brendan Brain
   starts in the same window (a *sequencing* problem, not a phase problem).
2. **Allowance consumption** — a longer/heavier run eats more of the shared
   window's quota (§3).

### 1.7 When does a scheduled routine's window actually start?

`[LIKELY]` At the moment its **first message is dispatched**, i.e. actual
execution start, **not** the nominal scheduled clock time. Schedulers have
jitter and queueing; "06:30" is a target, not a guarantee (repo LIMITATIONS #5:
"no hard scheduler"). This is precisely why the exact hypothesis is dangerous:
`window_start = scheduled + jitter`, and the reset inherits that jitter.

### 1.8 Every way this schedule can drift, overlap, fail, or share a window

| # | Failure | Mechanism | Under which hypothesis | Severity |
|---|---|---|---|---|
| A | Anchor lands in the *previous* window | StockBot started late → reset > 11:30 > anchor time | exact only | midday window lost that day |
| B | HealthBot lands in the midday window | anchor late, or midday window reset > 16:30 | exact only | HealthBot not fresh; phase drift |
| C | Ad‑hoc midday use floats the phase | first post‑reset msg at an off time, no anchor | both | afternoon/evening drift, self‑heals overnight |
| D | Intra‑window collision | Brendan Brain starts before StockBot finishes | n/a (sequencing) | Brain reads stale/missing trading output |
| E | Two routines share a window unintentionally | any two triggers < 5h apart in real time | both | shared / prematurely exhausted allowance |
| F | Cumulative intra‑day drift | back‑to‑back windows, each reset = prev_start+5h, jitter marches later | exact only | boundary collapse late in day |
| G | Missed anchor | routine dispatch failure | both | one midday window lost |
| H | DST transition | wall‑clock triggers shift together | both | night gap width changes 1h once; harmless (§4) |

The structural root of A/B/F is the same: **triggers spaced *exactly* 5h apart
with *zero* margin under the exact hypothesis.** The fix is small deliberate
buffers (§7) that cost negligible coverage and neutralize A/B/F outright.

---

## 2. StockBot diagnostic

**Data availability: NONE of the requested metrics exist in an inspectable
form.** I read every StockBot artifact in `trading-notebook/` (7 recap files,
2026‑07‑03 through 2026‑07‑12). Findings:

- Recaps record **trading content only** — NAV, trades, theses, scoreboard.
- **No scheduled time, no actual start, no finish time, no runtime** appears in
  any recap. (The only time reference across all files is market‑open framing.)
- **No token counts, no cache figures, no allowance figures** — the platform
  exposes none to a session (`docs/LIMITATIONS.md` #4, #19), and
  `tools/log_usage.py` **deliberately has no tokens field** ("REFUSES invented
  numbers by not having a tokens field at all").
- Tool use / web research: recaps *imply* heavy web research (independent
  re‑verification of filings, multi‑source price checks) but do not count
  calls.

Therefore I **cannot** compute mean/median/min/max/std/p75/p90/p95 runtime, nor
average/median/max tokens, nor allowance consumed. Reporting any such number
would be fabrication. What I can give you:

**The best available proxies** (all capturable going forward, none today):

| Requested metric | Best proxy | Where to capture it |
|---|---|---|
| Runtime | `actual_finish − actual_start` wall‑clock | recap footer timestamp + routine dispatch time |
| Input tokens | context size (attached repos, prompt length) — a near‑constant per routine | not exposed; treat as fixed cost |
| Output tokens | **characters of model output** ÷ ~4 | recap length + any Gmail draft length |
| Tool calls | count in the run transcript | recap "Reviewer's work" / desk‑agent notes already hint |
| Web research | count of WebSearch calls | transcript |
| Allowance consumed | subjective `full/high/mid/low/hit‑limit` at run end | human/agent note |

**Interim buffer recommendation (evidence‑honest):** with no runtime
distribution, I cannot honestly name a p90/p95 StockBot runtime. The repo's own
`SCHEDULE_PLAN.md` already chose a **40‑minute** buffer (06:30 trading → 07:10
editorial) as a conservative estimate. **Keep that 40‑minute buffer as the
interim value.** Once `routine_monitor.py` (§5) has ≥5 StockBot rows, run
`plan --routine stockbot --scheduled 06:30` and it prints the exact
`p90/p95/max + {2,3,5,10}min` table. The rule is fixed even though the number
isn't: **Brendan‑Brain start = 06:30 + high‑percentile StockBot runtime +
buffer.** See §7 for how to apply the two‑tier (90% / 95%) target.

> Note: because StockBot and Brendan Brain are **separate conversations**, the
> real fix is not a perfect buffer — it is the **freshness gate** the repo
> already built (§3.3). The buffer only reduces how often the gate has to
> report "trading pending."

---

## 3. Brendan Brain diagnostic

Same data reality: **no runtime, no tokens.** Only observable, already‑logged
fields exist — `system/CAPACITY_LEDGER.md` has a handful of rows
(`05:20–06:07`, etc.) with **start–end wall‑clock but no tokens by design.** So
again: method, not fabricated statistics.

### 3.1 Combined morning cost (StockBot + Brendan Brain)

Both draw from the **one** 06:30 window. Combined cost = StockBot cost + Brendan
Brain cost, against a single 5‑hour allowance. I cannot quantify it in tokens.
The tractable proxy is **wall‑clock minutes of active generation** and
**tool‑call volume**, both captured by the monitor. Track the *sum* of the two
routines' `runtime_min` and `out_chars` per morning; that sum, trended over
weeks, is your morning‑window load index.

### 3.2 Remaining capacity after both routines

`[UNVERIFIED — unmeasurable today]` No allowance readout exists. Best proxy:
log `allowance_remaining` as a coarse subjective flag (`high/mid/low`) at the
end of the Brendan Brain run, and separately note if you ever hit a limit
during the day. If `low`/`hit‑limit` appears on ≥2 mornings in a rolling 14‑day
window, that is the signal to trim (§3.4), not before (evidence‑first, matching
this repo's culture).

### 3.3 Is "Brendan Brain right after StockBot" more efficient than a separate
later conversation?

Two independent questions hide here:

- **Cost efficiency:** running Brendan Brain in the *same window* vs. a *later*
  window does **not** change its own token cost — a conversation costs what its
  context + turns cost regardless of which window it lands in. What changes is
  **which allowance it draws down.** Same‑window = both routines share the
  06:30 allowance (fine if that window has headroom). Later window = Brendan
  Brain gets a fresh allowance but you "spend" a window opening on it.
- **Correctness efficiency:** running Brendan Brain right after StockBot is
  better **only if** StockBot has actually finished and written its output —
  otherwise the editorial run reads a missing/stale trading block. This is a
  **sequencing** guarantee, and timing alone can't provide it across two
  conversations. The repo already solved this: `tools/check_inputs.py` +
  build‑the‑paper‑anyway `[FAIL]` gate (SCHEDULE_PLAN §"editorial gate"). **Use
  the gate; treat the buffer as an optimization that makes the gate rarely fire
  a FAIL, not as the mechanism.**

Verdict: same‑window back‑to‑back is the right default **because it claims the
morning window efficiently and the freshness gate covers the race** — not
because it saves tokens (it doesn't).

### 3.4 What actually inflates either routine's cost (and what to do)

The dominant, often‑invisible cost is **fixed per‑turn context**, not the
visible prompt:

| Cost driver | Why it's big | Fix (without hurting quality) |
|---|---|---|
| Attached repo `CLAUDE.md` + skills registry | reloaded every turn of every routine | keep CLAUDE.md tight; this repo's is already ~120 lines — fine. Don't let it bloat. |
| MCP tool schemas (GitHub, Shopify, QuickBooks, Gmail…) | **large** token block loaded per turn if the routine has those connectors attached | **attach only the connectors a routine needs.** StockBot needs web + Gmail‑draft; it does **not** need Shopify/QuickBooks schemas. This is likely your biggest silent cost. |
| Long notebook re‑reads | `health-notebook.md` is **363 KB** | never load the whole notebook into a routine's context; read the relevant chapter/section only. This applies to HealthBot most. |
| Verbose recaps re‑summarized downstream | Brendan Brain re‑reads trading recap | the inbox‑block export pattern already trims this — keep exports terse. |
| Repeated web searches for the same fact | multi‑source re‑verification | keep (it's a *correctness* feature for trading); don't cut. |
| Verbose output | output tokens scale with length | trading recap is intentionally rich — keep. FootyBot/anchor can be terse. |

**Do not blind‑shorten prompts.** The trading robot's independent
re‑verification and the editorial gate are quality‑bearing and must stay. The
high‑value, low‑risk cut is **connector hygiene**: don't attach Shopify /
QuickBooks / broad GitHub tool sets to routines that never call them.

---

## 4. Stress test — 16 scenarios

Assumptions: exact‑hypothesis unless noted (it is the pessimistic case; if
hour‑rounding is real, every "drift" below shrinks or vanishes). "S1..S4" =
the four daily windows.

| # | Scenario | Which window the msg belongs to | Next window shifts? | Loses fresh allowance? | Daily loop intact? | Recovery |
|---|---|---|---|---|---|---|
| 1 | Everything on time | S1 06:30 / anchor S2 11:30 / HealthBot S3 16:30 / FootyBot S4 21:30 | no | no | ✅ | none needed |
| 2 | StockBot +5 min runtime | still S1 | no (runtime ≠ phase) | no | ✅ | ensure Brain buffer > finish; gate covers it |
| 3 | StockBot +15 min runtime | still S1; **but** S1 reset now 11:45 → anchor at 11:30 lands in S1 (Failure A) | **yes**, midday window not opened at 11:30 | yes — midday window lost that day | ✅ by next morning | fire anchor at 11:35–11:40 (§7) to absorb start jitter |
| 4 | Brendan Brain starts late | still S1 (same window) | no | no | ✅ | if it starts after StockBot finished, the gate is happier; no phase effect |
| 5 | 11:30 anchor **fails** | — | midday window never opens | midday window lost (that day only) | ✅ | none required; self‑heals. Optional: manual one‑word msg anytime 11:30–16:00 reclaims it |
| 6 | Anchor runs 11:45 | opens S2 at 11:45, reset 16:45 | HealthBot 16:30 now *inside* S2 (Failure B) | HealthBot not fresh | drifts to :45, heals overnight | move HealthBot to 16:40 (§7) so anchor slip ≤10 min is absorbed |
| 7 | Manual use 11:20 | S1 (06:30 window) | no | no | ✅ | nothing — this is normal in‑window use |
| 8 | Manual use 16:20 | S2 (midday window) **if anchor fired**; else it *opens* a window at 16:20 and HealthBot 16:30 falls in it | with anchor: no. without: yes | with anchor: no. without: HealthBot not fresh | ✅ with anchor | **this is the anchor's payoff** — it makes 16:20 use safe |
| 9 | HealthBot at 16:30 while prior window still active | means S2 reset > 16:30 (late anchor/exact jitter) → HealthBot shares S2 | yes | HealthBot not fresh | drift, heals overnight | HealthBot buffer at 16:40; verify reset via monitor |
| 10 | HealthBot uses ~all window capacity | S3 | no | no (it's *its* window to spend) | ✅ | if you also want evening interactive room, that's FootyBot's separate S4 — fine |
| 11 | You keep using Claude until 21:25 | all S3 (16:30 window) | no | no | ✅ | 21:25 use is in‑window; FootyBot 21:30 still opens S4 |
| 12 | FootyBot at 21:30 | opens S4 (if S3 reset ≤ 21:30) | no | no | ✅ | with exact jitter, S3 reset could be 21:31 → FootyBot shares S3; buffer FootyBot to 21:40 (§7) |
| 13 | FootyBot runs late into night | still S4; emits turns until, say, 23:30 | no (runtime ≠ phase) | no | ✅ | ensure it finishes before ~02:30 so no message lands in the gap |
| 14 | Manual msg 02:30–06:30 (the gap) | opens a rogue window mid‑gap, e.g. 03:00 → reset 08:00 | **yes** — StockBot 06:30 now falls inside it (03:00 window still open) | StockBot **not fresh**; morning phase wrecked | ❌ until next day | **hard rule: never message in the gap.** If you did, either wait it out or accept one de‑phased day; it re‑heals the following night |
| 15 | Platform load / long tool call delays a routine | window opens at actual dispatch, later than scheduled | yes, by the delay (exact) | possibly (Failures A/B) | heals overnight | buffers in §7 absorb small delays; large delays → that boundary's window may collapse for the day |
| 16 | Routine fails and auto‑retries | retries are quick msgs inside the same window | no | no | ✅ | none; retries don't move phase. If *all* attempts fail, see #5 |
| 17 | **DST change (Pacific)** | all four wall‑clock triggers shift together, preserving 5h spacing; the transition happens at 02:00, inside the gap | no daytime effect | no | ✅ | spring‑forward shrinks the night gap to ~3h (still > 5h from FootyBot? gap is 06:30 − ~02:30 real; lost hour → ~3h real, still fine because FootyBot's S4 opened 21:30 prior). fall‑back grows it. **Harmless.** |

**Pattern across all 16:** the only *unrecoverable‑same‑day* failure is #14
(messaging in the night gap). Everything else either doesn't move the phase or
self‑heals overnight. The buffers in §7 remove the exact‑hypothesis drift in
#3, #6, #9, #12, #15.

---

## 5. Monitoring & diagnostics system

Delivered as a working, stdlib‑only tool (matches this repo's rules):
**`tools/routine_monitor.py`**, writing **`system/routine_runs.csv`**.

### CSV schema (one row per routine run)

```
date, routine, scheduled, actual_start, actual_finish, runtime_min,
session_start, expected_reset, window_model,
in_tok, out_tok, total_tok, out_chars,
tool_calls, web_searches, files_read, errors, allowance_remaining, notes
```

`in_tok/out_tok/total_tok` are present but stay **blank** — no platform number
exists. `out_chars`, `tool_calls`, `web_searches`, `files_read`, `runtime_min`
are the **proxies** you actually fill.

### Commands

- `log …` — append a run; prints inline flags immediately.
- `stats [--routine R]` — rolling **mean / median / min / max / std / p75 /
  p90 / p95** for `runtime_min`, `out_chars`, `tool_calls`, `web_searches`,
  and (if ever populated) `total_tok`. Recomputes over the whole log every call
  — i.e. **rolling averages/percentiles update after every new run**, as asked.
- `check` — runs **all flag rules** over the log.
- `plan --routine stockbot --scheduled 06:30` — prints the
  `p90/p95/max × {2,3,5,10}min` downstream‑start table once ≥5 rows exist;
  before that it prints "insufficient data — use the interim buffer."

### What it flags (all implemented and tested)

- **Runtime outliers** — beyond mean ± 2σ per routine.
- **Token/proxy outliers** — same test on `out_chars`, `tool_calls`.
- **Late routine starts** — `actual_start` > `scheduled` + 5 min.
- **Possible session overlap** — a run scheduled < 3 min before its own logged
  reset (prior window may still be open).
- **Missing anchor** — an `anchor` row with no `actual_start`.
- **Unexpected reset times** — `expected_reset` is computed under both
  hypotheses (`--window-model exact|hour`); logging the same day under both and
  comparing to observed behavior is how you *resolve* the §1.1 unknown.
- **Unusually high capacity** — surfaces via the outlier + `allowance_remaining`
  columns.
- **Drift onset** — a *trend* of late starts / shifting resets shows up as
  repeated flags on consecutive days in `check`.

### The token problem, stated honestly

There is **no token readout** (LIMITATIONS #4/#19). The tool's stance matches
`log_usage.py`: never invent a token number. The proxy hierarchy, best to
worst, is: **(1) wall‑clock `runtime_min`** (most robust, always available),
**(2) `tool_calls` + `web_searches`** (drivers of cost), **(3) `out_chars`/4 ≈
output tokens** (rough). Track all three; trend beats absolute.

*(Tested end‑to‑end on synthetic rows: stats, percentiles, outlier detection,
late‑start and error flags, and the buffer table all function. Those test
numbers were illustrative and were not committed.)*

---

## 6. The 11:30 anchor message

Goal: the **smallest reliable** message that opens a fresh window at minimum
cost.

- **Empty message:** `[LIKELY]` rejected — interfaces require non‑empty input.
  Do **not** rely on it.
- **Single char / period:** `[LIKELY]` accepted and sufficient to open a
  window; the window opens on receipt of your *user turn*, independent of the
  reply.
- **The real cost is not the message — it's the context the anchor
  conversation loads.** An anchor routine that has repos + MCP connectors
  attached pays the full per‑turn schema cost even to say ".". A **bare**
  routine (no repository selected, no connectors, no skills) makes the anchor
  genuinely cheap. **This is the dominant lever, not message length.**
- **Should you ask for a one‑word reply?** The window opens on *your* message
  regardless of reply length, but the model *will* answer, and the answer draws
  from the window too. Output for one word is trivial next to fixed context, so
  this is a minor optimization — still, instruct brevity to be clean.

**Recommended anchor (exact text to automate):**

> `New session anchor. Reply with only: ok`

Rationale: non‑empty (reliably processed), unambiguous, instructs a
one‑token reply, and — critically — **schedule it as a routine with no
repository and no connectors attached.** That combination, not a shorter
string, is what makes it cheap. Set its scheduled time to **11:35** (see §7:
absorbs up to ~5 min of StockBot start jitter under the exact hypothesis).

---

## 7. Final recommended operating system

### 7.1 The exact permanent schedule (robust under *both* window hypotheses)

The only change from your plan is **small cumulative buffers** on the three
daytime boundaries, so that under the pessimistic exact‑hypothesis a late
upstream routine can't push its reset past the next trigger. Under
hour‑rounding these buffers are harmless. Coverage cost ≈ 15 min/day of
"between‑window" time that automated routines don't use anyway.

| Time (PT, fixed daily) | Routine | Why this time |
|---|---|---|
| **06:30** | **StockBot** (Trading opening analysis) | market open; anchors the day; night gap guarantees a fresh window |
| **06:30 + [p90 StockBot runtime] + buffer** (interim **07:10**) | **Brendan Brain** editorial | same window as StockBot; gated by `check_inputs.py`, not timing alone |
| **11:35** | **Anchor** (`New session anchor. Reply with only: ok`) | +5 min past the 11:30 reset absorbs StockBot start jitter (Failure A) |
| **16:40** | **HealthBot** | +10 min cumulative; absorbs an anchor that slipped to ~11:40 (Failure B) |
| **21:45** | **FootyBot** | +15 min cumulative; absorbs afternoon jitter (Failure #12) |
| **~02:45 → 06:30** | **Inactive gap** | ~3h45 of silence re‑phases the loop daily; **never message here** |

If week‑1 monitoring confirms **hour‑rounding**, you may revert to clean
06:30 / 11:30 / 16:30 / 21:30 with no loss. Until confirmed, run the buffered
version.

### 7.2 The two recommended Brendan Brain times

Apply the rule **06:30 + StockBot high‑pct runtime + buffer** once you have
data. Until then:
- **≥90% reliability (earliest sane):** **07:05** interim (keep the repo's
  40‑min plan; tighten toward `p90 + 3min` when `plan` prints it).
- **≥95% reliability (conservative, recommended default):** **07:10–07:15**
  interim (`p95 + 5min`). Given the freshness gate publishes anyway on a miss,
  I recommend the 95% time — the marginal minutes are cheap insurance.

### 7.3 Rules for manual Claude use inside each session

- **Inside a window (any of S1–S4):** use Claude freely; it draws that window's
  allowance and moves nothing.
- **Between 11:30 and the anchor:** avoid, or if you must, *that* becomes the
  window opener — send it at/after 11:35, not before 11:30.
- **Never send a message from ~02:45 to 06:30** (the gap). This is the one hard
  rule; violating it de‑phases the whole next day (#14).

### 7.4 Rules for avoiding accidental drift

1. Never message in the night gap.
2. Keep the anchor at 11:35 firing; treat a missed anchor as "lost midday
   window," not an emergency.
3. Don't add connectors to routines that don't call them (cost + no benefit).
4. Sequence StockBot→Brain by the **gate**, not by hoping the buffer is perfect.

### 7.5 Recovery protocols

- **Session begins late / boundary collapsed for a day:** do nothing
  structural. The night gap re‑phases by next 06:30. Log it in the monitor;
  if it recurs ≥3×/14 days, widen that boundary's buffer by 5 min.
- **Anchor fails:** optional — send one manual `ok` any time before ~16:00 to
  reclaim the midday window; otherwise let it lapse. No drift either way.
- **You messaged in the gap:** accept one de‑phased day or, if before 06:30,
  stop and wait; the 06:30 routine will then share your rogue window for that
  day only.

### 7.6 Weekly diagnostic process

Every Sunday: `python3 tools/routine_monitor.py check` and `… stats`. Review
flags, update buffers if a boundary flagged ≥3×, and once StockBot has ≥5 rows
run `… plan --routine stockbot --scheduled 06:30` to refine the Brain time.
Fold this into the existing weekly review (CAPACITY_LEDGER cadence).

### 7.7 Adjustment thresholds

- **Move the Brendan Brain time** when StockBot's **p95 runtime + 5 min**
  crosses the current Brain start (monitor's `plan` makes this explicit), or
  when the freshness gate logs "trading pending" on ≥2 of the last 10 days.
- **Optimize a routine's prompt/context** when either: `allowance_remaining`
  reads `low`/`hit‑limit` on ≥2 mornings in 14 days, **or** a routine's
  `runtime_min`/`out_chars` p90 rises >30% over its 14‑day baseline without a
  scope change. Optimize **connectors and file‑read scope first** (§3.4);
  touch quality‑bearing prompt logic last, and only with the `safe-bot-edits`
  skill.

---

## Final summary by evidence class

### Confirmed behavior
- 5‑hour usage window opens on the first message after the prior window ends;
  account‑wide; weekly limit sits on top. Your core understanding is correct.
- 4×5h + 4h gap = a valid, repeatable 24h loop, and 4 fresh windows/day is the
  maximum achievable at fixed daily times.
- Separate routines are separate conversations but share the account window if
  co‑located in time (repo‑confirmed).
- No account‑usage/token API to sessions; no hard scheduler; no cross‑routine
  coordination primitive (repo `docs/LIMITATIONS.md`).
- Only first‑message time sets window phase; runtime does not.
- The anchor is not required for HealthBot freshness; it secures the 4th
  (midday) window and pins the afternoon phase.
- DST is harmless — the transition falls in the night gap.

### Likely behavior
- Window reset = first‑message + 5h (exact anchoring) — pessimistic default.
- A single character opens a window; an empty message does not.
- Window opens at actual dispatch time, not nominal scheduled time.

### Unverified assumptions (must measure)
- **Exact‑timestamp vs. top‑of‑hour rounding of the reset** — decisive; item #1
  to collect. The whole knife‑edge risk exists only under exact anchoring.
- Precise boundary behavior of a message sent within seconds of a reset.
- Whether the platform silently coalesces a failed‑and‑retried routine's turns.

### Diagnostic findings
- **StockBot and Brendan Brain have zero inspectable runtime/token data.** All
  requested statistics are uncomputable from existing artifacts; recaps carry
  no timestamps; the platform exposes no tokens. Proxies and a collection tool
  are provided instead of invented numbers.
- The largest *silent* cost is likely **per‑turn connector/context load**, not
  prompt length — the highest‑value optimization is connector hygiene and
  scoped file reads (never load the 363 KB health notebook whole).
- Sequencing StockBot→Brain by clock buffer alone is fragile; the repo's
  existing **freshness gate** is the correct mechanism, with the buffer as an
  optimization.

### Stress‑test results
- 16/17 scenarios are either phase‑neutral or self‑healing overnight. The lone
  same‑day‑unrecoverable failure is **messaging in the 02:45–06:30 gap** (#14).
- All exact‑hypothesis drift cases (#3, #6, #9, #12, #15) are neutralized by the
  small cumulative buffers in §7.1.

### Recommended schedule
- 06:30 StockBot · 07:10 Brendan Brain (interim; refine to p95+5) · 11:35
  anchor · 16:40 HealthBot · 21:45 FootyBot · 02:45–06:30 inactive. Revert to
  clean :30 times only if hour‑rounding is confirmed.

### Monitoring system
- `tools/routine_monitor.py` + `system/routine_runs.csv`: rolling
  stats/percentiles after every run; flags outliers, late starts, overlap risk,
  missing anchor, reset drift; `plan` computes the Brain buffer from real data
  once ≥5 rows exist. Token fields intentionally blank; proxies drive it.

### Next data to collect (in priority order)
1. **Resolve exact‑vs‑hour rounding.** Log StockBot's window under both
   `--window-model` values for a week and compare observed reset behavior
   (when limits actually refresh) to each prediction.
2. **StockBot start/finish times** for ≥5 runs → real p90/p95 → the true Brain
   buffer.
3. **Brendan Brain start/finish + out_chars** → morning‑window load index.
4. **A coarse `allowance_remaining` flag** at end of the morning run → the only
   available signal of real capacity pressure.
5. **Anchor reliability** — did it fire, did it open a fresh window — logged as
   an `anchor` row daily.
