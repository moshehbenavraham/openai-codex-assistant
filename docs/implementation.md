# Implementation Phases for Personal AI Infrastructure

## System Philosophy

- **System Over Models**: The orchestration and structure matter more than model intelligence
- **Text as Universal Interface**: All interactions and data are text/markdown-based
- **Unix Philosophy**: Build modular tools that do one thing well and can be chained together
- **Unified Context Management**: Single source of truth for all system knowledge

## Implementation Roadmap

Follow these phases to stand up and extend the Personal AI Infrastructure
(PAI) while protecting critical hygiene tasks. Move through the phases in
order and advance only after your work meets the exit criteria.

## Phase 1 - Establish the Workspace Shell

### Phase 1 Objectives

- Reproduce the baseline directory layout
- Stage configuration placeholders that downstream automation expects

### Phase 1 Tasks

- Create `~/pai/` and mirror the reference layout in a single shell session:

  ```bash
  mkdir -p ~/pai/{tools/custom,projects}
  touch ~/pai/{context.md,memory.md,config.json,pai.sh}
  ```

- Add the improved directory map to `context.md` so other agents inherit the
  canonical structure:

  ```markdown
  ~/pai/
  |- context.md          # System context and instructions
  |- tools/              # Tool definitions and implementations
  |  |- search.md
  |  |- create_image.md
  |  |- analyze.md
  |  \- custom/         # User-defined tools
  |- projects/           # Active project contexts
  |  \- project-name.md
  |- memory.md           # Conversation history and learnings
  |- config.json         # Runtime configuration for Codex CLI
  |- server.py           # Codex-aware orchestration layer
  \- pai.sh              # Command-line interface
  ```

- Populate `config.json` with Codex CLI defaults:

  ```json
  {
    "codex": {
      "bin": "codex",
      "model": "gpt-5-codex",
      "approval": "never",
      "sandbox": "workspace-write",
      "profile": null
    },
    "tools": {
      "enabled": ["search", "create_image", "analyze"],
      "allow_custom": true,
      "timeout_seconds": 30
    },
    "memory": {
      "max_entries": 1000,
      "auto_summarize_after": 100,
      "retention_days": 90
    }
  }
  ```

  Leave any optional secrets as placeholders (`"replace-me"`).
- Record any machine-specific setup dependencies in `docs/steps.md` so
  future agents can reproduce them.

### Phase 1 Exit Criteria

- `~/pai/` contains every placeholder file and directory
- `docs/steps.md` references every non-obvious setup decision you made

### Phase 1 Verification

- Run `ls ~/pai` and confirm the directory tree matches the map in
  `context.md`
- Open `docs/steps.md` and ensure your environment notes clearly describe any
  extra packages, permissions, or shell changes you applied

## Phase 2 - Author Core System Context

### Phase 2 Objectives

- Provide the orchestrator with a clear operating manual
- Ensure context metadata stays current automatically

### Phase 2 Tasks

- Draft `~/pai/context.md` in second-person form:

  ```markdown
  # Personal AI Infrastructure Context

  ## System Role
  You are PAI, a personal AI infrastructure system powered by GPT-5.
  Your purpose is to serve as an intelligent orchestration layer for personal productivity and knowledge management.

  ## Core Capabilities
  - Execute tools from ~/pai/tools/ directory
  - Maintain project context in ~/pai/projects/
  - Track important information in ~/pai/memory.md
  - Chain multiple operations to complete complex tasks

  ## Operating Principles
  1. Always check for active project context before responding
  2. Update memory.md with significant learnings or decisions
  3. Use tools when actions are needed beyond conversation
  4. Maintain markdown formatting for all outputs

  ## System State
  - Timestamp: <!-- auto:timestamp -->
  - Active Project: <!-- auto:project -->
  - Last Memory Update: <!-- auto:memory -->

  ## Tool Registry
  [Auto-populated from ~/pai/tools/]
  ```
- Add a "System State" block that references auto-updated tokens (timestamp,
  active project, last memory update). Mark each token with a placeholder such
  as `<!-- auto:timestamp -->` so automation can discover it.
- Append a "Tool Registry" section that lists every tool markdown file by
  slug. Direct agents to regenerate this section by script instead of manual
  edits.
- Validate formatting with `npx markdownlint "~/pai/context.md"` and address
  all violations immediately.

### Phase 2 Exit Criteria

