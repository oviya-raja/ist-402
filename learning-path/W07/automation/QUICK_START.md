# Quick Start Guide: W07 Assignment

## 🎯 Assignment Goal

Build and deploy an AI agent using **OpenAI Agent Builder UI** that automates a simple workflow.

## ✅ Recommended Workflow: Student Query Response Agent

**Why this workflow:**
- ✅ Simplest to implement
- ✅ Uses built-in tools only
- ✅ No API integration required
- ✅ Easy to document and demonstrate
- ✅ Aligns with assignment examples

---

## 🚀 Step-by-Step Implementation

### Step 1: Prepare Knowledge Base (5 minutes)

1. **Collect documents:**
   - Course materials
   - FAQ documents
   - Student handbook
   - Any relevant documentation

2. **Format:**
   - PDF, TXT, or DOCX files
   - Organize by topic if possible

---

### Step 2: Create Agent in Agent Builder UI (10 minutes)

1. **Go to Agent Builder:**
   - Navigate to https://platform.openai.com/agent-builder
   - Click "Create Assistant"

2. **Configure Basic Settings:**
   - **Name:** "Student Query Response Agent"
   - **Model:** gpt-4o (or gpt-4-turbo)
   - **Description:** "Answers student questions using knowledge base"

3. **Set Instructions:**
   ```
   You are a helpful assistant that answers student questions using the provided knowledge base.
   
   Guidelines:
   - Answer questions based on information in the knowledge base
   - If information is not in the knowledge base, say so clearly
   - Provide clear, concise answers
   - Cite sources when possible
   - Be friendly and professional
   ```

---

### Step 3: Enable Built-in Tools (5 minutes)

1. **Go to Tools section:**
   - Click "Tools" or "Capabilities" tab

2. **Enable File Search:**
   - ✅ Enable "File Search" tool
   - This allows agent to search your knowledge base

3. **Enable Code Interpreter (Optional):**
   - ✅ Enable "Code Interpreter" if you need data processing
   - Not required for basic Q&A

4. **Enable Web Search (Optional):**
   - ✅ Enable "Web Search" if you want agent to search web for additional info
   - Not required for knowledge base only

---

### Step 4: Upload Knowledge Base (10 minutes)

1. **Go to Knowledge section:**
   - Click "Knowledge" or "Files" tab

2. **Create Vector Store:**
   - Click "Create Vector Store" or "Add Files"
   - Name it: "Student Knowledge Base"

3. **Upload Files:**
   - Upload your prepared documents
   - Wait for processing to complete
   - Verify all files are processed

4. **Attach to Assistant:**
   - Ensure vector store is attached to your assistant
   - Should see it in "Knowledge" section

---

### Step 5: Test Agent (10 minutes)

1. **Go to Test Chat:**
   - Click "Test" or "Chat" tab in Agent Builder

2. **Test Questions:**
   - "What are the course requirements?"
   - "How do I submit assignments?"
   - "What is the grading policy?"
   - "When are office hours?"

3. **Verify:**
   - ✅ Agent answers from knowledge base
   - ✅ Answers are accurate
   - ✅ Agent cites sources (if configured)

---

### Step 6: Capture Screenshots (10 minutes)

