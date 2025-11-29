# Python Scripts for Agent Creation and Testing

This folder contains all Python scripts used to create, configure, and test the Job Fitment Analysis Agent.

## 📁 Scripts Overview

### Core Agent Creation Scripts
- **`create_agent.py`** - Creates the agent from scratch (uploads files, creates vector store, links to assistant)
- **`complete_agent_setup.py`** - Completes setup for existing assistant (updates prompt, uploads files, links)

### Testing Scripts
- **`test_agent_e2e.py`** - End-to-end test of the agent (verifies configuration, tests basic functionality)
- **`test_all_use_cases.py`** - Comprehensive test suite for all 5 use cases

### File Management Scripts
- **`add_files_to_vector_store.py`** - Adds files to existing vector store
- **`link_files_raw_api.py`** - Links files using raw HTTP API (recommended method)

### Utility Scripts
- **`utils.py`** - Common utilities (environment loading, API key management) - **REQUIRED by all scripts**
- **`verify_all_scripts.py`** - Verifies all scripts are working correctly

## 🚀 Quick Start

### Option 1: Full Automation (Recommended)
```bash
cd deliverables/1-functional-agent/scripts
python3 automate_phase2.py
```
This single command will:
- Verify environment and scripts
- Create/verify agent
- Upload knowledge base files
- Test all 5 use cases
- Provide comprehensive report

### Option 2: Step-by-Step

#### 1. Verify Environment
```bash
cd deliverables/1-functional-agent/scripts
python3 verify_all_scripts.py
```

#### 2. Create Agent
```bash
python3 create_agent.py
```

#### 3. Test Agent
```bash
python3 test_agent_e2e.py
python3 test_all_use_cases.py
```

## 📋 Requirements

### Environment Variables
The scripts require a `.env` file at the project root (`/Users/rajasoun/workspace/personal/oviya/ist-402/.env`) with:
```bash
OPENAI_API_KEY=sk-proj-...
ASSISTANT_ID=asst_...  # Optional, has default
VECTOR_STORE_ID=vs_...  # Optional, has default
```

### Python Dependencies
```bash
pip install openai httpx python-dotenv
```

## 📚 Documentation

See **`PYTHON_SCRIPTS_README.md`** in this folder for detailed documentation of each script.

## ⚠️ Important Notes

1. **`utils.py` is required** - All scripts depend on this file
2. **Run from this directory** - Scripts are designed to be run from `deliverables/1-functional-agent/scripts/`
3. **Paths are relative** - Scripts automatically find system prompt and knowledge base files
4. **Environment setup** - Make sure `.env` file is configured before running scripts

## 🔧 Path Structure

Scripts are located at:
```
deliverables/1-functional-agent/scripts/
```

They reference:
- **System prompt:** `../system-prompt.txt` (one level up)
- **Knowledge base:** `../../../../knowledge-base/` (at project root)
- **Environment file:** `../../../../.env` (at ist-402 root)

---

**Last Updated:** 2025-11-29  
**Status:** ✅ Scripts organized and ready to use