- `context.md` passes lint checks
- Placeholders clearly flag automation-managed fields

### Phase 2 Verification

- Execute `npx markdownlint "~/pai/context.md"` and resolve every warning
- Inspect the "System State" block to ensure each placeholder uses the
  `<!-- auto:token -->` format so automation tooling can parse it reliably
- Confirm the "Tool Registry" section references each markdown file in
  `~/pai/tools/` by slug

## Phase 3 - Implement and Test Tool Definitions

### Phase 3 Objectives

- Supply copy-ready tool specs that follow the Unix-style orchestration
  philosophy
- Guarantee each tool exposes parameters and return types that the server and
  agents can trust

### Phase 3 Tasks

- For each core tool (`search`, `create_image`, `analyze`), create a markdown
  file under `~/pai/tools/` with sections for Description, Parameters,
  Returns, Examples, and Verification.
- Reword parameter tables so they describe constraints in plain language
  (`max_results: integer >= 1, default 5`) to expose validation gaps that the
  original plan left implicit.
- Introduce a "Verification" subsection showing how to exercise the tool via
  the Codex CLI once Phase 4 is complete.
- When you add new tools, update `docs/tool_registry.md` (create it if absent)
  to summarize capabilities, expected latency, and safety considerations.
- Run `npx markdownlint "~/pai/tools/*.md"` to verify formatting and correct
  all failures before moving on.

### Phase 3 Exit Criteria

- Every tool markdown file documents inputs, outputs, and verification steps
- Linting passes across the `tools/` directory

### Phase 3 Verification

- Run `npx markdownlint "~/pai/tools/*.md"` and fix issues before proceeding
- Cross-check each tool spec against the "Tool Registry" entry you added in
  `docs/tool_registry.md` to guarantee consistency on parameters and safety
- Walk through the Verification subsection of one tool and confirm the sample
  command matches the Codex CLI workflow you expect to ship in Phase 4

## Phase 4 - Build the Codex CLI Orchestration Surface

### Phase 4 Objectives

- Deliver a functioning execution layer that mediates between Codex CLI
  requests and local tools
- Provide a CLI entry point that mirrors Codex-driven capabilities

### Phase 4 Tasks

- Implement `~/pai/server.py` with a `PAIClient` class:

  ```python
  """Bridge between local state and the Codex CLI."""

  import json
  import logging
  import os
  import shlex
  import subprocess
  from pathlib import Path
  from typing import Any, Dict, List

  LOGGER = logging.getLogger(__name__)

  class PAIClient:
      def __init__(self, config_path: Path) -> None:
          self.config = json.loads(config_path.read_text())
          codex_cfg = self.config.get("codex", {})
          self.codex_bin = os.getenv("CODEX_BIN", codex_cfg.get("bin", "codex"))
          self.approval = codex_cfg.get("approval", "never")
          self.sandbox = codex_cfg.get("sandbox", "workspace-write")
          self.model = codex_cfg.get("model", "gpt-5-codex")
          self.profile = codex_cfg.get("profile")
          self.base_args = self._build_base_args()

      def _build_base_args(self) -> List[str]:
          args = [self.codex_bin, "-a", self.approval, "-s", self.sandbox]
          if self.profile:
              args.extend(["-p", self.profile])
          if self.model:
              args.extend(["-m", self.model])
          return args + ["exec", "--json"]

      def chat(self, prompt: str) -> Dict[str, Any]:
          """Send a chat prompt through Codex and parse the JSONL response."""
          command = self.base_args + [prompt]
          LOGGER.debug("Running Codex command: %s", shlex.join(command))
          result = subprocess.run(
              command,
              check=False,
              capture_output=True,
              text=True,
          )
          if result.returncode != 0:
              raise RuntimeError(f"Codex CLI failed: {result.stderr}")

          messages: List[Dict[str, Any]] = []
          for line in result.stdout.splitlines():
              messages.append(json.loads(line))

          return {
              "raw": messages,
              "last": next(
                  (entry["msg"]["message"] for entry in reversed(messages)
                   if entry.get("msg", {}).get("type") == "agent_message"),
                  None,
              ),
          }

      def run_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
          prompt = f"Run tool {tool_name} with parameters: {json.dumps(parameters)}"
          return self.chat(prompt)
  ```
- Inject debug logging from the troubleshooting section
  (`logger.debug("Executing tool: %s", tool_name)`) so the debug pathway is
  not an afterthought.
