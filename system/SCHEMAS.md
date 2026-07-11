<!-- version: 1.1.0 (2026-07-11) — added live_state type (V2 kitchen); see audits/2026-07-11-arch-challenge-response.md #5 -->
# Markdown Frontmatter Schemas

All artifacts use YAML frontmatter between `---` fences. Validate:
`python3 tools/validate_frontmatter.py --all`

## Shared field vocabulary

| Field | Type | Notes |
|---|---|---|
| `id` | string | `<type>-<YYYYMMDD>-<slug>`, stable forever |
| `title` | string | human title |
| `created_at` / `updated_at` | ISO date or datetime | |
| `artifact_type` | enum | `task`, `timeline`, `knowledge`, `report`, `prediction`, `outcome`, `decision`, `watch`, `question`, `annotation`, `edition`, `operation`, `domain_profile`, `live_state` |
| `domain` | string | folder name under `domains/`, or `general` |
| `status` | enum | per-type, below |
| `sensitivity` | enum | `public`, `personal` (default), `private`, `health`, `financial` |
| `confidence` | enum | `speculative`, `low`, `medium`, `high`, `confirmed` |
| `source_references` | list | URLs or `sources/` ids, with access date |
| `created_by` | string | agent role or `brendan` |
| `origin_repository` / `origin_routine` | string | where it came from |
| `supersedes` / `superseded_by` | id | correction chains; never delete the old file |
| `derived_from` | list of ids | provenance for promoted knowledge |
| `related` | list of ids | soft links |
| `topics` / `entities` | list | retrieval keys, lowercase |

## task (queue/*/task-*.md) — required: id, title, artifact_type, domain, status, created_at, urgency, depth

```yaml
---
id: task-20260710-tacoma-4cyl
title: Research 2002-2004 Toyota Tacoma 2.4L extra cab
artifact_type: task
domain: vehicles
status: inbox        # inbox|triaged|active|waiting_for_brendan|continuing_with_assumption|scheduled|verification|ready_for_publication|published|completed|failed|cancelled|watching
created_at: 2026-07-10
urgency: normal      # low|normal|high|urgent
depth: standard      # quick|standard|deep
deadline: 2026-07-11         # optional
word_budget: 400             # optional, for publication
effort_budget: 1_pass        # 1_pass|2_pass|until_strong
publication_destination: newspaper   # newspaper|file_only|none
recurrence: none             # none|daily|weekly|watch
assigned_desk: vehicle_desk  # optional
lead_model: sonnet           # optional; default per MODEL_ROUTING_POLICY
requires_brendan_answer: false
assumptions: []              # list of strings, each stated when used
questions_for_brendan: []    # list of {q, kind: blocking|material|optional, asked_at, answered: ...}
origin_repository: brendan_brain
dedupe_key: vehicles/tacoma-2002-2004-2.4l-xtracab   # normalized; see tools/new_task.py
---
```
Body sections (in order, omit empty): `## Request`, `## Constraints`, `## Assumptions`,
`## Questions`, `## Research Log` (append-only, dated entries with model used),
`## Findings`, `## Verification`, `## Publication`.

Task files LIVE in the folder matching their lifecycle stage (`queue/inbox/`, `queue/active/`,
`queue/waiting_for_brendan/`, `queue/scheduled/`, `queue/watches/`, `queue/completed/`,
`queue/failed/`). Moving stage = `git mv` + update `status`. `status` is authoritative;
folder is a convenience view. `tools/build_queue_dashboard.py` flags mismatches.

## timeline (timeline/YYYY/MM/YYYY-MM-DD-slug.md) — required: id, artifact_type, created_at, sensitivity

Raw dated observations. MUST preserve uncertainty; no interpretation beyond what was said.
```yaml
---
id: tl-20260710-example
artifact_type: timeline
created_at: 2026-07-10
domain: health
sensitivity: health
entities: []
verbatim: true    # true if close to Brendan's words
---
Brendan mentioned X. (No diagnosis, no causal claim.)
```

## knowledge (domains/<d>/knowledge/*.md) — required: id, artifact_type, domain, confidence, derived_from, sensitivity

Durable facts/conclusions. `confidence: confirmed` requires Brendan confirmation or strong
multi-source evidence recorded in `source_references`. Corrections: new file with
`supersedes: <old-id>`; add `superseded_by` to the old file. Never edit old conclusions in place.

## prediction (predictions/*.md) — required: id, domain, confidence, horizon, created_at
## outcome (outcomes/*.md) — required: id, prediction_id (or subject), result, scored_at
## decision (decisions/*.md) — required: id, created_at, status (proposed|made|revisited)
## watch (queue/watches/*.md) — task schema + `recurrence`, `last_run`, `next_run`, `publish_policy: on_change|always|threshold`
## question (newspaper/questions/*.md) — required: id, task_id, kind (blocking|material|optional), status (open|answered|expired), asked_at
## annotation (newspaper/annotations/*.md) — required: id, edition_id, created_at, status (unprocessed|processed)
## edition (newspaper/editions/YYYY-MM-DD.md) — required: id, artifact_type: edition, created_at
## operation (system/operations/op-*.md) — required: id, artifact_type: operation, repos (map repo→status: planned|committed|pushed|failed), started_at
## domain_profile (domains/<d>/DOMAIN_PROFILE.md) — required: id, artifact_type: domain_profile, domain, status (active|dormant)
Optional `domain_status: provisional|permanent` (V2): provisional domains carry a review
date in system/V2_LEDGER.md and may be dissolved back to tasks without a forgetting workflow.

## live_state (e.g. domains/concierge/kitchen/PANTRY.md) — required: id, artifact_type, domain, updated_at, sensitivity
The ONE mutable memory class (MEMORY_POLICY): live operational inventory/state. Last-write-
wins edits IN PLACE are allowed and expected; git history is the audit trail; supersede
chains do NOT apply. Never store conclusions here — facts about current physical state only.

## Sensitivity rules (enforced by tools/brain_search.py and PUBLICATION_POLICY)

- Artifacts in the health domain (and `health`/`private`/`financial`-tagged artifacts anywhere) are excluded from retrieval unless the query
  declares a matching `--domain` or `--allow-sensitive` with justification.
- Newspaper content drawn from sensitive artifacts must pass the Publisher checklist
  (system/PUBLICATION_POLICY.md) and appears only in its own domain section.
