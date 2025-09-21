"""Personal AI Infrastructure execution layer."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

LOGGER = logging.getLogger(__name__)
_LOG_LEVEL = logging.DEBUG if os.getenv("PAI_DEBUG") else logging.INFO
logging.basicConfig(level=_LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s %(message)s")

PAI_HOME = Path(os.getenv("PAI_HOME", Path(__file__).resolve().parent))
DEFAULT_CONTEXT_PATH = PAI_HOME / "context.md"
DEFAULT_CONFIG_PATH = PAI_HOME / "config.json"


@dataclass
class PAIResponse:
    """Simple wrapper for CLI serialization."""

    ok: bool
    data: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps({"ok": self.ok, "data": self.data}, indent=2)


class ConfigurationError(RuntimeError):
    """Raised when configuration is missing or invalid."""


class PAIClient:
    """Bridge between local state and the Codex CLI."""

    def __init__(
        self,
        config_path: Path = DEFAULT_CONFIG_PATH,
        context_path: Path = DEFAULT_CONTEXT_PATH,
    ) -> None:
        self.config_path = config_path
        self.context_path = context_path
        self.config = self._load_config()
        self.codex_cfg = self.config.get("codex", {})
        self.codex_bin = os.getenv("CODEX_BIN", self.codex_cfg.get("bin", "codex"))
        self.approval = os.getenv("PAI_APPROVAL", self.codex_cfg.get("approval"))
        self.sandbox = os.getenv("PAI_SANDBOX", self.codex_cfg.get("sandbox", "workspace-write"))
        self.model = os.getenv("PAI_MODEL", self.codex_cfg.get("model", "gpt-5-codex"))
        self.profile = os.getenv("PAI_PROFILE", self.codex_cfg.get("profile"))
        self.base_args = self._build_base_args()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            LOGGER.warning("Config file not found at %s", self.config_path)
            raise ConfigurationError("Missing config.json; run Phase 1 setup.")
        with self.config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _build_base_args(self) -> List[str]:
        args = [self.codex_bin]

        approval = (self.approval or "").strip()
        sandbox = (self.sandbox or "").strip()

        if approval and approval.lower() in {"dangerously-bypass", "dangerously-bypass-approvals-and-sandbox"}:
            args.append("--dangerously-bypass-approvals-and-sandbox")
            if sandbox:
                args.extend(["--sandbox", sandbox])
        elif approval:
            args.extend(["--ask-for-approval", approval])
            if sandbox:
                args.extend(["--sandbox", sandbox])
        else:
            if sandbox:
                args.extend(["--sandbox", sandbox])

        if self.profile:
            args.extend(["--profile", self.profile])
        if self.model:
            args.extend(["--model", self.model])
        return args + ["exec", "--json"]

    def load_context(self) -> str:
        if not self.context_path.exists():
            LOGGER.error("Context file missing at %s", self.context_path)
            raise FileNotFoundError(f"Context file not found: {self.context_path}")
        return self.context_path.read_text(encoding="utf-8")

    def chat(self, prompt: str, project: Optional[str] = None) -> Dict[str, Any]:
        system_prompt = self._system_prompt(project)
        payload = f"{system_prompt}\n\nUser: {prompt}"
        LOGGER.debug("Executing chat prompt via Codex CLI")
        result = self._run_codex(payload)
        return result

    def run_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        LOGGER.debug("Executing tool: %s", tool_name)
        prompt = f"Run tool {tool_name} with parameters: {json.dumps(parameters)}"
        return self._run_codex(prompt)

    def _run_codex(self, prompt: str) -> Dict[str, Any]:
        command = self.base_args + [prompt]
        LOGGER.debug("Running Codex command: %s", shlex.join(command))
        env = os.environ.copy()
        bin_path = PAI_HOME / "bin"
        if bin_path.exists():
            env["PATH"] = f"{bin_path}{os.pathsep}{env.get('PATH', '')}"
        tmp_override = env.get("PAI_TMPDIR") or env.get("TMPDIR")
        if not tmp_override:
            tmp_path = PAI_HOME / "tmp"
            tmp_path.mkdir(parents=True, exist_ok=True)
            env["TMPDIR"] = str(tmp_path)

        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )
        except FileNotFoundError as exc:
            LOGGER.error("Codex CLI not found: %s", exc)
            return self._stub_response("Codex CLI not installed; install @openai/codex", stderr=str(exc))

        if result.returncode != 0:
            stderr = result.stderr.strip()
            LOGGER.error("Codex CLI exited with %s: %s", result.returncode, stderr)
            return self._stub_response(
                f"Codex CLI failed with exit code {result.returncode}; check stderr",
                stdout=result.stdout,
                stderr=result.stderr,
            )

        messages: List[Dict[str, Any]] = []
        last_text: Optional[str] = None
        error_message: Optional[str] = None
        for line in result.stdout.splitlines():
            candidate = line.strip()
            if not candidate:
                continue
            try:
                event = json.loads(candidate)
            except json.JSONDecodeError:
                LOGGER.debug("Skipping non-JSON line from Codex: %s", candidate)
                continue
            messages.append(event)
            message = event.get("msg", {})
            if not isinstance(message, dict):
                continue
            msg_type = message.get("type")
            if msg_type == "agent_message":
                payload = message.get("message")
                if isinstance(payload, dict):
                    role = payload.get("role")
                    content = payload.get("content")
                    if role == "assistant" and isinstance(content, str):
                        last_text = content
                elif isinstance(payload, str):
                    last_text = payload
            elif msg_type in {"error", "stream_error"}:
                text = message.get("message")
                if isinstance(text, str):
                    error_message = text

        if not last_text:
            LOGGER.debug("No assistant message found; using raw stdout")
            last_text = error_message or result.stdout.strip() or "Codex CLI returned no assistant message."

        data: Dict[str, Any] = {
            "raw": messages,
            "last": last_text,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": last_text,
                    }
                }
            ],
        }
        if error_message:
            data["error"] = error_message
        return data

    def _stub_response(
        self,
        message: str,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ) -> Dict[str, Any]:
        LOGGER.info("Returning stub response: %s", message)
        return {
            "error": message,
            "stdout": stdout or "",
            "stderr": stderr or "",
            "raw": [],
            "last": message,
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": message,
                    }
                }
            ],
        }

    def _system_prompt(self, project: Optional[str]) -> str:
        context = self.load_context()
        header = "Active project: none" if not project else f"Active project: {project}"
        return f"{header}\n\n{context}"


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Personal AI Infrastructure CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="Send a chat prompt")
    chat_parser.add_argument("message", help="Prompt to send to the assistant")
    chat_parser.add_argument("--project", help="Active project slug", default=None)

    tool_parser = subparsers.add_parser("run-tool", help="Execute a tool")
    tool_parser.add_argument("name", help="Tool name to run")
    tool_parser.add_argument("--params", help="JSON string of parameters", default="{}")

    context_parser = subparsers.add_parser("load-context", help="Print the system context")
    context_parser.add_argument("--path", help="Override context path", default=None)

    return parser.parse_args(argv)


def _cli_chat(client: PAIClient, args: argparse.Namespace) -> PAIResponse:
    data = client.chat(args.message, project=args.project)
    ok = data.get("error") is None
    return PAIResponse(ok=ok, data=data)


def _cli_run_tool(client: PAIClient, args: argparse.Namespace) -> PAIResponse:
    try:
        parameters = json.loads(args.params)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON for --params: {exc}") from exc
    data = client.run_tool(args.name, parameters)
    ok = data.get("error") is None
    return PAIResponse(ok=ok, data=data)


def _cli_load_context(client: PAIClient, args: argparse.Namespace) -> PAIResponse:
    context_path = Path(args.path) if args.path else client.context_path
    client.context_path = context_path
    data = {"context": client.load_context()}
    return PAIResponse(ok=True, data=data)


COMMAND_HANDLERS = {
    "chat": _cli_chat,
    "run-tool": _cli_run_tool,
    "load-context": _cli_load_context,
}


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    client = PAIClient()
    handler = COMMAND_HANDLERS[args.command]
    response = handler(client, args)
    print(response.to_json())
    return 0


if __name__ == "__main__":
    sys.exit(main())
