# 🛠️ Tools Wiring — Codex-Atlas

## Playwright MCP Server — Your Eyes

This MCP server is how we debug and validate anything in the browser. Always spin it up through the bridge so you inherit my logged-in Chrome profile.

### Hard Rules

- Launch with `mcp__playwright__` and pass `--browser chrome --extension`
- The bridge opens a fresh Chrome window on my Work profile; leave existing windows alone
- Never run Playwright headless here; screenshots and interactions must reflect my real environment
- Stay inside Playwright for visual checks, DOM scraping, screenshots, and interaction flows

### Launch Pattern

```
mcp__playwright__ tools --browser chrome --extension
```

That command routes through the bridge extension, attaches to the active Chrome profile, and boots a clean window. Every troubleshooting session starts with that exact incantation.

### Common Uses

- Smoke-test new builds against live auth sessions
- Capture screenshots or recordings to document regressions
- Inspect network calls or console errors in context
- Reproduce user flows while seeing the exact state I see

If the bridge fails, rebuild the session instead of falling back to headless mode. Headless runs break parity with my environment and are off-limits unless I sign off explicitly.
