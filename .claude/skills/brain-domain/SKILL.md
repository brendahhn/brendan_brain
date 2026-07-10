---
name: brain-domain
description: >-
  Create or evolve a Brendan OS domain. Use when Brendan mentions a new interest/hobby that
  doesn't fit existing domains, says "create a domain for this", or when ≥3 artifacts have
  accumulated for a topic without a home.
---
<!-- brendan-os-skill-version: 1.0.0 (2026-07-10) — canonical source: brendan_brain/.claude/skills/brain-domain -->
# brain-domain

Decision ladder first (system/DOMAIN_POLICY.md): single task → watch → domain → specialist
routine. Require a meaningful reason; don't create structural clutter for a one-off.

Create: `python3 tools/new_domain.py <slug> --title "..." [--sensitivity ...] --reason "..."`
Then: fill DOMAIN_PROFILE.md with what's known (link source artifacts), add an
INTEREST_PROFILE.md row (weight 2 until evidence), move any homeless artifacts in
(`git mv`, update `domain:` frontmatter), rebuild index + map, commit.

Proposing a new specialist ROUTINE (needs Brendan): write a decision artifact in
`decisions/` covering: why the domain needs unattended scheduled runs, proposed repo name,
the three-file pattern (prompt/notebook/idea-queue) it would follow, and what it would
exchange with the Brain via brain-sync. Surface in the newspaper questions section.
