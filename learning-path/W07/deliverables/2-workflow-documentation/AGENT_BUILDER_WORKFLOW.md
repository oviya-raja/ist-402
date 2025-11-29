# Agent Builder Workflow Configuration
## How the Workflow Works Within OpenAI Agent Builder

This document explains how the Job Fitment Analysis Agent workflow is configured and executed within the OpenAI Agent Builder platform.

---

## Understanding Agent Builder Workflow

### Two Types of Workflows:

1. **Logical Workflow** (Documented in `workflow-overview.md`)
   - Describes how the agent processes requests logically
   - Shows the business logic and decision flow
   - This is what the agent does internally

2. **Agent Builder Workflow Editor** (Visual Interface)
   - The visual workflow editor in OpenAI Platform
   - Where you configure the agent's behavior
   - Screenshots show this interface

---

## How the Workflow Works in Agent Builder

### Agent Builder Architecture

The OpenAI Agent Builder uses a **system prompt-driven approach** rather than a traditional visual workflow builder. Here's how it works:

```
┌─────────────────────────────────────────────────────────┐
│              AGENT BUILDER CONFIGURATION                │
│                                                          │
│  1. System Prompt (Instructions)                        │
│     └─> Contains workflow logic and routing            │
│                                                          │
│  2. Model (GPT-4o)                                      │
│     └─> Executes instructions from system prompt       │
│                                                          │
│  3. File Search Tool (Retrieval)                       │
│     └─> Accesses knowledge base automatically          │
│                                                          │
│  4. Knowledge Base (10 files)                          │
│     └─> Provides context and methodology               │
└─────────────────────────────────────────────────────────┘
```

### Workflow Execution in Agent Builder

**The workflow is NOT configured in a visual editor.** Instead, it's implemented through:

1. **System Prompt** (`deliverables/1-functional-agent/system-prompt.txt`)
   - Contains all workflow logic
   - Defines use case routing
   - Specifies processing steps
   - Defines decision points
   - **Location:** This is where the workflow lives

2. **Model Intelligence (GPT-4o)**
   - Reads and follows system prompt instructions
   - Makes decisions based on prompt logic
   - Routes to appropriate processing based on input

3. **File Search Tool**
   - Automatically triggered when knowledge base access needed
   - Retrieves relevant information from 10 files
   - Provides context for processing

---

## Where the Workflow Logic Lives

### Primary Location: System Prompt

**File:** `deliverables/1-functional-agent/system-prompt.txt`

The system prompt contains:
- **Use Case Routing Logic:** How to identify which use case (1-5)
- **Processing Steps:** Step-by-step instructions for each use case
- **Decision Points:** When to validate, when to ask for clarification
- **Error Handling:** How to handle invalid inputs
- **Output Formatting:** How to structure responses

### Example from System Prompt:

```
WORKFLOW LOGIC IN SYSTEM PROMPT:

1. When user provides input:
   - Parse company priorities (Priority 1, 2, 3)
   - Extract student profile components
   - Identify use case type

2. Route to appropriate processing:
   - Use Case 1: Find jobs → Provide guidance
   - Use Case 2: Check qualification → Calculate fitment
   - Use Case 3: Skill gaps → Identify gaps
   - Use Case 4: Compare jobs → Side-by-side analysis
   - Use Case 5: Strategy → Generate comprehensive plan

3. Process using knowledge base:
   - Retrieve company information
   - Retrieve calculation methodology
   - Retrieve skill gap framework

4. Generate response:
   - Format based on use case
   - Include mental health messaging
   - Provide actionable recommendations
```

---

## Agent Builder Interface Components

### What You Configure in Agent Builder:

1. **System Instructions** (System Prompt)
   - **Location in UI:** System instructions field
   - **Screenshot:** `deliverables/4-screenshots/prompt-instructions/02-system-instructions-config.png`
   - **Contains:** All workflow logic

2. **Model Selection**
   - **Location in UI:** Model dropdown
   - **Screenshot:** `deliverables/4-screenshots/agent-configuration/03-model-selection.png`
   - **Selected:** GPT-4o

3. **Tools Configuration**
   - **Location in UI:** Tools section
   - **Screenshot:** `deliverables/4-screenshots/tools-functions/07-tools-configuration.png`
   - **Enabled:** File Search (Retrieval)

4. **Knowledge Base (Files)**
   - **Location in UI:** Files/Storage section
   - **Screenshot:** `deliverables/4-screenshots/agent-configuration/05-06-files-uploaded-list.png`
   - **Files:** 10 knowledge base files

