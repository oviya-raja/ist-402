# Problem Definition: Built-in Tools Approach

## 📋 Assignment Objective

**Your group will automate specific workflows using OpenAI Agents to improve efficiency and reduce manual effort.**

## 🎯 This Approach: Built-in Tools Only

**Focus:** Use only OpenAI Agent Builder's built-in tools - no custom functions or API integration required.

---

## 💡 Recommended Workflows (Built-in Tools Only)

### Option 1: Student Query Response Agent ⭐ (Simplest)

**Workflow:** Automate FAQ responses using knowledge base

**Implementation:**
- Upload course materials, FAQs, documentation to knowledge base
- Enable **File Search** tool in Agent Builder
- Configure instructions for query handling
- Test with sample student questions

**Tools Needed:**
- ✅ File Search (built-in)
- ✅ Knowledge base (upload documents)

**API Integration:** ❌ None required

**Complexity:** ⭐ Low  
**Time:** 30-60 minutes

---

### Option 2: Document Summarization Agent ⭐⭐

**Workflow:** Automate document summarization

**Implementation:**
- Upload documents to knowledge base
- Enable **File Search + Code Interpreter** tools
- Configure instructions for summarization
- Test with various document types

**Tools Needed:**
- ✅ File Search (built-in)
- ✅ Code Interpreter (built-in)

**API Integration:** ❌ None required

**Complexity:** ⭐⭐ Low-Medium  
**Time:** 1-2 hours

---

### Option 3: Research Assistant Agent ⭐⭐

**Workflow:** Research and answer questions using web + knowledge base

**Implementation:**
- Upload reference materials to knowledge base
- Enable **Web Search + File Search** tools
- Configure instructions for research
- Test with research questions

**Tools Needed:**
- ✅ Web Search (built-in)
- ✅ File Search (built-in)

**API Integration:** ❌ None required

**Complexity:** ⭐⭐ Low-Medium  
**Time:** 1-2 hours

---

## 🛠️ Available Built-in Tools

### 1. File Search ✅
- Searches knowledge base (vector store)
- Semantic search across documents
- No coding required

### 2. Code Interpreter ✅
- Executes Python code
- Processes data and files
- No coding required

### 3. Web Search ✅
- Searches internet for information
- Accesses current web content
- No coding required

### 4. Computer Use ✅
- Browser automation
- Website interaction
- No coding required

**All tools are cloud-based and work entirely in Agent Builder UI!**

---

## 📊 Alignment with Rubric

### 1. Functional OpenAI Agent (20 pts)
- ✅ Agent fully functional using built-in tools
- ✅ Proper prompt engineering
- ✅ Appropriate tools enabled
- ✅ Handles edge cases
- ✅ Evidence of testing

### 2. Documented Workflows (20 pts)
- ✅ Step-by-step workflow documentation
- ✅ Workflow diagrams
- ✅ Integration points (built-in tools)
- ✅ Error handling strategies

### 3. GitHub Repository (20 pts) - Optional
- ✅ Documentation only
- ✅ README with setup instructions
- ✅ Team details

### 4. Screenshots (20 pts)
- ✅ Agent Builder configuration
- ✅ Tools setup
- ✅ Instructions
- ✅ Testing/execution
- ✅ Evidence of cloud deployment

### 5. Final PDF Report (20 pts)
- ✅ Project overview
- ✅ Workflow justification
- ✅ Implementation details
- ✅ Team roles
- ✅ Results and testing

---

## ✅ Implementation Checklist

- [ ] Select workflow (Student Query Response recommended)
- [ ] Create agent in Agent Builder UI
- [ ] Enable built-in tools (File Search, Code Interpreter, etc.)
- [ ] Upload knowledge base files (if applicable)
- [ ] Configure instructions in Agent Builder UI
- [ ] Test agent in Agent Builder chat interface
- [ ] Capture screenshots of setup
- [ ] Document workflow with step-by-step process
- [ ] Create workflow diagrams
- [ ] Document integration points (built-in tools)
- [ ] Prepare GitHub repository (optional)
- [ ] Create final PDF report

---

## 🚫 What This Approach Does NOT Include

- ❌ Custom function calling
- ❌ External API integration
- ❌ Local function deployment
- ❌ Complex web scraping
- ❌ Backend development

**If you need these, see:** `../FUNCTION_CALLING_GUIDE.md` (advanced approach)

---

## ✅ Why This Approach?

1. **Simplest** - No coding required
2. **Fastest** - 30 minutes to 2 hours
3. **Cloud-based** - No local setup
4. **Meets requirements** - Full rubric compliance
5. **Easy to document** - Simple workflows

---

**Status:** ✅ Focused on built-in tools only - Start here!

