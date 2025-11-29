# Week 3: RAG with Model Evaluation

## 🚀 Quick Start

1. **Prerequisites**: Complete **Week 1** (Prompt Engineering) and **Week 2** (Simple RAG) first
2. **Start Exercise**: Go to `01-exercises/01-rag-with-model-evaluation/`
3. **Review Concepts**: Use `03-learnings/` for quick reference
4. **Complete Assignment**: Check `02-assignments/` for the main RAG assignment

## 📁 Structure

### 📚 `01-exercises/` - Learning Materials
Step-by-step tutorial to build a complete RAG system with model evaluation.

**Contents:**
- `01-rag-with-model-evaluation/` - Complete RAG system with evaluation framework

### 🧠 `03-learnings/` - Concepts & Quick Reference
Quick reference for advanced RAG concepts, model evaluation, and best practices.

### 📝 `02-assignments/` - Assignment Requirements
Main RAG assignment with complete specification, evaluation criteria, and working notebook.

**Contents:**
- `W3_RAG_Assignment.ipynb` - Complete assignment notebook (6 objectives)
- `assignment.md` - Assignment specification and requirements
- `design/` - Architecture documentation and visualizations
  - `architecture.md` - Comprehensive architecture guide (interview-ready)
  - `rag_pipeline.html` - Interactive RAG pipeline diagram
- `diagrams/` - Visual diagrams
  - `rag-pipeline-architecture.png` - Two-phase RAG pipeline visualization
- `data/` - Generated data from assignment execution

## 📚 Learning Path

```
Week 1: Prompt Engineering
    ↓
Week 2: Simple RAG
    ↓
Week 3: RAG with Model Evaluation (You are here)
    ├── 01-exercises/01-rag-with-model-evaluation/
    ├── 02-assignments/ (main assignment)
    │   ├── W3_RAG_Assignment.ipynb
    │   ├── assignment.md
    │   ├── design/ (architecture docs)
    │   └── diagrams/ (visualizations)
    └── 03-learnings/ (reference)
```

## 🎯 What You'll Learn

- **Complete RAG System**: Build a full RAG system with Mistral-7B
- **Model Evaluation**: Compare and rank multiple QA models (6 models, 5 metrics)
- **Advanced FAISS**: Implement advanced indexing and retrieval
- **Business Context**: Create business-specific Q&A databases
- **Performance Metrics**: Evaluate accuracy, confidence, quality, speed, and robustness
- **Answerable vs Unanswerable**: Test system with different question types
- **System Analysis**: Comprehensive analysis and reflection on system performance

## 📖 Key Files

### Exercises
- `01-exercises/01-rag-with-model-evaluation/W3_RAG_System_Exercise.ipynb` - Exercise notebook
- `01-exercises/01-rag-with-model-evaluation/rag_system_exercise.py` - Standalone Python script
- `01-exercises/01-rag-with-model-evaluation/README.md` - Exercise instructions

### Assignment
- `02-assignments/W3_RAG_Assignment.ipynb` - Complete assignment notebook (6 objectives)
- `02-assignments/assignment.md` - Assignment specification
- `02-assignments/design/architecture.md` - Architecture documentation (interview-ready)
- `02-assignments/design/rag_pipeline.html` - Interactive pipeline visualization
- `02-assignments/diagrams/rag-pipeline-architecture.png` - Pipeline diagram

## 🏗️ Assignment Structure

The main assignment (`W3_RAG_Assignment.ipynb`) consists of 6 objectives:

1. **Objective 1**: Create Assistant System Prompt
2. **Objective 2**: Generate Business Database Content (21 Q&A pairs)
3. **Objective 3**: Implement FAISS Vector Database
4. **Objective 4**: Create Test Questions & RAG Pipeline
5. **Objective 5**: Model Evaluation & Ranking (6 models, 5 metrics)
6. **Objective 6**: System Analysis & Reflection

## 📊 Architecture Documentation

The `design/` folder contains comprehensive documentation:

- **architecture.md**: Complete architecture guide with:
  - System overview and design decisions
  - Component reuse and modularity
  - Technical highlights and challenges
  - Interview talking points
  - Visual design explanations

- **rag_pipeline.html**: Interactive visualization showing:
  - Phase 1: Pre-Processing (Objectives 1-3)
  - Phase 2: RAG Pipeline (Objectives 4-5)
  - Phase 3: Evaluation (Objective 6)
  - Detailed objectives breakdown

## 🔗 Navigation

- **Previous**: [`../W02/`](../W02/) - Week 2: Simple RAG
- **Previous**: [`../W01/`](../W01/) - Week 1: Prompt Engineering

## 💡 Key Features

- **100% Component Reuse**: Zero code duplication across objectives
- **Modular Architecture**: Each objective builds on previous work
- **Comprehensive Evaluation**: 6 models evaluated on 5 weighted metrics
- **Production-Ready Design**: Error handling, caching, and optimization
- **Interview-Ready Documentation**: Architecture guide suitable for job interviews
