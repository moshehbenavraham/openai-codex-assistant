# PAI (Personal AI Infrastructure) Implementation Plan

## Overview
This document outlines the comprehensive plan to integrate features from the sample_claude_code_pai PAI project into the codex-assistant project, supporting both Claude Code and OpenAI Codex as interchangeable assistant platforms.

## Core Objectives
- Transform codex-assistant into a full Personal AI Infrastructure (PAI) system
- Implement UFC (Universal File System Context) architecture
- Support both Claude Code and OpenAI Codex as assistant platforms
- Create platform abstraction layer for seamless switching between AI providers
- Enable dynamic context loading based on user intent
- Set up specialized agents for different tasks
- Implement voice interaction capabilities
- Create a seamless, context-aware AI assistant experience

## Phase 0: Prerequisites & Assessment (Week 1)

### 0.1 Current State Audit
- [ ] Document existing OpenAI Codex integration
- [ ] Inventory current PAI tools and functionality
- [ ] Backup existing configuration:
  ```bash
  tar -czf pai-backup-$(date +%Y%m%d).tar.gz pai/ .env scripts/
  ```
- [ ] Test existing OpenAI Codex functionality:
  ```bash
  CODEX_BIN=codex ./pai/pai.sh chat "test connection"
  ```

### 0.2 Platform Compatibility Assessment
- [ ] Compare Claude Code vs OpenAI Codex capabilities
- [ ] Identify common API patterns
- [ ] Document platform-specific features
- [ ] Create compatibility matrix

### 0.3 Dependencies Installation
- [ ] Install Bun runtime:
  ```bash
  curl -fsSL https://bun.sh/install | bash
  ```
- [ ] Verify Claude Code CLI:
  ```bash
  claude --version  # If installed
  ```
- [ ] Verify OpenAI Codex CLI:
  ```bash
  codex --version
  command -v codex  # ensure CLI is on PATH without relying on npm
  ```

## Phase 1: Foundation Setup (Week 1-2)

### 1.1 Platform Abstraction Layer
- [ ] Create platform detection mechanism:
  ```bash
  # .claude/platform-config.sh
  export AI_PLATFORM="${AI_PLATFORM:-claude}"  # or "codex"
  ```
- [ ] Implement platform router in `pai/platform-router.ts`
- [ ] Create unified interface for both platforms

### 1.2 UFC Directory Structure Creation
- [ ] Enhance existing `.claude/` directory
- [ ] Set up core context directories:
  ```
  .claude/
  |-- context/
  |   |-- projects/       # Active work and initiatives
  |   |-- tools/          # AI agents and capabilities
  |   |-- finances/       # Financial tracking
  |   |-- health/         # Wellness data
  |   |-- telos/          # Goals and objectives
  |   |-- learnings/      # Captured problem/solution pairs
  |   |-- documentation/  # System docs
  |-- commands/           # Executable markdown commands
  |-- hooks/              # Event-driven scripts
  |-- settings.json       # Platform configuration (Claude/Codex)
  ```

### 1.3 Base Context Files
- [ ] Create platform-agnostic context `.claude/context/BASE.md`
- [ ] Create Claude-specific `.claude/context/CLAUDE.md` with:
  - Claude Code specific configurations
  - MCP server settings
  - Claude-specific tool patterns
- [ ] Create Codex-specific `.claude/context/CODEX.md` with:
  - OpenAI Codex configurations
  - Codex tool mappings
  - Codex-specific patterns
- [ ] Both should include:
  - Assistant identity configuration (persona)
  - UFC system documentation
  - Global preferences and rules
  - Security protocols
  - Response structure guidelines

### 1.4 Dual Platform Configuration
- [ ] Configure `.claude/settings.json` for Claude Code:
  ```json
  {
    "platform": "claude",
    "fallback": "codex"
  }
  ```
- [ ] Configure `pai/config.json` for OpenAI Codex:
  ```json
  {
    "platform": "codex",
    "fallback": "claude"
  }
  ```
- [ ] Both configurations should include:
  - Environment variables
  - Permissions (allow/deny patterns)
  - MCP server configurations
  - Hook definitions
  - Status line setup

## Phase 2: Dynamic Context Loading (Week 1-2)

### 2.1 Hook System Implementation
- [ ] Create platform-aware hooks:
  - `.claude/hooks/load-dynamic-requirements.ts` (for Claude)
  - `pai/hooks/load-dynamic-requirements.ts` (for Codex; executed with Bun)
