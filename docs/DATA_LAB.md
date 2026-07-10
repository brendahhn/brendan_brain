<!-- version: 1.0.0 (2026-07-10) -->
# Data Lab

Reusable pattern for dataset exploration (surf/WSL data, league history, any personal
dataset). No dataset repo is currently in the manifest — pattern + fixtures only
(docs/LIMITATIONS.md #13). FootyBot's `inputs/` + `pipeline/` is the working in-domain
precedent and stays where it is.

## Task pattern
A Data Lab request is a normal queue task, `domain: <owning domain>`, with these REQUIRED
body sections (schema additions): `## Dataset` (location, permission boundary, tables/files
used), `## Method` (queries/code, assumptions, exploratory vs confirmatory — label which!),
`## Results`, `## Limitations`, `## Reproduce` (exact commands).

## Roles (in-task escalations per STAFFING_POLICY, not standing agents)
Explorer (haiku/sonnet: profile the data) → Hypothesis Researcher (sonnet) → Statistical
Reviewer (opus, MANDATORY before any "surprising" finding is published — surprise + small
samples is exactly the FootyBot overconfidence failure mode) → Insight Editor (sonnet:
newspaper-ready summary, exploratory findings labeled as exploratory).

## Boundaries
Employer datasets NEVER enter this repo or any personal repo (PRIVACY_POLICY #4). A work
Data Lab clones this pattern inside a work-owned environment.

## Natural requests that route here
"Look through my WSL dataset for overlooked indicators" · "Find something surprising in
this data" · "Test whether this relationship is real" (→ confirmatory, opus review) ·
"Only put it in the newspaper if the evidence is notable."
