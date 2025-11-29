# RAG Assignment: Week 3

## 📋 Overview

This is the main RAG (Retrieval-Augmented Generation) assignment for Week 3. You'll build a complete RAG system with model evaluation and analysis.

## 📁 Directory Structure

```
02-assignments/
├── W3_RAG_Assignment.ipynb          # Main assignment notebook (6 objectives)
├── assignment.md                     # Assignment specification
├── design/                           # Architecture documentation
│   ├── architecture.md               # Complete architecture guide
│   └── rag_pipeline.html            # Interactive pipeline diagram
├── diagrams/                         # Visual diagrams
│   └── rag-pipeline-architecture.png # Pipeline visualization
└── data/                             # Generated data (created during execution)
```

## 🎯 Assignment Objectives

The assignment consists of 6 objectives:

1. **Objective 1**: Create Assistant System Prompt
   - Design system prompt with business context
   - Load Mistral-7B-Instruct model
   - Test prompt with sample questions

2. **Objective 2**: Generate Business Database Content
   - Generate 21 Q&A pairs using Mistral
   - Include answerable and unanswerable examples
   - Organize by business categories

3. **Objective 3**: Implement FAISS Vector Database
   - Create embeddings using Sentence Transformers
   - Build FAISS index for semantic search
   - Test retrieval functionality

4. **Objective 4**: Create Test Questions & RAG Pipeline
   - Generate test questions (answerable and unanswerable)
   - Build complete RAG pipeline
   - Test pipeline with both question types

5. **Objective 5**: Model Evaluation & Ranking
   - Evaluate 6 QA models
   - Calculate 5 metrics (Accuracy, Confidence, Quality, Speed, Robustness)
   - Rank models by weighted composite score

6. **Objective 6**: System Analysis & Reflection
   - Analyze system performance
   - Identify strengths and limitations
   - Write critical reflection

## 📖 Key Files

### Main Assignment
- **`W3_RAG_Assignment.ipynb`**: Complete assignment notebook with all 6 objectives
  - Includes setup, functions, execution, and verification
  - 100% component reuse across objectives
  - Production-ready code with error handling

### Documentation
- **`assignment.md`**: Assignment specification and requirements
- **`design/architecture.md`**: Comprehensive architecture guide
  - System overview and design decisions
  - Component reuse and modularity
  - Technical highlights
  - Interview talking points
  - Visual design explanations
- **`design/rag_pipeline.html`**: Interactive RAG pipeline visualization
- **`diagrams/rag-pipeline-architecture.png`**: Static pipeline diagram

### Generated Data
- **`data/`**: Contains generated files from assignment execution
  - System prompts, Q&A database, embeddings, evaluation results, etc.

## 🚀 Getting Started

1. **Prerequisites**: Complete Week 1 and Week 2 exercises first
2. **Open Notebook**: Start with `W3_RAG_Assignment.ipynb`
3. **Follow Objectives**: Complete objectives 1-6 in order
4. **Review Documentation**: Check `design/architecture.md` for detailed explanations
5. **Visualize**: Open `design/rag_pipeline.html` for interactive diagram

## 📊 Evaluation Criteria

- **Technical Implementation**: RAG pipeline, FAISS, model evaluation
- **Code Quality**: Modularity, component reuse, error handling
- **Documentation**: Clear comments, architecture understanding
- **Analysis**: Critical reflection on system performance
- **Completeness**: All 6 objectives completed

## 💡 Key Features

- **100% Component Reuse**: Zero code duplication
- **Modular Design**: Each objective builds on previous
- **Comprehensive Evaluation**: 6 models × 5 metrics
- **Production-Ready**: Error handling, caching, optimization
- **Interview-Ready**: Architecture documentation suitable for job interviews

## 🔗 Related Resources

- **Exercise**: `../01-exercises/01-rag-with-model-evaluation/`
- **Learnings**: `../../03-learnings/`
- **Architecture Guide**: `design/architecture.md`
- **Interactive Diagram**: `design/rag_pipeline.html`
