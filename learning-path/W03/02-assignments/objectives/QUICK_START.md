# Quick Start Guide

## Simulate Notebook Execution

To run objectives sequentially (like in a notebook):

```bash
cd learning-path/W03/02-assignments/objectives

# Run Objective 0 first (Prerequisites & Setup)
python run_objectives.py 0

# Then run Objective 1 (it will use env from Objective 0)
python run_objectives.py 0 1

# Or run all objectives at once (0-6)
python run_objectives.py
```

**Note:** All objectives use `ObjectiveSupport` class for DRY (Don't Repeat Yourself) patterns. If the import fails, objectives gracefully fall back to manual checking.

## Step-by-Step Example

```bash
# Step 1: Run Objective 0 (Prerequisites & Setup)
python run_objectives.py 0

# Step 2: Run Objective 1 (System Prompts)
# Press Enter when prompted, or run:
python run_objectives.py 0 1

# Step 3: Run Objective 2 (Q&A Database)
python run_objectives.py 0 1 2

# Step 4: Run Objective 3 (Vector Database)
python run_objectives.py 0 1 2 3

# Or simply run all:
python run_objectives.py
```

## What Happens

1. **Objective 0** creates `env` (EnvironmentConfig) and sets up libraries
2. **Objective 1** uses `env` to create `system_prompt` and `inference_engine`
3. **Objective 2** uses `env`, `inference_engine`, and `system_prompt` to create `qa_database`
4. **Objective 3** uses `env` and `qa_database` to create embeddings and FAISS index
5. **Objective 4** uses all previous components to build complete RAG pipeline
6. **Objective 5** uses RAG pipeline to evaluate and rank 6 QA models (4 required + 2 additional)
7. **Objective 6** analyzes results and provides insights for reflection

The runner script preserves all state between objectives, just like a Jupyter notebook!

## Code Quality Features

- **DRY**: All objectives use `ObjectiveSupport` class to eliminate code duplication
- **Prerequisite Validation**: Automatic checking of required variables from previous objectives
- **Output Directory Setup**: Centralized directory creation across all objectives
- **Graceful Fallback**: Works even if `ObjectiveSupport` import fails (notebook compatibility)
- **SOLID Principles**: Each class has single responsibility
- **100% Component Reuse**: Objectives reuse components from previous objectives

See `CODE_REVIEW.md` for detailed code quality analysis and metrics.

