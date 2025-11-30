# Workflow Automation Scripts

Scripts to automate OpenAI Agent Builder workflow creation instead of manual clickops.

## Overview

Based on the [OpenAI Agent Builder documentation](https://platform.openai.com/docs/guides/agent-builder), workflows can be created in two ways:

1. **Visual UI (Agent Builder)** - Drag-and-drop interface (clickops)
2. **Agent SDK Code** - Download workflow code after UI creation

**Note:** As of current documentation, there's no direct API to create workflows from scratch. However, you can:
- Create workflow definitions programmatically
- Import workflow definitions if OpenAI adds import functionality
- Use the downloaded Agent SDK code for deployment

## Setup

### Environment Variables

1. **Create `.env` file in repository root:**
   ```bash
   # From repository root
   cp .env.example .env
   ```

2. **Edit `.env` and add your OpenAI API key and optional 2FA timeout:**
   ```bash
   OPENAI_API_KEY=sk-your-actual-api-key-here
   # Optional: 2FA wait timeout in seconds (default: 60)
   2FA_WAIT_TIMEOUT=60
   ```

3. **Verify `.env` is in `.gitignore`** (already configured ✅)

The script automatically loads `.env` from the repository root (3 levels up from `scripts/`).

### Installation

```bash
# Install dependencies (python-dotenv is already in requirements.txt)
pip install python-dotenv openai

# Or install all requirements
pip install -r requirements.txt
```

## Scripts

### `create_workflow_sdk.py`

Creates workflow definitions based on our documented workflows.

**Usage:**

```bash
# Create both workflows
python scripts/create_workflow_sdk.py --workflow both

# Create only job search workflow
python scripts/create_workflow_sdk.py --workflow job_search

# Create only qualification check workflow
python scripts/create_workflow_sdk.py --workflow qualification_check

# Attempt API creation (if available)
python scripts/create_workflow_sdk.py --workflow both --api
```

**Output:**
- Generates `workflow_definition.json` files
- Provides instructions for manual import or UI creation

## Workflow Definition Format

The script generates workflow definitions in a structured format that includes:

- **Nodes:** Agent, Transform, If/Else, Tool, End nodes
- **Edges:** Connections between nodes with conditions
- **Configuration:** System prompts, input schemas, formulas

## Current Limitations

⚠️ **Important:** OpenAI Agent Builder currently requires:
1. Creating workflows via the visual UI first
2. Then downloading the Agent SDK code for deployment

The script provides:
- ✅ Workflow definitions for reference
- ✅ Structured format matching Agent Builder concepts
- ✅ Ready-to-use configuration for manual UI creation
- ⚠️ API creation may not be available yet

## Alternative Approach

Since programmatic creation may not be fully available:

1. **Use the workflow definitions** as a blueprint
2. **Follow the interactive diagrams** in `docs/workflow-diagrams/workflows.html`
3. **Use step-by-step instructions** provided in the diagrams
4. **After UI creation**, download the Agent SDK code for version control

## Next Steps

1. Check OpenAI API updates for workflow creation endpoints
2. Monitor Agent Builder for import functionality
3. Use workflow definitions as documentation and reference
4. Follow UI creation with downloaded SDK code for automation

## References

- [OpenAI Agent Builder Guide](https://platform.openai.com/docs/guides/agent-builder)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- Workflow Diagrams: `docs/workflow-diagrams/workflows.html`

