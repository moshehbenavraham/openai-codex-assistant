# Tool: create_image

## Description

Generate an image from a natural-language prompt using the configured model.

## Parameters

| Name | Type | Constraints | Description |
| ---- | ---- | ----------- | ----------- |
| prompt | string | required, 1-600 chars | Describe the desired scene. |
| style | string | optional | Artistic modifiers, e.g., `watercolor`. |
| size | string | optional, default 1024x1024 | Pick a supported square size. |
|      |        |                             | 512x512, 768x768, or 1024x1024. |
| quality | string | optional, default standard | Choose draft or standard. |

## Returns

| Field | Type | Description |
| ----- | ---- | ----------- |
| image_url | string | Temporary URL for the generated image. |
| revised_prompt | string | Prompt text after preprocessing. |
| expires_at | string | ISO-8601 expiration timestamp. |

## Examples

```json
{
  "prompt": "Isometric workspace for personal AI infrastructure",
  "style": "vector art",
  "size": "768x768"
}
```

## Verification

1. Confirm the Codex CLI can reach your image backend or mock and that
   authentication succeeded (`codex login`).
2. Issue the following command:

   ```bash
   CODEX_BIN=codex ./pai/pai.sh run-tool create_image \
     --params '{"prompt":"minimalist app icon"}'
   ```

3. Confirm the response includes `image_url`, `revised_prompt`, and
   `expires_at` keys.
