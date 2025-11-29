# How to View Workflow in Agent Builder

## 🔗 Direct Links

### Agent Builder Home
**Link:** https://platform.openai.com/agent-builder

### Your Assistant (Agent Builder View)
**Link:** https://platform.openai.com/assistants/asst_49u4HKGefgKxQwtNo87x4UnA

---

## 📋 How to View the Workflow

### Method 1: View in Assistant Configuration Page

1. **Navigate to your assistant:**
   - Go to: https://platform.openai.com/assistants/asst_49u4HKGefgKxQwtNo87x4UnA
   - You should see the "Job Fitment Analysis Agent" configuration

2. **Look for Workflow Section:**
   - Scroll down to find "Workflow" or "Actions" section
   - The workflow logic is embedded in the **System Instructions** field
   - This is where the workflow lives in Agent Builder

3. **View System Instructions:**
   - Click on "System instructions" section
   - This contains all the workflow logic
   - The workflow is defined as instructions, not a visual diagram

### Method 2: Check Agent Builder Interface

1. **Go to Agent Builder:**
   - Navigate to: https://platform.openai.com/agent-builder
   - Look for your agent in the list
   - Click on it to view configuration

2. **Workflow Configuration:**
   - OpenAI Agent Builder uses a **prompt-based workflow**
   - The workflow is in the **System Instructions** field
   - Not a traditional visual workflow builder

---

## 📸 Screenshots of Workflow Configuration

Screenshots showing workflow-related views are saved in:
`deliverables/4-screenshots/agent-configuration/`

- `06-agent-builder-workflow.png` - Workflow view
- `10-workflow-editor.png` - Workflow editor interface
- `12-full-page-workflow.png` - Full page workflow view
- `15-workflow-actions-menu.png` - Workflow actions menu

---

## 🔍 Where the Workflow Actually Lives

### In Agent Builder Interface:

1. **System Instructions Field**
   - **Location:** Assistant configuration page → "System instructions" section
   - **Contains:** All workflow logic and routing instructions
   - **Screenshot:** `02-system-instructions-config.png`

2. **Tools Configuration**
   - **Location:** "Tools" section
   - **Shows:** File Search tool (enables knowledge base access)
   - **Screenshot:** `07-tools-configuration.png`

3. **Knowledge Base Files**
   - **Location:** "Storage" or "Files" section
   - **Shows:** 10 knowledge base files linked
   - **Screenshot:** `05-06-files-uploaded-list.png`

### In Code/Files:

1. **System Prompt File:**
   - **Location:** `deliverables/1-functional-agent/system-prompt.txt`
   - **Contains:** Complete workflow logic
   - This is what gets loaded into "System Instructions"

2. **Automation Script:**
   - **Location:** `deliverables/1-functional-agent/scripts/create_agent.py`
   - **Does:** Automatically loads system prompt into Agent Builder

---

## ⚠️ Important Note

**OpenAI Agent Builder does NOT use a traditional visual workflow builder.**

Instead:
- ✅ **Workflow is defined in System Instructions** (text-based)
- ✅ **Model (GPT-4o) reads and executes** the instructions
- ✅ **File Search tool** automatically accesses knowledge base when needed
- ✅ **All workflow logic** is in the system prompt

This is different from tools like Zapier or Microsoft Power Automate that have visual workflow builders.

---

## 🎯 What You'll See in Agent Builder

When you open your assistant, you'll see:

1. **Name:** "Job Fitment Analysis Agent"
2. **System Instructions:** (Contains workflow logic)
3. **Model:** GPT-4o
4. **Tools:** File Search (enabled)
5. **Knowledge Base:** 10 files linked
6. **Memory:** Default settings

The workflow logic is embedded in the System Instructions field - it's not a separate visual diagram.

---

## 📖 For Visual Workflow Diagrams

If you want to see visual workflow diagrams, those are in:
- **Location:** `deliverables/2-workflow-documentation/workflow-diagrams/`
- **Format:** Mermaid diagrams (`.mmd` files)
- **View:** Use https://mermaid.live to render them

These show the logical workflow, not the Agent Builder interface.

---

*Last Updated: 2025-11-29*

