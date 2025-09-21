# Tool: search

## Description

Query a search provider for recent information and return concise summaries.

## Parameters

| Name | Type | Constraints | Description |
| ---- | ---- | ----------- | ----------- |
| query | string | required, non-empty | Terms to search for. |
| max_results | integer | optional, >= 1, default 5 | Max result count. |
| freshness | string | optional, `standard\|news` | Bias toward recent sources. |

## Returns

| Field | Type | Description |
| ----- | ---- | ----------- |
| results | array | List of `{title, snippet, url, published_at}` entries. |
| provider | string | Identifier for the search backend. |

## Examples

```json
{
  "query": "personal ai infrastructure design",
  "max_results": 3
}
```

## Verification

1. Ensure the Codex CLI is authenticated (`codex login`) and
   `docs/runbooks/server_smoke_test.md` passes.
2. Run the in-chat dispatcher:

   ```bash
   ./pai/bin/tool search '{"query":"latest autonomous agent frameworks"}'
   ```

3. Expect the JSON response to include a `results` array with up to
   `max_results` entries.
