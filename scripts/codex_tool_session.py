#!/usr/bin/env python3
"""Interactive helper for running Codex tools with workspace-write sandbox."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import textwrap
from datetime import datetime
from pathlib import Path

try:
    import pexpect
except ModuleNotFoundError as exc:  # pragma: no cover - runtime guard
    sys.stderr.write(
        "codex_tool_session.py requires the 'pexpect' package.\n"
        "Install it in your virtual environment, e.g.:\n"
        "  python3 -m pip install pexpect\n"
    )
    raise SystemExit(1) from exc

PROMPT_PATTERN = r"codex>\s*"
APPROVAL_MARKERS = ("workspace", "sandbox", "write")
APPROVAL_TOKENS = ("y/n", "[y/n", "[y/n]")


class OutputTap:
    """Wires Codex stdout back to the console and transcript."""

    def __init__(self, writers, approver):
        self._writers = writers
        self._approver = approver

    def write(self, data):
        if not data:
            return
        for writer in self._writers:
            writer.write(data)
            writer.flush()
        if self._approver is not None:
            self._approver.feed(data)

    def flush(self):  # pragma: no cover - pexpect calls this implicitly
        for writer in self._writers:
            if hasattr(writer, "flush"):
                writer.flush()


class AutoApprover:
    """Sends 'y' when Codex asks for workspace-write approval."""

    def __init__(self, child, enabled, verbose_writer):
        self._child = child
        self._enabled = enabled
        self._verbose_writer = verbose_writer
        self._buffer = ""
        self._sent = False

    def feed(self, fragment):
        if not self._enabled or self._sent:
            return
        self._buffer += fragment.lower()
        if any(marker in self._buffer for marker in APPROVAL_MARKERS):
            if any(token in self._buffer for token in APPROVAL_TOKENS):
                self._child.sendline("y")
                self._sent = True
                if self._verbose_writer is not None:
                    self._verbose_writer.write(
                        "[codex-helper] Auto-approved workspace-write sandbox.\n"
                    )
                    self._verbose_writer.flush()
                # Keep buffer short after approval to avoid runaway growth.
                self._buffer = self._buffer[-1024:]
        else:
            # Trim to avoid unbounded accumulation across long sessions.
            self._buffer = self._buffer[-1024:]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Guide a Codex interactive session and run tools end-to-end.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
Examples:
  ./scripts/codex_tool_session.py
  ./scripts/codex_tool_session.py --tool search --params '{\"query\":\"hello\"}'
  ./scripts/codex_tool_session.py --handoff
"""
        ),
    )
    parser.add_argument(
        "--codex-bin",
        default=os.environ.get("CODEX_BIN", "codex"),
        help="Path to the Codex CLI (defaults to $CODEX_BIN or 'codex').",
    )
    parser.add_argument(
        "--sandbox",
        default=os.environ.get("CODEX_SANDBOX", "workspace-write"),
        help="Sandbox mode to request from Codex (default: workspace-write).",
    )
    parser.add_argument(
        "--no-auto-approve",
        dest="auto_approve",
        action="store_false",
        help="Require manual confirmation instead of sending 'y' automatically.",
    )
    parser.set_defaults(auto_approve=True)
    parser.add_argument(
        "--tool",
        help="Run a single tool command automatically before entering the loop.",
    )
    parser.add_argument(
        "--params",
        help="JSON string with parameters for --tool (default {}).",
    )
    parser.add_argument(
        "--params-file",
        help="Load JSON parameters for --tool from a file (overrides --params).",
    )
    parser.add_argument(
        "--stay",
        action="store_true",
        help="Keep the Codex session open after --tool instead of exiting immediately.",
    )
    parser.add_argument(
        "--handoff",
        action="store_true",
        help="After scripted runs, attach your terminal directly to Codex.",
    )
    parser.add_argument(
        "--transcript",
        help="Write a copy of the session to this file for later review.",
    )
    return parser.parse_args(argv)


def resolve_params(args: argparse.Namespace) -> str:
    if args.params_file:
        text = Path(args.params_file).read_text(encoding="utf-8")
        candidate = text.strip()
    elif args.params:
        candidate = args.params.strip()
    else:
        return "{}"

    # Validate JSON so Codex does not choke on typos.
    json.loads(candidate)
    return candidate


def start_codex(args: argparse.Namespace, transcript_file) -> pexpect.spawn:
    codex_path = shutil.which(args.codex_bin)
    if codex_path is None:
        raise SystemExit(
            f"Unable to find Codex CLI '{args.codex_bin}'. Install it or set --codex-bin."
        )

    command = [codex_path, "exec", "--sandbox", args.sandbox, "--json"]
    env = os.environ.copy()

    child = pexpect.spawn(command[0], command[1:], encoding="utf-8", timeout=60, env=env)
    approver = AutoApprover(child, args.auto_approve, verbose_writer=sys.stderr)

    writers = [sys.stdout]
    if transcript_file is not None:
        writers.append(transcript_file)

    child.logfile_read = OutputTap(writers, approver)
    return child


def wait_for_prompt(child: pexpect.spawn):
    child.expect(PROMPT_PATTERN)


def run_tool(child: pexpect.spawn, tool_name: str, params_json: str):
    command = f"Run tool {tool_name} with parameters: {params_json}"
    child.sendline(command)
    wait_for_prompt(child)


def interactive_loop(child: pexpect.spawn):
    print(
        textwrap.dedent(
            """
            [codex-helper] Enter tool name and JSON parameters. Press Enter on an empty
            tool name to exit. Prefix parameters with '@path/to/file.json' to load from a
            file. Type '!raw' to send a raw Codex command, or '!handoff' to hand control
            to the Codex prompt.
            """
        ).strip()
    )
    while True:
        try:
            tool = input("tool name> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not tool:
            break
        if tool == "!raw":
            try:
                raw = input("codex command> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            child.sendline(raw)
            wait_for_prompt(child)
            continue
        if tool == "!handoff":
            print("[codex-helper] Handing control to Codex; press Ctrl+] to return.")
            child.interact()
            continue

        try:
            params_raw = input("params JSON or @file> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if params_raw.startswith("@"):
            file_path = Path(params_raw[1:]).expanduser()
            try:
                params = file_path.read_text(encoding="utf-8").strip()
            except OSError as exc:
                print(f"[codex-helper] Failed to read {file_path}: {exc}")
                continue
        elif params_raw:
            params = params_raw
        else:
            params = "{}"

        try:
            json.loads(params)
        except json.JSONDecodeError as exc:
            print(f"[codex-helper] Invalid JSON: {exc}")
            continue

        run_tool(child, tool, params)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    transcript_file = None
    if args.transcript:
        transcript_path = Path(args.transcript).expanduser()
        transcript_path.parent.mkdir(parents=True, exist_ok=True)
        transcript_file = transcript_path.open("a", encoding="utf-8")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transcript_file.write(f"\n# Codex tool session {timestamp}\n")
        transcript_file.flush()

    child = start_codex(args, transcript_file)
    try:
        wait_for_prompt(child)

        if args.tool:
            params_json = resolve_params(args)
            run_tool(child, args.tool, params_json)
            if not args.stay and not args.handoff:
                child.sendline("exit")
                child.expect(pexpect.EOF)
                return 0

        interactive_loop(child)

        if args.handoff:
            print("[codex-helper] Handing control to Codex; press Ctrl+] to return.")
            child.interact()

        child.sendline("exit")
        child.expect(pexpect.EOF)
        return 0
    finally:
        if transcript_file is not None:
            transcript_file.close()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
