# Scheduling Runbook

## Prerequisites

- Install the `schedule` Python package: `pip install schedule`
- Export `PAI_HOME` to point at the `pai/` directory if it lives outside `~/pai`
- Confirm the Codex CLI is authenticated (`codex login`) and accessible via
  `CODEX_BIN` or the default `codex` binary

## Short-Interval Smoke Test

1. Run the scheduler with the built-in test overrides so you do not edit the
   production cadence:

   ```bash
   PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/scheduler.py \
     --interval-seconds 2 --cycles 4
   ```

   - `--interval-seconds 2` schedules both jobs every two seconds.
   - `--cycles 4` exits after four job completions (two full cycles).
   - Use `python3` instead of `.venv/bin/python` if you have globally installed
     the `schedule` package.
2. Wait for the console message `Reached 4 completed jobs; shutting down`.
3. Inspect `pai/logs/scheduler.log` for matching entries, for example:

   ```text
   2025-09-16 07:50:40,628 INFO __main__ Job morning_briefing completed
   2025-09-16 07:52:29,011 INFO __main__ Reached 4 completed jobs; shutting down
   ```

4. Remove the override flags to restore the standard schedule once testing is
   complete.

### Latest Verification Snapshot (2025-09-16)

- Command:

  ```bash
  PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/scheduler.py \
    --interval-seconds 2 --cycles 4
  ```

- Log extract:

  ```text
  2025-09-16 07:52:29,011 INFO __main__ Reached 4 completed jobs; shutting down
  ```

## Production Launch

1. Start the scheduler without override flags:

   ```bash
   PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/scheduler.py
   ```

2. Use a process manager (tmux, systemd service, or supervisord) to keep the
   process running after logout.
3. Confirm `PAI_DEBUG=1` logs tool executions without leaking secrets.
4. Document the launch in `docs/initial_plan.md` (or its successor) so other
   operators know the scheduler is active.

## Cron-Style Alternative

Some environments disallow persistent daemons. Use cron to trigger batches as
needed:

1. Edit the user crontab with `crontab -e`.
2. Add entries that run the scheduler for a fixed number of cycles, e.g.:

   ```cron
   # Fire the morning briefing and project summary on the hour
   0 * * * * PAI_HOME=/home/user/projects/codex-assistant/pai \
     PYTHONPATH=/home/user/projects/codex-assistant/pai \
     /home/user/projects/codex-assistant/.venv/bin/python \
     /home/user/projects/codex-assistant/pai/scheduler.py \
     --interval-seconds 5 --cycles 2 >> \
     /home/user/projects/codex-assistant/pai/logs/scheduler-cron.log 2>&1
   ```

   Adjust the binary path if you are not using the project virtual environment.
   The five-second interval lets both jobs run quickly before cron exits.
3. Confirm registration with `crontab -l | grep scheduler.py`.
4. Review the cron log and `pai/logs/scheduler.log` after the first run.

## Temporary Disable

1. Stop the process manager or terminate the `scheduler.py` process
2. Add a note to `docs/runbooks/scheduling.md` with the reason for suspension
3. Resume the scheduler once maintenance or downtime complete
