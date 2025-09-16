# Changelog

## 2025-09-16

- **Added**: You introduced Claude-focused operating guidance in `CLAUDE.md`
  and checked in `.claude/settings.local.json` so Claude Code inherits the
  local defaults.
- **Added**: You delivered the Codex-driven runtime under `pai/` by adding
  `server.py`, the `pai.sh` wrapper, background automation scripts
  (`scheduler.py`, `voice.py`, `optimize_memory.py`), and maintenance helpers
  such as `backup.sh` with supporting archive and log directories.
- **Added**: You published operational references including
  `docs/runbooks/maintenance.md`, refreshed `pai/context.md`, and seeded
  memory/configuration placeholders (`pai/memory.md`, `pai/config.json`) so
  downstream agents stay synchronized.
- **Updated**: You expanded `docs/implementation.md` with deeper phase guidance
  and aligned `AGENTS.md`, `.gitignore`, and `LICENSE` with the Codex-first
  workflow.
- **Updated**: You refactored `pai/server.py` and `pai/pai.sh` to drive the
  Codex CLI bridge (with stub fallbacks), redirected Codex rollouts into
  `pai/codex-sessions/` to satisfy sandbox policies, refreshed
  `docs/runbooks/server_smoke_test.md` to capture the live JSON output, and
  normalized top-level docs to pass `markdownlint`.
- **Updated**: You added scheduler override flags (`--interval-seconds`,
  `--cycles`) to `pai/scheduler.py`, documented the rapid smoke-test workflow
  plus cron-style execution in `docs/runbooks/scheduling.md`, and checked off
  the corresponding Phase 5 verification tasks in `docs/implementation.md`.
- **Updated**: You trimmed `docs/implementation.md` to list only the remaining
  Phase 5, Phase 6, and governance actions so completed work now lives solely
  in this changelog.
- **Removed**: You retired `docs/initial_plan.md` now that the implementation
  guide serves as the authoritative architecture record.

## 2025-09-15

- **Added**: You bootstrapped the repository with permissive licensing via
  `LICENSE`, automation hygiene in `.gitignore`, and a concise project overview
  in `README.md`.
- **Added**: You documented Codex CLI integration by introducing
  `docs/implementation.md`, `docs/steps.md`, `docs/tool_registry.md`, and
  runbooks covering scheduling and server smoke tests under `docs/runbooks/`.
- **Added**: You created baseline tool specifications (`pai/tools/search.md`,
  `pai/tools/create_image.md`, `pai/tools/analyze.md`) so the orchestration
  layer has copy-ready definitions.
- **Updated**: You framed the long-term architecture through the original
  `docs/initial_plan.md`, establishing the phased roadmap for future work.
