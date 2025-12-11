# WK12-SkillBuilder Learning Notes

## 📚 IST-402 GenAI Application Development

These learning notes are derived from hands-on implementation of the **Skill Builder for IST Students** project—a production-ready GenAI application demonstrating RAG, vector search, prompt engineering, and LangChain integration.

---

## 📑 Table of Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Project Overview](./01-project-overview.md) | Architecture, design patterns, module responsibilities |
| 02 | [Embeddings & Vector Search](./02-embeddings-vector-search.md) | OpenAI embeddings, FAISS, similarity search, chunking |
| 03 | [Prompt Engineering](./03-prompt-engineering.md) | Templates, few-shot, chain-of-thought, JSON output |
| 04 | [LangChain Integration](./04-langchain-integration.md) | ChatOpenAI, messages, callbacks, token tracking |
| 05 | [RAG Pipeline](./05-rag-pipeline.md) | Retrieval, augmentation, generation, citations |
| 06 | [API Integration](./06-api-integration-error-handling.md) | Error handling, logging, manager pattern |

---

## 🎯 Learning Objectives Covered

### Week 00 Concepts
- [x] Tokenization fundamentals
- [x] Embeddings and vector representations
- [x] Attention mechanisms (conceptual)
- [x] Tensor operations with NumPy

### Week 01 Concepts
- [x] Prompt engineering techniques
- [x] Zero-shot and few-shot learning
- [x] Chain-of-thought prompting
- [x] Temperature and sampling

### Week 02 Concepts
- [x] RAG foundations
- [x] Data engineering for RAG
- [x] Vector databases (FAISS)

### Week 03 Concepts
- [x] Production RAG patterns
- [x] Context window management
- [x] Multi-source retrieval

### Week 05 Concepts
- [x] Cost optimization (token tracking)
- [x] Inference considerations

### Week 06 Concepts
- [x] Error handling patterns
- [x] Input validation
- [x] API safety patterns

---

## 🛠️ Technologies Demonstrated

| Technology | Purpose | Notes File |
|------------|---------|------------|
| **Streamlit** | Web UI | [01](./01-project-overview.md) |
| **LangChain** | LLM orchestration | [04](./04-langchain-integration.md) |
| **OpenAI** | Embeddings & generation | [02](./02-embeddings-vector-search.md), [04](./04-langchain-integration.md) |
| **FAISS** | Vector similarity search | [02](./02-embeddings-vector-search.md) |
| **Pandas** | Data processing | [01](./01-project-overview.md) |

---

## 📊 Key Patterns & Flow Diagrams

### RAG Pipeline Pattern

```
Query → Embed → Search → Filter → Augment → Generate → Cite
```

### Vector Search Pattern Flow

```
Text Chunks → Embeddings → FAISS Index → Search → Results
```

### Prompt Template Pattern Flow

```
Template + Parameters → Format → Enhance → Send to LLM
```

---

## 📈 Study Path

### Recommended Reading Order

1. **Start Here**: [01-project-overview.md](./01-project-overview.md)
   - Understand the big picture
   - See how components connect

2. **Foundation**: [02-embeddings-vector-search.md](./02-embeddings-vector-search.md)
   - Core concept for RAG
   - FAISS implementation

3. **Prompts**: [03-prompt-engineering.md](./03-prompt-engineering.md)
   - Design effective prompts
   - Get structured outputs

4. **Generation**: [04-langchain-integration.md](./04-langchain-integration.md)
   - LangChain usage
   - Token management

5. **Integration**: [05-rag-pipeline.md](./05-rag-pipeline.md)
   - Full RAG flow
   - Multi-source retrieval

6. **Production**: [06-api-integration-error-handling.md](./06-api-integration-error-handling.md)
   - Error handling
   - API patterns

---

## 🔗 Quick Reference

### Embedding Model
- Model: `text-embedding-3-small`
- Dimensions: 1536
- Cost: $0.02/1M tokens

### Generation Model
- Model: `gpt-4o-mini`
- Default for cost-effectiveness
- Temperature: 0.0-1.0 range

### Similarity Threshold
- Threshold: 0.3 (30%)
- Filters irrelevant results
- Balances precision and recall

### Chunk Size
- Chunk Size: 1000 characters
- Overlap: 200 characters
- Preserves context between chunks

---

## 📝 Project Source

These notes are based on the **WK12-SkillBuilder** project:
- Full-stack Streamlit application
- RAG-powered concept explainer
- Multi-source vector search
- Quiz generation with JSON parsing
- Study plan generation
- AI conference discovery

---

## 🎓 Course Information

**Course**: IST-402  
**Week**: 12 - GenAI Application Development  
**Focus**: Production GenAI patterns and implementation

---

*Last Updated: December 2024*
