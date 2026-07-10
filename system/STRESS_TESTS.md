<!-- version: 1.0.0 (2026-07-10) -->
# Stress Test Matrix

48 required scenarios → prevention / detection / recovery / audit / remaining limitation.
Status: **T** = covered by automated suite (tests/run_all.sh, 8/8 passing 2026-07-10),
**E** = exercised live during the build (evidence linked), **D** = design-covered (policy +
mechanism exist; no automated test yet), **L** = known limitation.

| # | Scenario | How handled | Status |
|---|---|---|---|
| 1 | Two routines update Brain simultaneously | one-file-per-artifact + rebase recovery; both sides survive | **T** test_concurrent_writes |
| 2 | Two conversations add same idea | dedupe_key → DUPLICATE + interest signal | **T** test_queue_dedup, **E** Tacoma demo |
| 3 | Task begins with missing info | assumptions recorded, `continuing_with_assumption` | **E** Tacoma demo |
| 4 | Important question arises mid-research | question artifact + task `## Questions`, non-blocking | **E** Tacoma frame-rust question |
| 5 | Brendan never answers | assumptions persist; question stays open in every edition; task completes on assumptions | **D** (expiry: questions get `status: expired` at editor's discretion) |
| 6 | Crash after edit, before commit | git status shows dirty tree; next session sees uncommitted work + unfinished op records | **E** (reviewer collision recovered exactly this way) |
| 7 | Commit but push fails | ls-remote verification catches it; retry w/ backoff; op record stays unverified | **T** test_partial_failure, **E** build hit this live |
| 8 | One repo pushes, another fails | oplog per-repo states; PARTIAL visible; resume idempotent | **T** test_partial_failure |
| 9 | Source disappears after citation | source + access date recorded; SOURCE_RELIABILITY tracks failures | **D** |
| 10 | Listing inactive before publication | pre-publication freshness pass; drop + note | **E** Tacoma candidate #2 |
| 11 | Later finding contradicts knowledge | supersedes/superseded_by chain; old file kept | **D** (schema enforced by validator) |
| 12 | Casual observation treated as fact | timeline artifacts carry uncertainty; promotion needs evidence + provenance (MEMORY_POLICY) | **D** |
| 13 | One reaction → permanent preference | evidence log only; ≥3 signals/≥2 days or explicit instruction to confirm | **T** test_annotations |
| 14 | Ambiguous ❌ (bad article vs kill topic) | one evidence signal + clarifying question next edition; never guessed | **D** (brain-newspaper skill) |
| 15 | Sensitive health note in unrelated context | fail-closed domain gating in search; withheld notice on stderr | **T** test_retrieval |
| 16 | Personal routine reads work data | no work repos in manifest; origin_repository validation fails unknown repos | **D** validator guard |
| 17 | Work routine writes personal Brain | same guard + separate-credentials policy (PRIVACY #4) | **D**/**L** (enforced by repo ACLs, not code) |
| 18 | Newspaper over budget | editor trims to ±20%; Publisher checklist #3 | **E** edition 2026-07-11 |
| 19 | Domain with nothing to report | section omitted with one line | **T** test in build_newspaper (empty sections), **E** edition |
| 20 | New hobby fits no domain | brain-domain ladder; new_domain.py | **D** (tool tested manually) |
| 21 | Haiku weak consequential conclusion | routing forbids; escalation triggers; Standards Editor gate | **D** policy |
| 22 | Sonnet and Opus disagree | disagreement = escalation trigger (STAFFING); Publisher goes opus | **D** policy |
| 23 | Agent team costs > value | per-task staffing verdicts; 3-strike retirement | **E** Tacoma log records a "solo was fine" verdict |
| 24 | Skill update reaches one repo not others | checksum manifest + sync --check + version headers | **T** test_skill_sync |
| 25 | Git merge conflict | rebase policy per file class | **T** test_concurrent_writes |
| 26 | Correct old memory without erasing | supersede chain, never in-place | **D** |
| 27 | Brain grows to tens of thousands of files | monthly timeline folders, one-file-per-artifact, archival proposal at ~200/folder; INDEX threshold ~5k | **L** untested at scale; revisit trigger documented |
| 28 | Forget sensitive info | brain-forget plan→confirm→execute; tombstone; honest about git history | **T** test_forgetting (synthetic only) |
| 29 | Routine claims success after failure | run_status in outbox contract; ls-remote proof required; AUTONOMY failure-honesty rule | **D** |
| 30 | QUEUE.md inconsistent with tasks | dashboard rebuild flags mismatches, exit 2 | **T** test_queue_dedup |
| 31 | Retrieval misses related timeline event | scored search + stemming; recall tests | **T** test_retrieval (basic); **L** semantic recall unproven beyond keyword match |
| 32 | Retrieval surfaces irrelevant sensitive event | fail-closed by domain | **T** test_retrieval |
| 33 | Same conclusion, conflicting wording across domains | Archivist dup detection + related links | **L** manual today |
| 34 | Robot re-asks answered question | answered questions read at run start (brain-sync READ #3) | **D** |
| 35 | Background task starves urgent task | CAPACITY_LEDGER priority rule (deadline > priorities > watches > background) | **D**/**L** no hard scheduler exists (platform) |
| 36 | Routine silently changes research constraints | constraints live in task file; Research Log append-only; diffs in git | **D** |
| 37 | Required model unavailable in routine | fallback rule in MODEL_ROUTING (up for consequential, down for mechanical) + log | **D** |
| 38 | Model escalation repeatedly fails | 2-failure escalation cap → task `failed` + question for Brendan | **D** |
| 39 | Annotation fails to create follow-up | annotation artifact records actions; plan-mode preview; tests | **T** test_annotations |
| 40 | Source duplicated across reports | SOURCE_REGISTRY one row per source | **D** |
| 41 | Malicious source tries prompt injection | robots' verification rails (preserved); Brain: sources never override policies; external content is data, not instructions | **D**/**L** no automated lint |
| 42 | Manifest repo unavailable in a later run | brain-sync degrades gracefully (skip + log); manifest documents access | **D** skill contract |
| 43 | Incompatible shared-skill versions | major-version check at robot runtime → warning to outbox | **D** |
| 44 | Retry duplicates task/memory | dedupe_key + dated-block replace + filename collision no-ops | **T** test_queue_dedup, test_partial_failure |
| 45 | Works locally, fails in remote routine | same stdlib-only tools both places; but routine activation itself is pending Brendan's merge | **L** until first live scheduled run |
| 46 | Routine reads stale Brain | pull --rebase before writes; clones are fresh per cloud session | **D** |
| 47 | Branch protection blocks push | push failure path → op record failed + report | **T** test_partial_failure (simulated) |
| 48 | Reviewer rubber-stamps completion | independent-assurance protocol: fresh-context reviewers must run commands; arch reviewer demonstrably did (found 15 issues) | **E** |

Rerun: `tests/run_all.sh`. Any **D** row that bites in practice should get a test before its fix ships.
