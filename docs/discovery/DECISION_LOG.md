<!-- Discovery decision log — grows during the interview; graduates to docs/DECISION_LOG.md on approval. -->
# Brendan OS Discovery — Decision Log

Format: ID · decision · source · date. "Inferred default" = Fable's recommendation Brendan
didn't override; he can reverse any of these by saying so.

## Round 1 — Vision and daily experience (2026-07-14)

- **D1 · Morning surface**: The daily output must be easily readable OUTSIDE Claude.
  Personal OS is preferred if it can be done simply; Gmail acceptable as fallback.
  Brendan is not picky about the surface, is worried about token cost, and wants
  **printability** down the road. → Plan: newspaper stays canonical in git; publish step
  additionally writes the edition to Supabase (one cheap API row, no site rebuild, no
  meaningful token cost); Personal OS renders it + a print-friendly view later.
  (Brendan, R1; delivery mechanism = inferred default)
- **D2 · Cadence ceiling**: Nothing is more urgent than the daily run. **Max one run per
  day per routine; no intraday alerts, no real-time interrupts.** Proactive findings go in
  the next paper. This deletes all "immediate Gmail alert" ideas from the roadmap
  (inventory alerts etc. become newspaper items). (Brendan, R1, explicit)
- **D3 · Never-do additions**: All prior boundaries confirmed (no purchases, no sending,
  no banking, no customer PII in git, no employer data). Added: **email drafts may only
  ever be addressed to brendanhamor@gmail.com** — never draft to anyone else. (Brendan, R1)
- **D4 · Memory density**: Confirmed "decisions, preferences, projects, confirmed facts —
  not a transcript." Notes containing question batches (e.g. health questions) should be
  **decomposed into the relevant queues** (Brain research queue / robot idea queues) for
  eventual research. Brendan offered to add timelines per item; default: not required —
  router infers, deadline optional, 7-day default SLA (D6). (Brendan, R1)
- **D5 · Intake defaults for the bridge**: **Todos: always read by the router.** Notes:
  read every new note if token-cheap (haiku-tier triage); `@claude` in a note acts as an
  explicit route-me marker/override. Open: category exclusions (e.g. `love`, `health`) —
  Round 2. (Brendan, R1; @claude semantics = inferred default)
- **D6 · Uncertainty & SLA**: Plain-language confidence tiers (existing practice) are fine.
  **Unstated-deadline research: surface results within ~7 days**, treated as
  lower-than-deadline priority. (Brendan, R1)
- **D7 · Perfect day shape**: Overnight routines → one tailored morning paper (health
  summary prominent; idea-queue items get real breakdowns). Anything captured during the
  day is actioned next cycle, never same-day. Brendan expects to add routines over time.
  (Brendan, R1)
- **D8 · Noticing license**: Broad. The system may notice and suggest anything —
  stale projects ("whatever happened to X?"), trends across Oura/log/gym, cross-domain
  contradictions — **suggestions are explicitly welcomed**, channeled through the daily
  paper only (per D2). (Brendan, R1)

## Operational decisions made during Round 1 (production repair, Brendan-directed)

- **D9 · Push-to-main standing rule**: Routine sessions pinned to platform `claude/*`
  branches must land routine operational commits on main (CLAUDE.md amendment,
  2026-07-14). Source: Brendan — "runs haven't been pushing to main, fix that."
  Recovery: op-20260714-stranded-branch-recovery (all 4 repos verified).
- **D10 · Duplicate daily run 2026-07-14**: keen-ritchie-r2elmx (14:25 double-fire) NOT
  merged — duplicate artifacts. Brendan should check the routines UI for a duplicated
  Brendan OS schedule entry. (Fable, evidence-based; flagged to Brendan)

## Round 2 — Personal OS (2026-07-14)

