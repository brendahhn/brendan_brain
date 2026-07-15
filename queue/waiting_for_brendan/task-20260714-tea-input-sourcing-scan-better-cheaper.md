---
id: task-20260714-tea-input-sourcing-scan-better-cheaper
title: Tea input sourcing scan — better/cheaper suppliers for all components
artifact_type: task
domain: tea-business
status: waiting_for_brendan
created_at: 2026-07-14
urgency: normal
depth: deep
effort_budget: 1_pass
publication_destination: newspaper
recurrence: none
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: tea-business/tea-input-sourcing-scan-better-cheaper
---

## Request

Compare suppliers for: organic/clean chamomile and lemon balm; L-theanine, glycine, taurine powders; unbleached cotton tea bags; big muslin bags; herb tins (same size), powder tins (same or slightly smaller); boxes (same dimensions); stickers, mini scoops, instruction cards. Rank by unit cost delivered, but reject big-MOQ options (no ~500-unit buys). Report unit-cost per order using know-20260714-tea-bom. NEVER order or add to cart — findings only. Every link and price must be live-verified at research time (prior sessions gave Brendan nonexistent links and wrong prices).

## Constraints

verified links only; no cart actions; no MOQ >100 units without flagging

## Assumptions

(none yet)

## Questions

(none yet)

## Research Log

- 2026-07-15 [sonnet] Read know-20260714-tea-bom (domains/tea-business/bom-20260714.md) and
  know-20260713-tea-physical-inventory. **Gap found:** neither file, nor DOMAIN_PROFILE.md,
  records any current unit $ cost for any component — the BOM has quantities-per-order only.
  There is no existing cost baseline in the Brain to beat; this scan produces first candidate
  pricing signals, not a cost-delta comparison. Flagging this back to Brendan/the Brain as a
  data gap (a "log current supplier + unit cost" pass would let future scans do real deltas).
- 2026-07-15 [sonnet] Tested live verification capability before researching: attempted WebFetch
  on mountainroseherbs.com, starwest-botanicals.com, bulksupplements.com, uline.com,
  stickermule.com, amazon.com, etsy.com, and a control (en.wikipedia.org). **All returned HTTP
  403** via WebFetch. Cross-checked with direct `curl` through the session's egress proxy
  ($HTTPS_PROXY) — every one of those hosts, including the Wikipedia control, failed with
  "CONNECT tunnel failed, response 403". `curl -sS "$HTTPS_PROXY/__agentproxy/status"` confirms
  the proxy itself is enabled and healthy (no relay failures), so this is a destination-host
  policy block (per /root/.ccr/README.md: "403/407 from the proxy... destination host is not
  allowed... do not retry or route around it"), not a per-site bot-block and not a proxy fault.
  **Conclusion: WebFetch/curl cannot reach any external commerce site from this session.**
  Falling back to WebSearch only, per the task's explicit fallback instruction.
- 2026-07-15 [sonnet] Ran WebSearch for each component (queries logged below per component).
  WebSearch itself works, but for nearly every query the tool's own summary states the exact
  current price for the specific pack size needed "is not displayed in the search results" —
  results are mostly product-listing links, with occasional price fragments surfaced from
  either (a) the retailer's own page title (e.g. Sticker Mule deal pages), or (b) third-party
  aggregators/trackers (camelcamelcamel, Accio, blog cost-guides) which are not the primary
  source and may be stale, promo-specific, or quantity-mismatched. Per the task's rule, none of
  these meet the "fetched the actual page, quoted with access date" bar for "verified." Every
  price below is labeled unverified accordingly, sourced to the search query that produced it.

## Findings

**Overall:** No component below has a price that meets this session's verification bar — see
Verification section and the Research Log entries above for why (WebFetch/curl blocked
end-to-end on every commerce domain tested; WebSearch snippets don't reliably carry confirmed
current prices). Because the Brain also has no recorded baseline unit cost for any component
(see Research Log), I cannot honestly report "X is cheaper than what Brendan pays now" for
anything — only candidate suppliers/links worth Brendan spot-checking himself. MOQ signals are
somewhat more reliable (they're structural facts about how the listing is sold, not price
snapshots) but are still search-snippet-derived, not page-confirmed, so still flagged.

1. **Organic chamomile flowers** — Candidates: Mountain Rose Herbs, US-grown organic, sold
   loose by the bag (1 oz / 4 oz / 1 lb — no case requirement, single bag purchasable) —
   https://mountainroseherbs.com/chamomile-flowers-organic-us-grown. Alt: Starwest Botanicals
   Organic Chamomile (also via Amazon), similarly sold per-bag. Price: unverified (page fetch
   blocked; WebSearch did not surface a $ figure). MOQ: none apparent — buy one bag.
2. **Organic lemon balm** — Candidate: Starwest Botanicals Organic Lemon Balm Leaf, Cut &
   Sifted, 1 lb resealable bag — https://www.starwest-botanicals.com/product/lemon-balm-leaf-c-s-organic/.
   Price: unverified. MOQ: none — single bag.
3. **L-theanine powder** — Candidate: BulkSupplements L-Theanine Powder, sold in 100 g / 250 g /
   500 g / 1 kg — https://www.bulksupplements.com/products/ltheanine. Price: unverified (page
   blocked). One aggregator (Accio) surfaced a wholesale 25 kg case at roughly $40/kg, but that's
   a tonnage/wholesale figure unrelated to the small pack sizes needed here and not confirmed
   against the actual small-pack price — do not treat as usable. MOQ: none — single 100 g bag.
