# Update — 2025-09-19

## Objective
Shift the operational center of the Codex assistant system from external scripts to in-chat execution inside the OpenAI Codex CLI, while keeping the script-based tooling available as a backup path.

## Primary Focus: In-Chat Execution via OpenAI Codex CLI
- Document the new default workflow, including how to initiate Atlas from an interactive Codex CLI session and required environment prerequisites.
- Audit existing commands and scripts to identify which functionality must be exposed or wrapped for conversational use; prioritize high-frequency tasks first.
- Build or adapt helper commands/macros that let Atlas trigger common automation (builds, tests, deployments) without leaving the chat context.

## Supporting Changes
- Update onboarding guides (README, docs/) to highlight the in-chat path first, demoting external script usage to an advanced/legacy section.
- Review automation hooks (Playwright, voice system, UFC context loader) to ensure they can be invoked and monitored from inside the chat workflow.
- Adjust statusline and any CLI prompts so they assume in-chat control as the default environment.

## Legacy Script Path (Secondary)
- Preserve the existing scripts for headless or CI-style runs; clearly label them as secondary fallback tooling.
- Add notes describing when the legacy path is appropriate (e.g., offline automation, CI proofs) and how it stays in sync with the in-chat flow.

## Rollout Plan
1. Draft documentation changes and circulate for internal review.
2. Implement required command wrappers/adapters and validate them in a live Codex CLI session.
3. Update onboarding assets and announce the shift to the team.
4. Schedule a short validation cycle to confirm both in-chat and script-based paths remain functional.
