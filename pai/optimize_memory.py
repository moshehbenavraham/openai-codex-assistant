"""Memory optimization utilities for the Personal AI Infrastructure."""

from __future__ import annotations

import argparse
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

from server import PAIClient  # noqa: F401 - ensures config/environment ready

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

PAI_HOME = Path(os.getenv("PAI_HOME", Path(__file__).resolve().parent))
MEMORY_PATH = PAI_HOME / "memory.md"
ARCHIVE_DIR = PAI_HOME / "archive" / "memory"
LOG_DIR = PAI_HOME / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
FILE_HANDLER = logging.FileHandler(LOG_DIR / "optimize_memory.log")
FILE_HANDLER.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
LOGGER.addHandler(FILE_HANDLER)

SECTION_PATTERN = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")


def parse_sections(text: str) -> List[Tuple[str, List[str]]]:
    sections: List[Tuple[str, List[str]]] = []
    current_heading: str | None = None
    buffer: List[str] = []
    for line in text.splitlines():
        match = SECTION_PATTERN.match(line)
        if match:
            if current_heading is not None:
                sections.append((current_heading, buffer))
                buffer = []
            current_heading = match.group(1)
        else:
            if current_heading is not None:
                buffer.append(line)
    if current_heading is not None:
        sections.append((current_heading, buffer))
    return sections


def summarize(content: List[str]) -> str:
    text = " ".join(line.strip("- ") for line in content if line.strip())
    if not text:
        return "No details recorded."
    if len(text) > 160:
        return text[:157] + "..."
    return text


def optimize_memory(window_days: int) -> None:
    LOGGER.info("Starting memory optimization for entries older than %s days", window_days)
    if not MEMORY_PATH.exists():
        LOGGER.info("Memory file does not exist at %s", MEMORY_PATH)
        return
    content = MEMORY_PATH.read_text(encoding="utf-8")
    sections = parse_sections(content)
    if not sections:
        LOGGER.info("No dated sections found; nothing to optimize")
        return

    cutoff = datetime.utcnow().date() - timedelta(days=window_days)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    retained_lines: List[str] = []
    summaries: List[str] = []
    for heading, lines in sections:
        try:
            entry_date = datetime.strptime(heading, "%Y-%m-%d").date()
        except ValueError:
            LOGGER.warning("Skipping section with unrecognized date heading: %s", heading)
            retained_lines.extend([f"## {heading}"] + lines)
            continue
        if entry_date <= cutoff:
            archive_path = ARCHIVE_DIR / f"memory-{heading}.md"
            archive_path.write_text("\n".join([f"## {heading}"] + lines), encoding="utf-8")
            summary = summarize(lines)
            summaries.append(f"- {heading}: {summary}")
            LOGGER.info("Archived memory section for %s", heading)
        else:
            retained_lines.append(f"## {heading}")
            retained_lines.extend(lines)

    new_content: List[str] = ["# PAI Memory", ""]
    if summaries:
        timestamp = datetime.utcnow().isoformat()
        new_content.extend(["## Summaries", f"_Last updated: {timestamp}_", ""])
        new_content.extend(summaries)
        new_content.append("")
    if retained_lines:
        new_content.append("## Recent Entries")
        new_content.extend(retained_lines)
    MEMORY_PATH.write_text("\n".join(new_content).strip() + "\n", encoding="utf-8")
    LOGGER.info("Memory optimization complete")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Optimize long-term memory")
    parser.add_argument("--window", type=int, default=7, help="Archive entries older than this many days")
    parser.add_argument("--once", action="store_true", help="Run once and exit (default behavior)")
    args = parser.parse_args(argv)

    optimize_memory(args.window)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