- [ ] Implement `UserPromptSubmit` hook for both:
  - Semantic intent parsing
  - Context file selection logic
  - Agent activation rules

### 2.2 Unified Command System
- [ ] Create platform wrapper in `commands/platform-wrapper.md`:
  ```ts
  #!/usr/bin/env bun
  /** Routes command invocations to the active AI platform. */
  const [, , ...args] = process.argv;
  const platform = process.env.AI_PLATFORM ?? "claude";
  const binary = platform === "claude" ? "claude-code" : "codex";

  const proc = Bun.spawn({
    cmd: [binary, ...args],
    stdin: "inherit",
    stdout: "inherit",
    stderr: "inherit",
  });

  process.exit(await proc.exited);
  ```
- [ ] Port `commands/load-dynamic-requirements.md`:
  - Context loading rules by domain
  - Agent selection criteria
  - Special instructions per context

### 2.3 Context Categories
- [ ] Implement context loading for:
  - Website/Blog operations
  - Research & information gathering
  - Security/Pentesting tasks
  - Consulting/Advisory work
  - Financial analytics
  - Development projects
  - Learning capture
  - Conversational modes

## Phase 3: Agent System (Week 2)

### 3.1 Core Agents Creation
- [ ] Researcher Agent:
  - Web research capabilities
  - Information synthesis
  - Current events tracking

- [ ] Engineer Agent:
  - Production code development
  - Testing integration
  - Debugging workflows

- [ ] Designer Agent:
  - UI/UX development
  - Visual testing with Playwright
  - Browser automation

- [ ] Pentester Agent:
  - Security assessments
  - Vulnerability scanning
  - Network reconnaissance

- [ ] Architect Agent:
  - System design
  - Technical specifications
  - Architecture documentation

### 3.2 Agent Integration
- [ ] Update `AGENTS.md` with:
  - Agent descriptions
  - Voice IDs for TTS
  - Specialization areas
  - Invocation patterns

## Phase 4: Platform-Specific Integrations (Week 3-4)

### 4.1 Claude Code - MCP Servers
- [ ] Configure in `.claude/.mcp.json`:
  - Playwright (browser automation)
  - Stripe (payments)
  - Apify (web scraping)
  - Custom API servers
  - Follow Playwright MCP setup from `~/.claude/context/tools/CLAUDE.md`

### 4.2 Claude Code - Custom MCP Endpoints
- [ ] Implement custom servers for:
  - Personal API integration
  - Content management
  - Port scanning tools
  - HTTP analysis

### 4.3 OpenAI Codex - Tool Integration
- [ ] Map existing PAI tools to Codex:
  - search tool
  - analyze tool
  - memory management
  - create_image tool
- [ ] Create tool compatibility layer
- [ ] Implement fallback mechanisms

## Phase 5: Voice System (Week 4)

### 5.1 Voice Hooks
- [ ] Implement voice interaction hooks:
  - SessionStart hook
  - Stop hook
  - SubagentStop hook
  - Context compression hook

### 5.2 TTS/STT Configuration
- [ ] Set up voice system:
  - Voice ID mappings per agent
  - Speech optimization rules
  - Pronunciation hints
  - Natural flow patterns
  - Reference `~/.claude/context/documentation/voicesystem/CLAUDE.md`

## Phase 6: Command Creation (Week 4-5)

### 6.1 Core Commands
- [ ] Create executable markdown commands:
  - `capture-learning.md` - Problem/solution logging
  - `web-research.md` - Deep research workflows
  - `answer-finance-question.md` - Financial analysis
  - `session-summary.md` - Context summarization

### 6.2 Command Structure
- [ ] Follow unified format:
  - Single `.md` file with embedded TypeScript
  - `#!/usr/bin/env bun` shebang
  - Documentation + code in one file
  - Proper permissions and execution

## Phase 7: Integration with Existing PAI (Week 5)

### 7.1 PAI Tools Migration
- [ ] Integrate existing PAI tools:
  - `analyze.md` functionality
  - `search.md` capabilities
  - `create_image.md` integration
  - Memory management from `memory.md`

### 7.2 Context Merging
- [ ] Merge `pai/context.md` with UFC:
  - Preserve existing context
  - Map to UFC structure
  - Maintain compatibility

## Phase 8: Testing & Refinement (Week 5-6)

### 8.1 Platform Switching Tests
- [ ] Test platform detection:
  ```bash
  AI_PLATFORM=claude ./pai/pai.sh chat "test"
  AI_PLATFORM=codex ./pai/pai.sh chat "test"
  ```
