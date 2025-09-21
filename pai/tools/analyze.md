# Tool: analyze

## Description

Run structured analysis over text, code, or documents to produce actionable
guidance.

## Parameters

| Name | Type | Constraints | Description |
| ---- | ---- | ----------- | ----------- |
| subject | string | required | Content to analyze (text or file path). |
| analysis_type | string | required | Choose code, security, perf, or general. |
| depth | string | optional, default standard | Options: quick, standard, deep. |
| include_sources | boolean | optional, default false | Adds cites when true. |

## Returns

| Field | Type | Description |
| ----- | ---- | ----------- |
| analysis | object | Structured findings keyed by topic. |
| recommendations | array | Ordered list of follow-up actions. |
| sources | array | Citations returned when `include_sources` is true. |

## Examples

```json
{
  "subject": "docs/implementation.md",
  "analysis_type": "general",
  "depth": "quick"
}
```

## Verification

1. Ensure Codex CLI authentication succeeds (`codex login`).
2. Execute the request directly from chat:

   ```bash
   ./pai/pai.sh run-tool analyze --params '{"subject":"Runbook draft","analysis_type":"general"}'
   ```

3. Inspect the JSON response to confirm `analysis` and `recommendations`
   contain non-empty data.
