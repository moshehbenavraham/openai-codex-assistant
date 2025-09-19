# Environment Setup Checklist (In-Chat Workflow)

Use this checklist when preparing a Debian/Ubuntu (or WSL) host for Atlas’s
in-chat operations.

## 1. Install Bun

```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc
```

## 2. Install Codex CLI & Tooling (via Bun)

```bash
bun install -g @openai/codex markdownlint-cli
bunx codex login
```

## 3. Update System Packages

```bash
sudo apt update && sudo apt upgrade
```

## 4. Voice Interface Dependencies

```bash
sudo apt install espeak-ng portaudio19-dev alsa-utils
```

These packages support the prerecorded voice test Atlas can run from chat.

## 5. (WSL Only) Install wslu and Enable Browser Interop

```bash
sudo apt install wslu
wslview https://example.com
```

If you see “WSL Interoperability is disabled,” follow the remediation steps in
`docs/deployment_local.md`.

## 6. Clone the Repository

```bash
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/<your-org>/codex-assistant.git
cd codex-assistant
cp .env.example .env
export PAI_HOME=$(pwd)/pai
```

Populate secrets (e.g., `SUDO_PASSWORD`) before launching Atlas.

## 7. Optional: Legacy Script Prerequisites

Only required for headless runs. If you need them:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv venv .venv
source .venv/bin/activate
uv pip install SpeechRecognition pyttsx3 pyaudio schedule typing-extensions pexpect
```

## 8. Launch Atlas in Chat

```bash
bunx codex chat
```

Greet Atlas and request a workspace status report to confirm everything is wired
correctly.