- [ ] Test fallback mechanisms
- [ ] Verify context loading for both platforms

### 8.2 Component Testing
- [ ] Test each component:
  - Context loading accuracy
  - Agent invocation
  - Hook execution
  - Command functionality
  - Voice interaction

### 8.3 Integration Testing
- [ ] End-to-end workflows:
  - Research -> Documentation flow
  - Code development cycle
  - Financial analysis pipeline
  - Learning capture process

### 8.4 Performance Optimization
- [ ] Optimize for:
  - Token usage efficiency
  - Context switching speed
  - Response generation time
  - Memory management

## Phase 9: Documentation (Week 6-7)

### 9.1 User Documentation
- [ ] Platform selection guide
- [ ] Feature comparison matrix
- [ ] Create comprehensive docs:
  - Getting started guide
  - Command reference
  - Agent capabilities
  - Context structure guide
  - Troubleshooting

### 9.2 Developer Documentation
- [ ] Technical documentation:
  - Architecture overview
  - Hook system details
  - MCP server setup
  - Extension guidelines
  - API reference

## Phase 10: Deployment (Week 7-8)

### 10.1 Local Deployment
- [ ] Update `deployment_local.md`:
  - Dual platform setup (Claude Code + OpenAI Codex)
  - Platform switching instructions
  - Dependencies installation
  - Configuration steps
  - Testing procedures

### 10.2 Production Readiness
- [ ] Ensure production ready:
  - Security audit
  - Performance benchmarks
  - Error handling
  - Logging system
  - Backup procedures

## Key Implementation Notes

### Security Priorities
- NEVER commit sensitive data to public repos
- Always verify repository context before commits
- Protect API keys and credentials
- Implement proper permission boundaries

### Technical Standards
- Use TypeScript for all new code
- Prefer Bun over npm/yarn
- Single-file markdown commands
- Follow existing code conventions
- Implement proper error handling

### Platform Integration Strategy
- Support both Claude Code and OpenAI Codex
- Platform abstraction layer for seamless switching
- Codex-Assistant persona works with both platforms
- UFC for context management
- Hooks for event handling
- MCP for tool integration

## Success Metrics
- [ ] Context loads dynamically based on intent
- [ ] Agents activate appropriately
- [ ] Voice interaction works seamlessly
- [ ] Commands execute reliably
- [ ] System maintains context between sessions
- [ ] Performance meets responsiveness targets
- [ ] Security protocols enforced consistently

## Timeline Summary
- **Week 1**: Prerequisites and assessment
- **Week 2**: Foundation and platform abstraction
- **Week 3**: Dynamic loading and agents
- **Week 4**: Platform-specific integrations
- **Week 5**: Voice and commands
- **Week 6**: Testing and PAI integration
- **Week 7**: Documentation
- **Week 8**: Final deployment and refinement

## Next Steps
1. Complete Phase 0 prerequisites and assessment
2. Set up platform abstraction layer
3. Create dual-platform context files (BASE.md, CLAUDE.md, CODEX.md)
4. Implement platform detection and routing
5. Test both Claude Code and OpenAI Codex independently
6. Implement unified command wrapper
7. Gradually add agents and capabilities
8. Iterate based on usage patterns

## Validation Checklist
- [ ] Both platforms can be invoked independently
- [ ] Platform switching works via environment variable
- [ ] Context loads correctly for each platform
- [ ] Commands execute on both platforms
- [ ] Fallback mechanism activates when primary fails
- [ ] Voice system works with both platforms
- [ ] All existing PAI tools remain functional

---

## Troubleshooting Guide

### Common Issues
- **Platform detection fails**: Check `AI_PLATFORM` environment variable
- **Claude Code not found**: Ensure Claude Desktop app is installed
- **Codex command fails**: Verify `npm list -g @openai/codex`
- **Context not loading**: Check file permissions in `.claude/context/`
- **Hook execution errors**: Verify Bun/Python runtime versions

### Rollback Procedures
- Phase 1-2: Restore from `pai-backup-*.tar.gz`
- Phase 3+: Use git to revert changes
- Emergency: `git checkout main -- .`

---

*This implementation plan transforms codex-assistant into a comprehensive Personal AI Infrastructure supporting both Claude Code and OpenAI Codex, enabling intelligent context management, specialized agents, and seamless AI-assisted workflows with platform flexibility.*
