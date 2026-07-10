<!-- version: 1.0.0 (2026-07-10) -->
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

## Seeded active domains (evidence: existing robots + Brendan's requests)
health (robot) · fantasy_football (robot) · investing (robot) · jobs (robot) ·
news (News Scout) · vehicles (Tacoma interest) · surfing (WSL/data interest).
