# Quick Start Guide

## Simulate Notebook Execution

To run objectives sequentially (like in a notebook):

```bash
cd learning-path/W03/02-assignments/temp_objectives

# Run Objective 0 first
python run_objectives.py 0

# Then run Objective 1 (it will use env from Objective 0)
python run_objectives.py 0 1

# Or run all at once
python run_objectives.py
```

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

The runner script preserves all state between objectives, just like a Jupyter notebook!

