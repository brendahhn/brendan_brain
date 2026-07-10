<!-- version: 1.0.0 (2026-07-10) -->
# Architecture

## Shape
Five independent repos, five independent histories. `brendan_brain` is the exchange layer;
the four robots stay authoritative for their domains (their prompts/notebooks/queues are
untouched — audit: system/audits/2026-07-10-initial-audit.md).

```
brendan_brain (coordination)         specialist repos (domain authority)
├── queue/          ←──────────────  outbox blocks: queue/inbox/from-<robot>.md
├── preferences/    ──────────────→  read at robot run start (brain-sync skill)
├── newspaper/      (editions ← ready tasks + outboxes; annotations → tasks/evidence)
├── timeline/ domains/ predictions/ outcomes/ decisions/ sources/
├── system/         (policies, schemas, op ledger, audits, INDEX.tsv)
├── tools/          (stdlib Python: validate, search, queue, newspaper, annotations, oplog)
└── .claude/skills/ (canonical; synced by checksum to robots: brain-sync, brain-ops)
```

## Load-bearing decisions (and why)
1. **Markdown+Git only.** Single owner, <1k artifacts, full auditability, hand-editable.
   Index/SQLite deferred until evidence demands it (RETRIEVAL_POLICY threshold).
2. **One file per artifact, status in frontmatter, folders as views.** Makes concurrent
   writes mergeable and history legible. Generated dashboards are disposable.
3. **Robots exchange via one append-only outbox file each, dated blocks, same-day replace.**
   Idempotent retries, no shared-file contention, robot-side cost is one read + one append.
4. **Non-atomic cross-repo ops are embraced, not hidden**: op ledger with per-repo states,
   auto-committed so the record of a failure survives the failure.
5. **Sensitivity fails closed by domain** (health/investing), not by trusting a tag.
6. **Generation/review separation**: drafts need an explicit Publisher verdict to publish;
   consequential items escalate reviewer model per MODEL_ROUTING_POLICY.
7. **Skills have one canonical home** (here) + checksum-verified sync; version headers +
   runtime major-version check catch drift the sync missed.

## Agent organization
Roles are prompt+policy overlays, not daemons (agents/AGENT_REGISTRY.md): Chief of Staff
(sonnet) triages; analysts research; Standards Editor/Publisher (opus when consequential)
review with fresh context; Archivist files; Chief Skeptic attacks. Staffing beyond one
sonnet lead requires a logged justification and gets a logged verdict (cost discipline).

## What was deliberately NOT built
PostgreSQL/vector DB/web app (no demonstrated need); a hard scheduler (platform provides
none — CAPACITY_LEDGER holds policy + estimates instead); prompt edits to robots (proposed
as reviewable diffs instead); automatic history rewriting (forgetting stops at a plan).

Full policy set: system/. Review trail: system/audits/ (challenge + response).
