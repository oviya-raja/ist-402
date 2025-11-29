# Objective Scripts Runner

This directory contains extracted objective code from `W3_RAG_Assignment.ipynb` for easier debugging and testing.

## Files

- `objective_0.py` - Prerequisites & Setup
- `objective_1.py` - Design System Prompts
- `objective_2.py` - Generate Q&A Database
- `objective_3.py` - Implement Vector Database
- `objective_4.py` - Build Complete RAG Pipeline
- `objective_5.py` - Model Evaluation & Ranking
- `objective_6.py` - System Analysis & Reflection
- `objective_X.md` - Documentation for each objective
- `objective_support.py` - **Shared utility class (DRY principle)** - Prerequisite validation and directory setup
- `run_objectives.py` - **Runner script to execute objectives sequentially**
- `CODE_REVIEW.md` - Comprehensive code quality review

## Usage

### Run All Objectives (Sequential)

```bash
cd learning-path/W03/02-assignments/objectives
python run_objectives.py
```

This will run Objectives 0, 1, 2, 3, 4, 5, and 6 in sequence, preserving state between them (just like a notebook).

### Run Specific Objectives

```bash
# Run only Objective 0
python run_objectives.py 0

# Run Objectives 0 and 1
python run_objectives.py 0 1

# Run Objectives 1, 2, and 3 (requires 0 to be run first)
python run_objectives.py 1 2 3
```

### Run Individual Objective (Standalone)

**Note:** This won't work for objectives 1-3 because they depend on previous objectives' state.

```bash
# Only Objective 0 can run standalone
python objective_0.py
```

## How It Works

The `run_objectives.py` script:
1. Creates a shared global namespace (simulates notebook `globals()`)
2. Executes each objective script in sequence
3. Preserves state between objectives (like `env`, `system_prompt`, etc.)
4. Allows pausing between objectives for inspection

## State Preservation

The runner maintains these variables across objectives:
- `env` - EnvironmentConfig instance (from Objective 0)
- `system_prompt` - System prompt string (from Objective 1)
- `inference_engine` - InferenceEngine instance (from Objective 1)
- `qa_database` - Q&A database list (from Objective 2)
- `embedding_model` - SentenceTransformer model (from Objective 3)
- `faiss_index` - FAISS index (from Objective 3)
- `embed_query()` - Query embedding function (from Objective 3)
- `rag_query()` - RAG pipeline function (from Objective 4)
- `rankings_df`, `detailed_df` - Evaluation results (from Objective 5)
- `ObjectiveSupport` - Shared utility class for DRY patterns
- And all other globals created by each objective

## Code Quality

All objectives follow best practices:
- **DRY**: Uses `ObjectiveSupport` class to eliminate duplication
- **SOLID**: Single Responsibility Principle - each class has one purpose
- **KISS**: Simple, focused code without over-engineering
- **YAGNI**: No unnecessary abstractions or unused code

See `CODE_REVIEW.md` for comprehensive code quality analysis.

## Example Output

```
================================================================================
🚀 RUNNING OBJECTIVE 0
================================================================================
🔍 Checking environment...
   ✅ Running in local environment
...

✅ Objective 0 completed successfully!

⏸️  Pausing before next objective...
   (Press Enter to continue, or Ctrl+C to stop)

================================================================================
🚀 RUNNING OBJECTIVE 1
================================================================================
...
```

## Troubleshooting

**Error: `'env' not found`**
- Make sure you run Objective 0 first: `python run_objectives.py 0`

**Error: `'system_prompt' not found`**
- Run objectives in order: `python run_objectives.py 0 1`

**Error: Import errors**
- Make sure you're in the `objectives` directory
- Install required packages (Objective 0 handles this)

**Error: `ObjectiveSupport` not found**
- This is optional - objectives have graceful fallback
- If you want to use it, ensure `objective_support.py` is in the same directory
- Objectives will work without it (uses manual fallback code)

