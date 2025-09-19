# Server Smoke Test (In-Chat)

Use the Codex CLI chat with Atlas to validate CLI connectivity and sandbox
behavior.

## Primary Flow

1. Set the stage:
   ```text
   Atlas, confirm codex is on the PATH and show its version.
   ```
2. Run the ping:
   ```text
   Atlas, call the chat endpoint with a "ping" prompt and share the JSON response.
   ```
3. Atlas pastes the streamed output. A healthy response mirrors:
   ```json
   {
     "ok": true,
     "data": {
       "last": "No active project is currently set. Ready for your next instruction."
     }
   }
   ```
4. If sandbox approvals are needed, Atlas pauses and asks for confirmation before
   rerunning.

## Additional Checks

- `Atlas, list ~/.codex/sessions to confirm transcripts are being saved.`
- `Atlas, ensure pai/codex-sessions exists and point the Codex CLI there if we are in sandbox mode.`
- `Atlas, verify workspace-write access by touching tmp/codex-probe.txt and then deleting it.`

## Legacy Commands (Fallback Only)

Detached validation still works with:

```bash
CODEX_BIN=codex ./pai/pai.sh chat "ping"
```

Document any fallback usage in `docs/changelog.md` and return to the in-chat
workflow afterward.
