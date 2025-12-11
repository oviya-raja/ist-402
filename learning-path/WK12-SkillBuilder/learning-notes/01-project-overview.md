# WK12-SkillBuilder: Project Overview & Architecture

## Course Context
**Course:** IST-402 | **Week:** 12  
**Project Type:** Full-Stack GenAI Application

---

## 1. Project Purpose

The Skill Builder application demonstrates a production-ready GenAI system that integrates multiple AI/ML concepts into a cohesive learning tool for IST402 students.

### Core Capabilities
- **Concept Explainer**: RAG-powered explanations with semantic search
- **Quiz Generator**: AI-generated assessments with structured JSON output
- **Study Plan Generator**: Personalized learning paths using prompt engineering
- **Vector Search**: FAISS-based semantic similarity search
- **External API Integration**: OpenAI Web Search for real-time data

---

## 2. Architecture Patterns

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│         (Streamlit UI - app.py)         │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Application Layer               │
│    (Orchestration & Business Logic)     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Core Services                 │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐  │
│  │  Data   │ │ Prompt  │ │ Content  │  │
│  │Processor│ │Engineer │ │Generator │  │
│  └─────────┘ └─────────┘ └──────────┘  │
│  ┌─────────────┐ ┌──────────────────┐  │
│  │     API     │ │      Logger      │  │
│  │ Integration │ │                  │  │
│  └─────────────┘ └──────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         External Services               │
│   OpenAI API | FAISS | File System      │
└─────────────────────────────────────────┘
```

### Key Design Principles Applied

| Principle | Implementation |
|-----------|----------------|
| **Single Responsibility** | Each module handles one concern (data, prompts, generation) |
| **Dependency Injection** | Session state manages component lifecycle |
| **Interface Segregation** | Clean APIs between modules |
| **Open/Closed** | Extensible prompt types via PromptType enum |

---

## 3. Module Responsibilities

### `data_processor.py`
- CSV/Text file ingestion
- Data validation and preprocessing
- Vector store management (FAISS)
- Embedding generation (OpenAI)
- Semantic search operations

### `prompt_engineer.py`
- Prompt template management
- Few-shot example handling
- Chain-of-thought augmentation
- Dynamic prompt construction

### `content_generator.py`
- LangChain integration
- OpenAI model management
- Token usage tracking
- Response generation

### `api_integration.py`
- External API management
- OpenAI Web Search integration
- News/Conference data retrieval
- Context formatting

### `logger.py`
- Centralized logging
- API call monitoring
- Error tracking with context
- Daily log rotation

---

## 4. Data Flow: RAG Pipeline

```
User Query
    │
    ▼
┌─────────────────┐
│  1. RETRIEVAL   │
│  ─────────────  │
│  • Vector search│
│  • IST concepts │
│  • User notes   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. AUGMENTATION │
│  ─────────────  │
│  • Combine ctx  │
│  • Build prompt │
│  • Add metadata │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. GENERATION   │
│  ─────────────  │
│  • LLM call     │
│  • Parse output │
│  • Add citations│
└────────┬────────┘
         │
         ▼
    Response + Citations
```

---

## 5. Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **UI** | Streamlit | Interactive web interface |
| **LLM Orchestration** | LangChain | Model management, callbacks |
| **Vector Store** | FAISS | Similarity search |
| **Embeddings** | OpenAI text-embedding-3-small | Text vectorization |
| **Generation** | OpenAI GPT-4o-mini | Content generation |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Configuration** | PyYAML, python-dotenv | Config management |

---

## 6. Key Learnings

### What This Project Demonstrates

1. **RAG Implementation**: Complete retrieval-augmented generation pipeline
2. **Vector Search**: Production-ready semantic search with FAISS
3. **Prompt Engineering**: Multiple techniques (few-shot, CoT, role-based)
4. **API Integration**: External data enrichment patterns
5. **Error Handling**: Comprehensive logging and graceful degradation
6. **State Management**: Session-based component lifecycle
7. **Modular Design**: Clean separation of concerns

### Production Considerations Shown

- Environment variable management
- API key validation
- Fallback handling
- Token usage tracking
- Cost monitoring
- Log rotation

---

## Next Notes

- [02-embeddings-vector-search.md](./02-embeddings-vector-search.md) - Deep dive into embeddings and FAISS
- [03-prompt-engineering.md](./03-prompt-engineering.md) - Prompt design patterns
- [04-langchain-integration.md](./04-langchain-integration.md) - LangChain usage patterns
- [05-rag-pipeline.md](./05-rag-pipeline.md) - RAG implementation details
