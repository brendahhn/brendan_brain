<!-- version: 1.0.0 (2026-07-10) -->
# Limitations — stated honestly

## Requires Brendan before it's live end-to-end
1. **Robot integration is dark until activated.** The integration lives on four `claude/*`
   branches; scheduled robots run `main` and their routine configs don't yet include
   `brendan_brain`. Until Brendan merges + updates repo selections + applies the two-line
   prompt diffs, robots neither read nor write the Brain. The exchange protocol was proven
   in-session (op-20260710-roundtrip-health), not in a scheduled run.
2. **First scheduled-run validation outstanding** (stress scenario 45): local/session
   behavior is tested; the first real cloud robot run with the Brain attached should be
   watched and its CHANGELOG checked.

## Platform limitations (no fix available in-session)
3. **No universal conversation capture.** Capture happens only in sessions/routines that
   have the Brain repo and invoke the skills. There is no platform-wide tap on all Claude
   conversations. Wording like "any conversation" means "any Brain-enabled conversation."
4. **No account usage/quota API.** Capacity scheduling uses a conservative manual ledger
   (system/CAPACITY_LEDGER.md) and priority policy, not real usage data. Effort estimates
   improve from run history, nothing better is possible today.
5. **No hard scheduler.** Routines fire on their configured schedules; the Brain can only
   prioritize within a session. Deadline-critical work should get its own routine slot.
6. **Skill sync is session-borne.** Updates propagate when a session with the repos side by
   side runs `tools/sync_skills.sh`. Drift between syncs is detectable (checksums, version
   headers, runtime check) but not self-healing.
7. **Egress in routine sandboxes is WebSearch-only** (inherited; affects robots' source
   verification — health AUDIT_QUEUE backlog predates this build).

## Design limitations (accepted, with triggers to revisit)
8. **Forgetting is working-tree-only by default.** Git history retains deleted content in
   every clone until a Brendan-supervised history rewrite. brain-forget says this plainly
   and stops at a plan. For truly radioactive content: don't commit it — keep it out of git.
9. **Cross-clone duplicate prevention is impossible without a coordination server**; we
   detect post-merge (validator) and recover instead. Same for op-ledger races (last-write-wins
   on a single op file; acceptable at one-owner scale).
10. **Retrieval is keyword/metadata-level.** Semantic recall ("truck" → tacoma) needs alias
    maps or embeddings — deferred until retrieval tests show real misses (evidence-first rule).
11. **Scale untested** beyond dozens of artifacts; thresholds and archival triggers are
    documented (STRESS_TESTS #27) but unexercised.
12. **Sanitization linting is pattern-based** (numeric+unit scrub on health outbox); a
    determined mistake can pass it. The hard wall remains the export contract + Publisher
    checklist, both model-judgment.
13. **Data Lab has no dataset yet** — no surf/WSL dataset repo is in the manifest; the
    capability doc (docs/DATA_LAB.md) and task pattern exist, fixtures only.

## Mocked / synthetic (never presented as real)
- Tacoma listings in the demo edition; the electrolyte "finding"; all test fixtures.
  Every one is labeled SYNTHETIC in place.
