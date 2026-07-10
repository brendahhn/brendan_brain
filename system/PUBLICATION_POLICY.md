<!-- version: 1.0.0 (2026-07-10) -->
# Publication Policy (Newspaper)

The Managing Editor selects and edits; it does not dump. Length is not rewarded.

## Selection criteria (in order)
importance → confidence → urgency → personal relevance → novelty (coverage ledger:
`newspaper/coverage_ledger.md`) → actionability → Brendan's current interests
(preferences/INTEREST_PROFILE.md) → available space.

## Section defaults (words; overridable per edition via queue or annotation)
most_important 150 · investing 1000 · fantasy_football 500 · health 500 · jobs 300 ·
news 400 · open_research 500 · questions_and_system 200. Empty sections are omitted with
one line ("Nothing meaningful in <section> today.") or dropped entirely.

## Sourcing
Sections draw from: tasks in `ready_for_publication`, robot outbox files
(`queue/inbox/from-*.md`), watches with meaningful changes, open questions, proposed rules
awaiting approval, system failures. Every item links its source artifact id.

## Publisher checklist (final gate, fresh context when consequential)
1. Claims match their source artifacts; dates current; time-sensitive items (listings,
   prices) re-verified near publication or marked "as of <date>".
2. No sensitive leakage: health/private/financial content only in its own section, only
   generic conclusions, no Brendan-specific medical/biometric values (PRIVACY_POLICY).
3. Word budgets respected (±20%); nothing padded to fill space.
4. Repeat check against coverage_ledger.md — no re-running yesterday's story without change.
5. Questions for Brendan and unprocessed annotations surfaced.
6. Failures reported honestly (a robot that didn't run is news, not silence).
