# Built-in Tools in OpenAI Agent Builder

## ✅ Available Built-in Tools

OpenAI Agent Builder provides several built-in tools you can use directly - no custom code required!

## 🛠️ Built-in Tools Overview

### 1. **File Search** ✅

**What it does:**
- Searches your knowledge base (vector store)
- Retrieves relevant information from uploaded files
- Semantic search across documents

**When to use:**
- Student query responses
- FAQ automation
- Document-based Q&A
- Knowledge base queries

**How to enable:**
- Go to Agent Builder → Your Assistant → Tools
- Enable "File Search"
- Upload files to knowledge base

**Example use case:**
- Upload course materials → Agent answers student questions

---

### 2. **Code Interpreter** ✅

**What it does:**
- Executes Python code
- Can read/write files
- Can process data
- Can perform calculations

**When to use:**
- CSV file reading and processing
- Data analysis
- Document processing
- Calculations

**How to enable:**
- Go to Agent Builder → Your Assistant → Tools
- Enable "Code Interpreter"

**Example use case:**
- Upload CSV file → Agent reads and processes data

---

### 3. **Web Search** ✅

**What it does:**
- Searches the internet for up-to-date information
- Accesses web content
- Returns search results

**When to use:**
- Finding current information
- Research tasks
- General web queries

**How to enable:**
- Go to Agent Builder → Your Assistant → Tools
- Enable "Web Search"

**Example use case:**
- Agent searches web for current information

---

### 4. **Computer Use** ✅

**What it does:**
- Controls computer interface
- Can interact with browsers
- Can navigate websites
- Can click, type, scroll

**When to use:**
- Browser automation
- Website interaction
- Form filling
- Web navigation

**How to enable:**
- Go to Agent Builder → Your Assistant → Tools
- Enable "Computer Use"

**Example use case:**
- Agent navigates websites and interacts with forms

---

## 🎯 Recommended Approach: Use Built-in Tools First!

### Strategy: Start Simple

**For Student Query Response Agent:**
1. ✅ Enable **File Search** tool
2. ✅ Upload knowledge base files
3. ✅ Configure instructions
4. ✅ Test

**No custom code needed!**

---

### Strategy: Add Tools as Needed

**For Document Summarization:**
1. ✅ Enable **File Search** (for documents)
2. ✅ Enable **Code Interpreter** (for processing)
3. ✅ Configure instructions
4. ✅ Test

**Still no custom code needed!**

---

## 📋 Decision Matrix

| Task | Built-in Tool | Custom Function | Recommendation |
|------|--------------|-----------------|----------------|
| Knowledge base Q&A | ✅ File Search | ❌ | **Use File Search** |
| CSV file reading | ✅ Code Interpreter | ⚠️ | **Use Code Interpreter** |
| Document summarization | ✅ File Search + Code Interpreter | ⚠️ | **Use built-in tools** |
| Web information | ✅ Web Search | ⚠️ | **Try Web Search first** |
| Calendar scheduling | ❌ | ✅ Function Calling | **Need custom function** |
| Email access | ❌ | ✅ Function Calling | **Need custom function** |

---

## ✅ Best Practices

1. **Start with built-in tools**
   - Try File Search, Code Interpreter, Web Search first
   - Only add custom functions if needed

2. **Keep it simple**
   - Use built-in tools for most tasks
   - Avoid complex custom implementations

3. **Test each tool**
   - Enable one tool at a time
   - Test functionality
   - Document results

---

## 🚀 Quick Setup

### For Student Query Response Agent:

1. **Enable File Search:**
   - Agent Builder → Tools → Enable "File Search"

2. **Upload Knowledge Base:**
   - Agent Builder → Knowledge → Upload files
   - Wait for processing

3. **Configure Instructions:**
   - Agent Builder → Instructions
   - Set system prompt

4. **Test:**
   - Agent Builder → Test Chat
   - Ask sample questions

**That's it! No coding required.**

---

## 💡 Tips

- ✅ **Use built-in tools first** - They're powerful and easy to use
- ✅ **Test thoroughly** - Make sure tools work as expected
- ✅ **Document tool usage** - Include in your workflow documentation
- ✅ **Only add custom functions if absolutely necessary**

---

**Status:** ✅ Ready to use built-in tools

