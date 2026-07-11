---
id: audit-20260711-v2-preimplementation
title: V2 pre-implementation audit (15-point checklist)
artifact_type: report
domain: general
sensitivity: personal
confidence: high
created_at: 2026-07-11
created_by: systems_architect
topics: [audit, v2, architecture]
---
# V2 Pre-Implementation Audit — 2026-07-11

Every point verified against actual files, commands, and live tool calls in this session
(branch `claude/brendan-os-v2-operations-1rg97c`, identical to `origin/main` @ d57068d).

## 1. Repository structure
As BRAIN_MAP.md describes: agents/ decisions/ docs/ domains/ (7 profiles) newspaper/
outcomes/ people/ predictions/ preferences/ projects/ queue/ (inbox·active·scheduled·
waiting_for_brendan·watches·completed·failed + append-only inbox files) skills/ sources/
system/ tests/ timeline/ tools/. 23 artifacts indexed. Generated: QUEUE.md, BRAIN_MAP.md,
system/INDEX.tsv.

## 2. Schemas (system/SCHEMAS.md v1.0.0)
13 artifact types (task, timeline, knowledge, report, prediction, outcome, decision, watch,
question, annotation, edition, operation, domain_profile). Shared vocabulary incl.
sensitivity (public/personal/private/health/financial), confidence, supersedes/derived_from.
Validated by tools/validate_frontmatter.py (stdlib YAML-subset parser in tools/brainlib.py).

## 3. Queue states
13 task statuses (brainlib.TASK_STATUSES); folder = convenience view, status authoritative;
FOLDER_STATUS mapping enforced by dashboard. Dedup via dedupe_key (new_task.py, open-status
scan, +1-interest note on duplicates). Watches carry next_run/last_run/publish_policy
(run_watches.py due|mark).

## 4. Newspaper pipeline
build_newspaper.py (draft) → Managing Editor edit → Publisher checklist (fresh eyes;
checklist_notes + publisher_verdict frontmatter) → --publish (refuses overwrite) → commit/
push/verify → 3-5 headline notification. PUBLICATION_POLICY: selection order, word budgets
(most_important 150 · investing 1000 · ff 500 · health 500 · jobs 300 · news 400 ·
open_research 500 · q&system 200), epistemic labels mandatory ([FACT]/[CONC]/[OBS]/[ASSUME]/
[PRED]/[PREF]/[RULE?]/[RULE]/[Q]/[FAIL]). Coverage ledger prevents repeats. Two real
editions exist (2026-07-08, 2026-07-11) + archived demo.

## 5. Annotation vocabulary
Inline: ⭐ 🙂 ❌, `>>` comments. Keywords: INCORRECT/WRONG, QUESTION:, DEEPER/research this
deeper, WATCH, STOP COVERING, CORRECTION:, REMEMBER THIS:, FORGET THIS:, CHANGE PREFERENCE:.
process_annotations.py --date --apply; attributes to nearest `###` heading; one reaction =
evidence, never a rule (tested in test_annotations.sh).

## 6. Model routing (system/MODEL_ROUTING_POLICY.md)
haiku/sonnet/opus/fable tiers verified available via Agent tool `model` param. Escalation
triggers + de-escalation + per-task research-log recording. Routing happens via subagent
model overrides; scheduled routines inherit session model.

## 7. Agent definitions (agents/AGENT_REGISTRY.md)
11 roles (Systems Architect→fable, Chief of Staff→sonnet, Assignment Editor, Research
Associate→haiku, Senior Research Analyst→sonnet, Standards Editor→opus, Archivist,
Managing Editor, Publisher, Chief Skeptic→opus, QA Lead→sonnet). Roles are prompts+policies,
not daemons. Desks = domain profile overlays, not standing roles. Retirement rule exists
(3 not-worth-it verdicts).

## 8. Learning-related capabilities (V1 state)
Preference evidence log (preferences/PROPOSED_RULES.md) + promotion thresholds
(MEMORY_POLICY: ≥3 signals across ≥2 days or explicit instruction) + INTEREST_PROFILE
weights + coverage ledger + REJECTED_RULES + predictions/outcomes scoring. NO structured
learning above preferences: no output-format learning record, no research-method learning,
no workflow learning, no calibration reports, no weekly learning report. This is the V2 gap.

