# Scheduling Runbook (In-Chat)

Atlas runs the scheduler checks from inside the Codex CLI chat. Use the prompts
below as your operational checklist. Legacy shell commands remain available at
the end for detached environments.

## Primary In-Chat Smoke Test

1. Ask Atlas to verify prerequisites:
   ```text
   Atlas, confirm the scheduler script exists and show the first 10 lines.
   ```
2. Trigger the short-interval test:
   ```text
   Atlas, run the scheduler with --interval-seconds 2 and --cycles 4, then share the stdout and the new lines from pai/logs/scheduler.log.
   ```
3. Confirm Atlas reports `Reached 4 completed jobs; shutting down` (or similar)
   and posts the corresponding log excerpt.
4. When finished, remind Atlas to revert to the normal cadence if overrides were
   applied elsewhere.

## Production Operation from Chat

- Start the long-running scheduler:
  ```text
  Atlas, launch the scheduler for production cadence and keep me posted if it exits.
  ```
- Atlas should mention which process manager (tmux/systemd) it uses or suggest
  options if none are configured.
- Request periodic status:
  ```text
  Atlas, every morning at 09:00, summarize the last scheduler run and append it to docs/changelog.md.
  ```

## Observability

- `Atlas, tail pai/logs/scheduler.log | tail -n 20.`
- `Atlas, check for cron overrides touching scheduler.py.`
- `Atlas, list running processes filtering for scheduler.py.`

Atlas returns log snippets or process tables directly in chat so you do not need
an extra terminal.

## Legacy Commands (Fallback Only)

If you must run outside the chat (CI/cron), the canonical commands remain:

```bash
PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/scheduler.py --interval-seconds 2 --cycles 4
PAI_HOME=$(pwd)/pai PYTHONPATH=pai .venv/bin/python pai/scheduler.py
```

Remember to note the fallback use in `docs/changelog.md` and return to the
in-chat workflow afterward.
