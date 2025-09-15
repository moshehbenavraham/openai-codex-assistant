# Scheduling Runbook

## Prerequisites

- Install the `schedule` Python package: `pip install schedule`
- Export `PAI_HOME` to point at the `pai/` directory if it lives outside `~/pai`
- Confirm the Codex CLI is authenticated (`codex login`) and accessible via
  `CODEX_BIN` or the default `codex` binary

## Short-Interval Smoke Test

1. Edit `pai/scheduler.py` and change both schedules to `schedule.every(1).minutes`
2. Start the scheduler:

   ```bash
   PYTHONPATH=pai PAI_HOME=$(pwd)/pai python3 pai/scheduler.py
   ```

3. Observe `pai/logs/scheduler.log` or the console for at least two cycles
4. Restore the production cadence (`08:00` daily and `Friday 16:00`) and commit
   the file

## Production Launch

1. Revert `schedule.every(1).minutes` to the production cadence
2. Start the scheduler using a process manager (tmux, systemd, or supervisord)
3. Confirm `PAI_DEBUG=1` logs tool executions without leaking secrets
4. Document the launch in `docs/initial_plan.md`

## Temporary Disable

1. Stop the process manager or terminate the `scheduler.py` process
2. Add a note to `docs/runbooks/scheduling.md` with the reason for suspension
3. Resume the scheduler once maintenance or downtime complete
