"""Personal AI Infrastructure execution layer."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import requests
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit("The 'requests' package is required. Install it with 'pip install requests'.") from exc

LOGGER = logging.getLogger(__name__)
_LOG_LEVEL = logging.DEBUG if os.getenv("PAI_DEBUG") else logging.INFO
logging.basicConfig(level=_LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s %(message)s")

PAI_HOME = Path(os.getenv("PAI_HOME", Path(__file__).resolve().parent))
DEFAULT_CONTEXT_PATH = PAI_HOME / "context.md"
DEFAULT_CONFIG_PATH = PAI_HOME / "config.json"
DEFAULT_MEMORY_PATH = PAI_HOME / "memory.md"


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
    """Client responsible for orchestrating tool and chat calls."""

    def __init__(
        self,
        config_path: Path = DEFAULT_CONFIG_PATH,
        context_path: Path = DEFAULT_CONTEXT_PATH,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.config_path = config_path
        self.context_path = context_path
        self.session = session or requests.Session()
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            LOGGER.warning("Config file not found at %s", self.config_path)
            raise ConfigurationError("Missing config.json; run Phase 1 setup.")
        with self.config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def load_context(self) -> str:
        if not self.context_path.exists():
            LOGGER.error("Context file missing at %s", self.context_path)
            raise FileNotFoundError(f"Context file not found: {self.context_path}")
        return self.context_path.read_text(encoding="utf-8")

    def chat(self, prompt: str, project: Optional[str] = None) -> Dict[str, Any]:
        LOGGER.debug("Executing chat with project=%s", project)
        api_key = self.config.get("openai_api_key", "")
        model = self.config.get("default_model", "gpt-5-preview")
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": self._system_prompt(project)},
                {"role": "user", "content": prompt},
            ],
        }
        if not api_key or api_key == "replace-me":
            LOGGER.info("API key missing or placeholder; returning stub response")
            return {
                "model": model,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Stubbed response: configure openai_api_key to reach the API.",
                        }
                    }
                ],
            }
        return self._post("/chat/completions", payload)

    def run_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        LOGGER.debug("Executing tool: %s", tool_name)
        stub_handlers = {
            "search": self._stub_search,
            "create_image": self._stub_create_image,
            "analyze": self._stub_analyze,
        }
        if tool_name in stub_handlers:
            return stub_handlers[tool_name](parameters)
        raise ValueError(f"Unknown tool: {tool_name}")

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        base_url = self.config.get("base_url", "https://api.openai.com/v1")
        api_key = self.config.get("openai_api_key")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        url = f"{base_url.rstrip('/')}{path}"
        retries = int(self.config.get("max_retries", 3))
        timeout = int(self.config.get("timeout_seconds", 60))
        for attempt in range(1, retries + 1):
            try:
                response = self.session.post(url, headers=headers, json=payload, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as exc:
                LOGGER.warning("Request attempt %s failed: %s", attempt, exc)
                if attempt == retries:
                    raise
        raise RuntimeError("Request attempts exhausted")

    def _system_prompt(self, project: Optional[str]) -> str:
        context = self.load_context()
        header = "Active project: none" if not project else f"Active project: {project}"
        return f"{header}\n\n{context}"

    def _stub_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query", "")
        max_results = int(params.get("max_results", 5))
        return {
            "provider": "stub-search",
            "results": [
                {
                    "title": f"Result {idx + 1} for {query}",
                    "snippet": "Replace with real search integration.",
                    "url": f"https://example.com/{idx + 1}",
                    "published_at": "1970-01-01T00:00:00Z",
                }
                for idx in range(max_results)
            ],
        }

    def _stub_create_image(self, params: Dict[str, Any]) -> Dict[str, Any]:
        prompt = params.get("prompt", "")
        size = params.get("size", "1024x1024")
        return {
            "image_url": f"https://images.example.com/mock/{size}",
            "revised_prompt": prompt.strip() or "Describe the desired image.",
            "expires_at": "1970-01-01T00:00:00Z",
        }

    def _stub_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        subject = params.get("subject", "")
        return {
            "analysis": {"summary": f"Analysis placeholder for {subject}."},
            "recommendations": ["Configure live analysis pipeline."],
            "sources": [],
        }


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
    return PAIResponse(ok=True, data=data)


def _cli_run_tool(client: PAIClient, args: argparse.Namespace) -> PAIResponse:
    try:
        parameters = json.loads(args.params)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON for --params: {exc}") from exc
    data = client.run_tool(args.name, parameters)
    return PAIResponse(ok=True, data=data)


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
