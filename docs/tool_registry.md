# Tool Registry

## search

- **Description:** Execute text searches across configured data sources
  (internet or internal knowledge bases).
- **Parameters:** `query` (string, required), `max_results` (integer ≥ 1,
  default 5).
- **Expected Latency:** 1–3 seconds with a warm cache.
- **Safety:** Redact sensitive terms before logging; respect rate limits.
- **Verification:**

  ```bash
  CODEX_BIN=codex ./pai/pai.sh run-tool search --params '{"query":"status"}'
  ```

## create_image

- **Description:** Generate images from prompts via the configured diffusion
  model.
- **Parameters:** `prompt` (string, required), `size` (string from
  `256x256|512x512|1024x1024`, default `512x512`).
- **Expected Latency:** 5–15 seconds; longer for higher resolutions.
- **Safety:** Filter disallowed prompts and avoid persisting temporary URLs.
- **Verification:**

  ```bash
  CODEX_BIN=codex ./pai/pai.sh run-tool create_image --params '{"prompt":"blueprint"}'
  ```

## analyze

- **Description:** Produce structured analyses over text, code, or documents.
- **Parameters:** `subject` (string, required), `focus` (string, optional),
  `include_recommendations` (boolean, default `true`).
- **Expected Latency:** 2–6 seconds for standard depth.
- **Safety:** Sanitize referenced file paths and redact secrets in outputs.
- **Verification:**

  ```bash
  CODEX_BIN=codex ./pai/pai.sh run-tool analyze --params '{"subject":"release notes"}'
  ```
