---
id: audit-20260710-qa-skeptic-response
artifact_type: report
domain: general
sensitivity: personal
created_at: 2026-07-10
created_by: systems_architect
confidence: high
---
# Response to Chief Skeptic + QA Lead — 2026-07-10

Independent-assurance round 2: a fresh Opus Chief Skeptic attacked the completion claims;
a fresh Sonnet QA lead operated the system from the docs alone in a sandbox. Dispositions:

## Chief Skeptic (verdict: COMPLETION DISPROVEN on one blocking item)
| Finding | Disposition |
|---|---|
| 1 (CRITICAL) test suite 7/8 on HEAD — test_forgetting matched its own source in the sandbox clone; the recorded 8/8 predated committing the test file | **Accepted & repaired.** Marker now built at runtime + injected post-heredoc with a positive pre-deletion assertion (guards against vacuous pass — first fix WAS vacuous and was caught in-session); tests/ excluded from content sweeps. Suite 8/8 on committed HEAD, verified twice. |
| 2 (MAJOR) three docs claimed "8/8" while HEAD failed | **Accepted & repaired.** All three now record the true history including the failing period. |
| 3-14: 13 capability claims probed and HELD (sandboxing, fail-closed retrieval, legend fix, dedupe, oplog autocommit, robot mains untouched, edition integrity, round-trip, validator, skill sync, limitations honesty, git state) | No action needed; recorded as independently verified. |

## QA Lead (10 defects)
| # | Defect | Disposition |
|---|---|---|
| 1 BLOCKER publish silently overwrites a published edition | **Repaired**: --publish now REFUSES if the edition exists (explicit --force to supersede, after committing the original). |
| 2 BLOCKER watches could never fire (no next_run mechanics, no runner) | **Repaired**: tools/run_watches.py (`due`/`mark`), new_task seeds scheduler fields, OPERATIONS step 4 wired. Exercised on the real Tacoma watch (due → mark → next_run 2026-07-17 → not due). |
| 3 MAJOR forget left derived copies (outbox/editions/annotations/evidence) live | **Repaired**: brain-forget Phase 2 now mandates in-place redaction of every derived copy + full-repo final sweep; test extended with a derived outbox copy. Privacy outranks edition immutability; tombstone records the edits. |
| 4 MAJOR triage had no idempotency or scope definition | **Repaired (convention)**: `<!-- triaged YYYY-MM-DD -->` heading marker; scope limited to predictions/knowledge/questions sub-fields; predictions/README.md template added. No tool — model judgment with a mechanical guard. |
| 5 published editions kept status: draft | **Repaired**: --publish sets status: published and strips (DRAFT). |
| 6 publication_destination unused | **Repaired**: collection now requires `publication_destination: newspaper`; brain-ops mapping documents file_only. |
| 7 mid-word truncations (slug, question clip) | **Repaired**: word-boundary truncation in both. |
| 8 annotation attribution needs ### structure | **Repaired (doc)**: STRUCTURE RULE added to brain-newspaper. |
| 9 forget grep ambiguity (--include=*.md misses INDEX.tsv) | **Repaired (doc)**: skill now says grep everything. |
| 10 run_all.sh comment overclaimed | **Repaired**: comment states the intentional tests/results/ record. |

QA usability verdict on DAILY_GUIDE: "mostly yes for a non-developer", with the watch trust
gap as the one serious issue — now closed by #2. Skill updates re-synced to all four robot
repos (op-20260710-skill-sync-v1-qa-fixes, all repos verified).

Suite after all repairs: **8/8 PASS on committed HEAD** (tests/results/, latest run).
