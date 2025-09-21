# Local Usage (Codex CLI Chat)

These procedures assume you completed the deployment guide and now operate Atlas
from a live OpenAI Codex CLI chat session. The chat is the primary control plane;
legacy scripts are documented in an appendix for rare fallback cases.

## 1. Start or Resume a Session

1. Open WSL and navigate to the project root:
   ```bash
   cd ~/projects/codex-assistant
   ```
2. Launch the chat:
   ```bash
   bunx codex chat
   ```
3. Tell Atlas what you need:
   ```text
   Atlas, boot up for the day and confirm the workspace path.
   ```
4. Atlas responds with repository status, UFC context availability, and any
   outstanding tasks captured in `.claude` hooks.

### Reconnecting Mid-Day

If the CLI drops, relaunch `bunx codex chat` and remind Atlas to reload context:

```text
Atlas, reconnect to the earlier session, reload UFC context, and show the last log entries you have.
```

## 2. Daily Health Checks (In Chat)

Run each of these by asking Atlas directly:

- **Scheduler:**
  ```text
  Atlas, run the scheduler smoke test with the 2-second interval and show me the log snippet.
  ```
- **Backups & Memory:**
  ```text
  Atlas, perform a backup dry run, then execute the memory optimizer once and report timestamps.
  ```
- **Voice pipeline:**
  ```text
  Atlas, replay the prerecorded voice test (muted) and confirm the transcription in pai/logs/voice.log.
  ```
- **Tool sanity:**
  ```text
  Atlas, call the search tool with a noop query just to prove the link is alive.
  ```

Atlas prints results inline, attaches relevant log tails, and highlights follow-up
issues without switching terminals.

## 3. Observability from Chat

Common prompts:

- `Atlas, tail pai/logs/scheduler.log | head -n 20 so I can see the most recent runs.`
- `Atlas, list archives in pai/archive sorted by newest.`
- `Atlas, summarize the last five entries in docs/changelog.md.`

Atlas will run the necessary shell commands and paste the output or a concise
summary (with links back to the files).

## 4. Running Tools and Automation

Atlas can invoke tools, Playwright sessions, and custom scripts from the chat.
Examples:

```text
Atlas, open a Playwright session against the staging dashboard and capture a screenshot.
Atlas, run bun test in the pai project and summarize failing assertions.
Atlas, trigger the voice hook via ~/.claude/context/documentation/voicesystem/CLAUDE.md instructions and log the outcome.
```

When you need a quick tool sanity check, call the local dispatcher directly:

```bash
./pai/bin/tool search '{"query":"status"}'
```

Reserve `CODEX_BIN=codex ./pai/pai.sh run-tool …` for non-chat automation.

When tool runs require approvals, Atlas pauses and tells you what to confirm.

## 5. Coordinating with UFC and Hooks

- Ask Atlas to list available UFC contexts: `Atlas, show me ls ~/.claude/context`.
- Request context reloads after editing hooks: `Atlas, reload the user_prompt hook and confirm checksum.`
- Use the chat to edit commands: `Atlas, open ~/.claude/commands/<name>.md, apply the fix, and run bunx markdownlint to verify.`

## 6. Legacy Appendix (Secondary Path)

Only follow these steps when an interactive chat is impossible (CI, cron, or
non-interactive environments). Always call out that you are in the legacy flow.

- **Activate the Python environment (if needed):**
  ```bash
  source .venv/bin/activate  # assuming uv venv .venv
  ```
- **Scheduler smoke test:**
  ```bash
  PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/scheduler.py --interval-seconds 2 --cycles 4
  ```
- **Backup + optimizer:**
  ```bash
  PAI_HOME=$(pwd)/pai ./pai/backup.sh --dry-run
  PAI_HOME=$(pwd)/pai python3 pai/optimize_memory.py --once
  ```
- **Voice sample:**
  ```bash
  PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/voice.py --audio-file pai/tests/audio/hello.wav --mute
  ```
- **Codex tool helper (legacy):**
  ```bash
  ./scripts/codex_tool_session.py --tool search --params '{"query":"status"}'
  ```

Return to the chat workflow when finished and document the detour in the
changelog.
