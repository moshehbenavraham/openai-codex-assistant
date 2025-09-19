# Codex-Atlas Personal AI Infrastructure

Codex-Atlas (Atlas) now runs primarily from an interactive OpenAI Codex CLI chat
session. The project repository still ships the legacy script harness, but that
path is a fallback reserved for headless automation and CI. Day-to-day work
happens in the conversation you are reading right now.

## Primary Workflow: In-Chat with OpenAI Codex CLI

1. **Install the CLI with Bun (once per machine):**
   ```bash
   bun install -g @openai/codex markdownlint-cli
   bunx codex login
   ```
   Configure any additional secrets in `.env` before opening Atlas.
2. **Launch the Codex CLI chat:**
   ```bash
   cd /home/<user>/projects/codex-assistant
   bunx codex chat
   ```
3. **Invite Atlas into the session:** the CLI loads this repository as its
   working directory so Atlas can shell out, run tests, update docs, and manage
   UFC context on demand—no extra wrapper script required.
4. **Ask for work:** e.g.,
   - `Atlas, run the scheduler health check and show the log tail.`
   - `Atlas, capture a status update in docs/changelog.md.`
   - `Atlas, open a Playwright session and smoke test the UI.`
5. **Stay in chat for automation:** Atlas can trigger Bun scripts, voice hooks,
   Playwright, UFC loaders, and git hygiene directly. Only fall back to the
   legacy shell helpers when you explicitly need a detached run.

### Verifying the Session

Ask Atlas to execute a quick diagnostic:

```text
Atlas, verify Codex CLI access with a noop tool call.
```

Atlas should report the JSON streamed back by the CLI. If approvals or sandbox
constraints appear, resolve them interactively and retry from the same chat.

## Secondary Workflow: Legacy Automation Scripts

The previous shell-first harness remains in `pai/` and `scripts/` for
headless/CI use cases.

- Use this path when you cannot maintain an interactive session (e.g., nightly
  cron, remote lab hardware).
- Python dependencies must be installed with `uv` now: `uv pip install -r
  pai/requirements.txt` (or the equivalent commands documented under
  “Legacy Automations”).
- Manual invocations such as `CODEX_BIN=codex ./pai/pai.sh chat "ping"` are no
  longer the recommended flow but still work once the environment is prepared.

See `docs/usage_local.md` for the in-chat procedures and the legacy appendix for
script examples.

## Documentation Map

- `docs/deployment_local.md` – Full workstation setup for the in-chat workflow,
  plus an appendix covering the legacy shell harness.
- `docs/usage_local.md` – Daily operations from inside the Codex CLI chat,
  including health checks, logging, and legacy fallbacks.
- `docs/runbooks/` – Task-specific guides (scheduler, maintenance, voice,
  server smoke tests) rewritten to assume in-chat execution first.
- `docs/tool_registry.md` – Asking Atlas to run tools in conversation, with
  fallback shell commands.
- `docs/changelog.md` – History of infrastructure updates (latest entries cover
  the migration to the in-chat primary workflow).
- `UPDATE.md` – Current initiative summary for whoever is on call.

## Repository Conventions

- Bun is the default JavaScript/TypeScript runtime (`bun install`, `bunx`).
- Python usage is legacy-only; when required, prefer `uv pip install ...` over
  `pip install`.
- Keep markdown linted with `bunx markdownlint "**/*.md"`.
- Never commit or publish the private `~/.claude/` directory; double-check
  `git remote -v` before committing.