- Create `pai.sh` as a POSIX-compliant wrapper:

  ```bash
  #!/usr/bin/env bash
  set -euo pipefail

  SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
  export PAI_HOME="${PAI_HOME:-${SCRIPT_DIR}}"
  export CODEX_BIN="${CODEX_BIN:-codex}"

  python3 "${SCRIPT_DIR}/server.py" "$@"
  ```

  Document usage (`./pai.sh chat "Summarize my tasks"`).
- Verify the CLI by running `CODEX_BIN=codex ./pai.sh chat "ping"` and confirm
  you receive a well-formed JSON response or a stubbed placeholder during
  development.
- Capture the verification transcript and store it under
  `docs/runbooks/server_smoke_test.md` for reproducibility.

### Phase 4 Exit Criteria

- CLI and server agree on tool discovery paths and respond to a smoke-test
  request
- Debug logging toggles via an env var such as `PAI_DEBUG=1`

### Phase 4 Verification

- From the project root, run `CODEX_BIN=codex ./pai.sh chat "ping"` and capture
  the response JSON (or stub) along with any logs
- Store the transcript in `docs/runbooks/server_smoke_test.md` and describe
  the environment variables or mock configuration you used
- Toggle `PAI_DEBUG=1 CODEX_BIN=codex ./pai.sh chat "ping"` and verify debug
  statements log the executed Codex tool names without leaking secrets

## Phase 5 - Layer Advanced Interfaces

### Phase 5 Objectives

- Add automation and multimodal surfaces without destabilizing the core

### Phase 5 Tasks

- Implement `~/pai/scheduler.py` using the provided `schedule` pattern and
  guard each job with try/except plus logging to prevent silent exits.
- Build `~/pai/voice.py` with dependency checks so the script guides you if
  `speech_recognition` or `pyttsx3` are missing.
- Document cron-style alternatives in `docs/runbooks/scheduling.md` for
  environments where long-running daemons are discouraged.
- Test `scheduler.py` by temporarily shortening intervals
  (`schedule.every(1).minutes`) and observing log output for at least two
  cycles before restoring production timings.

### Phase 5 Exit Criteria

- Scheduler and voice scripts run without uncaught exceptions during local
  tests
- Runbooks explain how to enable or disable these interfaces safely

### Phase 5 Verification

- Temporarily set `schedule.every(1).minutes` in `scheduler.py`, run the script
  for two cycles, and review the log output under `~/pai/logs/`
- Execute `python ~/pai/voice.py --check-deps` (or your equivalent flag) to
  confirm the script reports missing packages with actionable guidance
- Update `docs/runbooks/scheduling.md` with the log sample and instructions for
  reverting the interval to the production cadence

## Phase 6 - Operational Maintenance and Continuous Improvement

### Phase 6 Objectives

- Keep the system reliable as memory grows and new projects appear

### Phase 6 Tasks

- Ship `~/pai/backup.sh` with executable permissions
  (`chmod +x ~/pai/backup.sh`) and confirm it rotates archives using the `find`
  prune logic.
- Build `~/pai/optimize_memory.py` around the provided pseudocode. Implement
  weekly summarization routines and archive raw entries under
  `~/pai/archive/memory/`.
- Schedule the backup and optimization scripts via your preferred scheduler
  (cron or systemd timer) and document the setup in
  `docs/runbooks/maintenance.md`.
- Review the "Best Practices" and "Troubleshooting" sections quarterly, and
  update them whenever you add tooling, notice new failure modes, or adjust the
  cleanup cadence.

### Phase 6 Exit Criteria

- Backups and memory optimization run on schedule with logs stored under
  `~/pai/logs/`
- Documentation reflects the current maintenance workflow and known caveats

### Phase 6 Verification

- Run `~/pai/backup.sh --dry-run` (add a dry-run flag if absent) to validate
  archive rotation without overwriting existing files, then inspect
  `~/pai/logs/backup.log`
- Execute `python ~/pai/optimize_memory.py --once` and confirm the script
  writes summaries to `~/pai/archive/memory/` while logging actions
- Document the cron or systemd entries in `docs/runbooks/maintenance.md` and
  include the command you used to verify their status (`systemctl list-timers`
  or `crontab -l`)

## Ongoing Governance

- After each phase, update `docs/initial_plan.md` with the implementation
  decisions you made so the reference architecture stays authoritative.
