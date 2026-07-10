<!-- version: 1.0.0 (2026-07-10) -->
# Dynamic Staffing Policy

Default: **one sonnet lead per task.** Staffing changes must be justified in the task's
research log and reviewed against results.

Add haiku support when: bulk extraction/classification/dedup/normalization, or several
independent cheap searches, or the lead would waste expensive context on mechanical work.

Add an opus reviewer when: evidence conflicts; conclusion materially affects health or money;
high confidence on limited evidence; strong divergence from credible consensus; unusual
ambiguity; Brendan requested scrutiny; a previous conclusion failed; a consequential durable
rule is proposed.

Use fable when: architecture must change; several domains need coordination; agents
repeatedly fail; a major capability is required; a comprehensive audit is requested.

Teams (peer agents) only when workers own genuinely separate components, need direct
debate, or parallelism materially cuts elapsed time AND expected quality gain justifies
cost. Otherwise use subagents reporting to one lead.

## Cost discipline
- Every multi-agent task records staff count, models, and an honest one-line verdict in its
  research log: did the extra staffing improve the result?
- Three consecutive "no" verdicts for a pattern → record retirement note in
  agents/AGENT_REGISTRY.md and stop using it.
- No decorative personas. A role exists only if it has distinct inputs, outputs, and a
  completion standard (see agents/AGENT_REGISTRY.md).
