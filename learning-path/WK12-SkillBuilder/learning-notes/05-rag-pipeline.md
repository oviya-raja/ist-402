# RAG Pipeline Implementation

## Course Context
**Concepts:** RAG Foundations, RAG Production, Agentic RAG  
**Related Weeks:** W02 (RAG Foundations), W03 (RAG Production), W09 (Agentic RAG)

---

## 1. What is RAG?

**Retrieval-Augmented Generation (RAG)** combines:
- **Retrieval**: Finding relevant information from a knowledge base
- **Augmentation**: Adding retrieved context to the prompt
- **Generation**: Using an LLM to produce the final response

### Why RAG?

| Problem | RAG Solution |
|---------|--------------|
| LLM knowledge cutoff | Retrieve current information |
| Hallucinations | Ground responses in facts |
| Domain specificity | Use custom knowledge bases |
| Transparency | Cite sources |

---

## 2. RAG Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query: "Explain RAG concept"                              │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    1. RETRIEVAL                          │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │    │
│  │  │ Embed Query  │───►│ Vector Search│───►│ Top-K     │  │    │
│  │  │              │    │ (FAISS)      │    │ Results   │  │    │
│  │  └──────────────┘    └──────────────┘    └───────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   2. AUGMENTATION                        │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │    │
│  │  │ Original     │ +  │ Retrieved    │ =  │ Enhanced  │  │    │
│  │  │ Query        │    │ Context      │    │ Prompt    │  │    │
│  │  └──────────────┘    └──────────────┘    └───────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    3. GENERATION                         │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │    │
│  │  │ Enhanced     │───►│ LLM          │───►│ Response  │  │    │
│  │  │ Prompt       │    │ (GPT-4o-mini)│    │+ Citations│  │    │
│  │  └──────────────┘    └──────────────┘    └───────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Complete RAG Flow Steps

The Concept Explainer demonstrates a full RAG pipeline with these steps:

### Step-by-Step Process

1. **User Action**: User clicks "Generate Explanation" button
2. **Initialize Generator**: Check/create content generator
3. **RETRIEVAL - IST Concepts**: Search IST concepts vector store
4. **RETRIEVAL - User Notes**: Search user's learning notes vector store
5. **RETRIEVAL - Identify Related**: Extract related concepts from results
6. **RETRIEVAL - Load Database**: Load concept info from CSV database
7. **AUGMENTATION - Combine Context**: Merge all retrieved information
8. **GENERATION - LLM Call**: Generate explanation with enhanced context
9. **Display with Citations**: Show response with source references

---

## 4. Multi-Source Retrieval

### The Project Uses Two Vector Stores

```
┌─────────────────────────────────────────────────────────────┐
│                    RETRIEVAL SOURCES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │  IST Concepts DB    │    │  User Notes       │        │
│  │  (Built at startup) │    │  (Uploaded by user) │        │
│  │                     │    │                     │        │
│  │  • Course concepts  │    │  • Personal notes   │        │
│  │  • Learning obj.    │    │  • Study materials  │        │
│  │  • Prerequisites    │    │  • Custom context   │        │
│  └──────────┬──────────┘    └──────────┬──────────┘        │
│             │                          │                    │
│             ▼                          ▼                    │
│       ┌─────────────────────────────────────┐              │
│       │        Vector Search Results         │              │
│       │   (Combined context for generation)  │              │
│       └─────────────────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Benefits of Multi-Source RAG

| Benefit | Description |
|---------|-------------|
| **Comprehensive** | Multiple knowledge sources |
| **Personalized** | User notes customize responses |
| **Accurate** | Official content + personal context |
| **Traceable** | Citations from both sources |

---

## 5. Context Augmentation Strategies

### Strategy 1: Simple Concatenation

```
Enhanced Prompt = Original Query + "\n\nContext:\n" + Retrieved Text
```

### Strategy 2: Structured Context (Used in Project)

```
Base Description
    │
    ▼
┌─────────────────┐
│ Add Related     │
│ Concepts        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Add User Notes  │
│ Excerpts        │
└────────┬────────┘
         │
         ▼
    Final Prompt
```

### Strategy 3: Explicit Context Sections

```
CONCEPT: {concept_name}

BASE INFORMATION:
{base_description}

RELATED CONCEPTS (from knowledge base):
{related_concepts_text}

YOUR NOTES (relevant excerpts):
{user_notes_text}

Based on all the above, provide a comprehensive explanation...
```

---

## 6. Relevance Filtering

### Similarity Threshold

Only include search results with similarity score > 0.3 (30%)

### Why Filter?

```
Query: "What is RAG?"

Search Results:
┌─────────────────────────────────────────────┐
│ Rank 1: "RAG combines retrieval..."         │ ← sim: 0.92 ✓ Include
│ Rank 2: "Retrieval-augmented generation..." │ ← sim: 0.87 ✓ Include
│ Rank 3: "LLMs use attention mechanisms..."  │ ← sim: 0.45 ✓ Include
│ Rank 4: "My weekend hiking trip..."         │ ← sim: 0.15 ✗ Exclude
│ Rank 5: "Recipe for chocolate cake..."      │ ← sim: 0.08 ✗ Exclude
└─────────────────────────────────────────────┘
```

### Threshold Selection

| Threshold | Effect |
|-----------|--------|
| 0.1 - 0.2 | Very permissive, more noise |
| 0.3 - 0.4 | Balanced (used in project) |
| 0.5 - 0.6 | Strict, might miss relevant |
| 0.7+ | Very strict, high precision |

---

## 7. Citation Generation

### Tracking Sources for Citations

During retrieval, build citation data:
- Source file name
- Chunk ID
- Similarity score
- Excerpt from chunk

### Citation Display Flow

```
Search Results
    │
    ▼
