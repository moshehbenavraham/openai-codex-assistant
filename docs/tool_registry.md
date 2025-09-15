# Tool Registry

## search

- **Capability:** Execute web or knowledge-base searches  
  for fresh data
- **Expected Latency:** 1-3 seconds with a warm cache
- **Safety Considerations:** Respect rate limits and redact sensitive queries
  before logging

## create_image

- **Capability:** Produce images from prompts using the configured diffusion
  API
- **Expected Latency:** 5-15 seconds, slower for large sizes
- **Safety Considerations:** Filter disallowed prompts and avoid persisting
  temporary URLs

## analyze

- **Capability:** Generate structured analysis over text, code, or documents
- **Expected Latency:** 2-6 seconds for standard depth, longer for deep dives
- **Safety Considerations:** Sanitize file paths and redact findings that
  expose secrets
