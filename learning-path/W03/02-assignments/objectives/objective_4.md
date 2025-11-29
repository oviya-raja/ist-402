## Objective 4: Build Complete RAG Pipeline

### 🎯 Goal
Build a complete RAG (Retrieval-Augmented Generation) pipeline that combines semantic search with LLM generation, enabling accurate, context-aware responses grounded in the knowledge base.

<details>
<summary><b>📥 Prerequisites</b> (Click to expand)</summary>

| Item | Source | Required | Description |
|------|--------|----------|-------------|
| `env` | Objective 0 | ✅ Yes | Environment configuration and timing system |
| `inference_engine` | Objective 1 | ✅ Yes | Model loading and generation (100% reuse) |
| `system_prompt` | Objective 1 | ✅ Yes | System prompt for RAG context |
| `qa_database` | Objective 2 | ✅ Yes | Knowledge base Q&A pairs |
| `embedding_model` | Objective 3 | ✅ Yes | SentenceTransformer for embeddings |
| `faiss_index` | Objective 3 | ✅ Yes | FAISS vector index for retrieval |
| `embed_query()` | Objective 3 | ✅ Yes | Function to convert queries to embeddings |

**Note:** Objectives 0, 1, 2, and 3 must be completed first. Achieves **100% component reuse**.

</details>

<br>

<details>
<summary><b>🔧 Core Concepts</b> (Click to expand)</summary>

| Concept | Description |
|--------|-------------|
| **RAG (Retrieval-Augmented Generation)** | Combines retrieval (accurate, up-to-date info) with generation (natural responses). Grounds answers in knowledge base, reducing hallucinations |
| **Query Processing** | Convert user question to embedding using `embed_query()` from Objective 3 |
| **Retrieval** | Use FAISS to find top-k most similar Q&A pairs from knowledge base |
| **Augmentation** | Combine retrieved context with system prompt and user query |
| **Generation** | Use `inference_engine` from Objective 1 to generate response with Mistral model |
| **Pipeline Orchestration** | Complete end-to-end flow: Query → Embed → Retrieve → Augment → Generate |

**Why This Matters:**
RAG systems combine the best of both worlds: accurate retrieval from a knowledge base and natural language generation. This allows the system to provide up-to-date, accurate answers while maintaining conversational quality.

</details>

<br>

<details>
<summary><b>📊 Design Choices</b> (Click to expand)</summary>

| Choice | Selected | Rationale |
|--------|----------|-----------|
| **Generation Model** | `inference_engine` from Objective 1 | 100% reuse - no duplicate model loading |
| **Top-K Retrieval** | 3 documents | Balances context richness with prompt length |
| **Max Tokens** | 300 | Allows comprehensive answers without verbosity |
| **Temperature** | 0.7 | Balanced creativity and coherence for QA |
| **Similarity Threshold** | 0.3 | Filters irrelevant results while being inclusive |

**Why This Approach:**
- **100% Component Reuse**: Uses `inference_engine` from Objective 1, `embed_query()` from Objective 3, `qa_database` from Objective 2
- **Modular Design**: Each pipeline step is a separate function, following SRP
- **Top-3 Retrieval**: Provides sufficient context without overwhelming the prompt
- **Temperature 0.7**: Allows natural variation while staying on-topic

</details>

<br>

<details>
<summary><b>📤 Outputs</b> (Click to expand)</summary>

**Files Created:**
| File | Location | Description |
|------|----------|-------------|
| `rag_test_results.csv` | `data/rag_pipeline/` | Test results for answerable and unanswerable questions |
| `pipeline_config.txt` | `data/rag_pipeline/` | RAG pipeline configuration parameters |

**Global Functions:**
- `rag_query(query)` - Complete RAG pipeline entry point
- `search_faiss()`, `format_context()`, `build_prompt()`, `generate_response()` - Pipeline components
- `embed_query()` - Reused from Objective 3

</details>

<br>

<details>
<summary><b>📋 FAISS Index Details</b> (Click to expand)</summary>

**Pipeline Components:**

| Component | Source | Purpose |
|-----------|--------|---------|
| **embed_query()** | Objective 3 | Convert user query to embedding vector |
| **search_faiss()** | Objective 4 | Search FAISS index for similar Q&A pairs |
| **format_context()** | Objective 4 | Format retrieved Q&A as context string |
| **build_prompt()** | Objective 4 | Combine system prompt + context + query |
| **generate_response()** | Objective 4 | Uses `inference_engine` from Objective 1 |

**100% Component Reuse:**
- **inference_engine** from Objective 1 - Model loading and generation
- **embed_query()** from Objective 3 - Query embedding
- **faiss_index** from Objective 3 - Vector search
- **qa_database** from Objective 2 - Knowledge base
- **system_prompt** from Objective 1 - Context for generation

</details>

<br>

<details>
<summary><b>📚 Learning Objectives Demonstrated</b> (Click to expand)</summary>

1. **RAG Architecture**: Complete pipeline from query to response
2. **Component Reuse**: 100% reuse of components from Objectives 0-3
3. **Pipeline Orchestration**: Coordinating retrieval and generation steps
4. **Context Augmentation**: Combining retrieved knowledge with user queries
5. **Error Handling**: Graceful handling of unanswerable questions

</details>

<br>

<details>
<summary><b>💡 Tips</b> (Click to expand)</summary>

- **Component Reuse**: All components from Objectives 0-3 are reused - no duplicate code
- **inference_engine**: Reuses cached model from Objective 1 for fast generation
- **Top-K Selection**: Top-3 provides good context balance without overwhelming the prompt
- **Temperature**: 0.7 allows natural variation while maintaining accuracy
- **Similarity Threshold**: 0.3 filters irrelevant results while being inclusive
- **Error Handling**: Gracefully handles unanswerable questions and errors

</details>

---

**Next Step:** Proceed to Objective 5 for model evaluation and ranking.

