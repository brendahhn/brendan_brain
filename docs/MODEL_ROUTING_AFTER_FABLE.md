<!-- Discovery deliverable 2026-07-14 (Fable). Extends system/MODEL_ROUTING_POLICY.md. -->
# Model Routing After Fable (access ends 2026-07-18)

| Role | Preferred | Fallback |
|---|---|---|
| architecture_lead | fable (to 07-18) | **opus** |
| implementation | sonnet | opus |
| exploration/recon | haiku | sonnet |
| routing/scans | haiku | sonnet |
| normal_research | sonnet | opus |
| high_risk_review | opus | (no downgrade — defer if unavailable) |

Rules: routine sessions inherit their configured model; subagent `model` param is how
routing happens in practice. Escalation/de-escalation triggers unchanged from
MODEL_ROUTING_POLICY. Downgrades for mechanical work are automatic and logged; upgrades
for consequential work are automatic; NO token counts fabricated (platform exposes none).
Usage conservation: batch mechanical work to haiku; the 4-windows/day ceiling analysis in
system/audits/2026-07-12-routine-session-diagnostic.md governs schedule design.
Opus assumes the architecture lead role via docs/FABLE_ARCHITECTURE_HANDOFF.md §Opus
instructions. The system must never block on a missing Fable.