4. **Glycine powder** — Candidate: BulkSupplements Glycine Powder, 100 g–5 kg —
   https://www.bulksupplements.com/products/glycine-pure-powder. Price: unverified. MOQ: none.
5. **Taurine powder** — Candidate: BulkSupplements Taurine Powder, 100 g–25 kg —
   https://www.bulksupplements.com/products/taurine. Price: unverified. MOQ: none.
   (For all three powders, PureBulk.com surfaced as a second potential supplier in search but
   was not independently checked for price/MOQ this pass.)
6. **Unbleached cotton tea bags** — Candidates: NUIBY unbleached drawstring tea filter bags,
   100-count (Amazon, https://www.amazon.com/Filter-Unbleached-Natural-Drawstring-Herbal/dp/B01LX1GGOL);
   Housim reusable unbleached cotton tea bags, 50-pack, search snippet quoted "$8.99 ($0.18/bag)"
   (https://www.amazon.com/Reusable-Unbleached-Strainer-Friendly-Infuser/dp/B085PYJZDD) — that
   $/unit figure came from the WebSearch snippet text, not a fetched page, so treat as a lead,
   not a confirmed price. MOQ: 50–100 count packs — under the cap either way.
7. **Big muslin bags** — Candidates: Biglotbags 100-pack cotton double-drawstring muslin bags,
   search snippet said "on sale from $8.99" (ambiguous — unclear if that's per-bag or a
   mis-scraped smaller-pack price; https://biglotbags.com/products/10-x-12-inches-100-cotton-single-drawstring-premium-quality-muslin-bags);
   The Cotton Factory quoted "starting at $1.25 per bag" wholesale (https://www.thecottonfactory.org/products/bulk-muslin-bags).
   Both unverified and the Biglotbags figure specifically looks unreliable (likely misattributed
   during scraping). MOQ: packs as small as 25–100 appear available — under the cap, unconfirmed.
8. **Herb tins ("big jar")** — Candidate: PremiumVials 100-pack 4 oz aluminum screw-top tins
   (https://www.premiumvials.com/100-pack-metal-tins-4-oz-aluminum-containers-with-lids-screw-top-round-tin-cans-for-cosmetic-lip-balm-diy-salves-candles-wax/)
   — **MOQ sits exactly at the 100-unit cap boundary; flagging as borderline, confirm with
   Brendan before treating as compliant.** Alt: Specialty Bottle (specialtybottle.com) sells 4 oz
   tins with "no small-order fees" per search summary, implying smaller quantities than a fixed
   100-case are purchasable — potentially the safer MOQ choice, but not price-confirmed. Price:
   unverified for both.
9. **Powder tin (slightly smaller)** — Candidate: RestaurantWare 2 oz round tin, screw lid,
   sold in a 100-count box (https://www.restaurantware.com/products/chef-101-2-oz-round-black-tin-container-with-screw-lid-100-count-box)
   — **MOQ = 100, again at the cap boundary, flag.** Alt: Specialty Bottle 1/2 oz / 1 oz / 2 oz
   screw-top tins, "no small-order fees" (https://www.specialtybottle.com/metal-tin-containers/screw-top)
   — likely allows smaller quantities but not confirmed. Price: unverified for both.
10. **Boxes (fixed dimensions)** — Candidates surfaced: Teal Packaging, PackHit, CustomBoxMakers
    (kraft box printers). WebSearch aggregator summaries quoted "$0.44/unit" and "$0.30/unit"
    figures and noted "orders below 100 units carry 3–8x higher per-unit surcharges," with some
    providers' MOQ starting at 50 units. These figures are aggregator/blog-derived, not
    sourced to one specific product page or box spec, and are low-confidence. No usable link-plus-
    price pair could be verified this pass. MOQ: appears to vary 50–100+ by vendor — needs a
    direct quote against Drink Siesta's actual box dimensions, which this pass did not obtain.
11. **Stickers** — Candidate: Sticker Mule custom die-cut stickers. Search surfaced several of
    Sticker Mule's own promo page titles directly: "$1 for 10" (stickermule.com/deals/4b02bdaf),
    "$9 for 50" (stickermule.com/deals/ee2c2ae3), "$0.80 for 10" (stickermule.com/deals/f167bd20).
    These are page titles pulled live by search, which is somewhat more credible than an
    aggregator paraphrase, but they are promo/first-order deals that may not reflect Brendan's
    steady-state reorder price, and the page itself was not fetched to confirm current status —
    still marked unverified. MOQ: as low as 10 — comfortably under the cap.
12. **Mini scoops** — Candidate: BeakersWorld 1/4 tsp plastic measuring scoop, 100-pack
    (https://beakersworld.com/product/1-4-teaspoon-plastic-measure-natural-pack-of-100-measuring-scoops/);
    alt Walmart "Bulk Pack of 100 Pink Plastic Measuring Scoops, 1.5 tsp"
    (https://www.walmart.com/ip/Bulk-Pack-of-100-Pink-Plastic-Measuring-Scoops-1-5-Teaspoon-10ml-Perfect-for-Coffee-Tea-Milk-Powder-and-More/5256348693).
    **MOQ = 100 for both — exactly at the cap, not over it, but flag as boundary.** Price:
    unverified for both.
13. **Instruction cards** — Candidate: VistaPrint custom cards, search snippet said "50 for $10"
    (~$0.20/card, unverified, and note this pricing was for standard business cards, not
    confirmed against an instruction-card template/size — could differ). MOO's per-100 price was
    not surfaced by search this pass. MOQ: ~50, under the cap.

## Verification

Every entry below: access attempted 2026-07-15.

| Item | Link | Live-fetch status | Price status | MOQ status |
|---|---|---|---|---|
| Chamomile | mountainroseherbs.com/chamomile-flowers-organic-us-grown | unverified — WebFetch 403; curl to host also 403 (proxy policy) | unverified — no $ in search | unverified, likely none |
| Lemon balm | starwest-botanicals.com/product/lemon-balm-leaf-c-s-organic/ | unverified — WebFetch 403; curl 403 | unverified | unverified, likely none |
| L-theanine | bulksupplements.com/products/ltheanine | unverified — WebFetch 403; curl 403 | unverified (25kg wholesale figure discarded as inapplicable) | unverified, likely none |
| Glycine | bulksupplements.com/products/glycine-pure-powder | unverified — WebFetch 403; curl 403 | unverified | unverified, likely none |
| Taurine | bulksupplements.com/products/taurine | unverified — WebFetch 403; curl 403 | unverified | unverified, likely none |
| Tea bags (NUIBY) | amazon.com/.../dp/B01LX1GGOL | unverified — WebFetch 403 on amazon.com (curl-confirmed proxy block) | unverified | 100-count listed, unverified |
| Tea bags (Housim) | amazon.com/.../dp/B085PYJZDD | unverified — same | unverified (snippet said $8.99/$0.18ea) | 50-count listed, unverified |
| Muslin bags (Biglotbags) | biglotbags.com/products/10-x-12-inches... | unverified — WebFetch 403; curl 403 | unverified, snippet figure looks unreliable | 100-pack listed, unverified |
| Muslin bags (Cotton Factory) | thecottonfactory.org/products/bulk-muslin-bags | unverified — WebFetch 403; curl 403 | unverified ("$1.25/bag" snippet) | unverified |
| Herb tin (PremiumVials 4oz) | premiumvials.com/100-pack-metal-tins-4-oz... | unverified — WebFetch 403; curl 403 | unverified | **MOQ = 100, at cap boundary — flagged** |
| Herb tin (Specialty Bottle) | specialtybottle.com/metal-tin-containers/... | unverified — WebFetch 403; curl 403 | unverified | unverified, "no small-order fees" claimed |
| Powder tin (RestaurantWare 2oz) | restaurantware.com/products/chef-101-2-oz... | unverified — WebFetch 403; curl 403 | unverified | **MOQ = 100, at cap boundary — flagged** |
| Powder tin (Specialty Bottle) | specialtybottle.com/metal-tin-containers/screw-top | unverified — WebFetch 403; curl 403 | unverified | unverified, "no small-order fees" claimed |
| Boxes | tealpackaging.com / packhit.com / customboxmakers.com | unverified — WebFetch 403; curl 403 | unverified (aggregator-derived $0.30–$0.44/unit, low confidence) | unverified, vendor MOQs reported 50–100+ |
| Stickers | stickermule.com/deals/4b02bdaf, /ee2c2ae3, /f167bd20 | unverified — WebFetch 403; curl 403 (page titles only, live search) | unverified (promo pricing, may not persist) | MOQ ~10, unverified but low-risk |
| Mini scoops (BeakersWorld) | beakersworld.com/product/1-4-teaspoon... | unverified — WebFetch 403; curl 403 | unverified | **MOQ = 100, at cap boundary — flagged** |
| Mini scoops (Walmart) | walmart.com/ip/Bulk-Pack-of-100-Pink... | unverified — WebFetch 403; curl 403 | unverified | **MOQ = 100, at cap boundary — flagged** |
| Instruction cards (VistaPrint) | vistaprint.com/business-cards/standard | unverified — WebFetch 403; curl 403 | unverified ("50 for $10" snippet, wrong product type) | MOQ ~50, unverified |

Infrastructure note: WebFetch and direct `curl` (through the session's own egress proxy) both
failed with 403 on every external commerce domain tested this session, including a Wikipedia
control — confirmed proxy-status healthy via `curl "$HTTPS_PROXY/__agentproxy/status"`. This
looks like a session-level egress policy restriction rather than a research failure; a future
run with commerce-site access (or Brendan clicking the links above himself) is needed to turn
any of these into genuinely verified prices.

## Publication

This scan could not verify any supplier price or link to the standard Brendan requires (live
page fetch with access date) — the session's network access was blocked end-to-end for every
commerce site tried, including a control site, so WebSearch snippets are all that's reported,
clearly marked unverified. Separately, the Brain currently has no recorded baseline unit cost
for any tea-business input, so even fully-verified prices this run would only be a first
data point, not a "cheaper than what you pay now" comparison. Candidate leads worth Brendan's
own click-through: Sticker Mule for stickers (MOQ as low as 10) and Mountain Rose Herbs/Starwest
Botanicals for the herbs (no case MOQ, buy single bags) look structurally promising on MOQ
grounds alone. Three packaging items — the 4 oz herb tin, the 2 oz powder tin, and the mini
scoops — showed MOQs sitting exactly at the 100-unit cap boundary and should be double-checked
before ordering. Epistemic confidence: low on all prices (unverified), moderate on MOQ
structure, and this task should be re-run once web access from this environment reaches
commerce sites, or handed to Brendan for direct verification.
