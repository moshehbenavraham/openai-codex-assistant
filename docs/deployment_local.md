# Local Deployment (WSL2 Ubuntu on Windows 10)

Follow this guide to install and validate the Personal AI Infrastructure (PAI)
on a Windows 10 host using WSL2 with Ubuntu.

## 1. Prepare Windows

1. Enable required features from an elevated PowerShell prompt:

   ```powershell
   dism.exe /online /enable-feature \
     /featurename:VirtualMachinePlatform \
     /all /norestart
   dism.exe /online /enable-feature \
     /featurename:Microsoft-Windows-Subsystem-Linux \
     /all /norestart
   ```

2. Reboot when prompted.
3. Install the latest WSL2 kernel update: <https://aka.ms/wsl2kernel>.
4. Set WSL2 as the default version:

   ```powershell
   wsl --set-default-version 2
   ```

5. Install Ubuntu (22.04 LTS recommended) from the Microsoft Store and launch it
   once to create your Linux user.

## 2. Configure Ubuntu

1. Update packages:

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. Install audio/voice dependencies:

   ```bash
   sudo apt install espeak-ng portaudio19-dev alsa-utils wslu
   ```

3. Install build tooling for Python packages:

   ```bash
   sudo apt install build-essential python3-venv python3-dev
   ```

4. (Optional) Test Windows browser integration:

   ```bash
   wslview https://example.com
   ```

   If you see "WSL Interoperability is disabled", follow the recovery steps in
   `docs/steps.md`.

## 3. Install Node.js and CLI Tools

1. Install NVM and Node.js 22:

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   source ~/.bashrc
   nvm install 22
   nvm use 22
   ```

2. Install the Codex CLI and markdownlint:

   ```bash
   npm install -g @openai/codex markdownlint-cli
   codex login
   ```

## 4. Clone the Repository

1. Clone the project:

   ```bash
   mkdir -p ~/projects
   cd ~/projects
   git clone https://github.com/<your-org>/codex-assistant.git
   cd codex-assistant
   ```

2. Copy the environment template and add the sudo password you want automation
   to use:

   ```bash
   cp .env.example .env
   echo "SUDO_PASSWORD=<your-password>" >> .env
   ```

3. Export `PAI_HOME` for the current shell:

   ```bash
   export PAI_HOME=$(pwd)/pai
   ```

## 5. Bootstrap Python

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install Python packages:

   ```bash
   pip install SpeechRecognition pyttsx3 pyaudio schedule typing-extensions pexpect
   ```

3. Generate the voice test fixture:

   ```bash
   mkdir -p pai/tests/audio
   espeak-ng -w pai/tests/audio/hello.wav "hello from pai"
   ```

## 6. Prepare the Workspace

1. Ensure required directories exist:

   ```bash
   mkdir -p pai/{tools/custom,projects,archive/memory,logs}
   ```

2. Review `docs/steps.md` and `docs/runbooks/voice.md` for any environment
   nuances that apply to your setup.

## 7. Smoke Tests

Run each command from the project root. Expect stubbed responses if Codex cannot
write inside the sandbox.

1. Chat bridge:

   (Give it a minute or so, it's doing some work here!)

   ```bash
   CODEX_BIN=codex ./pai/pai.sh chat "ping"
   ```

2. Tool execution (expect a stub error when Codex cannot write to `/tmp`; see
   the Usage guide for the interactive workaround):

   ```bash
   CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{"query":"test"}'
   ```

3. Scheduler quick run (writes to `pai/logs/scheduler.log`):

   ```bash
   PYTHONPATH=pai \
     .venv/bin/python pai/scheduler.py \
     --interval-seconds 2 --cycles 4
   ```

4. Backup dry run (check `pai/logs/backup.log`):

   ```bash
   ./pai/backup.sh --dry-run
   ```

5. Memory optimizer (logs to `pai/logs/optimize_memory.log`):

   ```bash
   python3 pai/optimize_memory.py --once
   ```

6. Voice pipeline using the prerecorded sample:

   ```bash
   PYTHONPATH=pai \
     .venv/bin/python pai/voice.py \
     --audio-file pai/tests/audio/hello.wav --mute
   ```

## 8. Manual Tool Runs (Sandbox Limitation)

The public Codex CLI enforces a read-only sandbox during unattended execution.
When you need real tool results, prefer the helpers in `scripts/` so you do not
have to copy/paste commands or troubleshoot the approval prompts:

- One-shot run while staying in control of the terminal:

  ```bash
  ./scripts/codex_tool_session.py --tool search --params '{"query":"example"}'
  ```

  The helper launches Codex in workspace-write mode, auto-approves the prompt,
  prints the JSONL responses, and exits once the command finishes. Add `--stay`
  to leave the session open for follow-up runs.

- Guided interactive loop (tool + JSON prompt each time):

  ```bash
  ./scripts/codex_tool_session.py
  ```

  Enter the tool name and JSON when prompted. Type `!handoff` to attach directly
  to the Codex prompt or `!raw` to send an arbitrary Codex command. Use
  `--transcript tmp/codex.log` if you want to archive the responses.

- Raw Codex fallback with safety rails:

  ```bash
  ./scripts/codex_interactive.sh
  ```

  The wrapper simply prints the sandbox mode and then executes
  `codex exec --sandbox workspace-write --json`. Use this if you prefer to
  drive Codex entirely by hand.

If Codex shows an approval prompt that the helper does not capture, type `y`
yourself and rerun the command. Copy the tool result back into your notes or
documentation as needed.

> For day-to-day workflows (scheduler, maintenance, voice, and the interactive
> workaround), see [docs/usage_local.md](docs/usage_local.md).

## 9. Optional: Schedule Maintenance Jobs

1. Create the cron definition:

   ```bash
   cat <<'CRON' > pai/cron_maintenance
   # PAI maintenance jobs
   0 2 * * * PAI_HOME=$(pwd)/pai \
     $(pwd)/pai/backup.sh >> $(pwd)/pai/logs/backup-cron.log 2>&1
   30 2 * * 0 PAI_HOME=$(pwd)/pai PYTHONPATH=$(pwd)/pai \
     /usr/bin/python3 $(pwd)/pai/optimize_memory.py --once >> \
     $(pwd)/pai/logs/optimize-cron.log 2>&1
   CRON
   ```

2. Register and confirm:

   ```bash
   crontab pai/cron_maintenance
   crontab -l
   ```

3. Review the cron log files after the first scheduled run.

## 10. Daily Usage

1. Reactivate your environment when opening a new shell:

   ```bash
   source .venv/bin/activate
   export PAI_HOME=$(pwd)/pai
   ```

2. Chat with PAI via the wrapper:

   ```bash
   CODEX_BIN=codex ./pai/pai.sh chat "What's my focus today?"
   ```

3. Consult the runbooks in `docs/runbooks/` for scheduler, maintenance, and
   voice tasks.

## 11. Troubleshooting

- Codex errors mentioning `/tmp` usually mean the sandbox is read-only; rerun
  after granting write access or accept the stubbed response.
- `Audio input unavailable` indicates WSL cannot access a microphone. Continue
  using the prerecorded sample or configure ALSA/PulseAudio passthrough.
- If speech synthesis fails, inspect `pai/logs/voice.log` and reinstall the
  voice Python packages.
- Always run `npx markdownlint "**/*.md"` after editing docs to keep formatting
  consistent.

Once all smoke tests complete (with real or stubbed responses), your local WSL2
installation of PAI is ready for daily use.
