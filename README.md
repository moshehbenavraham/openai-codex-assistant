# OpenAI Codex Personal Assistant

Personal AI Infrastructure (PAI) that wraps the OpenAI Codex CLI with local
automation (scheduler, voice interface, backups) plus detailed runbooks.

## Key Documents

- [docs/deployment_local.md](docs/deployment_local.md) – End-to-end setup for
  Windows 10 + WSL2, including smoke tests.
- [docs/steps.md](docs/steps.md) – Environment checklist for reprovisioning
  Ubuntu/WSL hosts.
- [docs/usage_local.md](docs/usage_local.md) – Daily operations plus current
  sandbox limitations and workarounds.
- [docs/runbooks/](docs/runbooks) – Operational procedures for scheduler,
  maintenance, and voice workflows.
- [docs/changelog.md](docs/changelog.md) – Project history and recent updates.
- [docs/tool_registry.md](docs/tool_registry.md) – High-level overview of the
  available tools.

## Quick Start

```bash
git clone https://github.com/<your-org>/codex-assistant.git
cd codex-assistant
cp .env.example .env  # add your sudo password
python3 -m venv .venv && source .venv/bin/activate
pip install SpeechRecognition pyttsx3 pyaudio schedule typing-extensions pexpect
npm install -g @openai/codex markdownlint-cli
codex login
export PAI_HOME=$(pwd)/pai
mkdir -p pai/tests/audio && espeak-ng -w pai/tests/audio/hello.wav "hello from pai"
```

Run the smoke tests (expects Codex CLI access; sandboxed environments may
return stubbed responses):

```bash
CODEX_BIN=codex ./pai/pai.sh chat "ping"
CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{"query":"test"}'
PYTHONPATH=pai \
  .venv/bin/python pai/scheduler.py \
  --interval-seconds 2 --cycles 4
./pai/backup.sh --dry-run
python3 pai/optimize_memory.py --once
PYTHONPATH=pai \
  .venv/bin/python pai/voice.py \
  --audio-file pai/tests/audio/hello.wav --mute
```

Need real tool output instead of the sandbox stub? Use the helpers in
`scripts/`:

```bash
./scripts/codex_tool_session.py --tool search --params '{"query":"example"}'
./scripts/codex_interactive.sh  # raw Codex prompt with workspace-write enabled
```

For deeper instructions, maintenance scheduling, and troubleshooting, follow
the deployment guide listed above.
