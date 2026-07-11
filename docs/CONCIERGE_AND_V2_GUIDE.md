<!-- version: 1.0.0 (2026-07-11) — V2 user guide -->
# Brendan OS V2 — What's New and How to Use It

V2 turns the Brain from a research system into practical life operations. Everything here
is **provisional for ~30 days** (system/V2_LEDGER.md) — what you don't use gets proposed
for removal, not silently kept.

## Just talk — the router figures out the rest
In any Brain-enabled session, say what you want naturally. The system decides between:
answer now · answer + remember · answer now + deep overnight pass · same-day task ·
background research · standing watch — and **tells you its decision in one sentence**.
Override in plain words, anytime:
- "Answer this now." / "This is just a one-off question." → answer only, **nothing saved**
- "Remember this." / "Don't save this."
- "Give me the quick answer and research it overnight."
- "Put this in tomorrow's paper." · "Make this a watch." · "I need this before dinner."
One-off tech questions (iPhone storage etc.) are answered and deliberately NOT remembered.

## Kitchen
- **Paste a receipt or grocery list** in any session → pantry updates (with expiry guesses
  you should sanity-check). Photos work too (the session transcribes first).
- **"Plan this menu" / "what should I make with what I have"** → menu plan with a
  night-before prep list, timed cook-day plan, and shopping gaps vs your pantry.
- **After cooking, react**: "we cooked it — the filling was perfect, puffs went soft" →
  outcome recorded, preferences learned (as evidence, never silent rules).
- Kitchen research reads ONLY the sanitized food-guidance file the health robot maintains —
  never your health data — and any guidance-fit notes stay out of the newspaper.
- Kitchen output defaults to files, not articles; say "put it in the paper" when you want it.

## Newspaper changes
- New optional **Concierge** section (~300w) — only appears when something asked for it.
- **Time-aware mornings**: recommended routine times are Trading 06:30 PT → Brendan OS
  editorial 07:10 PT (paper ~07:25) (set these in the routines UI — SCHEDULE_PLAN). If a robot didn't
  produce output, the paper says so with a [FAIL] line and publishes anyway — no waiting,
  no fabrication. A market-close trading pass can update the archive later without
  touching the morning edition.

## Cowork
Use Cowork for big interactive work (decks, spreadsheets, plans). At the end, paste the
one-paragraph handoff prompt from `.claude/skills/cowork-handoff/SKILL.md` — the session
writes a structured block into the Brain's inbox and the next daily run files everything.
Cowork never becomes a second memory.

## Connectors (governed by system/CONNECTOR_POLICY.md)
Gmail/Calendar/Drive produce decisions (follow-ups, receipts→pantry, prep deadlines), not
data dumps, and everything external is sanitized against prompt injection.
**Action needed from you:**
1. Answer the blocking question: is the connected Shopify store (and QuickBooks) yours,
   work, or a demo? Until then the Brain won't touch them.
2. Enable Google Calendar/Drive for Brain sessions if you want time-aware papers and
   curated doc ingestion.
3. Banking stays disconnected by design; the policy documents what must be proven first.

## Web research honesty
Routine sandboxes can search the web but (by current network policy) not open pages or
drive a browser. Findings say which tier they came from; volatile facts are dated "as of".
To enable live page fetching/browser automation for a routine, give its environment a more
permissive network policy in claude.ai settings — the workflows are already written to use
it when available.

## Learning, without creep
The system records what works (your reactions, repeated edits, source quality, prediction
calibration) and produces a **weekly review only when there's something material** — with
proposals, never silent changes. Interest shifts become questions to you; your profile is
never rewritten behind your back. Improvement experiments are capped at 3 open at a time.
