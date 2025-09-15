# Repository Guidelines

## Project Structure & Module Organization

The repository centers on configuration and process docs for the personal AI infrastructure. Top-level files include `README.md` for a quick elevator pitch and `LICENSE` for reuse terms. Use the `docs/` directory for all workflow instructions: `initial_plan.md` tracks the reference architecture, while `steps.md` covers environment setup tasks. Keep new project briefs, tool specs, or agent playbooks inside `docs/` and favor short, linkable Markdown sections so downstream agents can parse them quickly.

## Build, Test, and Development Commands

There is no compiled artifact, but keep the documentation runnable. Use `npx markdownlint "**/*.md"` to catch formatting drift before sending a change. Run `rg --files` or `rg <keyword>` from the repo root to locate prior guidance for reuse. When updating command snippets, verify them in a fresh shell to ensure they match a Debian-based WSL environment as described in `docs/steps.md`.

## Documentation

Only valid safe ASCII characters are allowed, UTF-8 LF line endings, and Unix-style paths

## Coding Style & Naming Conventions

Write Markdown with ATX headings and one topic per section. Indent lists with two spaces, wrap code fences with explicit language tags, and prefer inline code for single commands. Name new documents descriptively (e.g., `docs/tool_registry.md`). Keep instructions in second person, describe shell commands in the order they should be executed, and avoid speculative language that could confuse automated agents.

## Testing Guidelines

Treat command sequences as tests: execute them end-to-end, confirm they succeed, and note prerequisites or expected prompts. When proposing code examples, provide minimal, copy-ready snippets and annotate parameters inline. If documenting API behavior, include quick verification steps so agents can assert expected outputs without guesswork.

## Commit & Pull Request Guidelines

Follow the existing imperative subject style (`Initial commit`). Keep subjects under 60 characters and expand on context in the body when introducing new tooling or workflows. Pull requests should summarize intent, list touched docs, and highlight any manual steps reviewers must follow. Link related issues or tasks, and include screenshots or terminal captures when behavior changes.

## Agent-Specific Instructions

Assume automated agents will consume these docs: spell out defaults, note when human judgment is required, and flag irreversible actions. Update `docs/initial_plan.md` whenever architecture assumptions shift so downstream automation stays aligned.
