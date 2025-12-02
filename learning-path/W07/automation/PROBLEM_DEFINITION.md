# Problem Definition: W07 Assignment

## 📋 Assignment Objective

**Your group will automate specific workflows using OpenAI Agents to improve efficiency and reduce manual effort.**

## 📝 Instructions

Develop and deploy an AI agent using **OpenAI Agent Builder tools** that integrates with selected APIs and services to perform defined tasks.

## 🎯 Project Goals

1. Identify workflows suitable for automation
2. Build and deploy an OpenAI agent using Agent Builder
3. Integrate external data sources and APIs
4. Ensure collaborative development using version control
5. Document and present the setup and implementation

## 📦 Required Deliverables

1. **Functional OpenAI Agent** with defined capabilities
2. **Documented workflows** and integration points
3. **GitHub repository** with code, README, and contributor details (Optional)
4. **Screenshots** of OpenAI Agent Builder setup (local/cloud)
5. **Final report** with project details in PDF

## 💡 Example Workflows

The assignment provides these examples:

1. **Automating student query responses using a knowledge base**
   - Use File Search tool in Agent Builder
   - Upload knowledge base documents
   - Agent answers questions from knowledge base

2. **Scheduling meetings using calendar API**
   - Use Function Calling in Agent Builder
   - Integrate with Google Calendar API or similar
   - Agent can schedule/check availability

3. **Summarizing emails or documents**
   - Use File Search + Code Interpreter tools
   - Upload documents or connect email API
   - Agent generates summaries

## 🎯 Recommended Approach

### Strategy: Use Agent Builder UI + Built-in Tools

**Key Principles:**
- ✅ **Primary focus:** Agent Builder UI (not complex SDK development)
- ✅ **Use built-in tools:** File Search, Code Interpreter, Web Search
- ✅ **Simple API integration:** Only if needed (Calendar, Email APIs)
- ✅ **Knowledge base approach:** Upload documents, use File Search

## 📋 Workflow Options

### Option 1: Student Query Response Agent (Simplest) ⭐

**Workflow:** Automate FAQ responses using knowledge base

**Implementation:**
- Upload course materials, FAQs, documentation to knowledge base
- Enable File Search tool in Agent Builder
- Configure instructions for query handling
- Test with sample student questions

**Tools Needed:**
- File Search (built-in)
- Knowledge base (upload documents)

**API Integration:** None required

**Complexity:** Low

---

### Option 2: Document Summarization Agent ⭐⭐

**Workflow:** Automate document summarization

**Implementation:**
- Upload documents to knowledge base
- Enable File Search + Code Interpreter tools
- Configure instructions for summarization
- Test with various document types

**Tools Needed:**
- File Search (built-in)
- Code Interpreter (built-in)

**API Integration:** Optional

**Complexity:** Low-Medium

---

### Option 3: Calendar Meeting Scheduler Agent ⭐⭐⭐

**Workflow:** Schedule meetings using calendar API

**Implementation:**
- Enable Function Calling in Agent Builder
- Define function schema for calendar operations
- Implement external function (Google Calendar API)
- Configure agent instructions

**Tools Needed:**
- Function Calling (built-in)
- External API: Google Calendar API

**API Integration:** Required

**Complexity:** Medium

---

## 🛠️ Implementation Strategy

### Phase 1: Agent Builder UI Setup

1. Create assistant in Agent Builder UI
2. Configure instructions/system prompt
3. Enable built-in tools (File Search, Code Interpreter, Web Search)
4. Upload knowledge base files (if applicable)
5. Test in Agent Builder chat interface
6. Capture screenshots

### Phase 2: API Integration (If Needed)

1. Define function schema in Agent Builder UI
2. Implement external function (simple API wrapper)
3. Deploy as webhook (if required)
4. Connect function to assistant
5. Test function calls

### Phase 3: Documentation

1. Document workflows with diagrams
2. Document integration points
3. Capture screenshots
4. Test all capabilities
5. Prepare final report

## 📊 Alignment with Rubric

### 1. Functional OpenAI Agent (20 pts)
- Agent is fully functional
- Demonstrates intelligent decision-making
- Proper prompt engineering and context handling
- Appropriate tools and integrations
- Handles edge cases and errors gracefully
- Clear documentation of capabilities
- Evidence of thorough testing

### 2. Documented Workflows (20 pts)
- Comprehensive workflow documentation
- Clear step-by-step automation processes
- Detailed diagrams (triggers, actions, data flow, decision points)
- Integration points documented (APIs, data sources, authentication)
- Error handling strategies documented
- Workflow optimization notes

### 3. GitHub Repository (20 pts) - Optional
- Well-organized structure
- Meaningful commits
- Comprehensive README (project overview, setup, usage, API docs, team details)
- Professional markdown formatting
- Proper .gitignore file

### 4. Screenshots (20 pts)
- Agent Builder configuration
- Tools/functions setup
- Prompt instructions
- Memory settings
- Testing/execution
- Evidence of deployment

### 5. Final PDF Report (20 pts)
- Project overview and objectives
- Workflow identification and justification
- Implementation details with technical specifications
- Team roles and responsibilities
- Challenges faced and solutions
- Results and testing outcomes
- Future improvements
- All required screenshots embedded and labeled

## ✅ Implementation Checklist

- [ ] Select workflow from examples
- [ ] Create agent in Agent Builder UI
- [ ] Enable built-in tools (File Search, Code Interpreter, etc.)
- [ ] Upload knowledge base files (if applicable)
- [ ] Configure instructions in Agent Builder UI
- [ ] Test agent in Agent Builder chat interface
- [ ] Capture screenshots of setup
- [ ] Document workflow with step-by-step process
- [ ] Create workflow diagrams
- [ ] Document integration points
- [ ] Prepare GitHub repository (if applicable)
- [ ] Create final PDF report

## 🚫 What to Avoid

- ❌ Complex web scraping (Playwright automation)
- ❌ Heavy backend development
- ❌ Complex multi-service orchestration
- ❌ Workflows requiring extensive custom code

**Focus on:**
- ✅ Simple workflows using Agent Builder UI
- ✅ Built-in tools (File Search, Code Interpreter, etc.)
- ✅ Simple API integration (if needed)
- ✅ Knowledge base approach (upload documents)

---

**Status:** ✅ Aligned with assignment requirements