**Required Screenshots (for Rubric):**
1. ✅ **Agent configuration page** - Shows agent name, model, description
2. ✅ **Tools/Capabilities section** - Shows File Search enabled (and other tools)
3. ✅ **Knowledge base/Vector store** - Shows uploaded files and vector store
4. ✅ **Instructions/System prompt** - Shows your configured instructions
5. ✅ **Testing/execution** - Shows test chat with sample questions and answers
6. ✅ **Evidence of deployment** - Shows agent is active and accessible (this is automatic with Agent Builder - it's cloud-based)

**Note about "local/cloud" requirement:**
- **Agent Builder is cloud-based** - It's accessed at platform.openai.com
- Your agent is automatically "deployed" in the cloud when you create it
- Screenshots showing the agent working in Agent Builder UI = evidence of cloud deployment
- If you use external functions (APIs), those might be local or cloud - document where they're hosted

---

### Step 7: Document Workflow (30 minutes)

**Create workflow documentation:**

1. **Workflow Steps:**
   - Trigger: Student asks question
   - Action: Agent searches knowledge base
   - Action: Agent retrieves relevant information
   - Action: Agent generates answer
   - End: Student receives answer

2. **Create Diagram:**
   - Simple flowchart showing workflow
   - Use tools like draw.io, Lucidchart, or Mermaid

3. **Document Integration Points:**
   - Knowledge base (File Search tool)
   - Vector store (OpenAI managed)
   - No external APIs required

---

## 📋 Deliverables Checklist (Aligned with Rubric)

### 1. Functional OpenAI Agent (20 pts)
- [ ] ✅ Agent fully functional in Agent Builder UI
- [ ] ✅ Demonstrates intelligent decision-making
- [ ] ✅ Proper prompt engineering (instructions configured)
- [ ] ✅ Appropriate tools enabled (File Search, etc.)
- [ ] ✅ Handles edge cases (test with various questions)
- [ ] ✅ Clear documentation of capabilities
- [ ] ✅ Evidence of thorough testing (test results documented)

### 2. Documented Workflows (20 pts)
- [ ] ✅ Step-by-step workflow documentation
- [ ] ✅ Workflow diagram (triggers, actions, data flow)
- [ ] ✅ Integration points documented (File Search tool, knowledge base)
- [ ] ✅ Error handling strategies documented
- [ ] ✅ Workflow optimization notes

### 3. GitHub Repository (20 pts) - Optional
- [ ] ✅ Well-organized structure
- [ ] ✅ Comprehensive README (project overview, setup, usage, team details)
- [ ] ✅ Meaningful commits
- [ ] ✅ Professional markdown formatting
- [ ] ✅ Proper .gitignore file

### 4. Screenshots (20 pts)
- [ ] ✅ Agent Builder configuration page
- [ ] ✅ Tools/functions setup (showing File Search enabled)
- [ ] ✅ Prompt instructions/system prompt
- [ ] ✅ Knowledge base/vector store (showing uploaded files)
- [ ] ✅ Testing/execution (test chat with questions and answers)
- [ ] ✅ Evidence of deployment (Agent Builder is cloud-based - screenshots showing agent working = deployment evidence)

### 5. Final PDF Report (20 pts)
- [ ] ✅ Project overview and objectives
- [ ] ✅ Workflow identification and justification
- [ ] ✅ Implementation details with technical specifications
- [ ] ✅ Team roles and responsibilities
- [ ] ✅ Challenges faced and solutions
- [ ] ✅ Results and testing outcomes
- [ ] ✅ Future improvements
- [ ] ✅ All required screenshots embedded and labeled

---

## 🎯 Alternative Workflows (If Needed)

### Option 2: Document Summarization Agent

**Setup:**
1. Upload documents to knowledge base
2. Enable File Search + Code Interpreter
3. Configure instructions for summarization
4. Test with sample documents

**Tools:**
- File Search (built-in)
- Code Interpreter (built-in)

**Complexity:** ⭐⭐ Low-Medium

---

### Option 3: Calendar Meeting Scheduler

**Setup:**
1. Enable Function Calling in Agent Builder
2. Define function schema for calendar operations
3. Implement Google Calendar API wrapper
4. Connect function to assistant

**Tools:**
- Function Calling (built-in)
- External API: Google Calendar API

**Complexity:** ⭐⭐⭐ Medium

---

## 💡 Tips for Success

1. **Start Simple:**
   - Use Student Query Response Agent
   - No API integration needed
   - Can be done entirely in UI

2. **Use Built-in Tools:**
   - File Search for knowledge base
   - Code Interpreter for processing
   - Avoid custom functions if possible

3. **Document Everything:**
   - Take screenshots at each step
   - Document workflow clearly
   - Include test results

4. **Test Thoroughly:**
   - Test with various questions
   - Verify accuracy
   - Check error handling

---

## 🚫 Common Mistakes to Avoid

1. ❌ **Overcomplicating:**
   - Don't build complex web scraping
   - Don't create extensive backend code
   - Keep it simple!

2. ❌ **Ignoring Built-in Tools:**
   - Use File Search instead of custom functions
   - Use Code Interpreter for data processing
   - Leverage what's already available

3. ❌ **Skipping Documentation:**
   - Screenshots are required (20 pts)
   - Workflow documentation is required (20 pts)
   - Don't skip these!

4. ❌ **Not Testing:**
   - Test thoroughly before submission
   - Document test results
   - Show evidence of functionality

---

## 📚 Resources

- **Agent Builder UI:** https://platform.openai.com/agent-builder
- **Built-in Tools Guide:** `BUILT_IN_TOOLS.md`
- **Problem Definition:** `PROBLEM_DEFINITION.md`

---

## ✅ Success Criteria

Your agent is successful if:
- ✅ Works in Agent Builder UI
- ✅ Answers questions from knowledge base
- ✅ Handles edge cases gracefully
- ✅ Well documented with screenshots
- ✅ Workflow clearly explained

---

**Time Estimate:** 2-3 hours total
- Setup: 30 minutes
- Testing: 30 minutes
- Documentation: 1-2 hours

**Status:** ✅ **Ready to implement!**