## 9. Browser capabilities (verified live this session)
- Chromium binaries present (/opt/pw-browsers: chromium-1194, headless_shell-1194).
- playwright-core installs fine from npm (registry.npmjs.org is proxy-exempt).
- BUT arbitrary-host egress is DENIED by the environment's network policy:
  `https://example.com` → CONNECT 403 (curl, Playwright, and WebFetch all blocked;
  proxy status log shows "gateway answered 403 to CONNECT (policy denial)").
- WebSearch WORKS (server-side, returns titles/URLs/content summaries).
- Conclusion: in THIS environment the "browser" is WebSearch-first; live DOM automation
  requires Brendan to select a more permissive network policy for the environment
  (claude.ai → environment settings) or run in local Claude Code. Browser workflows must
  therefore be capability-probing and degrade honestly. Matches LIMITATIONS.md §7.

## 10. Connector availability (ListConnectors, live)
| Connector | State | Enabled in this session |
|---|---|---|
| Gmail | connected | yes (tools visible: get_message, apply_sensitive_*_label — read/label surface) |
| Intuit QuickBooks | connected (authless) | yes (full tool suite) |
| Shopify | connected | yes (full tool suite incl. orders/customers/analytics/GraphQL) |
| Indeed | connected | no (org-connected, toggled off here) |
| Google Calendar | unknown | no |
| Google Drive | unknown | no |
| S&P Global | unknown | no |
| Grasshopper Bank | unknown | no — and BANKING IS OUT OF SCOPE this phase per spec |
No Google Sheets connector listed. GitHub via MCP (session-scoped to brendahhn/brendan_brain).

## 11. Skills
5 canonical in .claude/skills/ (brain-ops, brain-sync, brain-newspaper, brain-domain,
brain-forget) + registry + sync mechanism (tools/sync_skills.sh, sync_manifest.tsv,
version headers, runtime self-check). safe-bot-edits is Brendan-authored in robots, not
Brain-owned.

## 12. Routine schedules (ROUTINE_REGISTRY, inferred — configs live outside git)
Jobs daily morning · FootyBot nightly ~23:30 PT · Health ~daily + Sunday digest · Trading
~daily pre-market · Brendan OS on-demand/scheduled. All four robots MERGED to main with
brain-sync; sole remaining activation step: adding brendan_brain to each routine's repo
selection (UI-only). Platform scheduling: cron via routines; CronCreate minimum interval
hourly per tool docs; ScheduleWakeup granularity 60s within a session. No hard scheduler
(LIMITATIONS §5).

## 13. Privacy boundaries
5-level sensitivity model; search-gate in brain_search.py (--domain match or
--allow-sensitive REASON); newspaper generic-conclusions-only for health; personal/work
boundary; origin_repository manifest check; secrets never in git; forgetting stops at plan.
Tested (test_retrieval, test_newspaper_sensitivity).

## 14. Test coverage
8 shell tests in sandboxed clones (queue_dedup, concurrent_writes, partial_failure,
retrieval, annotations, newspaper_sensitivity, forgetting, skill_sync). Baseline run this
session: 7 PASS, 1 FAIL — test_skill_sync fails ONLY because ../health-notebook is not
checked out in this session (environmental; fix: skip-with-notice when specialist repos
absent). STRESS_TESTS.md holds the scenario catalog. Tests run against committed HEAD.

## 15. Open issues
GitHub: 0 open issues, 0 open PRs (verified via MCP). Known outstanding from docs:
routine repo-selection activation (Brendan, UI), first scheduled-run validation,
LIMITATIONS list (no usage API, session-borne skill sync, keyword retrieval, etc.).

## V2 gap summary (what this build must add)
Intake routing beyond new_task.py flags (no immediate-vs-queued decision layer, no
ephemeral/no-memory mode) · no concierge/practical-life domain · no kitchen/pantry
structures or ingestion tools · no browser policy or injection defenses · no connector
policies (connectors exist but ungoverned) · no Cowork handoff · domain creation exists but
no signal-detection/proposal flow · no learning engine above preference evidence · no OCI ·
no skill foundry criteria · capacity ledger is a stub (no per-task usage records) · schedule
is not time-aware re: market open → editorial ordering.
