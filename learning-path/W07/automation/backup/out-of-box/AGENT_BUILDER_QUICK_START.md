# Agent Builder Workflow - Quick Start

## 🎯 Goal

Create a visual workflow in Agent Builder for Student Query Response.

---

## 🚀 5-Minute Setup

### Step 1: Open Agent Builder
**URL:** https://platform.openai.com/agent-builder

### Step 2: Create Workflow
1. Click **"Create Workflow"** or **"+"** button
2. Name: **"Student Query Response Workflow"**

### Step 3: Add Nodes

#### Node 1: User Input (Trigger)
- Drag **"Agent"** node to canvas
- Name: "User Input"
- Configure as **entry point**
- Input: `question` (string)

#### Node 2: Query Agent
- Drag **"Agent"** node to canvas  
- Name: "Student Query Response Agent"
- **Model:** gpt-4o
- **Instructions:**
  ```
  You are a helpful assistant that answers student questions using the provided knowledge base.
  
  Guidelines:
  - Answer questions based on information in the knowledge base
  - If information is not in the knowledge base, say so clearly
  - Provide clear, concise answers
  - Cite sources when possible
  - Be friendly and professional
  ```
- **Tools:** Enable **File Search**
- **Knowledge Base:** Attach "Student Knowledge Base"

#### Node 3: End
- Drag **"End"** node to canvas
- Output: Agent response

### Step 4: Connect
- User Input → Query Agent → End

### Step 5: Test
- Click **"Test"** or **"Preview"**
- Input: `{"question": "What are the course requirements?"}`
- Verify answer

### Step 6: Publish
- Click **"Publish"**
- Save workflow

---

## ✅ Done!

Your workflow is now in Agent Builder and ready to use!

---

## 📸 Screenshot This

Capture screenshot of:
- Workflow canvas showing all nodes connected
- This is your workflow diagram for submission!

---

**Time:** 5-10 minutes  
**Status:** ✅ Ready to create!

