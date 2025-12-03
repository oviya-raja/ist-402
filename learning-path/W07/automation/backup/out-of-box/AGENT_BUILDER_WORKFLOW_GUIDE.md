# Agent Builder Workflow Guide

## 🔍 Understanding Agent Builder vs Assistants

**Two Different Interfaces:**

1. **Assistants** (platform.openai.com/assistants) ✅ **What you have now**
   - Simple assistant with tools
   - Chat-based interface
   - Your current setup

2. **Agent Builder** (platform.openai.com/agent-builder) ⭐ **Visual Workflows**
   - Visual workflow builder
   - Drag-and-drop nodes
   - Multi-step processes
   - Conditional logic
   - **This is what you want!**

---

## 🎯 Creating a Workflow in Agent Builder

### Step 1: Access Agent Builder

1. **Go to:** https://platform.openai.com/agent-builder
2. **Click:** "Create Workflow" or "New Workflow" button
3. **Name it:** "Student Query Response Workflow"

---

### Step 2: Design Your Workflow

For your Student Query Response use case, here's a simple workflow:

```
┌─────────────────┐
│  User Input     │ (Trigger)
│  (Question)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent Node     │ (Your Assistant)
│  File Search    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response       │ (End)
│  Return Answer  │
└─────────────────┘
```

---

### Step 3: Add Nodes to Canvas

#### Node 1: User Input (Trigger)

1. **Drag "Agent" node** from the **Core** section to canvas
2. **Configure:**
   - **Name:** "User Input"
   - **Type:** Entry point / Trigger
   - **Input Schema:**
     ```json
     {
       "question": {
         "type": "string",
         "description": "Student question"
       }
     }
     ```
   - **System Prompt:** "Accept student question input"

#### Node 2: Query Response Agent

1. **Drag another "Agent" node** to canvas
2. **Configure:**
   - **Name:** "Student Query Response Agent"
   - **Model:** gpt-4o
   - **System Instructions:** 
     ```
     You are a helpful assistant that answers student questions using the provided knowledge base.
     
     Guidelines:
     - Answer questions based on information in the knowledge base
     - If information is not in the knowledge base, say so clearly
     - Provide clear, concise answers
     - Cite sources when possible
     - Be friendly and professional
     ```
   - **Tools:** Enable File Search
   - **Knowledge Base:** Attach "Student Knowledge Base" vector store

#### Node 3: End Node

1. **Drag "End" node** from **Core** section
2. **Configure:**
   - **Output:** Return the agent's response

---

### Step 4: Connect Nodes

1. **Connect User Input → Query Response Agent**
   - Click on User Input node
   - Drag connection line to Query Response Agent
   - Pass `question` as input

2. **Connect Query Response Agent → End**
   - Click on Query Response Agent
   - Drag connection line to End node
   - Pass agent response as output

---

### Step 5: Test the Workflow

1. **Click "Preview" or "Test" button**
2. **Enter test input:**
   ```json
   {
     "question": "What are the course requirements?"
   }
   ```
3. **Run workflow**
4. **Verify output** shows answer from knowledge base

---

### Step 6: Publish Workflow

1. **Click "Publish" button**
2. **Name the version:** "v1.0"
3. **Get workflow ID** for deployment

---

## 🎨 Visual Workflow Example

Here's what your workflow should look like:

```
┌─────────────────────────────────────────────────┐
│              Agent Builder Canvas                │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────┐         ┌──────────────┐      │
│  │  User Input  │────────▶│   Agent      │      │
│  │  (Trigger)   │         │ File Search  │      │
│  └──────────────┘         └──────┬───────┘      │
│                                   │              │
│                            ┌──────▼───────┐      │
│                            │     End      │      │
│                            │   (Output)   │      │
│                            └──────────────┘      │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## 📋 Step-by-Step Instructions

### Complete Setup in Agent Builder

1. **Go to Agent Builder:**
   - https://platform.openai.com/agent-builder

2. **Create New Workflow:**
   - Click "Create Workflow" or "+" button
   - Name: "Student Query Response Workflow"

3. **Add Trigger Node:**
   - Drag "Agent" node from left panel
   - Configure as entry point
   - Set input: `question` (string)

4. **Add Main Agent Node:**
   - Drag another "Agent" node
   - Configure:
     - Model: gpt-4o
     - Instructions: (your system prompt)
     - Tools: File Search
     - Knowledge Base: Student Knowledge Base

5. **Add End Node:**
   - Drag "End" node
   - Configure output

6. **Connect Nodes:**
   - User Input → Agent → End

7. **Test:**
   - Click "Test" or "Preview"
   - Enter: `{"question": "What are the course requirements?"}`
   - Verify response

8. **Publish:**
   - Click "Publish"
   - Save workflow

---

## 🔄 Alternative: Use Your Existing Assistant

**Option:** You can reference your existing assistant in the workflow:

1. **In Agent Builder workflow:**
   - Add "Agent" node
   - Instead of configuring new agent, **reference existing assistant**
   - Use Assistant ID: `asst_HhWz11KVfZgudaIxXlqXHLt2`

**Note:** This depends on Agent Builder's current features. Check if there's an option to "Use Existing Assistant" or "Import Assistant".

---

## 🎯 Simple Workflow for Your Use Case

### Minimal Workflow (2 Nodes):

```
Node 1: User Input
├─ Input: question (string)
└─ Output: question

Node 2: Query Agent
├─ Model: gpt-4o
├─ Instructions: (your prompt)
├─ Tools: File Search
├─ Knowledge Base: Student Knowledge Base
└─ Output: answer
```

---

## ✅ Verification Checklist

After creating workflow:

- [ ] Workflow created in Agent Builder
- [ ] Nodes connected correctly
- [ ] File Search tool enabled
- [ ] Knowledge base attached
- [ ] Workflow tested successfully
- [ ] Workflow published

---

## 📸 Screenshots to Capture

1. **Agent Builder Canvas** - Showing workflow diagram
2. **Node Configuration** - Showing agent settings
3. **Test Results** - Showing workflow execution
4. **Published Workflow** - Showing workflow ID

---

## 🚀 Quick Start

```bash
# 1. Go to Agent Builder
open https://platform.openai.com/agent-builder

# 2. Click "Create Workflow"

# 3. Follow steps above

# 4. Test and publish
```

---

## 💡 Tips

1. **Start Simple:** Begin with 2-3 nodes
2. **Test Frequently:** Use preview mode
3. **Use Templates:** Check if Agent Builder has templates
4. **Document:** Take screenshots of your workflow

---

## ⚠️ Important Notes

- **Agent Builder workflows are separate** from Assistants
- Your existing assistant (`asst_HhWz11KVfZgudaIxXlqXHLt2`) is in Assistants interface
- Agent Builder workflows are visual and can be more complex
- You can create a simple workflow that uses your assistant's configuration

---

**Status:** ✅ Guide ready - Follow steps to create workflow in Agent Builder!

