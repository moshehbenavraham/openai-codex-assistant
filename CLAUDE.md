# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Personal AI Infrastructure (PAI) project that provides a Codex CLI-based assistant runtime. The system orchestrates various AI tools and maintains project context through a structured directory layout.

## Key Commands

### Running the PAI CLI
```bash
# From project root
./pai/pai.sh chat "Your message here"
./pai/pai.sh run-tool search --params '{"query": "test"}'
./pai/pai.sh load-context

# With debug output
PAI_DEBUG=1 ./pai/pai.sh chat "message"

# Override Python binary
PYTHON_BIN=python3.11 ./pai/pai.sh chat "message"
```

### Testing and Development
```bash
# Run the server directly with smoke test
./pai/pai.sh chat "ping"

# Check scheduler (temporarily reduce intervals for testing)
python pai/scheduler.py

# Run backup script
./pai/backup.sh --dry-run

# Optimize memory
python pai/optimize_memory.py --once
```

## Architecture

### Core Components

1. **PAI Server** (`pai/server.py`): Main orchestration layer that interfaces with the Codex CLI. Implements PAIClient class with methods for chat, tool execution, and context loading. Currently uses stub implementations for tools (search, create_image, analyze).

2. **Tool System** (`pai/tools/`): Markdown-based tool definitions that describe parameters, returns, and verification steps. Tools are registered in the context file for discovery.

3. **Context Management** (`pai/context.md`): System instructions and state tracking with auto-update placeholders for timestamp, active project, and memory updates.

4. **Memory System** (`pai/memory.md`, `pai/optimize_memory.py`): Persistent knowledge storage with optimization routines for long-term maintenance.

### Directory Structure

The PAI system lives in the `pai/` subdirectory with:
- Configuration: `config.json` (requires openai_api_key setup)
- Tools: `tools/*.md` (search, create_image, analyze)
- Projects: `projects/` for active project contexts
- Archives: `archive/memory/` for compressed historical data
- Logs: `logs/` for operational logging

## Implementation Status

The project follows a phased implementation approach (see `docs/implementation.md`):
- Phase 1-3: Complete (workspace setup, context, tool definitions)
- Phase 4: Partial (server implemented with stubs, needs Codex CLI integration)
- Phase 5-6: Components present but require configuration

## Important Notes

- The server currently returns stub responses when API key is missing or set to "replace-me"
- Tools (search, create_image, analyze) have stub implementations that need real integration
- Debug mode available via `PAI_DEBUG=1` environment variable
- Python 3.12+ with requests library required