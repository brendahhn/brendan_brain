<!-- version: 1.0.0 (2026-07-10) -->
# Agents & Models

## Simple version
Cheap models do cheap work, expensive models do consequential work, and nobody grades
their own homework. You don't manage any of this — it's policy the system follows and logs.

## The model ladder (system/MODEL_ROUTING_POLICY.md)
- **Haiku**: extraction, classification, dedup, formatting. Never draws consequential
  conclusions.
- **Sonnet**: most research, synthesis, queue triage, newspaper editing. The workhorse.
- **Opus**: adversarial review, conflicting evidence, anything materially affecting health
  or money, contrarian calls, repeated failures.
- **Fable**: architecture changes, cross-domain coordination, deep audits.

Escalation is automatic on triggers (evidence conflict, high confidence on thin evidence,
contradicts consensus, prior failure, durable-rule proposal, you asking for scrutiny).
Every task's Research Log names the model used and why it escalated.

## The roles (agents/AGENT_REGISTRY.md)
Roles are job descriptions a session or subagent assumes — not standing daemons:
Chief of Staff (triage/staffing) · Assignment Editor (your words → task) · Research
Associate (mechanical support) · Senior Research Analyst (the research) · Standards Editor
(adversarial check on consequential work) · Archivist (filing/indexes) · Managing Editor
(builds the paper) · Publisher (final gate) · Chief Skeptic (attacks completion claims) ·
QA Lead (operates the system cold) · Systems Architect (structural change).

## The two iron rules
1. **Generation and review are separated.** The Publisher rereads sources with fresh eyes;
   consequential items get an opus reviewer who received none of the author's reasoning.
   This caught real bugs three times during the build (see system/audits/).
2. **Staffing must earn its cost.** Default is one sonnet lead. Extra agents need a logged
   justification and get a logged worth-it verdict; three "no" verdicts retire the pattern.
   No decorative personas.

## What you can say
- "Go deep, and have opus check it" → escalated review.
- "Quick answer" → cheapest competent path.
- "Why did you conclude this?" → the Research Log has models, sources, and reasoning.
