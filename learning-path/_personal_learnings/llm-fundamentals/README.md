# LLM Fundamentals - Personal Notes

Core AI concepts and how LLMs work.

## 📁 Structure

This directory follows the same pattern as `W03/02-assignments/objectives`:

```
llm-fundamentals/
├── README.md                    # This file
├── core-concepts.md             # Core concepts documentation
└── objectives/                  # Standalone Python objectives
    ├── README.md                # Objectives guide
    ├── objective_1_tokens.py   # Tokens: Text → Tokens
    ├── objective_1_tokens.md   # Documentation
    ├── objective_2_embeddings.py # Embeddings: Tokens → Vectors
    ├── objective_2_embeddings.md
    ├── objective_3_attention.py # Attention: Vector Relationships
    ├── objective_4_layers.py    # Transformer Layers
    ├── objective_5_tensors.py   # Working with Tensors
    ├── objective_6_parameters.py # Model Parameters
    ├── run_objectives.py        # Run all objectives sequentially
    └── llm_fundamentals_support.py # Shared utilities
```

## 🧠 Core Concepts

### 1. Tokens
Text split into small units (tokens).

### 2. Embeddings
Tokens → vectors (numerical representation).

### 3. Vector Relationships (Attention)
The model computes how each token/vector relates to every other.

### 4. Layers
Stacked attention + feedforward blocks that apply transformations repeatedly.

### 5. Tensors
Data and weights stored in multi-dimensional arrays.

### 6. Parameters (Weights)
Learned numerical values inside tensors, updated during training.

## 🔗 Flow

**LLM = Tokens → Embeddings → Vector Relationships (Attention) → Layers → Tensors → Parameters (Weights)**

## 🚀 Usage

### Run Individual Objectives

```bash
cd objectives
python objective_1_tokens.py
python objective_2_embeddings.py
```

### Run All Objectives Sequentially

```bash
cd objectives
python run_objectives.py
```

### Run Specific Objectives

```bash
python run_objectives.py 1 2 3
```

## 📓 Notebook Integration

Each objective can be:
1. **Run standalone** as a Python script
2. **Combined into a Jupyter notebook** - each objective becomes a cell
3. **Documented** with markdown files that become markdown cells

This gives you flexibility to:
- Debug individual objectives
- Run quick experiments
- Build a complete learning notebook
- Share individual concepts

## 🎯 Key Learnings

Document your understanding of:
- How transformers work
- Attention mechanisms
- Training vs inference
- Model architectures

