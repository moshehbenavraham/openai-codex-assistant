# Changelog

## 2025-09-16

- **Fixed**: Patched `scripts/codex_tool_session.py` to launch Codex with the
  `-` stdin sentinel so automated tool runs no longer fail with "No prompt
  provided" and documented the behavior in `docs/usage_local.md`.
- **Fixed**: Updated `scripts/codex_interactive.sh` to call the interactive
  Codex CLI (defaulting to `workspace-write`) and documented the new argument
  handling in `docs/usage_local.md` so operators can pass prompts without
  breaking sandbox selection.
- **Added**: Created `scripts/codex_tool_session.py` (guided loop + auto-approve)
  and `scripts/codex_interactive.sh` (raw CLI wrapper) so operators can obtain
  real Codex tool output without manual sandbox wrangling.
- **Updated**: Extended `docs/deployment_local.md`, `docs/usage_local.md`, and
  `README.md` with the helper workflow, transcript tips, and the new `pexpect`
  dependency in the Python install step.
- **Updated**: Documented the voice interface dependency check, captured the
  missing `espeak-ng` requirement after installing `SpeechRecognition` and
  `pyttsx3`, and added `docs/runbooks/voice.md` so operators can finish the
  Phase 5 audio validation.
- **Updated**: Installed `espeak-ng`, `portaudio19-dev`, `alsa-utils`, and
  `pyaudio`, then taught `pai/voice.py` to log into `pai/logs/voice.log` and
  fail gracefully when no input device is configured.
- **Updated**: Noted the new audio prerequisites in `docs/steps.md` so fresh
  machines include the required system and Python packages.
- **Added**: Wrote `docs/deployment_local.md` covering end-to-end WSL2 setup and
  smoke tests for the local environment.
- **Updated**: Refreshed `README.md` with quick-start commands and linked
  runbooks for the new deployment flow.
- **Updated**: Expanded `docs/tool_registry.md` with parameter summaries and
  verification commands for `search`, `create_image`, and `analyze`.
- **Added**: Captured WSL2 usage workflows in `docs/usage_local.md` and
  clarified the sandbox limitation plus manual tool workaround in
  `docs/deployment_local.md`.
- **Added**: Published `.env.example` so local sudo credentials can be managed
  without risking secrets in version control.
- **Updated**: Added CLI flags to `pai/voice.py` for prerecorded audio and mute
  mode, captured a sample run in `docs/runbooks/voice.md`, stored
  `pai/tests/audio/hello.wav` for repeatable tests, and recorded the latest
  scheduler verification snippet in `docs/runbooks/scheduling.md`.
- **Updated**: Registered cron jobs via `pai/cron_maintenance`, ran
  `backup.sh --dry-run` and `optimize_memory.py --once`, and logged the results
  plus troubleshooting notes in `docs/runbooks/maintenance.md` to close out
  Phase 6 checks.
- **Updated**: Removed the obsolete governance reminder about
  `docs/initial_plan.md` now that `docs/implementation.md` is the authoritative
  roadmap.