- **D11 · Tab census**: All tabs live. Heavy: Notes, Todos, Gym (mobile at gym), Calendar,
  Tea Finance (manual Amazon purchases + sales), Home. Friction: Log + Data depend on a
  manual Oura refresh Brendan forgets → **auto-pull Oura daily without a click**. Projects =
  idea parking; **agents should add/update there so he sees it**. Tea Inventory used but
  has a save bug (D14). Trash stays. (Brendan, R2)
- **D12 · Database auth**: Option B — add a simple password gate + rotate keys BEFORE the
  bridge ships. (Brendan, R2, explicit)
- **D13 · Agent write rules on Personal OS**: Agents MAY create todos, add calendar events,
  add/update projects, write/refresh Log (Oura). **Never wipe data. Complete todos by
  checking, never deleting. Notes: a `FOR CLAUDE` category may be deleted after
  internalizing; every other note is never deleted even after capture.** Safe > sorry.
  (Brendan, R2, explicit)
- **D14 · Tea Stock save bug**: confirmed as the top Website Builder task, plus a general
  UI/UX redesign mandate ("take it away… make it look nicer"). Code wiring looks correct
  (same autosave path as working tabs); suspected missing/mis-schema'd `tea_inventory`
  table in Supabase; unverifiable from this session (egress blocked, D18). (Brendan, R2)
- **D15 · Home = cockpit**: newspaper + brain queue status + open questions + failure
  flags, laid out as widgets/columns "like a true newspaper"; comprehensive morning
  digest. **Questions get answer text boxes under them**; plus a **feedback box** on Home
  the next-day run reads and learns from (this becomes the primary annotation channel).
  (Brendan, R2)
- **D16 · Notes visibility**: no private categories — router may see everything, including
  full sub-bullet trees (must be read in full). (Brendan, R2, explicit — supersedes the
  R1 open question about excluding `love`)
- **D17 · Oura → HealthBot**: emphatic yes; HealthBot decides what data it wants and may
  evolve it. Oura Web (cloud.ouraring.com) retires in September — export path is Oura API /
  Membership Hub; site's edge function already uses the API. Daily auto-pull to be
  implemented without Brendan clicking (prefer a Supabase scheduled job over burning
  routine tokens). Raw health numbers stay out of git — summaries only. (Brendan, R2)
- **D18 · Environment egress gap**: this session's network policy blocks supabase.co →
  Brendan must allow it (and any future bridge domains) in the environment/network policy
  for routines that run the bridge. (discovered, R2)
- **D19 · Deploy + data safety**: site edited on GitHub, Vercel assumed auto-deploy from
  main. Standing constraint: **never lose site data**; migrations/backups before any
  schema change; historical note that "stuff not saving" has been a recurring failure
  class. (Brendan, R2)
- **D20 (open) · StockBot ambition**: Brendan floated "ultimate goal make a lot of money,"
  self-flagged as getting ahead. Current confirmed rule: trading is fictitious forever.
  Needs an explicit decision — see Round 3 Q. NO real-money action regardless; at most
  recommendations Brendan executes himself. (flagged)

## Round 3 — Intake and routing (2026-07-14)

- **D21 · Scrub-everything + all-caps delete rule**: The router scrubs EVERY note.
  Deletion is authorized ONLY by a literal all-caps "FOR CLAUDE" (category or in-text).
  Lowercase "for Claude" = route it, never delete. (Brendan, R3, explicit)
- **D22 · Tag→robot routing**: Note categories map to destinations: `footybot` → FootyBot,
  `health` → HealthBot, `tea` → tea business desk, etc. Brendan will add `finances`
  eventually. Taxonomy stays editable; he re-tags to correct routing and will guide the
  exact system over time. Feedback box remains the other correction channel. (Brendan, R3)
