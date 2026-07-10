# Predictions
One file per prediction; scored into outcomes/ when the horizon passes (OPERATIONS step 5).
Template (schema: system/SCHEMAS.md):

```markdown
---
id: prediction-YYYYMMDD-<slug>
artifact_type: prediction
domain: investing
confidence: medium        # speculative|low|medium|high
horizon: YYYY-MM-DD       # when this becomes scoreable
created_at: YYYY-MM-DD
created_by: trading-robot
origin_repository: trading-notebook
derived_from: [<outbox block or task id>]
sensitivity: financial
---
<one-sentence prediction with the exit/success condition, verbatim from the source>
```
