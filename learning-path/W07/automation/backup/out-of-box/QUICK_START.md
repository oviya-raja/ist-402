# Quick Start: Built-in Tools Only

## 🎯 Goal

Build an AI agent using **only built-in tools** in OpenAI Agent Builder UI - no coding required!

## ✅ Recommended: Student Query Response Agent

**Why:**
- ✅ Simplest to implement (30-60 minutes)
- ✅ Uses File Search tool only
- ✅ No API integration needed
- ✅ Entirely in Agent Builder UI
- ✅ Meets all assignment requirements

---

## 🚀 Step-by-Step (30-60 minutes)

### Step 1: Prepare Knowledge Base (5 min)

1. **Collect documents:**
   - Course materials
   - FAQ documents
   - Student handbook
   - Any relevant docs

2. **Format:** PDF, TXT, or DOCX files

---

### Step 2: Create Agent (10 min)

1. **Go to:** https://platform.openai.com/agent-builder
2. **Click:** "Create Assistant"
3. **Configure:**
   - **Name:** "Student Query Response Agent"
   - **Model:** gpt-4o
   - **Description:** "Answers student questions using knowledge base"

4. **Set Instructions:**
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

### Step 3: Enable File Search Tool (5 min)

1. **Go to:** Tools section
2. **Enable:** "File Search" tool
3. **That's it!** No other tools needed for basic Q&A

---

### Step 4: Upload Knowledge Base (10 min)

1. **Go to:** Knowledge section
2. **Create Vector Store:** "Student Knowledge Base"
3. **Upload Files:** Your prepared documents
4. **Wait:** For processing to complete
5. **Verify:** Files are attached to assistant

---

### Step 5: Test Agent (10 min)

1. **Go to:** Test Chat
2. **Ask questions:**
   - "What are the course requirements?"
   - "How do I submit assignments?"
   - "What is the grading policy?"
3. **Verify:** Agent answers from knowledge base

---

### Step 6: Capture Screenshots (10 min)

**Required (5-6 screenshots):**
1. ✅ Agent configuration page
2. ✅ Tools section (File Search enabled)
3. ✅ Knowledge base (uploaded files)
4. ✅ Instructions/system prompt
5. ✅ Test chat (questions and answers)
6. ✅ Agent working (evidence of cloud deployment)

**Note:** Agent Builder is cloud-based - screenshots showing agent working = deployment evidence

---

### Step 7: Document Workflow (30 min)

1. **Workflow Steps:**
   - Student asks question
   - Agent searches knowledge base (File Search)
   - Agent retrieves information
   - Agent generates answer
   - Student receives answer

2. **Create Diagram:**
   - Simple flowchart
   - Use draw.io, Lucidchart, or Mermaid

3. **Document Integration:**
   - File Search tool (built-in)
   - Knowledge base (vector store)
   - No external APIs

---

## 📋 Deliverables Checklist

### 1. Functional Agent (20 pts)
- [ ] Agent works in Agent Builder UI
- [ ] File Search tool enabled
- [ ] Knowledge base uploaded
- [ ] Tested with sample questions
- [ ] Handles edge cases

### 2. Documented Workflows (20 pts)
- [ ] Step-by-step workflow documented
- [ ] Workflow diagram created
- [ ] Integration points documented (File Search)
- [ ] Error handling documented

### 3. GitHub Repository (20 pts) - Optional
- [ ] README with setup instructions
- [ ] Team details
- [ ] Documentation only (no code needed)

### 4. Screenshots (20 pts)
- [ ] Agent configuration
- [ ] Tools setup
- [ ] Instructions
- [ ] Knowledge base
- [ ] Testing/execution
- [ ] Deployment evidence

### 5. Final PDF Report (20 pts)
- [ ] Project overview
- [ ] Workflow justification
- [ ] Implementation details
- [ ] Team roles
- [ ] Results and testing
- [ ] Screenshots embedded

---

## 🎯 Alternative Workflows

### Option 2: Document Summarization

**Tools:** File Search + Code Interpreter  
**Time:** 1-2 hours

1. Upload documents
2. Enable File Search + Code Interpreter
3. Configure summarization instructions
4. Test

---

### Option 3: Research Assistant

**Tools:** Web Search + File Search  
**Time:** 1-2 hours

1. Upload reference materials
2. Enable Web Search + File Search
3. Configure research instructions
4. Test

---

## ✅ Success Criteria

Your agent is successful if:
- ✅ Works in Agent Builder UI
- ✅ Uses built-in tools only
- ✅ Answers questions accurately
- ✅ Well documented
- ✅ Screenshots captured

---

## 💡 Tips

1. **Start simple** - Use File Search only first
2. **Test thoroughly** - Try various questions
3. **Document everything** - Screenshots and workflow
4. **Keep it simple** - Built-in tools are powerful!

---

**Time Estimate:** 30-60 minutes setup + 1-2 hours documentation

**Status:** ✅ Ready to implement - No coding required!