┌─────────────────┐
│ Extract Metadata│
│ • File name     │
│ • Chunk ID      │
│ • Similarity    │
│ • Excerpt       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Citation  │
│ Object          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Display to User │
│ (Expandable)    │
└─────────────────┘
```

---

## 8. Knowledge Base Preparation

### IST Concepts Vector Store Preparation Steps

1. **Load CSV**: Read IST concepts from CSV file
2. **Create Text Chunks**: Combine concept information into searchable text
3. **Generate Embeddings**: Convert chunks to vectors
4. **Build FAISS Index**: Create vector store
5. **Store Metadata**: Track concept names, weeks, difficulty

### User Notes Vector Store Preparation Steps

1. **Upload File**: User uploads TXT, CSV, or Markdown file
2. **Load Document**: Use LangChain loaders (for MD/TXT)
3. **Chunk Text**: Use LangChain RecursiveCharacterTextSplitter
4. **Generate Embeddings**: Create vectors for chunks
5. **Build FAISS Index**: Create vector store
6. **Store Metadata**: Track file name, chunk IDs, source

---

## 9. RAG Query Processing Flow

### Complete Flow with Execution Logging

```
Step 1: User Action
    │
    ▼
Step 2: Initialize Generator
    │
    ▼
Step 3: RETRIEVAL - IST Concepts Vector Store
    │
    ▼
Step 4: RETRIEVAL - User Notes Vector Store
    │
    ▼
Step 5: RETRIEVAL - Identify Related Concepts
    │
    ▼
Step 6: RETRIEVAL - Load Concept from Database
    │
    ▼
Step 7: AUGMENTATION - Combine All Context
    │
    ▼
Step 8: GENERATION - Generate with LLM
    │
    ▼
Step 9: Display with Citations
```

---

## 10. RAG Evaluation Considerations

### Quality Metrics

| Metric | Description | How to Measure |
|--------|-------------|----------------|
| **Retrieval Precision** | Relevant results / Total results | Check if retrieved chunks are useful |
| **Retrieval Recall** | Found relevant / Total relevant | Check if important info was found |
| **Answer Relevance** | Does answer address query? | Human evaluation or LLM judge |
| **Faithfulness** | Is answer grounded in context? | Check for hallucinations |

### Improving RAG Quality

1. **Better Chunking**: Optimize chunk size and overlap
2. **Query Expansion**: Rephrase queries for better retrieval
3. **Reranking**: Re-score results before augmentation
4. **Hybrid Search**: Combine semantic + keyword search
5. **Context Compression**: Summarize long context

---

## 11. Production RAG Patterns

### Pattern 1: Fallback Chain

```
Try Primary Source
    │
    ▼
┌─────────────────┐
│ Results Found?  │
│ Similarity OK?  │
└────────┬────────┘
         │
    ┌────┴────┐
   Yes       No
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Use    │ │ Try Secondary│
│ Results│ │ Source       │
└────────┘ └──────────────┘
```

### Pattern 2: Query Expansion

```
Original Query
    │
    ▼
┌─────────────────┐
│ Generate        │
│ Variations      │
│ • {query}       │
│ • {query} def   │
│ • {query} exp   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Search All      │
│ Variations      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Deduplicate     │
│ & Rank          │
└─────────────────┘
```

### Pattern 3: Context Window Management

```
Retrieved Results
    │
    ▼
┌─────────────────┐
│ Sort by         │
│ Similarity      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Add Chunks      │
│ Until Token     │
│ Limit Reached   │
└─────────────────┘
```

---

## 12. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **RAG Architecture** | Retrieval → Augmentation → Generation |
| **Multi-Source RAG** | Combine multiple knowledge bases |
| **Relevance Filtering** | Use similarity threshold to filter noise |
| **Citation Tracking** | Store metadata for source attribution |
| **Context Augmentation** | Structured context sections work best |
| **Production Patterns** | Fallbacks, query expansion, context limits |

---

## RAG Pipeline Summary

```
┌────────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE SUMMARY                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUT: User Query                                             │
│    │                                                            │
│    ▼                                                            │
│  RETRIEVAL                                                      │
│    • Embed query using OpenAI embeddings                       │
│    • Search IST concepts vector store (k=5)                    │
│    • Search user notes vector store (k=3)                      │
│    • Filter by similarity threshold (>0.3)                     │
│    │                                                            │
│    ▼                                                            │
│  AUGMENTATION                                                   │
│    • Load concept info from CSV database                       │
│    • Append related concepts from vector search                │
│    • Append relevant user notes excerpts                       │
│    • Build structured prompt with all context                  │
│    │                                                            │
│    ▼                                                            │
│  GENERATION                                                     │
│    • Send enhanced prompt to GPT-4o-mini                       │
│    • Track token usage with callbacks                          │
│    • Generate response grounded in context                     │
│    │                                                            │
│    ▼                                                            │
│  OUTPUT: Response + Citations                                   │
│    • Display generated explanation                             │
│    • Show references from user notes                           │
│    • Include metadata (tokens, cost, model)                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Related Concepts

- [Embeddings & Vector Search](./02-embeddings-vector-search.md) - Foundation of retrieval
- [Prompt Engineering](./03-prompt-engineering.md) - Designing augmented prompts
- [LangChain Integration](./04-langchain-integration.md) - Generation implementation
