"""PAI scheduler for recurring automations."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Callable

try:
    import schedule
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("Install the 'schedule' package to use scheduler.py") from exc

from server import PAIClient

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def _install_file_handler() -> None:
    home = Path(os.getenv("PAI_HOME", Path(__file__).resolve().parent))
    log_dir = home / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "scheduler.log")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    LOGGER.addHandler(handler)



def safe_job(name: str, func: Callable[[], None]) -> Callable[[], None]:
    """Wrap a job with logging and error handling."""

    def wrapper() -> None:
        LOGGER.info("Running job: %s", name)
        try:
            func()
        except Exception as exc:  # pragma: no cover - runtime guard
            LOGGER.exception("Job %s failed: %s", name, exc)
        else:
            LOGGER.info("Job %s completed", name)

    return wrapper


def morning_briefing(client: PAIClient) -> None:
    client.chat("Provide my morning briefing with calendar, weather, and focus items.")


def project_summary(client: PAIClient) -> None:
    client.chat("Summarize progress on all active projects.")


def main() -> None:
    home = os.getenv("PAI_HOME")
    if not home:
        os.environ["PAI_HOME"] = str(os.path.dirname(__file__))
    _install_file_handler()
    client = PAIClient()
    schedule.every().day.at("08:00").do(safe_job("morning_briefing", lambda: morning_briefing(client)))
    schedule.every().friday.at("16:00").do(safe_job("project_summary", lambda: project_summary(client)))
    LOGGER.info("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
