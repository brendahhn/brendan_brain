---
id: health-notebook
domain: health
type: notebook
sensitivity: health
owner: health-robot
status: degraded
---

# Health Robot Notebook

This is the Health Research Robot's persistent memory. It is read first and written
back last on every run. See `health-robot-prompt.md` for the operating prompt (currently MISSING).

## STATE

- **Provisioning incomplete.** As of the first recorded run, neither `health-robot-prompt.md`
  nor this notebook existed in the repo. Both are configured to live at the repo root but
  were never committed. The robot cannot run research until `health-robot-prompt.md` is
  restored (must be non-empty and end with a final non-blank line of exactly `## END`).

## CHANGELOG

- PROMPT VALIDATION FAILED on 2026-07-11: health-robot-prompt.md missing/truncated/no ## END marker. Ran nothing.
  (Notebook was also absent and was created solely to record this failure; no research was performed.)
