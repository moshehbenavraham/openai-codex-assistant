# Environment Setup Checklist

Follow these steps in order to configure a Debian or WSL host for the Personal
AI Infrastructure.

## Install NVM (Node Version Manager)

1. `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash`
2. `source ~/.bashrc`

## Install Node.js v22 (latest LTS)

1. `nvm install 22`
2. `nvm use 22`

## Update System Packages

1. `sudo apt update`
2. `sudo apt upgrade`

## Install Voice Interface Dependencies

1. `sudo apt install espeak-ng portaudio19-dev alsa-utils`
2. `python3 -m venv .venv` (if not already created)
3. `.venv/bin/pip install SpeechRecognition pyttsx3 pyaudio`

## Install WSL Utilities (WSL-only)

1. `sudo apt install wslu`

## Validate Browser Integration (WSL-only)

1. `wslview https://example.com`
2. If you see `WSL Interoperability is disabled`, run:
   - `sudo sh -c 'echo :WSLInterop:M::MZ::/init:PF > /proc/sys/fs/binfmt_misc/register'`
   - `sudo sh -c 'echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop'`
3. Confirm interop is enabled: `cat /proc/sys/fs/binfmt_misc/WSLInterop`

## Add Windows System Paths (WSL-only)

1. `echo 'export PATH=$PATH:/mnt/c/Windows/System32:/mnt/c/Windows' >> ~/.bashrc`
2. `source ~/.bashrc`
3. `which wslview`

## Install Codex CLI

1. `npm install -g @openai/codex`
2. `which codex`
3. Run `codex` once to confirm it launches.
4. Authenticate: `codex login`

## Install markdownlint CLI

1. `npm install -g markdownlint-cli`

## Prepare the Personal AI Infrastructure Workspace

1. `mkdir -p pai/{tools/custom,projects,archive/memory,logs}`
2. Keep the workspace under the project tree when the home directory is
   sandboxed.
3. `mkdir -p pai/tests/audio` and populate test fixtures (e.g.,
   `espeak-ng -w pai/tests/audio/hello.wav "hello from pai"`).