- Before shipping changes, run `npx markdownlint "**/*.md"` from the
  repository root.
- Track every modification through version control with imperative commit
  subjects (`Add scheduler runbook`).

Following these phases keeps the Personal AI Infrastructure iterable while
maintaining the rigorous documentation standards downstream agents rely on.

## Usage Examples

### Daily Workflow

```bash
# Start your day
CODEX_BIN=codex ./pai/pai.sh chat "What's my focus today based on active projects?"

# Set project context
CODEX_BIN=codex ./pai/pai.sh chat "Switch the active project to website-redesign"

# Execute complex task
CODEX_BIN=codex ./pai/pai.sh chat "Analyze the security of our deployment and create a report"

# Quick tool execution
CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{"query":"GPT-5 best practices"}'
```

### Creating Custom Tools

```markdown
# ~/pai/tools/custom/deploy.md

# Tool: deploy

## Description
Deploy current project to production

## Parameters
- environment: string - "staging" | "production"
- version: string - Version tag

## Implementation
Custom Python script at ~/pai/tools/custom/deploy.py
```

### Python Integration

```python
import json
import os
import subprocess
from pathlib import Path

class PAIClient:
    def __init__(self, pai_home: Path):
        self.pai_home = pai_home
        self.codex_bin = os.getenv("CODEX_BIN", "codex")

    def _exec(self, prompt: str) -> dict:
        command = [
            self.codex_bin,
            "-a",
            "never",
            "-s",
            "workspace-write",
            "exec",
            "--json",
            prompt,
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        return events

    def chat(self, message: str) -> str:
        events = self._exec(message)
        for entry in reversed(events):
            msg = entry.get("msg")
            if msg and msg.get("type") == "agent_message":
                return msg["message"]["content"]
        raise RuntimeError("Codex did not return a chat response")

pai = PAIClient(Path.home() / "pai")
print(pai.chat("Summarize my recent code changes"))
```

## Advanced Features

### Scheduled Tasks

```python
# ~/pai/scheduler.py
import schedule
import time
from pai_client import PAIClient

pai = PAIClient()

def morning_briefing():
    pai.chat("Generate my morning briefing with calendar, weather, and news")

def project_summary():
    pai.chat("Summarize progress on all active projects")

schedule.every().day.at("08:00").do(morning_briefing)
schedule.every().friday.at("16:00").do(project_summary)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Voice Interface

```python
# ~/pai/voice.py
import speech_recognition as sr
import pyttsx3
from pai_client import PAIClient

class VoicePAI:
    def __init__(self):
        self.pai = PAIClient()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio)
            return text

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def interact(self):
        command = self.listen()
        response = self.pai.chat(command)
        self.speak(response)
```

## System Maintenance

### Backup Strategy

```bash
#!/bin/bash
# ~/pai/backup.sh

# Daily backup of critical files
tar -czf ~/backups/pai-$(date +%Y%m%d).tar.gz \
    ~/pai/memory.md \
    ~/pai/projects/ \
    ~/pai/tools/custom/

# Keep last 30 days
find ~/backups -name "pai-*.tar.gz" -mtime +30 -delete
```

### Memory Optimization

```python
# ~/pai/optimize_memory.py

def summarize_old_memories():
    """Summarize memories older than 30 days"""
    # Load memory.md
    # Group by week
    # Generate summaries using GPT-5
    # Archive originals
    # Update memory.md with summaries
```

## Best Practices

1. **Keep tools focused**: Each tool should do exactly one thing
2. **Document everything**: Clear markdown documentation for all components
3. **Version control**: Track changes to tools and context
4. **Regular cleanup**: Summarize old memories, archive completed projects
5. **Test incrementally**: Verify each component before building on it
6. **Monitor usage**: Track which tools and patterns are most valuable
7. **Iterate based on needs**: Add tools and features as patterns emerge

## Troubleshooting

### Common Issues

**Context not loading**: Check file paths and permissions
**Tools not found**: Verify markdown format and server parsing
**Memory growing too large**: Implement summarization routine
**Codex CLI errors**: Re-run `codex login`, confirm sandbox flags, or inspect stderr for command failures

### Debug Mode

```python
# Add to server.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log all tool executions
logger.debug(f"Executing tool: {tool_name} with {parameters}")
```

This system provides a powerful yet simple personal AI infrastructure that can be extended and customized based on your specific needs.
