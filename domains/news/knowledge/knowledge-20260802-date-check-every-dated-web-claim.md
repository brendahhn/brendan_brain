---
id: knowledge-20260802-date-check-every-dated-web-claim
title: Date-check every dated claim from web search — aggregator summaries recycle stale content as current
artifact_type: knowledge
domain: news
confidence: medium
sensitivity: public
created_at: 2026-08-02
created_by: brain-daily-run
origin_repository: trading-notebook
derived_from: [inbox-trading-robot-20260802, inbox-trading-robot-20260801, inbox-trading-robot-20260731, inbox-trading-robot-20260729]
topics: [research-hygiene, web-search, dated-claims, epistemics, cross-domain]
---
Search-aggregator summaries do NOT reliably carry forward accurate dates: they recycle
stale-dated content as if it were current. This is a general research-hygiene rule for any
domain that leans on live web search for time-sensitive claims (news, trading, jobs, sports),
not a trading-specific quirk. Every dated claim — a price, an earnings date, an outbreak count,
a policy effective date, a credit-rating action, a headline — needs an explicit date-check
against a primary source before it is trusted or acted on.

Evidence: the trading desk has caught this failure mode repeatedly across independent runs and
agents — a three-year-old sovereign-credit-rating headline resurfacing as current (08-02); a
search-summary hallucination claiming a real company's Q2 earnings had already released when
they had not, re-dated to ~Aug 5 (07-31/08-01); a full year-old earnings figure and recycled
prior-run price snapshots masquerading as fresh (07-29/07-30). The pattern recurs even when
different agents and different tickers are involved, which is what makes it a cross-domain
caution rather than a one-off.

Concrete consequence already recorded: the mis-dated earnings date corrupted a live prediction
(prediction-20260712-hdsn-earnings assumed a 2026-07-29 print that had actually slipped to
~Aug 5), scored incorrect on 08-02 partly because its premise was contaminated. The cost of
skipping the date-check is real.

Proposed by the trading-robot as durable, cross-domain knowledge; promoted here on
multi-occurrence evidence per MEMORY_POLICY. Not yet Brendan-confirmed as a standing rule.
