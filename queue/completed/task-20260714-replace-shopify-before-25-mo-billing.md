---
id: task-20260714-replace-shopify-before-25-mo-billing
title: Replace Shopify before ~$25/mo billing starts in August
artifact_type: task
domain: tea-business
status: published
created_at: 2026-07-14
urgency: high
depth: deep
effort_budget: 1_pass
publication_destination: newspaper
recurrence: none
requires_brendan_answer: false
origin_repository: brendan_brain
dedupe_key: tea-business/replace-shopify-before-25-mo-billing
deadline: 2026-07-31
---

## Request

Shopify will start charging ~$25/month in August; not worth it for 14 orders/6 weeks. Brendan uses Shopify ONLY for order notifications + checkout behind his Lovable storefront. Research cheaper alternatives that hook into a Lovable site (Stripe Payment Links/Checkout, Square, Lemon Squeezy, Big Cartel, Shopify Starter $5 tier, etc.): monthly cost, per-transaction fees on ~$45 orders, Lovable embed path, order-notification mechanism (email/webhook), migration effort from current 2-product store. Recommend one; include verified pricing pages accessed live — NO unverified links or prices.

## Constraints

every price/link live-verified; provider-neutral inventory engine unaffected

## Assumptions

(none yet)

## Questions

(none yet)

## Research Log
- 2026-07-15 [sonnet] Read task file + system/BROWSER_RESEARCH_POLICY.md. Probed Tier 2
  (direct WebFetch) first: attempted stripe.com/pricing, squareup.com/us/en/pricing,
  lemonsqueezy.com/pricing, bigcartel.com/pricing, shopify.com/starter, shopify.com/pricing —
  **all six returned HTTP 403** on first and (for several) second attempt. Checked
  `$HTTPS_PROXY/__agentproxy/status`: `recentRelayFailures: []`, confirming the 403s are the
  vendor sites' own bot-protection, not a proxy fault. Per policy, downgraded to **Tier 1
  (WebSearch) for all five candidates** — every figure below is `[CONC-inferred]`
  (search-snippet synthesis), not `[FACT-verified]` direct-page confirmation, and is labeled
  accordingly.
