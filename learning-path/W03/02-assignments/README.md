# Week 3 Assignments - RAG System with Model Evaluation

## 📝 Purpose
Main assignment for Week 3: Build a complete RAG system with model evaluation and comparison.

## 📁 Files

- **`rag-assignment-specification.md`** - Complete assignment specification with:
  - All 6 steps (System Prompt → Database Generation → FAISS → Testing → Model Ranking)
  - Technical requirements and dependencies
  - Deliverables checklist
  - Evaluation criteria
- **`W3_RAG_Assignment_Final.ipynb`** - Working notebook with:
  - Educational content (LangChain, FAISS, RAG, Embeddings overview)
  - Assignment structure ready for implementation
  - All 6 steps to complete

## 🎯 Assignment Steps

Complete all 6 steps in order:

1. **Step 1**: Create an Assistant System Prompt
   - Choose a business context (e.g., "Tech Startup - AI Consultant")
   - Design system prompt defining AI role

2. **Step 2**: Generate Business Database Content
   - Use Mistral-7B to create 10-15 Q&A pairs
   - Cover different aspects of your chosen business

3. **Step 3**: Implement FAISS Vector Database
   - Convert Q&A database into embeddings
   - Build FAISS index for similarity search

4. **Step 4**: Create Test Questions
   - Generate answerable questions (from database)
   - Generate unanswerable questions (outside database)

5. **Step 5**: Implement and Test Questions
   - Test RAG system with both question types
   - Document results and performance

6. **Step 6**: Model Experimentation and Ranking
   - Test with 4+ QA models from Hugging Face
   - Rank models by performance
   - Compare accuracy, confidence, speed

## 📖 How to Use

1. **Prerequisites**: Complete Week 1 and Week 2 exercises first
2. **Read Specification**: Review `rag-assignment-specification.md` thoroughly
3. **Open Notebook**: Work in `W3_RAG_Assignment_Final.ipynb`
4. **Follow Steps**: Complete all 6 steps in order
5. **Submit**: Submit your completed notebook

## 📚 Prerequisites

- ✅ **Week 1**: Prompt Engineering completed
- ✅ **Week 2**: Simple RAG exercise completed
- ✅ **Week 3 Exercise**: RAG with Model Evaluation exercise completed
- ✅ HuggingFace token ready (get from https://huggingface.co/settings/tokens)
- ✅ Google Colab or local environment (GPU recommended)

## 🎯 Evaluation Criteria

- **Creativity** in business context and agentic role design
- **Technical Implementation** of RAG pipeline with FAISS
- **Quality Analysis** of different Q&A models
- **Clear Documentation** with meaningful comments
- **Critical Thinking** in model comparison and limitations analysis

