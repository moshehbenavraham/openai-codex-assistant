# Server Smoke Test

## Environment

- `PAI_HOME=$(pwd)/pai`
- `PYTHON_BIN=python3`
- `CODEX_BIN=codex`
- Codex CLI logged in (`codex login`) and configured for the desired model

## CLI Verification

```bash
CODEX_BIN=codex ./pai/pai.sh chat "ping"
```

Sample output:

```json
{
  "ok": true,
  "data": {
    "model": "gpt-5-preview",
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "Stubbed response: configure Codex to reach the live agent."
        }
      }
    ]
  }
}
```

The stub response indicates the Codex CLI is either unavailable or still using
placeholder settings. Update `pai/config.json` (model, sandbox policy, Codex
binary) or adjust environment variables, then re-run the command. When you need
debug logs, run the smoke test with `PAI_DEBUG=1 CODEX_BIN=codex ./pai/pai.sh
chat "ping"` and inspect stderr for tool execution statements.