- 2026-07-15 [sonnet] Ran 10 WebSearch queries covering: Stripe processing fees/Payment Links
  embed/notifications; Square online payment fees/payment links/webhooks; Lemon Squeezy
  pricing/checkout-overlay embed; Big Cartel plans/transaction-fee policy/free-tier features;
  Shopify Starter plan pricing/fee-stacking/Buy Button mechanics. Cross-checked each figure
  against ≥2 independent 2026-dated sources where possible (NerdWallet, Merchant Insiders,
  multiple Shopify-pricing breakdown sites, Stripe's own docs.stripe.com pages, Square's own
  developer/help docs, Lemon Squeezy's own docs.lemonsqueezy.com pages). Stripe embed
  mechanism and Square payment-link/webhook mechanism were corroborated directly against
  Stripe's and Square's own documentation domains (docs.stripe.com, squareup.com/help,
  developer.squareup.com), which WebSearch was able to surface content from even though the
  marketing/pricing root domains 403'd.
- 2026-07-15 [sonnet] Found one live disagreement worth flagging: aggregator sources agree
  Shopify Starter ($5/mo) adds a Starter-specific 5% transaction fee "even when using Shopify
  Payments," but they disagree on whether the *card processing* rate on top of that is the
  standard 2.9%+30¢ (most sources) or itself elevated to ~5% (one source, likely conflating
  the two 5%s). Could not resolve against Shopify's own pricing page (403 blocked both
  attempts). Treated the 2.9%+30¢-on-top reading as the more likely correct one (repeated
  across more independent sources, and consistent with Shopify's general Payments rate card),
  but flagged as uncertain in Verification below — doesn't change the recommendation either
  way since Starter loses badly under either reading.
- 2026-07-15 [sonnet] Did the per-order math for a $45 order and for the actual observed
  volume (14 orders / ~6 weeks, per task description) rather than a generic "per month"
  estimate, since 14 orders/6wk is well below any monthly-fee break-even point for most of
  these tools. See Findings.

## Findings

**Bottom line up front: transaction-fee percentage dominates at this volume, not the monthly
fee.** At 14 orders × $45 = $630 in revenue over ~6 weeks, even a "free" plan with a high
percentage fee costs more than a paid plan with a low one, and a plan that stacks two
percentage fees (Shopify Starter) is much worse than either alone.

| Option | $/mo | Fee on a $45 order | Total fee cost over 14 orders | Lovable embed path | Order notifications | Migration effort |
|---|---|---|---|---|---|---|
| **Stripe Payment Links / Checkout** | $0 | 2.9% + $0.30 = **$1.61** | **$22.47** | Paste a hosted Payment Link URL as a "Buy" button (`https://buy.stripe.com/...`), or embed Stripe's `<stripe-buy-button>` web component via a `<script>` tag directly in the Lovable page — no backend needed for either | Automatic email receipt to customer + Stripe Dashboard order view; optional `checkout.session.completed` webhook if Brendan later wants automated fulfillment | **Low.** Recreate 2 products as 2 Payment Links in the Stripe Dashboard; swap the checkout links/embed on the Lovable site; no customer/order data migration needed (Shopify was checkout-only) |
| **Square (Free plan)** | $0 | 3.3% + $0.30 = **$1.79** | **$25.05** | Create a Payment Link in Square Dashboard, save as a "buy button," paste embed snippet into Lovable site (or just link out) | Toggle-on email notification per payment link (Dashboard → Payments & orders → Payment links → Settings); webhooks available via Square API for automation | Low-medium. Similar to Stripe: recreate 2 items as payment links. Square's free-plan online rate rose from 2.9%→3.3%+30¢ as of Jan 2026 |
| **Lemon Squeezy** | $0 | 5% + $0.50 = **$2.75** | **$38.50** | Embed `lemon.js` (~2.3kB) via `<script>` tag; tag any `<a>` with class `lemonsqueezy-button` to open a checkout overlay on top of the Lovable site (no redirect) | Built-in email receipts (it's a Merchant of Record, handles tax too) + dashboard + webhooks | Low. But it's overkill for a US-only micro-business — the MoR tax handling isn't needed and the fee is the highest of the pay-as-you-go options |
| **Big Cartel** | $0 (free tier, ≤5 products) or $15/mo (Platinum, needed only past 5 products/for custom domain) | No Big Cartel platform fee; pass-through processor fee (Stripe) = **$1.61** | **$22.47** (free tier) or **~$22 + ~$21 pro-rated $15/mo** if Platinum needed | **Poor fit as-is** — Big Cartel is a full hosted storefront (its own subdomain/domain, own product pages), not a lightweight checkout widget; there's no documented simple "drop this button into any site" path the way Stripe/Square/Lemon Squeezy have. Using it would mean running a second storefront alongside Lovable, defeating the "checkout only, behind Lovable" goal | Order-management dashboard; third-party integrations (e.g. Zapier) for other notification routing | **High relative to the others** — would mean rebuilding a store on Big Cartel, not just swapping a checkout link |
| **Shopify Starter ($5/mo)** | $5 | Starter-specific 5% transaction fee **stacks on top of** standard card processing (~2.9%+30¢ most-sourced reading) = ~7.9% + $0.30 = **$3.86** (uncertain: one source reads this as ~10%+30¢ ≈ $4.80 — see Verification) | **~$54** (≈$5.83 in monthly fees pro-rated + ~$54 in per-order fees over ~1.4 months) — i.e. **worse than just staying on the current ~$25/mo Basic-tier plan** (~$25×1.4mo + 14×$1.61 ≈ $57 either way is in the same range, so Starter saves little to nothing) | Shopify's Buy Button embed code (`<script>` + product widget) pastes into any HTML site including a Lovable page; same mechanism Brendan already knows from Shopify | Same Shopify order-notification emails/Dashboard Brendan already has | **Lowest effort of all** (literally just downgrade the existing store's plan) — but the 5% Starter surcharge specifically penalizes small-storefront/buy-button use, which is exactly Brendan's use case, so the low migration effort doesn't pay off financially |

### RECOMMENDATION: Stripe Payment Links (or Stripe Checkout if a bit more control is wanted)

At 14 orders / 6 weeks, **Stripe is the cheapest option by a clear margin ($22.47 in total fees
over the period, zero monthly fee) and has the simplest embed path into a Lovable site** — a
single hosted-link "Buy" button or a copy-pasted `<stripe-buy-button>` script tag, no backend
required. It replaces both of Brendan's current Shopify uses: checkout (via the Payment Link)
and order notifications (automatic email receipt + Stripe Dashboard order log), with an
optional webhook if he later wants automation. Square is the closest runner-up (~$25.05 in fees
over the period, essentially the same embed pattern) and worth a second look only if Brendan
ever wants in-person/POS payments unified with online. Lemon Squeezy is a reasonable but
strictly more expensive alternative (its extra tax/Merchant-of-Record handling isn't needed for
a small US operation). Big Cartel and Shopify Starter are **not recommended**: Big Cartel is
architecturally a full storefront rather than a drop-in checkout, and Shopify Starter's 5%
Starter-plan surcharge stacks with card-processing fees precisely on the low-volume,
small-basket use case Brendan has, eating most or all of the savings versus just staying on
Shopify's ~$25/mo plan.

**Migration plan sketch:** create the two products as Stripe Payment Links in the Stripe
Dashboard (free, no code), replace the Shopify checkout links/buttons on the Lovable storefront
with the Stripe Payment Link URLs (or the Buy Button embed snippet), confirm Stripe's automatic
email-receipt setting is on, then cancel Shopify before the 2026-07-31 deadline. No product,
customer, or order-history migration is required since Shopify was never used as the storefront
or system of record.

## Verification

- **Tier 1 (WebSearch) only for all pricing figures** — Tier 2 (direct WebFetch) was attempted
  first for every vendor's own pricing page and returned HTTP 403 in every case (confirmed not
  a proxy issue via `$HTTPS_PROXY/__agentproxy/status`, `recentRelayFailures: []`). Every price
  below is `[CONC-inferred]` search-snippet synthesis, access-dated 2026-07-15, not a
  `[FACT-verified]` direct page read.
  - Stripe 2.9% + $0.30, no monthly fee — verified 2026-07-15 via WebSearch (multiple sources
    incl. content attributed to stripe.com/pricing; corroborated by NerdWallet, Merchant
    Insiders, checkoutpage.com). Direct fetch of stripe.com/pricing: 403, could not verify live
    on the primary page itself.
  - Stripe Payment Links Buy Button embed mechanism (`<script>` + `<stripe-buy-button>` web
    component) — verified 2026-07-15 via WebSearch surfacing docs.stripe.com/payment-links/
    buy-button content directly (docs subdomain was reachable through search even though
    stripe.com/pricing was not).
  - Square Free-plan online rate 3.3% + $0.30 (raised from 2.9%+30¢ Jan 2026) — verified
    2026-07-15 via WebSearch (Swipesum, Merchant Insiders, NerdWallet, Beacon Payments all
    independently report the same Jan 2026 increase). Direct fetch of squareup.com pricing
    pages: 403 both attempts, could not verify live on the primary page.
  - Square payment-link creation, embed-as-buy-button, and email-notification toggle path —
    verified 2026-07-15 via WebSearch surfacing squareup.com/help and developer.squareup.com
    content directly.
  - Lemon Squeezy 5% + $0.50 flat, no monthly fee — verified 2026-07-15 via WebSearch, multiple
    sources including content attributed to lemonsqueezy.com/pricing itself plus independent
    aggregators (Swell, Owelet, Creatdrop). Direct fetch of lemonsqueezy.com/pricing: 403,
    could not verify live on the primary page.
  - Lemon Squeezy `lemon.js` checkout-overlay embed — verified 2026-07-15 via WebSearch
    surfacing docs.lemonsqueezy.com content directly (script tag, `lemonsqueezy-button` class
    behavior).
  - Big Cartel: free tier 5 products / Platinum $15/mo (50 products) / Diamond $30/mo (500
    products), no Big Cartel platform transaction fee on any tier — verified 2026-07-15 via
    WebSearch (checkthat.ai, Wise, avada.io). Direct fetch of bigcartel.com/pricing: 403, could
    not verify live on the primary page. Whether the free tier's payment-processor connection
    (Stripe/PayPal) is fully unrestricted was **not independently confirmed** beyond aggregator
    summaries — flagged as a soft gap.
  - Shopify Starter $5/mo + 5% Starter transaction fee even with Shopify Payments — verified
    2026-07-15 via WebSearch, consistent across many independent 2026 pricing-breakdown sites.
    Direct fetch of shopify.com/starter and shopify.com/pricing: 403 both, could not verify
    live on the primary page.
  - Shopify's combined Starter rate (Starter 5% + card-processing rate) — **could not fully
    resolve**: most sources imply standard 2.9%+30¢ card processing stacks on top of the 5%
    Starter fee; one source's wording could be read as the card rate itself being 5%. Marking
    this specific sub-figure **unverified-precise** (directionally high either way, doesn't
    change the recommendation).
  - Shopify Buy Button embeds into any HTML site (WordPress/Squarespace/Wix/custom, which
    covers a Lovable-built site) — verified 2026-07-15 via WebSearch surfacing shopify.com/
    buy-button and help.shopify.com content.
  - Stripe/Square/Shopify order-notification mechanisms (automatic email receipts, dashboard
    order views, `checkout.session.completed` webhook for Stripe, `payment.updated` webhook for
    Square) — verified 2026-07-15 via WebSearch surfacing docs.stripe.com and
    developer.squareup.com content directly.