5. **Memory Settings**
   - **Location in UI:** Memory section
   - **Screenshot:** `deliverables/4-screenshots/memory-settings/08-memory-settings.png`
   - **Settings:** Default conversation memory

---

## Workflow Execution Flow

### How It Works When User Sends a Message:

```
1. USER SENDS MESSAGE
   ↓
2. AGENT BUILDER RECEIVES INPUT
   ↓
3. GPT-4o READS SYSTEM PROMPT
   ↓
4. SYSTEM PROMPT INSTRUCTIONS EXECUTED:
   ├─> Parse input
   ├─> Validate company names
   ├─> Identify use case
   ├─> Route to processing module
   └─> Determine if knowledge base needed
   ↓
5. FILE SEARCH TOOL ACTIVATED (if needed)
   ├─> Searches knowledge base
   ├─> Retrieves relevant information
   └─> Provides context to model
   ↓
6. GPT-4o PROCESSES WITH CONTEXT:
   ├─> Applies workflow logic from system prompt
   ├─> Uses knowledge base information
   ├─> Makes decisions (routing, calculations)
   └─> Generates response
   ↓
7. RESPONSE FORMATTED
   ├─> Based on use case type
   ├─> Includes mental health messaging
   └─> Provides actionable recommendations
   ↓
8. RESPONSE SENT TO USER
```

---

## Screenshots Showing Workflow Configuration

### Workflow-Related Screenshots:

1. **Agent Builder Workflow View**
   - `deliverables/4-screenshots/agent-configuration/06-agent-builder-workflow.png`
   - Shows the Agent Builder interface

2. **Workflow Editor**
   - `deliverables/4-screenshots/agent-configuration/10-workflow-editor.png`
   - Shows workflow editor interface

3. **Full Page Workflow**
   - `deliverables/4-screenshots/agent-configuration/12-full-page-workflow.png`
   - Complete workflow view

4. **Workflow Actions Menu**
   - `deliverables/4-screenshots/agent-configuration/15-workflow-actions-menu.png`
   - Workflow configuration options

### Note About Agent Builder Workflow Editor:

The OpenAI Agent Builder may have a visual workflow editor, but for this project:
- **The workflow logic is primarily in the system prompt**
- The visual editor (if used) would show the high-level flow
- The detailed logic is in the system prompt instructions

---

## Key Difference: Logical vs. Visual Workflow

### Logical Workflow (Documented)
**Location:** `workflow-overview.md`, `step-by-step-process.md`

- Describes WHAT the agent does
- Shows the business logic
- Explains decision points
- Documents data flow

### Visual Workflow (Agent Builder UI)
**Location:** Agent Builder interface (screenshots available)

- Shows HOW it's configured in the platform
- Visual representation of agent setup
- Configuration panels and settings
- Tool and file management

---

## Where to Find Workflow Information

### For Logical Workflow (What Agent Does):
1. **Main Workflow:** `workflow-overview.md`
   - High-level workflow
   - Use case workflows
   - Decision points

2. **Step-by-Step Process:** `step-by-step-process.md`
   - 22 detailed steps
   - Processing phases
   - Data transformations

3. **System Prompt:** `deliverables/1-functional-agent/system-prompt.txt`
   - Actual workflow implementation
   - Routing logic
   - Processing instructions

### For Agent Builder Configuration (How It's Set Up):
1. **Screenshots:** `deliverables/4-screenshots/agent-configuration/`
   - Visual configuration
   - UI screenshots
   - Setup evidence

2. **Integration Points:** `integration-points.md`
   - How Agent Builder integrates
   - API details
   - Configuration methods

---

## Summary

**The workflow for the agent is configured in:**

1. **System Prompt** (Primary)
   - File: `deliverables/1-functional-agent/system-prompt.txt`
   - Contains all workflow logic and routing

2. **Agent Builder Interface** (Configuration)
   - System instructions field (where prompt is entered)
   - Tools configuration (File Search enabled)
   - Files section (knowledge base)
   - Model selection (GPT-4o)

3. **Documentation** (Reference)
   - `workflow-overview.md` - Logical workflow
   - `step-by-step-process.md` - Detailed steps
   - Screenshots - Visual configuration evidence

**The workflow executes automatically** when users interact with the agent, following the instructions in the system prompt.

---

**Last Updated:** 2025-11-29  
**Status:** Complete

