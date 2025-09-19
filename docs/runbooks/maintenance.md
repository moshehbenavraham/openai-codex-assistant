# Maintenance Runbook (In-Chat)

Backups and memory optimization are now coordinated inside the Codex CLI chat.
Ask Atlas to perform each step and capture evidence in the convo transcript.

## Manual Backup via Chat

1. Dry run:
   ```text
   Atlas, execute backup.sh with --dry-run and paste the resulting log lines.
   ```
2. Atlas reports the tar command and dry-run completion.
3. Full run:
   ```text
   Atlas, run backup.sh for real and list the newest archive in pai/archive.
   ```
4. Request verification:
   ```text
   Atlas, show tail -n 5 pai/logs/backup.log.
   ```

## Manual Memory Optimization via Chat

1. Confirm dated sections:
   ```text
   Atlas, inspect pai/memory.md and confirm the latest dated entry.
   ```
2. Run optimizer:
   ```text
   Atlas, execute optimize_memory.py --window 7 --once and report the log summary.
   ```
3. Validate archives:
   ```text
   Atlas, list pai/archive/memory sorted by newest.
   ```

## Scheduling from Chat

- Cron review: `Atlas, cat pai/cron_maintenance and explain the cadence.`
- Register jobs: `Atlas, install pai/cron_maintenance via crontab and confirm with crontab -l.`
- systemd alternative: `Atlas, show the status of the pai-backup.timer and pai-optimize.timer user units.`

Atlas surfaces command output and tells you if the timers/cron entries already
exist or need updates.

## Troubleshooting Prompts

- `Atlas, check disk usage for pai/archive and warn me if it exceeds 80%.`
- `Atlas, grep "ERROR" in pai/logs/backup.log and summarize findings.`
- `Atlas, verify RETENTION_DAYS is set before the next run.`

## Legacy Commands (Fallback Only)

For headless contexts you may still run:

```bash
PAI_HOME=$(pwd)/pai ./pai/backup.sh --dry-run
PAI_HOME=$(pwd)/pai ./pai/backup.sh
PAI_HOME=$(pwd)/pai python3 pai/optimize_memory.py --once
```

Log the fallback usage in `docs/changelog.md` and return to the chat workflow
once the detached job finishes.
