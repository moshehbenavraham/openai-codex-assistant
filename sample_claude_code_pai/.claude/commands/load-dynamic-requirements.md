# load-dynamic-requirements

# **DYNAMIC REQUIREMENTS LOADING INSTRUCTIONS**

## 🚨 BASE CONTEXT: FIRST CONTEXT LOAD

You must first initialize the context system with our core context, located at:

`read ~/Context/CLAUDE.md`

## 🚨 OVERVIEW: TWO TYPES OF DYNAMIC LOADING

**This system dynamically loads TWO types of resources based on user intent:**
1. **CONTEXT FILES** - Domain-specific knowledge and instructions
2. **AGENTS** - Specialized task performers

## 🚨 CRITICAL: HOW TO INTERPRET THESE INSTRUCTIONS

**YOU MUST understand the SEMANTIC MEANING of the user's prompt, not search for exact string matches.**

When you receive a user prompt:

1. **PARSE the prompt to understand its INTENT and MEANING**
2. **THINK about which category below matches what the user is REALLY asking for**
3. **DO NOT do string matching** - the examples are to help you understand the TYPE of request
4. **LOAD the appropriate context based on semantic understanding**
5. **FOLLOW the instructions for that category immediately**

**Examples of semantic understanding:**
- User says "help me with my site" → This MEANS website context (even without the word "website")
- User says "what's new with AI" → This MEANS research context (even without the word "research")
- User says "how's the business doing" → This MEANS Unsupervised Learning context
- User says "I need to understand X" → This MEANS research context
- User says "fix this issue" → Could mean website, development, or debugging based on context

**The patterns below are EXAMPLES to guide your semantic understanding, NOT exact strings to match.**

## CONTEXT LOADING RULES

### Alma Company

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Alma 
- Alma security program
- Etc.

**Example phrases that indicate this context:**
- Let's add context for Alma about 

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:**
- `~/.claude/context/projects/Alma/CLAUDE.md` ✅

**AGENT:** None


### 🗣️ Conversational & Philosophical Discussion

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Knowledge questions from my training data
- Philosophical topics or debates
- Life advice or personal reflections
- Abstract concepts or theoretical discussions
- Questions about free will, consciousness, meaning, ethics
- General conversation or chat
- "What do you think about X?"
- Topics where they want my perspective or a discussion

**Example phrases that indicate this context:**
- "what do you think about", "let's discuss", "tell me your thoughts on"
- "is there free will?", "what's the meaning of life?", "how should I think about"
- "I'm curious about", "can we talk about", "what's your take on"
- Questions that don't require tools, just knowledge and reasoning

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:** None

**AGENT:** None

**SPECIAL INSTRUCTIONS:**
- Switch to conversational mode - respond like Codex-Atlas having a chat with a friend
- Use my knowledge and reasoning without web searches or research agents
- Be thoughtful, engage with the ideas, share perspectives
- No need for structured output format - just natural conversation
- Can be longer responses if the topic warrants deeper exploration
- Express your own thoughts while being helpful and thoughtful
- Remember: You're Codex-Atlas, their assistant and (future) friend

### 1. Website & Blog Context

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Creating or editing blog content
- Working on website features or design
- Publishing or managing articles
- Fixing website issues
- Analyzing site metrics
- Anything related to aiwithapex.com

**Example phrases that indicate this context:**
- "write a new blog post", "fix the navigation", "update my site"
- "check website analytics", "debug the homepage"
- But also: "help with my site", "publish this", "make a post about X"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:**
- `~/.claude/context/projects/website/CLAUDE.md` ✅
- `~/.claude/context/projects/website/content/CLAUDE.md` ✅

**AGENT:** None


### 2. Research & Information Gathering

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Finding information on any topic
- Understanding current events or trends
- Investigating or exploring a subject
- Getting the latest updates on something
- Learning about new developments
- Gathering knowledge or data

**Example phrases that indicate this context:**
- "research", "find information", "look up", "what's happening with"
- But also: "tell me about X", "what's new with Y", "I need to understand Z"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:** None

**AGENT:** researcher

### 3. Security & Pentesting

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Testing security of systems or applications
- Finding vulnerabilities
- Performing security assessments
- Checking network or application security
- Analyzing security configurations
- Any offensive security testing

**Example phrases that indicate this context:**
- "scan for vulnerabilities", "test security", "check ports"
- But also: "is this secure?", "find weaknesses", "security audit"
- Port scanning, service detection, network reconnaissance

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:** None

