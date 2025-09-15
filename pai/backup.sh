#!/usr/bin/env bash
set -euo pipefail

PAI_HOME=${PAI_HOME:-"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"}
BACKUP_DIR="${PAI_HOME}/archive"
LOG_DIR="${PAI_HOME}/logs"
mkdir -p "${BACKUP_DIR}" "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/backup.log"
DRY_RUN=false
RETENTION_DAYS=${RETENTION_DAYS:-30}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      echo "Unknown argument: $1" | tee -a "${LOG_FILE}"
      exit 1
      ;;
  esac
done

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_NAME="pai-${TIMESTAMP}.tar.gz"
TARGET_PATH="${BACKUP_DIR}/${ARCHIVE_NAME}"

{
  echo "[$(date --iso-8601=seconds)] Starting backup (dry_run=${DRY_RUN})"
  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "tar -czf ${TARGET_PATH} -C ${PAI_HOME} context.md memory.md projects tools config.json pai.sh server.py scheduler.py voice.py optimize_memory.py backup.sh"
  else
    tar -czf "${TARGET_PATH}" \
      -C "${PAI_HOME}" context.md memory.md projects tools config.json pai.sh server.py scheduler.py voice.py optimize_memory.py backup.sh || {
        echo "Backup failed"
        exit 1
      }
    echo "Created archive ${TARGET_PATH}"
    find "${BACKUP_DIR}" -name 'pai-*.tar.gz' -mtime +"${RETENTION_DAYS}" -print -delete
  fi
  echo "[$(date --iso-8601=seconds)] Backup finished"
} >>"${LOG_FILE}" 2>&1

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Dry run complete. See ${LOG_FILE} for details."
else
  echo "Backup created at ${TARGET_PATH}. See ${LOG_FILE} for details."
fi
