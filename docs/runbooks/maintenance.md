# Maintenance Runbook

## Backup Procedure

1. Ensure `PAI_HOME` points at the active workspace (e.g., `export PAI_HOME=$(pwd)/pai`)
2. Run a dry run to confirm the archive plan:

   ```bash
   PAI_HOME=$(pwd)/pai ./pai/backup.sh --dry-run
   ```

3. Review `pai/logs/backup.log` for the simulated `tar` command
4. Execute the real backup:

   ```bash
   PAI_HOME=$(pwd)/pai ./pai/backup.sh
   ```

5. Confirm a new `pai-<timestamp>.tar.gz` file exists in `pai/archive`
6. Verify rotation removed archives older than `RETENTION_DAYS` (default 30)

## Memory Optimization

1. Populate `pai/memory.md` with dated sections using `## YYYY-MM-DD`
2. Run a single optimization pass:

   ```bash
   PAI_HOME=$(pwd)/pai python3 pai/optimize_memory.py --window 7
   ```

3. Check `pai/archive/memory/` for archived entries
4. Review `pai/logs/optimize_memory.log` for a success message
5. Inspect `pai/memory.md` to confirm summaries appear under `## Summaries`

## Scheduling Backups and Optimization

1. Add cron entries (example):

   ```cron
   PAI_HOME=<pai_home>
   0 2 * * * $PAI_HOME/backup.sh
   30 2 * * 0 python3 $PAI_HOME/optimize_memory.py --window 7
   ```

2. For systemd timers, document the unit files in this runbook and enable them:

   ```bash
   systemctl --user enable --now pai-backup.timer
   ```

3. Record the current status for review:

    ```bash
    systemctl --user list-timers | grep pai
    ```

4. Update this runbook whenever schedules or retention policies change
