<!-- version: 1.0.0 (2026-07-10) -->
# Privacy & Sensitivity Policy

## Sensitivity levels
- `public` — safe anywhere.
- `personal` (default) — Brendan-only surfaces (newspaper, Brain, his repos).
- `private` — intimate/personal; retrieval only with explicit domain match; never in the
  newspaper unless Brendan asked for that exact topic.
- `health` — medical observations, symptoms, meds, biometrics. Retrieval only for
  health-domain work. Newspaper: generic research conclusions only, never Brendan-specific
  values (labs, doses, symptoms); the Health section links to the health repo for detail.
- `financial` — portfolio/positions (hypothetical today). Domain-scoped like health.

## Hard rules
1. Sensitive artifact content never appears in: commit messages, cross-domain retrieval
   results, logs, test fixtures, other repos, or any external output.
2. `tools/brain_search.py` excludes `health|private|financial` unless the query declares a
   matching `--domain` or `--allow-sensitive <reason>`; the reason is logged in the artifact
   or task research log.
3. The Health Robot's personal context (health-notebook `architecture/` Part 8, personalized
   findings) stays in health-notebook. The Brain's `domains/health/` holds only task state,
   questions, sanitized summaries, and generic conclusions.
4. Personal/work boundary: no employer data enters this repo; no personal data leaves toward
   a work system. A future work system clones this architecture with separate account, repos,
   credentials, memory. Guardrail: `origin_repository` frontmatter must name a manifest repo;
   anything else fails validation.
5. Secrets/credentials never enter git. If spotted, stop and alert Brendan.
6. All repos private. Git history of sensitive files means true deletion requires history
   rewriting — the forgetting workflow (docs/FORGETTING.md) must say so explicitly.

## Test obligations
Sensitive-retrieval leakage and newspaper leakage are covered by tests/test_retrieval.py and
tests/test_newspaper.py using SYNTHETIC sensitive fixtures only (tests/fixtures/). Real
health/financial content must never be used as test data.
