#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$REPO_ROOT"

CODEX_BIN="${CODEX_BIN:-codex}"
DEFAULT_SANDBOX="${SANDBOX:-workspace-write}"

if ! command -v "$CODEX_BIN" >/dev/null 2>&1; then
  echo "[codex-interactive] Unable to find Codex CLI ('$CODEX_BIN')." >&2
  echo "Install the Codex CLI and/or export CODEX_BIN before retrying." >&2
  exit 1
fi

SANDBOX_VALUE="$DEFAULT_SANDBOX"
EXTRA_ARGS=()

if [[ $# -gt 0 ]]; then
  case "$1" in
    read-only|workspace-write|danger-full-access)
      SANDBOX_VALUE="$1"
      shift
      ;;
    --)
      shift
      ;;
  esac
fi

if [[ $# -gt 0 ]]; then
  EXTRA_ARGS=("$@")
fi

if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
  EXTRA_DISPLAY="${EXTRA_ARGS[*]}"
else
  EXTRA_DISPLAY="(none)"
fi

cat <<EOT
[codex-interactive] Starting Codex CLI.
[codex-interactive] Sandbox: $SANDBOX_VALUE
[codex-interactive] Extra Codex args: $EXTRA_DISPLAY
[codex-interactive] Type your tool commands at the 'codex>' prompt.
[codex-interactive] Use Ctrl+C to abort or 'exit' to end the Codex session.
EOT

exec "$CODEX_BIN" --sandbox "$SANDBOX_VALUE" "${EXTRA_ARGS[@]}"
