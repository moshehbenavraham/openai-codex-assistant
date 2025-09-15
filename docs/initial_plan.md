# Personal AI Infrastructure (PAI) - Implementation Guide

## System Philosophy

- **System Over Models**: The orchestration and structure matter more than model intelligence
- **Text as Universal Interface**: All interactions and data are text/markdown-based
- **Unix Philosophy**: Build modular tools that do one thing well and can be chained together
- **Unified Context Management**: Single source of truth for all system knowledge

## Implementation Roadmap

Follow the phased checklist in [docs/implementation.md](implementation.md) to
execute this plan in controlled increments.

## Architecture Overview

### Directory Structure

```
~/pai/
├── context.md          # Main system context and instructions
├── tools/              # Tool definitions and implementations
│   ├── search.md
│   ├── create_image.md
│   ├── analyze.md
│   └── custom/         # User-defined tools
├── projects/           # Active project contexts
│   └── [project_name].md
├── memory.md           # Conversation history and learnings
├── config.json         # Codex CLI configuration defaults
├── server.py           # Codex orchestration layer
├── scheduler.py        # Recurring automation runner
├── voice.py            # Voice interface script
├── optimize_memory.py  # Long-term memory optimizer
├── backup.sh           # Snapshot utility (executable)
└── pai.sh              # Command-line interface
```

## Core Components

### 1. System Context

**~/pai/context.md**

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
- Timestamp: [auto-updated]
- Active Project: [auto-updated from environment]
- Last Memory Update: [auto-updated]

## Tool Registry
[Auto-populated from ~/pai/tools/]
```

### 2. Tool System

Each tool is a markdown file that defines its interface and maps to implementation:

**~/pai/tools/search.md**

```markdown
# Tool: search

## Description
Search the web for current information

## Parameters
- query: string (required) - Search query
- max_results: integer (optional, default: 5) - Number of results

## Returns
- results: array of {title, snippet, url}

## Example
Input: {"query": "latest AI developments", "max_results": 3}
Output: {"results": [{"title": "...", "snippet": "...", "url": "..."}]}
```

**~/pai/tools/create_image.md**

```markdown
# Tool: create_image

## Description
Generate images using DALL-E 3

## Parameters
- prompt: string (required) - Image description
- style: string (optional) - Style modifiers
- size: string (optional, default: "1024x1024")

## Returns
- image_url: string - URL of generated image
- revised_prompt: string - Actual prompt used
```

**~/pai/tools/analyze.md**

```markdown
# Tool: analyze

## Description
Deep analysis of topics, code, or documents

## Parameters
- subject: string (required) - What to analyze
- type: string (required) - "code" | "security" | "performance" | "general"
- depth: string (optional, default: "standard") - "quick" | "standard" | "deep"

## Returns
- analysis: object - Structured analysis results
- recommendations: array - Actionable recommendations
```

### 3. Codex Orchestrator

**~/pai/server.py**

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

The orchestrator focuses on preparing prompts, invoking `codex`, and capturing
the Codex agent's JSONL output. Tool execution remains codified through
markdown specs, but the heavy lifting lives inside the Codex runtime rather
than a bespoke HTTP API.

### 4. Configuration

**~/pai/config.json**

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

The `codex` block mirrors the CLI flags so downstream automation can override
settings without hand-editing scripts.

### 5. Command Line Interface

**~/pai/pai.sh**

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PAI_HOME="${PAI_HOME:-${SCRIPT_DIR}}"
export CODEX_BIN="${CODEX_BIN:-codex}"

python3 "${SCRIPT_DIR}/server.py" "$@"
```

The shell wrapper centralizes environment variables (`PAI_HOME`, `CODEX_BIN`)
before delegating to the Python orchestrator, ensuring every surface uses the
same Codex configuration.

### 6. Project Templates

**~/pai/projects/example_project.md**

```markdown
# Project: [Project Name]

## Overview
Brief description of the project and its goals

## Status
- Phase: Planning | Development | Testing | Deployed
- Priority: High | Medium | Low
- Deadline: YYYY-MM-DD

## Context
Key information needed for AI assistance:
- Technology stack
- Design decisions
- Constraints and requirements

## Current Focus
What we're working on right now

## Completed
- [x] Task 1
- [x] Task 2

## Next Steps
- [ ] Upcoming task 1
- [ ] Upcoming task 2

## References
- Documentation: [links]
- Repository: [links]
- Related projects: [links]
```

### 7. Memory Structure

**~/pai/memory.md**

```markdown
# PAI Memory Log

## 2024-12-20T10:30:00
**User**: Create a security analysis tool
**Response**: Created new tool definition for security analysis
**Tools Used**: create_tool, analyze

## 2024-12-20T09:15:00
**User**: What's my focus today?
**Response**: Based on your active project, focus on Codex integration
**Tools Used**: None

[Automatically maintained, older entries summarized]
```

## Implementation Steps

### Day 1: Foundation

1. Create directory structure
2. Set up `context.md` with system instructions
3. Install and authenticate the Codex CLI: `npm install -g @openai/codex && codex login`
4. Create a basic `server.py` that shells out to `codex exec --json`

### Day 2: Core Tools

1. Define 3-5 essential tools in markdown
2. Wire tool prompts through the Codex CLI helper
3. Test tool discovery and execution via `pai.sh`
4. Set up the command-line interface with `CODEX_BIN` overrides

### Day 3: Memory & Projects

1. Implement memory logging system
2. Create project switching mechanism
3. Add context awareness to responses
4. Test project-specific behaviors via Codex prompts

### Day 4: Refinement

1. Add custom tool support
2. Implement error handling
3. Set up logging and monitoring
4. Create backup system for memory

### Day 5: Optimization

1. Test complete workflows through the Codex CLI
2. Optimize context loading and tool prompts
3. Add convenience scripts
4. Document common patterns

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
CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{\"query\":\"GPT-5 best practices\"}'
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
