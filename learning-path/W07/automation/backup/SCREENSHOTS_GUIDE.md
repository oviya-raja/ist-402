# Screenshots Guide: What to Capture

## 📸 Why Screenshots Are Required (20 pts)

Screenshots demonstrate that you've actually built and configured the agent in Agent Builder UI. They provide visual proof of your implementation.

## 🎯 Required Screenshots (Per Rubric)

The rubric requires screenshots showing:

1. ✅ **Agent configuration** - Basic settings, model selection
2. ✅ **Tools/functions** - Which tools are enabled
3. ✅ **Prompt instructions** - Your system prompt/instructions
4. ✅ **Memory settings** - If applicable
5. ✅ **Testing/execution** - Agent actually working
6. ✅ **Evidence of deployment** - Agent is accessible and working

## 📋 Specific Screenshots to Take

### 1. Agent Configuration Page
**What to capture:**
- Agent name
- Model selection (gpt-4o, gpt-4-turbo, etc.)
- Description
- Basic settings

**How to capture:**
- Go to Agent Builder → Your Assistant → Configuration
- Take screenshot showing all basic settings

---

### 2. Tools/Functions Setup
**What to capture:**
- File Search enabled (or other tools)
- Any custom functions defined
- Tool configuration

**How to capture:**
- Go to Agent Builder → Your Assistant → Tools
- Take screenshot showing enabled tools

---

### 3. Prompt Instructions/System Prompt
**What to capture:**
- Your configured instructions
- System prompt text
- Any specific guidelines

**How to capture:**
- Go to Agent Builder → Your Assistant → Instructions
- Take screenshot showing your instructions (you can scroll if long)

---

### 4. Knowledge Base/Vector Store
**What to capture:**
- Uploaded files
- Vector store name
- File processing status
- Number of files

**How to capture:**
- Go to Agent Builder → Your Assistant → Knowledge
- Take screenshot showing vector store and files

---

### 5. Testing/Execution
**What to capture:**
- Test chat interface
- Sample questions asked
- Agent responses
- Tool usage (if visible)

**How to capture:**
- Go to Agent Builder → Your Assistant → Test Chat
- Ask a few test questions
- Take screenshot showing conversation

---

### 6. Evidence of Deployment
**What to capture:**
- Agent is accessible
- Agent is working
- URL showing platform.openai.com (cloud deployment)

**How to capture:**
- Any screenshot showing agent working = deployment evidence
- Agent Builder is cloud-based (platform.openai.com)
- Screenshots of working agent = proof of cloud deployment

---

## ❓ About "Local/Cloud" Requirement

### What the Rubric Means:

The rubric mentions "Clear evidence of local or cloud deployment." Here's what this means:

**For Agent Builder:**
- ✅ **Agent Builder is cloud-based** - It's accessed at https://platform.openai.com/agent-builder
- ✅ **Your agent is automatically deployed in the cloud** when you create it
- ✅ **Screenshots showing agent working = evidence of cloud deployment**

**If You Have External Functions:**
- If you use Function Calling with external APIs:
  - **Cloud deployment:** Functions hosted on cloud services (AWS, Google Cloud, etc.)
  - **Local deployment:** Functions running on your local machine (for testing)
  - **How it works:** Cloud agent → Webhook URL → Tunnel (ngrok) → Local function
  - See **[FUNCTION_CALLING_GUIDE.md](FUNCTION_CALLING_GUIDE.md)** for detailed setup
- Document where your external functions are hosted

**For This Assignment:**
- If using only built-in tools (File Search, Code Interpreter) → Everything is cloud-based
- Screenshots of Agent Builder UI = evidence of cloud deployment
- No additional "deployment" steps needed

---

## 💡 Tips for Good Screenshots

1. **Be Clear:**
   - Use high resolution
   - Ensure text is readable
   - Crop unnecessary parts

2. **Label Screenshots:**
   - Add labels in your report: "Figure 1: Agent Configuration"
   - Include captions explaining what each screenshot shows

3. **Show Key Elements:**
   - Highlight important settings
   - Show tool enablement clearly
   - Include test results

4. **Take Multiple Angles:**
   - Configuration view
   - Tools view
   - Test chat view
   - Knowledge base view

---

## 📝 Screenshot Checklist

Before submitting, ensure you have:

- [ ] ✅ Agent configuration screenshot
- [ ] ✅ Tools/functions screenshot
- [ ] ✅ Instructions/prompt screenshot
- [ ] ✅ Knowledge base/vector store screenshot
- [ ] ✅ Testing/execution screenshot (with actual conversation)
- [ ] ✅ Evidence of deployment (agent working = cloud deployment)

**Minimum:** 5-6 screenshots covering all aspects

---

## 🎯 Example Screenshot Plan

**For Student Query Response Agent:**

1. **Screenshot 1:** Agent configuration page
   - Shows: Name, Model, Description
   - Caption: "Agent Configuration - Student Query Response Agent"

2. **Screenshot 2:** Tools section
   - Shows: File Search enabled
   - Caption: "Tools Setup - File Search Enabled"

3. **Screenshot 3:** Instructions
   - Shows: System prompt text
   - Caption: "Agent Instructions - Query Response Guidelines"

4. **Screenshot 4:** Knowledge base
   - Shows: Vector store with uploaded files
   - Caption: "Knowledge Base - Course Materials Uploaded"

5. **Screenshot 5:** Test chat
   - Shows: Question and answer conversation
   - Caption: "Testing - Agent Responding to Student Query"

6. **Screenshot 6:** Agent working (any view)
   - Shows: Agent is accessible and functional
   - Caption: "Deployment Evidence - Agent Active in Cloud"

---

## ✅ Summary

**Key Points:**
- Agent Builder is cloud-based (platform.openai.com)
- Screenshots of working agent = evidence of cloud deployment
- Take 5-6 clear screenshots covering all aspects
- Label and caption screenshots in your report
- Show actual functionality, not just configuration

**For This Assignment:**
- Focus on Agent Builder UI screenshots
- Show agent working = deployment evidence
- No complex deployment documentation needed

---

**Status:** ✅ Ready to capture screenshots

