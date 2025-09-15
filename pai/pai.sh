#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PAI_HOME="${SCRIPT_DIR}"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}"

PYTHON_BIN=${PYTHON_BIN:-python3}
exec "${PYTHON_BIN}" "${SCRIPT_DIR}/server.py" "$@"
