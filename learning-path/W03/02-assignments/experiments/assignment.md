# RAG-Based Question Answering System with Mistral

**Objective:** Design and implement a Retrieval-Augmented Generation (RAG) system using Mistral-7B-Instruct, FAISS vector database, and custom business data.

**Submission:** Submit the link to your completed notebook.

---

## 🎯 6 Objectives

### 1. Create Assistant System Prompt
- Design a system prompt with a specific role (e.g., "marketing expert for a tech startup")
- Choose a business context to use throughout the assignment
- Use `mistralai/Mistral-7B-Instruct-v0.3`

### 2. Generate Business Database Content
- Use Mistral to generate **10-15 Q&A pairs** for your chosen business
- Cover different aspects of the business
- **Add clear comments** showing the database pairs

### 3. Implement FAISS Vector Database
- Convert Q&A database to embeddings using sentence transformers
- Store embeddings in FAISS index for efficient similarity search
- **Comment the implementation process**

### 4. Create Test Questions
- Generate **5+ answerable** questions (can be answered from database)
- Generate **5+ unanswerable** questions (require information not in database)
- Use Mistral to generate both types

### 5. Implement and Test RAG System
- Build complete RAG pipeline (Query → Embed → Search → Retrieve → Augment → LLM → Answer)
- Run both question types through the pipeline
- **Comment differences** between answerable vs. unanswerable results

### 6. Model Experimentation and Ranking
- Test **4 required models + 2 of your choice** (6 total):
  - `consciousAI/question-answering-generative-t5-v1-base-s-q-c`
  - `deepset/roberta-base-squad2`
  - `google-bert/bert-large-cased-whole-word-masking-finetuned-squad`
  - `gasolsun/DynamicRAG-8B`
  - + 2 additional models of your choice
- **Rank models** by 5 metrics: **Accuracy**, **Confidence Handling**, **Quality**, **Speed**, **Robustness**
- Test with both answerable and unanswerable questions
- Compare performance across question types

---

## 🔧 Technical Requirements

**Installation:**
```python
!pip install transformers torch sentence-transformers faiss-cpu langchain
```

**Key Components:**
1. **System Prompt Design** - Clear agentic role definition
2. **Database Generation** - Mistral-generated business Q&A pairs (10-15 pairs)
3. **FAISS Implementation** - Vector storage and semantic search
4. **Question Testing** - Both answerable & unanswerable queries (5+ each)
5. **Model Comparison** - Performance analysis and ranking (6 models)
6. **Confidence Analysis** - Model uncertainty vs. output quality

---

## ✅ Deliverables

- ✅ **Business context** & role definition
- ✅ **Generated Q&A database** (10-15 pairs, clearly commented)
- ✅ **Working FAISS vector database** with embeddings
- ✅ **Test questions** (answerable vs. unanswerable, 5+ each)
- ✅ **RAG pipeline** implementation
- ✅ **Model rankings** with performance analysis (6 models)
- ✅ **Reflection** on strengths, weaknesses, and real-world applications

---

## 📊 Evaluation Criteria

- **Creativity** in business context and agentic role design
- **Technical Implementation** of RAG pipeline with FAISS
- **Quality Analysis** of different Q&A models
- **Clear Documentation** with meaningful comments
- **Critical Thinking** in model comparison and limitations analysis

---

## ⏱️ Estimated Time

- **CPU**: ~25-30 minutes
- **GPU**: ~15-20 minutes
- **Longest step**: Objective 6 (Model Evaluation) - 15-25 min

---

**Note:** Build a system deployable for real business use. Consider scalability, accuracy, and user experience.
