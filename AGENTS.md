# Repository Guidelines

## Project Structure & Module Organization

The repository captures documentation and runtime assets for the Personal AI
Infrastructure (PAI). Top-level files include `README.md` for the elevator
pitch and `LICENSE` for reuse terms. All workflow guidance lives under `docs/`:

- `docs/implementation.md` is the authoritative phased rollout plan. Update
  checklists there as work lands.
- `docs/changelog.md` records a reverse-chronological history of changes.
- `docs/runbooks/` holds reproducible procedures (e.g., server smoke tests).
- `docs/steps.md` documents machine setup requirements.

Runtime code resides in `pai/` (CLI wrapper, server, tools, logs). Keep new
project briefs, tool specs, and agent playbooks inside `docs/` using short,
linkable sections so downstream automation can parse them quickly.

## Build, Test, and Development Commands

The deliverable is documentation plus the PAI CLI bridge. Treat the following
as required smoke tests:

- `CODEX_BIN=codex ./pai/pai.sh chat "ping"`
- `CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{"query":"test"}'`

Run them after touching `pai/` or any tool specs. Use
`npx markdownlint "**/*.md"` before shipping changes. `rg --files` or
`rg <keyword>` helps surface prior guidance. Verify shell snippets in a fresh
Debian/WSL session that matches `docs/steps.md`.

When you need additional inspection:

- `PAI_DEBUG=1 CODEX_BIN=codex ./pai/pai.sh chat "message"` (debug logging)
- `PYTHON_BIN=python3.11 ./pai/pai.sh chat "message"` (override Python)
- `python pai/scheduler.py` (temporarily lower intervals for smoke tests)
- `./pai/backup.sh --dry-run` and `python pai/optimize_memory.py --once`

## Documentation

Only safe ASCII characters are permitted. Use UTF-8 with LF endings and
Unix-style paths.

## Coding Style & Naming Conventions

Write Markdown with ATX headings and one topic per section. Indent lists with
two spaces, wrap code fences with explicit language tags, and prefer inline
code for single commands. Name new documents descriptively (e.g.,
`docs/tool_registry.md`). Keep instructions in second person, order shell
commands as they should be executed, and avoid speculative language that could
confuse automated agents.

## Testing Guidelines

Treat command sequences as tests: execute them end-to-end, confirm they succeed,
and note prerequisites or prompts. When proposing code examples, provide
minimal, copy-ready snippets and annotate parameters inline. If documenting API
behavior, include verification steps so agents can assert outputs without
guesswork.

## Commit & Pull Request Guidelines

Follow the existing imperative subject style (`Add scheduler runbook`). Keep
subjects under 60 characters and expand in the body when introducing new
tooling or workflows. Pull requests should summarize intent, list touched docs,
and highlight any manual steps reviewers must follow. Link related issues or
tasks, and include screenshots or terminal captures when behavior changes.

## Agent-Specific Instructions

Assume automated agents will consume these docs: spell out defaults, note when
human judgment is required, and flag irreversible actions. Update the Phase
checklists in `docs/implementation.md` and the history in `docs/changelog.md`
whenever you change architecture or tooling so downstream automation stays
aligned. Keep Codex rollout logs inside `pai/codex-sessions/` (symlinked from
`~/.codex/sessions`); do not commit those artifacts.

## Runtime & Architecture Snapshot

- **PAI Server** (`pai/server.py`): Shells out to the Codex CLI (`codex exec
  --json`), parses JSONL events, and falls back to structured stub responses if
  the CLI fails.
- **CLI Wrapper** (`pai/pai.sh`): Exports `PAI_HOME`, respects `CODEX_BIN`, and
  launches the Python bridge.
- **Tool Specs** (`pai/tools/*.md`): Markdown definitions for `search`,
  `create_image`, and `analyze`. Keep these aligned with
  `docs/tool_registry.md`.
- **Context & Memory** (`pai/context.md`, `pai/memory.md`): System instructions
  with auto-managed placeholders and long-term knowledge storage. Maintenance
  scripts live in `pai/backup.sh` and `pai/optimize_memory.py`.
- **Docs**: `docs/implementation.md` tracks phased progress, while
  `docs/changelog.md` logs milestones. Smoke tests and other procedures reside
  under `docs/runbooks/`.

Implementation status (see `docs/implementation.md`): Phases 1–4 complete with
Codex integration verified; Phase 5 focuses on scheduler validation; Phase 6 is
partially complete (scripts shipped, scheduling outstanding).
