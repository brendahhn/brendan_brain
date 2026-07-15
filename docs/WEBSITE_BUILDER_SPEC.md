<!-- Discovery deliverable 2026-07-14 (Fable). -->
# Website Builder Spec (manual sessions — D24)

Trigger: Brendan opens a Claude Code session on personal-os (the paper lists pending site
tasks; no standing routine, no auto-launch).

Standard flow: task → feature branch → implement → build passes → **browser verification
in Chromium against the real Supabase** (data-safety: never against prod tables without
backup for schema-touching work) → PR with before/after screenshots → merge after checks →
Vercel auto-deploys → post-deploy smoke check → mark task done (paper notes it next day).

Standing mandates: Tea Stock save fix first · Home cockpit (newspaper columns/widgets,
status strip, question boxes, feedback box) · FOR CLAUDE category · Mark-fulfilled button
+ home-batch entry + actual-vs-projected on Tea tab · full UI/UX redesign license ("take
it away") with mobile-first (gym use) · NEVER lose data: backup before migrations;
soft-delete stays; component structure may be split from the 849-line single file.

Guardrail: hard rules in repo CLAUDE.md (to be added Phase 1): no table drops, no
key-in-code, no seed-overwrites of live rows; deny-rules in .claude/settings.json.
