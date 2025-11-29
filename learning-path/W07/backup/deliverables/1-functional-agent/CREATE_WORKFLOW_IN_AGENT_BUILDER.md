# How to Create Workflow in Agent Builder

## ⚠️ Important: Workflow API Limitation

**The OpenAI Python SDK does not currently have a workflows API endpoint.**

Agent Builder workflows need to be created in the **visual UI interface**.

However, the workflow logic is **already configured** in your assistant:
- ✅ System prompt contains workflow logic
- ✅ File Search tool is enabled  
- ✅ Knowledge base is linked
- ✅ Assistant is functional

---

## 🔧 Creating Workflow in Agent Builder UI

### Step-by-Step Instructions:

1. **Navigate to Agent Builder:**
   - Go to: https://platform.openai.com/agent-builder
   - Click **"Create"** button

2. **Add Workflow Nodes:**
   
   **From Components Panel (left sidebar):**
   
   a. **Start Node** (Core section)
      - Drag "Start" node to canvas
      - This is the entry point
   
   b. **Agent Node** (Core section)
      - Drag "Agent" node to canvas
      - Configure:
        - Name: "Job Fitment Analysis Agent"
        - Link to existing assistant: `asst_49u4HKGefgKxQwtNo87x4UnA`
   
   c. **File Search Node** (Tools section)
      - Drag "File Search" node to canvas
      - Configure:
        - Vector Store: `vs_692b61d3ae9481918de6616f9afa7b99`
        - This enables knowledge base access
   
   d. **End Node** (Core section)
      - Drag "End" node to canvas
      - This is the exit point

3. **Connect the Nodes:**
   - Connect: **Start** → **Agent** → **File Search** → **End**
   - Click and drag from output of one node to input of next

4. **Save and Publish:**
   - Click **"Publish"** button (top right)
   - Name the workflow: "Job Fitment Analysis Workflow"
   - Save

5. **Capture Screenshots:**
   - Screenshot the complete workflow canvas
   - Screenshot each node configuration
   - Save to: `deliverables/4-screenshots/agent-configuration/`

---

## 📋 Workflow Definition Reference

A workflow definition JSON has been created as reference:
- **File:** `deliverables/1-functional-agent/workflow-definition.json`

**Workflow Structure:**
```
Start
  ↓
Agent (Job Fitment Analysis Agent)
  ↓
File Search (Knowledge Base)
  ↓
End
```

---

## ✅ Current Status

**What's Already Working:**
- ✅ Assistant created: `asst_49u4HKGefgKxQwtNo87x4UnA`
- ✅ System prompt configured (contains workflow logic)
- ✅ File Search tool enabled
- ✅ Knowledge base linked (10 files)
- ✅ All 5 use cases tested and working

**What Needs to Be Done:**
- ⏳ Create visual workflow in Agent Builder UI
- ⏳ Link workflow to existing assistant
- ⏳ Capture screenshots of workflow

---

## 🔗 Quick Links

- **Agent Builder:** https://platform.openai.com/agent-builder
- **Your Assistant:** https://platform.openai.com/assistants/asst_49u4HKGefgKxQwtNo87x4UnA
- **Workflow Definition:** `deliverables/1-functional-agent/workflow-definition.json`

---

## 📝 Note

The workflow **logic is already working** through:
1. System prompt (defines workflow steps)
2. File Search tool (automatically triggered)
3. Assistant API (executes workflow)

The visual workflow in Agent Builder is a **representation** of this logic, not a requirement for functionality. However, for the assignment, you need to create it in Agent Builder UI and capture screenshots.

---

*Last Updated: 2025-11-29*