- **D23 · Autonomous domain creation**: Auto-create domains when a topic accumulates —
  "massive file cabinet it autonomously uses." Supersedes propose-first (DOMAIN_POLICY
  ladder still applies: don't create clutter for one-offs; announce creations in the paper).
  (Brendan, R3, explicit)
- **D24 · Website Builder cadence**: Option B — no standing routine. Daily paper flags
  pending site tasks; Brendan launches a Builder session manually. (Brendan, R3)
- **D25 · Travel domain**: created on main (23e7cf6) — Europe trip is BOOKED, confirmations
  in Gmail (~May–June 2026). Details need Gmail search or Brendan paste (R4). (Brendan, R3)
- **D26 · Trading stays paper; alpha mandate noted**: Paper-only stands. Brendan expects
  the paper book to target meaningful alpha, not index-hugging ("should be netting a lot
  more than barely beating the S&P"). Any mandate change to the Trading Robot goes through
  its proposed-prompt-change channel (safe-bot-edits), not silently. Real-money execution
  remains permanently out of scope for the system. (Brendan, R3)
- **D27 · Shopify → Tea Finance auto-append**: Yes — paid orders append income entries
  (amount/product/date, no customer PII) once Shopify integration ships. (Brendan, R3)
- **D28 · Nudges + same-day path**: Unanswered questions may nudge ("don't be afraid of
  me"). Same-day/urgent work happens only when Brendan manually runs a session. (Brendan, R3)
- **D29 · .claude-folder article**: Brendan shared a guide wanting "this system." Verdict:
  ~80% already implemented (CLAUDE.md contracts, .claude/skills, agent registry, permission
  policies). Worth adopting: settings.json deny rules (QuickBooks lockout, rm -rf, .env),
  possibly a data-safety PreToolUse hook for the personal-os repo. Not worth it now:
  rules/ split (contracts are already modular per-file), CLAUDE.local.md, heavy hook
  suites in routine sandboxes. (Fable assessment, R3)

## Round 4 — Gmail and Calendar (2026-07-14)

- **D30 · Gmail scope**: brendanhamor@gmail.com only; connector is connected at org level.
  Important mail: job interviews, travel; low precision bar ("whateva"). (Brendan, R4)
- **D31 · Missed-reply detection**: IN — the paper flags people awaiting his reply.
  Blocked until the connector exposes search/list tools (see D33). (Brendan, R4)
- **D32 · Gmail drafts**: worked ~3 weeks ago, broken since. Verified cause: the connector
  surface changed platform-side — current sessions expose only get_message + trash/spam
  labels; no compose/draft, no search (tool descriptions reference search_threads/get_thread
  existing in the connector but unexposed). Not fixable in our code. Mitigation: newspaper
  delivery moves to Personal OS Home (D15), making Gmail-draft briefings redundant; robots'
  Gmail-draft steps get a graceful fallback (save to digests/, already health-robot
  behavior). Brendan may try disconnecting/reconnecting Gmail in claude.ai settings to
  refresh scopes; re-probe each session. (Brendan + audit, R4)
- **D33 · Gmail scanning**: design lands in Phase 3 but stays dormant until search tools
  appear in sessions. Nothing else blocks on it. (audit, R4)
- **D34 · Calendar = Personal OS only**: Brendan uses ONLY the site's Calendar tab. No
  Google Calendar connector needed — calendar prep runs entirely through the bridge.
  Major simplification: R4's Google Calendar questions are moot. (Brendan, R4, explicit)
- **D35 · Prep lead times**: trips 14 days, everything else 7. (Brendan, R4)
- **D36 · Euro trip**: "Euro logistics" = the booked Europe trip. Details still needed
  (dates/cities) — via paste or future Gmail search; travel domain waits on them. (Brendan, R4)

## Round 5 pre-work — Shopify probe (2026-07-14, read-only, no customer data)

- **D37 · Store facts**: "Drink Siesta", Basic plan, USD, PDT. TWO products, one variant
  each: Loose Leaf (SKU SIESTA-LL-30, $44.99, inventory 5) and Tea Bags (SKU
  SIESTA-TB-30, $44.99, **inventory -5 — negative**, i.e. Shopify counts are not being
  maintained). Products map 1:1 to the App.jsx BOM's loose/bag order types. Ownership
  question closed on main. (probe, R5 pre-work)

## Round 5 — Tea business (2026-07-14)

- **D38 · Shopify role + exit**: Shopify is ONLY order notification + checkout behind
  Brendan's Lovable storefront; its inventory numbers are ignored ("I will give u my
  inventory"). Shopify starts charging ~$25/mo in August → NOT worth it. Research task
  queued (deadline 2026-07-31, newspaper) to pick a cheaper checkout that hooks into the
  Lovable site. (Brendan, R5, explicit)
- **D39 · Inventory truth**: Brendan's physical counts (07-13 snapshot filed:
  know-20260713-tea-physical-inventory) + Personal OS Tea Stock after the save-fix.
  Deduction fires when BRENDAN marks an order fulfilled (Personal OS button; Shopify's
  fulfillment field is unmaintained — verified: all 14 orders show UNFULFILLED there).
  Commentary/nudges about low stock welcome. (Brendan, R5)
- **D40 · BOM confirmed** with corrections (know-20260714-tea-bom): bags = −1 sticker,
  +large muslin, +30 tea bags; loose = "one big jar" + extra sticker, no tea bags.
  OPEN: loose = herb tin + powder tin (site recipe) or single big jar? (Brendan, R5)
- **D41 · Low-stock rule**: flag any component at ≤4 orders remaining, in the paper.
  At the 07-13 count: tea bags (2), L-theanine (3), taurine (3) already flag. (Brendan, R5)
- **D42 · Sourcing constraints**: unit cost matters but no big MOQs (~500-unit buys out);
  chamomile/lemon balm organic + clean; unbleached cotton tea bags; boxes/tins keep
  dimensions (powder tins may shrink slightly, herb tins cannot). **Ingredients: NEVER
  order, never even add to cart — attention-only.** Stricter than the generic Amazon
  cart-prep default; encoded in the sourcing task. (Brendan, R5, explicit)
- **D43 · Verified-links mandate**: Brendan has been given nonexistent links and wrong
  prices by past Claude sessions. All sourcing/pricing output must be live-verified at
  research time (BROWSER_RESEARCH_POLICY + source-verification); unverifiable → say so,
  never present. Routine-sandbox egress (WebSearch-only) is the constraint to respect.
  (Brendan, R5, explicit)
- **D44 · Sales aggregate**: $669.86 gross, 14 orders since 2026-06-02, 13:1 tea-bags:loose
  — tea-bag ceiling is the binding inventory constraint. Backfill of Tea Finance from
  Shopify aggregates approved ("sure go for it"); ships with the bridge. (probe + Brendan, R5)
- **D45 · Fulfillment backlog surfaced**: #1013 (paid 07-09) and #1014 (paid 07-14, 2 items)
  unfulfilled per Brendan. Names stay out of git. (Brendan, R5)

## Round 6 — Personal inventory / L-theanine (2026-07-14)

- **D46 · Count baseline**: 07-13 photo count was post-#1013; #1014 (2 tea-bag orders)
  packed after → effective stock = photo − 2 tea-bag orders. Current: tea bags ~14 (0
  orders 🔴), L-theanine ~6g 🔴, taurine ~81g (1 order) 🔴. No fulfillment backlog.
  Sourcing task bumped URGENT, leads with those three. (Brendan, R6)
- **D47 · Shared L-theanine jar**: personal (0.5 g/weekday, none weekends) and business
  (6 g/order) draw from ONE jar "for better or worse" — one projected stream, two
  deduction rules. Missed personal days (Encinitas weekends → skipped Mondays): NO
  correction UI; drift reconciles via recounts and Brendan's messages. (Brendan, R6)
- **D48 · Display + home batches**: actual vs projected side by side. Home batches
  (~20-day supply for Brendan + his mom, order-scale ingredients, no packaging) are
  manually reported and deduct ingredients only — manual entry in Tea tab. L-theanine is
  the only standing deterministic rule; others enter via home-batch reports. (Brendan, R6)
- **D49 · BOM final**: loose = herb tin + powder tin (two tins); site recipe correct.
  Storefront = Lovable site + Shopify checkout, confirmed. (Brendan, R6)

## Round 7 — Router, Cowork, skills, newspaper (2026-07-14)

- **D50 · Jobs robot PAUSED** by Brendan intentionally ("I'm not running rn") — registry +
  priorities updated on main; editions report "paused", never [FAIL]. Job search remains a
  priority; only the robot is off. (Brendan, R7)
- **D51 · Ops Router runs inside the existing daily Brendan OS routine** — new scan steps
  (Personal OS notes/todos, Shopify orders, inboxes) before triage; no new routine, same
  once-daily budget, fast empty exit. (Brendan, R7)
- **D52 · Brendan-assigned tasks become agent-created todos in Personal OS.** (Brendan, R7)
- **D53 · Cowork + multi-AI**: Brendan doesn't use Cowork yet but WANTS to; sometimes uses
  ChatGPT; wants flexibility → ship the model-neutral handoff format (lightweight): one
  paste-able prompt block that ends any external-AI/Cowork session with an outbox block
  the Brain's normal triage absorbs. (Brendan, R7)
- **D54 · Skills**: Scout pitches only, never installs; quarantine pilots; full audit first.
  Claude Mem: SKIP for now. PLUS a standing "never stagnant" mandate: a recurring AI-growth
  scan (Skill Scout duty, ~monthly in the paper) pitching new skills/tools/capabilities so
  Brendan's AI setup keeps advancing. (Brendan, R7, explicit)
- **D55 · FOR CLAUDE as a real note category** (site redesign adds it) — better than
  in-header text; all-caps in-text remains the fallback trigger. Newspaper gains Tea
  Business + Gym/Oura sections; suggestions welcomed. (Brendan, R7)

## Round 8 — Usage & multi-AI (2026-07-15, Wednesday; Brendan at ~50% weekly limit)

- **D56 · Usage pressure is a design constraint**: ~50% of weekly limit consumed by
  Wednesday. docs/USAGE_REDUCTION_PLAN.md M1–M8 adopted as recommendations; Brendan
  decides M1 (FootyBot pause). "Not super greedy" = default posture. (Brendan, R8)
- **D57 · FootyBot verdict pending**: Brendan leaning to drop ("honestly dumb, gets so
  much stuff wrong"). Fable recommendation: PAUSE now, resume ~08-11 single-lane WITH the
  missing data inputs (ADP export etc.) — accuracy problem is input starvation; repo and
  memory kept. Deletion is his call, not taken unilaterally. (Brendan + Fable, R8)
- **D58 · StockBot ROI mandate**: make daily trading run "worth my while" — sharpen
  mandate (D26 alpha) via proposed-prompt-change (safe-bot-edits), not more runs. (Brendan, R8)
- **D59 · Claude Code + Codex/GPT side-by-side**: Brendan has accounts for both and wants
  them cooperating ("I need something like this"). Confirmed feasible: both run in VS Code
  /CLI on the same repo; separate providers = separate limits, so Codex implementation
  passes cost zero Claude tokens; coordination via git + the model-neutral handoff
  (external-ai-handoff). Division: Codex = personal-os mechanical code tasks (Claude
  reviews PRs); Claude-only = brendan_brain + robot repos (policy adherence). Handoff
  skill PULLED FORWARD to Phase 1. (Brendan, R8)
- **D60 · No-VS-Code constraint (work computer)**: Brendan can't install anything for a few
  weeks. Multi-AI plan runs browser-only: Claude Code on web (already how everything here
  runs) + Codex cloud in the ChatGPT web UI (GitHub-connected, opens PRs) + plain-ChatGPT
  handoff paste as fallback. Codex GitHub access: personal-os ONLY, never brendan_brain
  or robot repos (D59 boundary). VS Code was never a requirement of the build. (Brendan, R8)
