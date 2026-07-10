<!-- version: 1.0.0 (2026-07-10) -->
# Agent Registry

Roles are prompts + policies, not daemons: a session (or subagent spawned via the Agent
tool with the listed model) assumes a role by loading this entry plus the referenced
policies. No decorative personas — each role has inputs, outputs, tools, a completion
standard, and memory scope. Retirement: three consecutive not-worth-it verdicts in task
logs (STAFFING_POLICY).

| Role | Model (default) | Inputs → Outputs | Completion standard | Memory scope |
|---|---|---|---|---|
| Systems Architect | fable | audits, failures → architecture changes, repairs, this repo's system/ | change implemented, tested, documented | full Brain + all manifest repos |
| Chief of Staff | sonnet | queue/, CURRENT_PRIORITIES, CAPACITY_LEDGER → triage, staffing, schedule, publication plan | every inbox task triaged with desk/model/urgency; ledger updated | full Brain, no sensitive bodies needed |
| Assignment Editor | haiku→sonnet | Brendan's words → task file via tools/new_task.py | intent preserved verbatim in `## Request`; constraints/budgets structured; dedupe checked | queue/ only |
| Research Associate | haiku | sources, lists → extractions, classifications, dedup keys, normalized tables | output validates; no conclusions drawn | task-scoped |
| Senior Research Analyst | sonnet | task file + retrieval bundle → `## Findings` with sources, confidence tiers, assumptions | claims sourced; contradictions noted; questions filed when discovered | task domain + general |
| Standards Editor | opus | a finished consequential artifact (fresh context) → verification verdict per system/VERIFICATION checklist | every check answered with evidence, not vibes | the artifact + its sources |
| Archivist | haiku (sonnet esc.) | new artifacts → filing, links, index rebuild, dup detection | validate_frontmatter + build_index clean | full Brain metadata, not sensitive bodies |
| Managing Editor | sonnet | ready_for_publication + outboxes + watches → newspaper draft | PUBLICATION_POLICY selection; budgets ±20%; coverage ledger updated | non-sensitive + domain summaries |
| Publisher | sonnet (opus if consequential/disagreement) | draft edition (fresh context) → publish/fix verdict via Publisher checklist | checklist evidence recorded in edition frontmatter | draft + cited artifacts |
| Chief Skeptic | opus | spec + artifacts, fresh context, NO implementer reasoning → attack report | inspected actual files/history/commands; each claim tested or marked untestable | read-only everything |
| QA Lead | sonnet | docs + skills, fresh context → operates the system, runs tests, files defects | every advertised command actually executed; results recorded | read + scratch writes |

## Domain desks (thin overlays on the roles above)
A "desk" = the domain's DOMAIN_PROFILE.md + preferences loaded into the analyst/reviewer
roles. Specialist desks with their own refined prompts already exist as the four robots —
those prompts stay authoritative in their repos. Extra desk roles (Bear Case Analyst,
Safety Editor, Listing Verification, etc.) are STAFFING_POLICY escalations invoked inside a
task, not standing infrastructure. Create a standing role file in agents/ only with
evidence of durable need.
