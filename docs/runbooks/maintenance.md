# Maintenance Runbook

Keep long-term storage healthy by running the backup and memory optimization
jobs regularly, capturing evidence in `pai/logs/`, and documenting any schedule
changes here.

## Prerequisites

- Export `PAI_HOME` to the active workspace (recommended:
  `export PAI_HOME=$(pwd)/pai`).
- Ensure `pai/archive/` and `pai/logs/` exist (`backup.sh` will create them if
  needed).
- Confirm the Codex workspace is quiescent before running maintenance to avoid
  archiving files mid-write.

## Manual Backup Procedure

1. Run a dry run to validate the archive manifest:

   ```bash
   PAI_HOME=$(pwd)/pai ./pai/backup.sh --dry-run
   ```

2. Inspect `pai/logs/backup.log` for a line beginning with
   `tar -czf <target> -C <pai_home> ...`. This confirms the script would bundle
   `context.md`, `memory.md`, `projects/`, `tools/`, and the runtime scripts.
   - Latest run (2025-09-16 09:00 local) produced:

     <!-- markdownlint-disable MD013 -->
     ```text
     [2025-09-16T09:00:03+03:00] Starting backup (dry_run=true)
     tar -czf /home/xamgibson/projects/codex-assistant/pai/archive/pai-20250916-090003.tar.gz \
       -C /home/xamgibson/projects/codex-assistant/pai \
       context.md memory.md projects tools config.json pai.sh server.py \
       scheduler.py voice.py optimize_memory.py backup.sh
     [2025-09-16T09:00:03+03:00] Backup finished
     ```
     <!-- markdownlint-enable MD013 -->
3. Execute the real backup:

   ```bash
   PAI_HOME=$(pwd)/pai ./pai/backup.sh
   ```

4. Verify results:
   - `ls -1 pai/archive` should include the new `pai-YYYYMMDD-HHMMSS.tar.gz`.
   - `tail -n5 pai/logs/backup.log` should show `Created archive` followed by
     a `find` rotation entry. Set `RETENTION_DAYS` to override the default 30.
5. If the script exits non-zero, review the log and available disk space before
   retrying. The log captures failures with full context.

## Manual Memory Optimization

1. Ensure `pai/memory.md` contains dated sections (`## YYYY-MM-DD`).
2. Run a one-off optimization pass (default window archives entries older than
   seven days):

   ```bash
   PAI_HOME=$(pwd)/pai python3 pai/optimize_memory.py --window 7 --once
   ```

3. Validate outcomes:
   - Archived entries land in `pai/archive/memory/memory-YYYY-MM-DD.md`.
   - `tail -n5 pai/logs/optimize_memory.log` shows `Archived memory section` and
     `Memory optimization complete`.
   - `pai/memory.md` now includes a `## Summaries` block with the latest
     timestamp plus a `## Recent Entries` section for active content.
   - Latest run (2025-09-16 09:00 local) reported:

     <!-- markdownlint-disable MD013 -->
     ```text
     2025-09-16 09:00:17,570 INFO __main__ Starting memory optimization for entries older than 7 days
     2025-09-16 09:00:17,570 INFO __main__ No dated sections found; nothing to optimize
     ```
     <!-- markdownlint-enable MD013 -->
4. If no dated sections are detected the script logs "No dated sections found";
   update the source file and rerun.

## Scheduling Backups and Optimization

### Cron

1. Open the user crontab: `crontab -e`.
2. Add entries similar to:

   ```cron
   # PAI maintenance (export PAI_HOME inline for non-login shells)
   0 2 * * * PAI_HOME=/home/user/projects/codex-assistant/pai \ \
     /home/user/projects/codex-assistant/pai/backup.sh >> \ \
     /home/user/projects/codex-assistant/pai/logs/backup-cron.log 2>&1
   30 2 * * 0 PAI_HOME=/home/user/projects/codex-assistant/pai \ \
     PYTHONPATH=/home/user/projects/codex-assistant/pai \ \
     python3 /home/user/projects/codex-assistant/pai/optimize_memory.py \ \
     --window 7 --once >> \ \
     /home/user/projects/codex-assistant/pai/logs/optimize-cron.log 2>&1
   ```

3. Confirm the new jobs are registered: `crontab -l | grep PAI`.
4. After the first scheduled run, review the cron-specific log files and
   `pai/logs/*.log` for success markers.
5. Current installation (2025-09-16) uses `pai/cron_maintenance` with:

   ```cron
   # PAI maintenance jobs
   0 2 * * * PAI_HOME=/home/xamgibson/projects/codex-assistant/pai \
     /home/xamgibson/projects/codex-assistant/pai/backup.sh >> \
     /home/xamgibson/projects/codex-assistant/pai/logs/backup-cron.log 2>&1
   30 2 * * 0 PAI_HOME=/home/xamgibson/projects/codex-assistant/pai \
     PYTHONPATH=/home/xamgibson/projects/codex-assistant/pai /usr/bin/python3 \
     /home/xamgibson/projects/codex-assistant/pai/optimize_memory.py --once >> \
     /home/xamgibson/projects/codex-assistant/pai/logs/optimize-cron.log 2>&1
   ```

### systemd Timers (user scope)

1. Create `~/.config/systemd/user/pai-backup.service`:

   ```ini
   [Unit]
   Description=PAI backup

   [Service]
   Type=oneshot
   Environment=PAI_HOME=%h/projects/codex-assistant/pai
   ExecStart=%h/projects/codex-assistant/pai/backup.sh
   ```

2. Create the companion timer `~/.config/systemd/user/pai-backup.timer`:

   ```ini
   [Unit]
   Description=Nightly PAI backup

   [Timer]
   OnCalendar=*-*-* 02:00:00
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```

3. Repeat the pattern for memory optimization (e.g., service name
   `pai-optimize.service`, timer at Sunday 02:30 with
   `ExecStart=%h/projects/codex-assistant/pai/optimize_memory.py --window 7 --once`).
4. Enable the timers:

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now pai-backup.timer pai-optimize.timer
   ```

5. Verify schedule health:

   ```bash
   systemctl --user list-timers "pai-*"
   journalctl --user -u pai-backup.service -u pai-optimize.service --since "-1 day"
   ```

### Troubleshooting

- Missing archives usually indicate `PAI_HOME` was unset; confirm the variable
  in your cron/systemd unit matches the project path.
- Permission errors often stem from running as root under WSL; rerun as the
  workspace user so relative paths resolve correctly.
- If rotation deletes recent archives, check `RETENTION_DAYS`; increase it or
  export a larger value before invoking `backup.sh`.
- For optimization issues, ensure every memory entry starts with
  `## YYYY-MM-DD`; any other headings are skipped and logged.
