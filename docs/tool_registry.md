# Tool Registry

Atlas can invoke tools directly from the Codex CLI chat. Use the prompts below
for the primary workflow; fallback shell commands remain for legacy automation.

## search

- **What it does:** Query configured data sources for text matches.
- **Ask Atlas:**
  ```text
  Atlas, run the search tool for "deployment status" with the default settings and summarize the hits.
  ```
- **Parameters:** `query` (required string), `max_results` (integer, default 5).
- **Latency:** 1–3 seconds in a warm session.
- **Safety:** Avoid logging sensitive terms; Atlas will redact before persisting.
- **Chat verification:**
  ```bash
  ./pai/bin/tool search '{"query":"status"}'
  ```
- **Legacy fallback (detached):**
  ```bash
  ./scripts/codex_tool_session.py --tool search --params '{"query":"status"}'
  ```

## create_image

- **What it does:** Generate an image from a text prompt via the configured diffusion model.
- **Ask Atlas:**
  ```text
  Atlas, generate an image for "atlas robot blueprint" at 512 by 512 and share the link.
  ```
- **Parameters:** `prompt` (string, required), `size` (`256x256|512x512|1024x1024`, default `512x512`).
- **Latency:** 5–15 seconds.
- **Safety:** Confirm prompts comply with content policy and avoid leaking temporary URLs.
- **Chat verification:**
  ```bash
  ./pai/pai.sh run-tool create_image --params '{"prompt":"blueprint"}'
  ```
- **Legacy fallback (detached):**
  ```bash
  ./scripts/codex_tool_session.py --tool create_image --params '{"prompt":"blueprint"}'
  ```

## analyze

- **What it does:** Produce structured analyses over text, code, or documentation.
- **Ask Atlas:**
  ```text
  Atlas, analyze docs/usage_local.md with focus on gaps in the in-chat migration notes and include recommendations.
  ```
- **Parameters:** `subject` (string, required), `focus` (optional string), `include_recommendations` (boolean, default `true`).
- **Latency:** 2–6 seconds for standard depth.
- **Safety:** Sanitize file paths and suppress secrets before sharing results.
- **Chat verification:**
  ```bash
  ./pai/pai.sh run-tool analyze --params '{"subject":"release notes"}'
  ```
- **Legacy fallback (detached):**
  ```bash
  ./scripts/codex_tool_session.py --tool analyze --params '{"subject":"release notes"}'
  ```

Atlas surfaces tool output in the chat transcript. Use the legacy commands only
when running detached workflows and note the choice in `docs/changelog.md`.
