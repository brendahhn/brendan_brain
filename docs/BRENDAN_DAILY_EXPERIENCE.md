<!-- Discovery deliverable 2026-07-14 (Fable). -->
# Brendan's Daily Experience (target state)

## Morning (~7:30)
Opens Personal OS Home on his phone. Sees a newspaper-style page (widgets/columns):
- **Today's edition**: Most Important, Investing, Health, Fantasy, Jobs(paused), Tea
  Business, Gym/Oura mix, Concierge, Travel countdown when a trip is near.
- **Brain status strip**: queue counts (researching/waiting/done), failure flags, watches.
- **Questions for Brendan**: each with an answer text box (writes to Supabase; next run
  reads them).
- **Feedback box** at the bottom: anything he types trains tomorrow's run (likes,
  dislikes, "more of X", routing corrections).
His Oura data refreshed itself overnight (Supabase scheduled job) — Log/Data are current
without him clicking anything.

## During the day
He jots notes (category = destination: footybot/health/tea/FOR CLAUDE/...) and todos.
Nothing happens until the next daily run — by design. Urgent? He opens a session manually.
At the gym, the Gym tab works as today, just nicer.

## Overnight (the one daily Brendan OS run + robot runs)
Robots run their own schedules and drop outbox blocks. The Brendan OS run: scans Personal
OS notes/todos + Shopify orders + inboxes + feedback box + question answers → routes
(intake modes; tags win; FOR CLAUDE notes ingested then deleted, all-caps rule) →
researches queue tasks → updates tea projections (fulfillment marks, L-theanine weekday
tick, home batches) → writes tomorrow's edition to git AND to Supabase → creates/updates
todos/projects/calendar prep (trips 14d, else 7d) → verifies pushes to main.

## Weekly-ish
Skill Scout "AI growth corner" pitches (monthly-ish). Physical recounts whenever Brendan
feels like it — a photo or numbers reconcile projections. Printable edition view (later).
