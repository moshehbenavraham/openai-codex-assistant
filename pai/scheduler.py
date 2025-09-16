"""PAI scheduler for recurring automations."""

from __future__ import annotations

import argparse
import logging
import os
import time
from pathlib import Path
from typing import Callable, Optional

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



def safe_job(
    name: str,
    func: Callable[[], None],
    *,
    on_complete: Optional[Callable[[str], None]] = None,
) -> Callable[[], None]:
    """Wrap a job with logging, error handling, and completion hook."""

    def wrapper() -> None:
        LOGGER.info("Running job: %s", name)
        try:
            func()
        except Exception as exc:  # pragma: no cover - runtime guard
            LOGGER.exception("Job %s failed: %s", name, exc)
        else:
            LOGGER.info("Job %s completed", name)
            if on_complete:
                on_complete(name)

    return wrapper


def morning_briefing(client: PAIClient) -> None:
    client.chat("Provide my morning briefing with calendar, weather, and focus items.")


def project_summary(client: PAIClient) -> None:
    client.chat("Summarize progress on all active projects.")


def _register_jobs(
    client: PAIClient,
    *,
    interval_minutes: Optional[int] = None,
    interval_seconds: Optional[int] = None,
    on_complete: Optional[Callable[[str], None]] = None,
) -> None:
    """Register scheduler jobs using either production or test cadence."""

    if interval_seconds:
        schedule.every(interval_seconds).seconds.do(
            safe_job("morning_briefing", lambda: morning_briefing(client), on_complete=on_complete)
        )
        schedule.every(interval_seconds).seconds.do(
            safe_job("project_summary", lambda: project_summary(client), on_complete=on_complete)
        )
        return

    if interval_minutes:
        schedule.every(interval_minutes).minutes.do(
            safe_job("morning_briefing", lambda: morning_briefing(client), on_complete=on_complete)
        )
        schedule.every(interval_minutes).minutes.do(
            safe_job("project_summary", lambda: project_summary(client), on_complete=on_complete)
        )
        return

    schedule.every().day.at("08:00").do(
        safe_job("morning_briefing", lambda: morning_briefing(client), on_complete=on_complete)
    )
    schedule.every().friday.at("16:00").do(
        safe_job("project_summary", lambda: project_summary(client), on_complete=on_complete)
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PAI scheduler controller")
    parser.add_argument(
        "--interval-minutes",
        type=int,
        help="Override production cadence with a unified per-minute interval for tests.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=int,
        help="Override production cadence with a unified per-second interval for rapid smoke tests.",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        help="Number of completed jobs before exiting (useful for smoke tests).",
    )
    args = parser.parse_args(argv)

    home = os.getenv("PAI_HOME")
    if not home:
        os.environ["PAI_HOME"] = str(os.path.dirname(__file__))
    _install_file_handler()
    if args.interval_minutes and args.interval_seconds:
        parser.error("Specify only one of --interval-minutes or --interval-seconds")

    client = PAIClient()
    completed_jobs: list[str] = []

    def _mark_complete(name: str) -> None:
        completed_jobs.append(name)

    on_complete = _mark_complete if args.cycles else None
    _register_jobs(
        client,
        interval_minutes=args.interval_minutes,
        interval_seconds=args.interval_seconds,
        on_complete=on_complete,
    )
    LOGGER.info("Scheduler started")
    while True:
        schedule.run_pending()
        if args.cycles and len(completed_jobs) >= args.cycles:
            LOGGER.info("Reached %s completed jobs; shutting down", args.cycles)
            break
        time.sleep(1)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
