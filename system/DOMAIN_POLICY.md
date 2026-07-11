<!-- version: 1.1.0 (2026-07-11) — V2: detection signals, provisional domains, propose_domains.py -->
# Domain Policy

Domains are folders under `domains/` created by the brain-domain skill
(`python3 tools/new_domain.py <slug> --title "..."`). Do not pre-create empty domains.

## When a topic deserves…
- **A single task**: default. One-off question or research idea.
- **A watch**: Brendan says "keep watching" or a task's subject changes over time (listings,
  prices, a team's news).
- **A domain**: ≥3 artifacts accumulated OR a recurring interest with its own preferences.
- **A specialist routine**: a domain needs scheduled unattended runs with its own memory —
  propose to Brendan (new repo + routine config are his call).
- **A new agent role / skill**: only after STAFFING_POLICY evidence shows a durable need.

## Domain skeleton (created on demand)
`DOMAIN_PROFILE.md` (required; schema `domain_profile`) plus subfolders as needed:
`knowledge/ research/ observations/ predictions/ tasks/ preferences.md ACTIVE_QUESTIONS.md`.
Only DOMAIN_PROFILE.md is mandatory — no empty scaffolding clutter.

## Detection & proposal (V2)
`python3 tools/propose_domains.py` scans REAL signals only — per-topic artifact counts,
task/question accumulation, preference-evidence mentions (≥3 distinct, no existing home) —
and drafts a proposal in `system/proposals/` covering: name · why · what moves/links ·
initial structure · routine? · skill? · agent? · maintenance cost · provisional/permanent.
A session refines the draft and surfaces it via the newspaper questions section. One casual
question NEVER becomes a domain; "engagement telemetry"/"saved docs" signals don't exist
here and are not pretended (arch-challenge response #14).

## Provisional domains (V2)
`domain_status: provisional` + review date. Created freely under the autonomy ladder for
sustained activity; reviewed at ~30 days: promote to permanent (evidence in the profile) or
dissolve — files move back to `general`/tasks with an operations note; nothing is deleted.

## Seeded active domains (evidence: existing robots + Brendan's requests)
health (robot) · fantasy_football (robot) · investing (robot) · jobs (robot) ·
news (News Scout) · vehicles (Tacoma interest) · surfing (WSL/data interest) ·
concierge (V2, provisional — practical life ops).
