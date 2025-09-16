# Local Usage (WSL2 Ubuntu on Windows 10)

These instructions assume you completed the setup in
[`docs/deployment_local.md`](docs/deployment_local.md) on a Windows 10 host with
WSL2 Ubuntu.

## 1. Open a Working Session

```bash
cd ~/projects/codex-assistant
source .venv/bin/activate
export PAI_HOME=$(pwd)/pai
```

Repeat these steps in each new terminal before running commands.

## 2. Quick Health Checks

Run the block below to confirm the scheduler, maintenance, and voice pipeline
still work. Tool calls will emit a stub error because of the Codex sandbox (see
section 4).

```bash
CODEX_BIN=codex ./pai/pai.sh chat "ping"
PYTHONPATH=pai .venv/bin/python pai/scheduler.py --interval-seconds 2 --cycles 4
./pai/backup.sh --dry-run
python3 pai/optimize_memory.py --once
PYTHONPATH=pai \
  .venv/bin/python pai/voice.py \
  --audio-file pai/tests/audio/hello.wav --mute
```

Check `pai/logs/` afterwards if you want to inspect the details.

## 3. Keep the Scheduler Running

Open a dedicated terminal/tmux pane and run:

```bash
PYTHONPATH=pai .venv/bin/python pai/scheduler.py
```

Leave it running; the scheduler writes activity to `pai/logs/scheduler.log`.

## 4. Running Codex Tools (Sandbox Limitation)

The public Codex CLI enforces a read-only sandbox for unattended runs, so
commands like `./pai/pai.sh run-tool search ...` will return:

```text
Codex CLI failed with exit code 1; check stderr
```

Use the helper scripts under `scripts/` whenever you need real tool output:

- **Single run:**

  ```bash
  ./scripts/codex_tool_session.py --tool search --params '{"query":"hello world"}'
  ```

  The script auto-approves the workspace-write prompt, prints each JSONL event,
  and exits once the tool completes.

- **Interactive loop:**

  ```bash
  ./scripts/codex_tool_session.py
  ```

  Enter the tool name and JSON payload when prompted. Special commands:
  - `!raw` — send a raw Codex command.
  - `!handoff` — attach your terminal directly to the Codex prompt (Ctrl+] to
    return).
  - Add `--transcript tmp/codex.log` when launching to capture results on disk.

- **Raw CLI fallback:**

  ```bash
  ./scripts/codex_interactive.sh
  ```

  This wrapper prints the chosen sandbox mode and then runs
  `codex --sandbox workspace-write` for you to control manually. Pass a
  different sandbox (e.g., `read-only`) as the first argument or use `--` to
  forward a prompt/extra flags directly to the Codex CLI.

If Codex shows an approval prompt that the helper cannot recognize, type `y`
yourself and rerun the command. Copy responses into your notes or task logs,
then exit the session.

## 5. Maintenance Jobs

Cron entries are already loaded from `pai/cron_maintenance`. Verify them with:

```bash
crontab -l
```

- Backup logs: `pai/logs/backup-cron.log`
- Memory optimizer logs: `pai/logs/optimize-cron.log`

To run a manual dry-run backup or optimizer pass, reuse the commands in
section 2.

## 6. Voice Interface

- Dependency check:

  ```bash
  PYTHONPATH=pai .venv/bin/python pai/voice.py --check-deps
  ```

- Automated smoke test (no microphone required):

  ```bash
  PYTHONPATH=pai \
    .venv/bin/python pai/voice.py \
    --audio-file pai/tests/audio/hello.wav --mute
  ```

- Live mic: drop the `--audio-file` flag and speak after `Listening for voice input`.
  Logs accumulate in `pai/logs/voice.log`.

## 7. Logs and Runbooks

| Purpose            | Location                     |
|--------------------|------------------------------|
| Scheduler logs     | `pai/logs/scheduler.log`     |
| Backup logs        | `pai/logs/backup.log`        |
| Memory optimizer   | `pai/logs/optimize_memory.log`|
| Voice interactions | `pai/logs/voice.log`         |

Detailed procedures live in `docs/runbooks/`.

## 8. Common Issues

- **Codex stub output**: Use the interactive CLI flow described above.
- **Audio input unavailable**: WSL has no microphone access; continue using the
  prerecorded sample or configure ALSA/PulseAudio passthrough.
- **Text-to-speech errors**: Reinstall `pyttsx3`/`pyaudio` inside `.venv` and
  check `pai/logs/voice.log`.
- **Docs formatting**: Run `npx markdownlint "**/*.md"` after editing markdown.

With these habits, you can operate the Personal AI Infrastructure locally while
working around the current Codex sandbox limitations.
