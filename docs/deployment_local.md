# Local Deployment (In-Chat First)

This guide prepares a Windows 10 + WSL2 workstation so Atlas can operate from
inside an interactive OpenAI Codex CLI chat—the default workflow today. The
legacy shell harness is preserved in an appendix for CI and offline jobs.

## Phase 0: Know the Players

- **Atlas (Codex-Atlas):** Runs from a live Codex CLI chat session. You ask for
  work, Atlas drives the terminal.
- **UFC + hooks:** Provide scoped context automatically once the repository is
  the CLI working directory.
- **Legacy scripts:** Remain available under `pai/` and `scripts/`, but only for
  headless automation. When you need them, state explicitly that you are leaving
  the chat workflow.

## Phase 1: Prepare Windows 10 for WSL2

1. Enable virtualization features (elevated PowerShell):
   ```powershell
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   ```
2. Reboot when prompted.
3. Install the WSL2 kernel update: <https://aka.ms/wsl2kernel>.
4. Set WSL2 as the default: `wsl --set-default-version 2`.
5. Install Ubuntu 22.04 LTS from the Microsoft Store and launch it once to
   create your Linux user.

## Phase 2: Configure Ubuntu (Once)

```bash
sudo apt update && sudo apt upgrade
sudo apt install espeak-ng portaudio19-dev alsa-utils wslu
```

- `espeak-ng` / `portaudio19-dev` support the voice pipeline when you test it.
- `wslu` keeps browser integration working (`wslview`).
- For browser checks: `wslview https://example.com`. If interop is disabled,
  follow the recovery steps in `docs/steps.md`.

## Phase 3: Install Bun and the Codex CLI

```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc
bun install -g @openai/codex markdownlint-cli
bunx codex login
```

Bun is also the default package manager for any TypeScript utilities you add to
this repo.

## Phase 4: Clone the Repository and Prime Environment

```bash
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/<your-org>/codex-assistant.git
cd codex-assistant
cp .env.example .env
# Populate secrets: at minimum set SUDO_PASSWORD if you intend to use legacy scripts.
export PAI_HOME=$(pwd)/pai
```

## Phase 5: Launch the In-Chat Workflow

1. Start the CLI session from the project root:
   ```bash
   bunx codex chat
   ```
2. When the prompt appears, greet Atlas and set expectations:
   ```text
   Atlas, confirm you can access this repository and note that we'll operate from chat.
   ```
3. Atlas should acknowledge the workspace, UFC hooks, and readiness to execute
   shell commands on your behalf.

### Essential First Commands (from inside chat)

- `Atlas, run a repo sanity check (git status, bun --version).`
- `Atlas, open the UFC context index so I know it's wired.`
- `Atlas, tail pai/logs/scheduler.log if it exists.`

All actions, logs, and follow-ups remain inside the conversation transcript for
traceability.

## Phase 6: Validate Automations without Leaving Chat

Ask Atlas to trigger health checks one at a time so you can watch output inline.
Suggested order:

1. Scheduler smoke test
   ```text
   Atlas, run the short scheduler health check and show me the log tail.
   ```
2. Maintenance dry runs
   ```text
   Atlas, execute the backup dry run and memory optimizer once, then report the timestamps.
   ```
3. Voice pipeline sample
   ```text
   Atlas, play the prerecorded voice test (muted) and confirm the transcription in logs.
   ```
4. Tool ping
   ```text
   Atlas, call the search tool with a noop query just to prove the CLI wiring.
   ```

Atlas can open Playwright sessions, capture transcripts, and archive results
without you ever leaving the chat prompt. If a command needs interactive
approval (sandbox prompts, etc.), Atlas will surface the request and wait for
confirmation.

## Appendix A: Legacy Script Harness (Secondary)

Only use this path when you explicitly need a detached run (cron, CI, or offline
machines without the Codex CLI chat available).

1. **Python environment (legacy only):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc
   uv venv .venv
   source .venv/bin/activate
   uv pip install SpeechRecognition pyttsx3 pyaudio schedule typing-extensions pexpect
   ```
2. **Voice fixture (optional):**
   ```bash
   mkdir -p pai/tests/audio
   espeak-ng -w pai/tests/audio/hello.wav "hello from pai"
   ```
3. **Scripted smoke tests:**
   ```bash
   CODEX_BIN=codex ./pai/pai.sh chat "ping"
   CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{"query":"status"}'
   PYTHONPATH=pai .venv/bin/python pai/scheduler.py --interval-seconds 2 --cycles 4
   ./pai/backup.sh --dry-run
   python3 pai/optimize_memory.py --once
   PYTHONPATH=pai .venv/bin/python pai/voice.py --audio-file pai/tests/audio/hello.wav --mute
   ```
4. **Interactive helpers:**
   ```bash
   ./scripts/codex_tool_session.py --tool search --params '{"query":"example"}'
   ./scripts/codex_interactive.sh
   ```

When you pivot to this appendix, note it in changelog entries and clearly signal
when you return to the in-chat flow.