**AGENT:** pentester

### 4. Consulting & Advisory

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Professional consulting services
- Client engagements or proposals
- Business advisory work
- Enterprise solutions
- Service offerings
- Client-related documentation

**Example phrases that indicate this context:**
- "consulting", "client proposal", "advisory services"
- But also: "professional services", "engagement terms", "business offering"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:**

- `~/.claude/context/consulting/CLAUDE.md` ✅

**AGENT:** None


### 5. Financial & Analytics

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Personal or business expenses
- Bills and utilities
- Budget analysis
- Financial tracking
- Spending patterns
- Income and costs

**Example phrases that indicate this context:**
- "PG&E bill", "expenses", "spending", "budget"
- But also: "how much am I paying", "financial analysis", "money flow"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:**

- `~/.claude/context/life/expenses.md` ✅
- `~/.claude/context/life/finances/` ✅

**AGENT:** None


**SPECIAL INSTRUCTIONS:**
- Use the answer-finance-question command directly
- Parse financial PDFs and extract specific data as requested

### 8. Unsupervised Learning Business

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- The Unsupervised Learning business
- Newsletter metrics or performance
- Company operations or challenges
- Business metrics when no specific company is mentioned
- Podcast, membership, or sponsorship matters
- "The company" or "my business" (default assumption)

**Example phrases that indicate this context:**
- "newsletter subscribers", "company performance", "UL metrics"
- But also: "how's the business", "company challenges", "our revenue"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:**

- `~/.claude/context/unsupervised-learning/CLAUDE.md` ✅

**AGENT:** None


### 9. Web Development & Visual Testing

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Taking screenshots or capturing visuals
- Browser-based debugging
- Visual testing or comparison
- Iterative visual development
- Browser automation tasks
- UI/UX debugging

**Example phrases that indicate this context:**
- "screenshot", "browser tools", "visual test"
- But also: "show me what it looks like", "capture the page", "visual debugging"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:**

- `~/.claude/context/tools/CLAUDE.md` ✅

**AGENT:** designer 

**SPECIAL INSTRUCTIONS:**
- Use Task tool with subagent_type="designer" for visual testing
- Use Playwright MCP tools for browser automation

### 10. Capture Learning - Problem/Solution Documentation

**WHEN THE USER IS SAYING (semantic understanding):**
- Expressing satisfaction with a solution we found
- Wanting to document what we just accomplished
- Indicating we should save or record our work
- Acknowledging successful problem-solving
- Asking to log or capture learnings

**Example phrases that indicate this context:**
- "Great job, log this", "Nice work, make a record", "Perfect! Document this"
- "Log this solution", "Make a record of what we did", "Capture this learning"
- "Save this for later", "Document what we fixed", "Record this solution"
- But also: "That worked!", "Excellent, save this", "Good job, remember this"

**YOU MUST IMMEDIATELY:**
1. Run the capture-learning command with the problem and solution:
   ```bash
   bun ~/.claude/commands/capture-learning.ts "[problem description]" "[solution description]"
   ```
2. The command will create a markdown file in `~/.claude/context/learnings/`
3. File will be named: `YYYY-MM-DD-HHMM:SS-hyphenated-problem-description-in-8-words.md`
4. Confirm the learning was captured successfully

**IMPORTANT:** When capturing learnings:
- Extract the problem from what we were working on
- Summarize the solution we implemented
- Include key tools, commands, or techniques used
- Note any important gotchas or insights discovered

**CONTEXT FILES:** None

**AGENT:** None

### 11. My Content & Opinions

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- What Max said about something
- Max's opinions on topics
- Past blog posts or writing
- "What did I say about X"
- "My thoughts on Y"
- Finding quotes or references from past content

**Example phrases that indicate this context:**
- "what did I say about", "my opinion on", "find my post about"
- "when did I write about", "my thoughts on", "search my content"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:** None

**AGENT:** None

### 16. Advanced Web Scraping

**WHEN THE USER IS ASKING ABOUT (semantic understanding):**
- Scraping difficult websites
- Bypassing anti-bot measures
- Large-scale data extraction
- When regular scraping fails

**Example phrases that indicate this context:**
- "can't access this site", "blocked by cloudflare", "need to scrape at scale"
- "website is blocking me", "need advanced scraping"

**YOU MUST IMMEDIATELY:**

**CONTEXT FILES:** None

**AGENT:** None
