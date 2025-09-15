
# Install NVM (Node Version Manager)

curl -o- <https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh> | bash

# Reload your shell configuration

source ~/.bashrc

# Install Node.js v22 (latest LTS)

nvm install 22
nvm use 22

# Update and Upgrade

sudo apt update

sudo apt upgrade

# Install WSL Utilities

sudo apt install wslu

# Test Browser

# This should open in your Windows browser

wslview <https://example.com>

# If you get "WSL Interopability is disabled. Please enable it before using WSL."

sudo sh -c 'echo :WSLInterop:M::MZ::/init:PF > /proc/sys/fs/binfmt_misc/register'

sudo sh -c 'echo 1 > /proc/sys/fs/binfmt_misc/WSLInterop'

# Check if its enabled

cat /proc/sys/fs/binfmt_misc/WSLInterop

# Add Windows System32 to PATH

echo 'export PATH=$PATH:/mnt/c/Windows/System32:/mnt/c/Windows' >> ~/.bashrc
source ~/.bashrc

# Check if wslview is installed

which wslview

# Test Browser

# This should open in your Windows browser

wslview <https://example.com>

# Finally Install

npm install -g @openai/codex

which codex

# Let's GO

codex

# Authenticate the Codex CLI before first use

codex login

# Codex recommends installing markdown lint

npm install -g markdownlint-cli

# Personal AI Infrastructure Workspace Notes

# For sandboxed environments, create the PAI workspace inside the project tree:

mkdir -p pai/{tools/custom,projects,archive/memory,logs}

# This keeps the structure portable when home directory writes are restricted.
