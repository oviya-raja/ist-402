# LLM Fundamentals Objectives

This directory contains standalone Python scripts for learning LLM fundamentals, organized as independent objectives that can be run separately or combined into a Jupyter notebook.

## 📁 Structure

- `objective_1_tokens.py` - Tokenization: Text → Tokens
- `objective_2_embeddings.py` - Embeddings: Tokens → Vectors
- `objective_3_attention.py` - Attention: Vector Relationships
- `objective_4_layers.py` - Transformer Layers
- `objective_5_tensors.py` - Working with Tensors
- `objective_6_parameters.py` - Model Parameters & Configuration
- `objective_X.md` - Documentation for each objective
- `run_objectives.py` - Runner script to execute objectives sequentially
- `llm_fundamentals_support.py` - Shared utility functions

## 🚀 Usage

### Run All Objectives (Sequential)

```bash
cd learning-path/_personal_learnings/llm-fundamentals/objectives
python run_objectives.py
```

This will run all objectives in sequence, preserving state between them (like a notebook).

### Run Specific Objectives

```bash
# Run only Objective 1 (Tokens)
python run_objectives.py 1

# Run Objectives 1 and 2
python run_objectives.py 1 2

# Run Objectives 1, 2, and 3
python run_objectives.py 1 2 3
```

### Run Individual Objective (Standalone)

Each objective can be run independently:

```bash
# Run tokens objective
python objective_1_tokens.py

# Run embeddings objective
python objective_2_embeddings.py
```

## 📚 Objectives Overview

1. **Objective 1: Tokens** - Understanding tokenization
2. **Objective 2: Embeddings** - Converting tokens to vectors
3. **Objective 3: Attention** - How attention mechanisms work
4. **Objective 4: Layers** - Transformer layer architecture
5. **Objective 5: Tensors** - Working with PyTorch tensors
6. **Objective 6: Parameters** - Model weights and configuration

## 📓 Notebook Integration

These objectives can be combined into a Jupyter notebook:
- Each objective becomes a notebook cell
- Documentation (`.md` files) becomes markdown cells
- Run all cells sequentially for complete learning flow

## 🎯 Learning Path

```
Objective 1 (Tokens)
    ↓
Objective 2 (Embeddings)
    ↓
Objective 3 (Attention)
    ↓
Objective 4 (Layers)
    ↓
Objective 5 (Tensors)
    ↓
Objective 6 (Parameters)
```

Each objective builds on the previous one, creating a complete understanding of LLM fundamentals.

