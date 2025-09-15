# Server Smoke Test

## Environment

- `PAI_HOME=$(pwd)/pai`
- `PYTHON_BIN=python3`
- `CODEX_BIN=codex`
- Codex CLI logged in (`codex login`) and configured for the desired model
- When running under the Codex CLI sandbox, point rollouts inside the workspace
  so Landlock can write session logs:

  ```bash
  mkdir -p pai/codex-sessions
  mv ~/.codex/sessions ~/.codex/sessions.bak
  ln -s $(pwd)/pai/codex-sessions ~/.codex/sessions
  cp -R ~/.codex/sessions.bak/* pai/codex-sessions/
  ```

## CLI Verification

```bash
CODEX_BIN=codex ./pai/pai.sh chat "ping"
```

Sample output when Codex responds successfully:

```json
{
  "ok": true,
  "data": {
    "last": "No active project is currently set. Ready for your next instruction.",
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "No active project is currently set. Ready for your next instruction."
        }
      }
    ]
  }
}
```

If your environment blocks outbound requests you will instead see
`ok: false` and an `error` field describing the network failure. In that case,
restore connectivity (or rerun outside the sandbox) and retry. For verbose
traces, run `PAI_DEBUG=1 CODEX_BIN=codex ./pai/pai.sh chat "ping"` and watch
the debug log lines emitted before the JSON payload. The rollouts and CLI logs
land in `pai/codex-sessions/` for easier inspection inside the workspace.