- No prices or URLs in this task were invented, reconstructed from memory, or copied from a
  prior session — every figure traces to a 2026-07-15 WebSearch result, and every case where
  the primary vendor page itself could not be fetched is marked above.

## Publication

Shopify's free trial ends in August (~$25/mo after), but for Drink Siesta's ~14 orders every 6
weeks, the fix isn't a cheaper Shopify tier — it's dropping Shopify entirely. **Stripe Payment
Links is the recommended replacement**: no monthly fee, a 2.9%+30¢ per-order fee (about $1.61
on a $45 order, ~$22 total over 14 orders), and it drops into the existing Lovable storefront as
either a plain "Buy" link or a one-line embedded button — no new backend. Square is a close,
slightly pricier runner-up; Lemon Squeezy costs more per order; Big Cartel isn't built to sit
"behind" another site the way Brendan needs; and Shopify's own $5/mo Starter tier is a trap here
— its 5% surcharge stacks with card fees and ends up costing about as much as just staying on
the $25/mo plan. Migration is light: recreate the 2 products as Stripe Payment Links and swap
the checkout links on the Lovable site before 2026-07-31, no data migration needed.
**Epistemic confidence: medium-high on the recommendation and relative ranking (multiple
independent 2026 sources agree on each headline fee), medium on exact figures** — every
vendor's own pricing page returned HTTP 403 to direct fetch this run (bot-protection, not a
proxy fault), so all prices are WebSearch-corroborated rather than directly confirmed on the
primary page; one sub-figure (Shopify Starter's combined percentage) is explicitly flagged as
imprecise above.
