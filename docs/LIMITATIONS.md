<!-- version: 1.1.0 (2026-07-11) — V2 additions at bottom -->
# Limitations — stated honestly

## Requires Brendan before it's live end-to-end
1. **UPDATE 2026-07-10 (activation):** integration is MERGED to every robot's `main` and
   prompt steps are applied; post-merge round-trips verified from the merged mains
   (op-20260710-postmerge-roundtrips). The single remaining activation step is adding
   `brendan_brain` to each routine's repository selection — only possible in the claude.ai
   routines UI (docs/START_HERE.md). Until then the guarded steps no-op harmlessly.
2. **First scheduled-run validation outstanding** (stress scenario 45): local/session
   behavior is tested; the first real cloud robot run with the Brain attached should be
   watched and its CHANGELOG checked.

## Platform limitations (no fix available in-session)
3. **No universal conversation capture.** Capture happens only in sessions/routines that
   have the Brain repo and invoke the skills. There is no platform-wide tap on all Claude
   conversations. Wording like "any conversation" means "any Brain-enabled conversation."
4. **No account usage/quota API.** Capacity scheduling uses a conservative manual ledger
   (system/CAPACITY_LEDGER.md) and priority policy, not real usage data. Effort estimates
   improve from run history, nothing better is possible today.
5. **No hard scheduler.** Routines fire on their configured schedules; the Brain can only
   prioritize within a session. Deadline-critical work should get its own routine slot.
6. **Skill sync is session-borne.** Updates propagate when a session with the repos side by
   side runs `tools/sync_skills.sh`. Drift between syncs is detectable (checksums, version
   headers, runtime check) but not self-healing.
7. **Egress in routine sandboxes is WebSearch-only** (inherited; affects robots' source
   verification — health AUDIT_QUEUE backlog predates this build).

## Design limitations (accepted, with triggers to revisit)
8. **Forgetting is working-tree-only by default.** Git history retains deleted content in
   every clone until a Brendan-supervised history rewrite. brain-forget says this plainly
   and stops at a plan. For truly radioactive content: don't commit it — keep it out of git.
9. **Cross-clone duplicate prevention is impossible without a coordination server**; we
   detect post-merge (validator) and recover instead. Same for op-ledger races (last-write-wins
   on a single op file; acceptable at one-owner scale).
10. **Retrieval is keyword/metadata-level.** Semantic recall ("truck" → tacoma) needs alias
    maps or embeddings — deferred until retrieval tests show real misses (evidence-first rule).
11. **Scale untested** beyond dozens of artifacts; thresholds and archival triggers are
    documented (STRESS_TESTS #27) but unexercised.
12. **Sanitization linting is pattern-based** (numeric+unit scrub on health outbox); a
    determined mistake can pass it. The hard wall remains the export contract + Publisher
    checklist, both model-judgment.
13. **Data Lab has no dataset yet** — no surf/WSL dataset repo is in the manifest; the
    capability doc (docs/DATA_LAB.md) and task pattern exist, fixtures only.

## Mocked / synthetic (never presented as real)
- Tacoma listings in the demo edition; the electrolyte "finding"; all test fixtures.
  Every one is labeled SYNTHETIC in place.

## V2 additions (2026-07-11, all live-verified)
14. **Web egress in this environment is WebSearch-only.** Arbitrary-host fetches (curl,
    Playwright, WebFetch) get CONNECT 403 from the org egress policy. Browser workflows
    are written tier-adaptive (BROWSER_RESEARCH_POLICY); tier 2/3 need a permissive
    environment network policy or a local session. Chromium + playwright-core themselves
    work (verified) — only the network gate blocks them here.
15. **Gmail connector surface in this session is read-by-id + trash/spam labels only**;
    its own tool docs reference search/list tools that aren't exposed here. Calendar/Drive
    expose zero tools until enabled. No Google Sheets connector exists.
16. **Shopify/QuickBooks are connected but BLOCKED by policy** pending Brendan's ownership
    answer (q-20260711-shopify-ownership) — work-boundary rule.
17. **Receipt ingestion is manual-paste** (no OCR/receipt connector). Photo → session
    transcription → paste format works today.
18. **Cross-routine timing is best-effort**: the 06:30-trading→07:05-editorial order is
    recommended times + a mechanical [FAIL]-and-publish gate, not a scheduler guarantee.
19. **Usage instrumentation has no token data** (no platform API) — observable fields only;
    usefulness is filled from Brendan's reactions, so fresh rows say "pending".
20. **The kitchen acceptance scenario ran at search tier**: methods synthesized from
    search-result content, labeled [CONC-inferred]; no direct page verification was
    possible in this environment.
21. **`tools/sanitize_external.py` is pattern-based and bypassable by construction.** It
    normalizes unicode, decodes visible base64, collapses whitespace, and neutralizes
    fence-spoofing (all regression-tested), but novel encodings, markdown-link/tracking-
    pixel exfiltration, and instruction phrasings outside its pattern list WILL pass it
    silently (verified by QA with two crafted payloads). It is a tripwire, not a wall —
    the wall is the fence contract: everything between UNTRUSTED markers is data, never
    instructions, no matter what it says (BROWSER_RESEARCH_POLICY rule 1).
22. **Connector "fail-closed" is policy, not mechanism** — see CONNECTOR_POLICY
    "Enforcement honesty": a session CAN physically call Shopify/QuickBooks tools; the
    mechanical option is a permission deny-rule in .claude/settings.json (recommended).
23. **Commerce/shopping site egress is blocked in the scheduled-run environment** (observed
    2026-07-15, tea input-sourcing scan). Direct WebFetch/curl to retail & supplier domains
    (mountainroseherbs.com, bulksupplements.com, uline.com, stickermule.com, amazon.com,
    etsy.com, and vendor pricing roots like stripe.com/pricing, squareup.com) return HTTP 403
    at the destination-host level — a network-policy block for this session, not per-site
    bot-protection and not a proxy fault (proxy status showed no relay failures). WebSearch
    still works, and some *docs* subdomains (docs.stripe.com, developer.squareup.com) are
    reachable via search. CONSEQUENCE: any research needing live prices/stock/listings from
    commerce sites will be search-corroborated at best and often [FAIL] outright — it cannot
    do primary-page verification. Sourcing/price-scrape tasks should be run from an
    environment with commerce egress, or handed to Brendan for click-through.
