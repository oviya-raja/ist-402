# Embeddings & Vector Search with FAISS

## Course Context
**Concepts:** Embeddings, Vector Databases, Similarity Search  
**Related Weeks:** W00 (Embeddings), W02 (Vector Databases)

---

## 1. What Are Embeddings?

Embeddings are **dense vector representations** of text that capture semantic meaning in high-dimensional space.

### Key Properties

| Property | Description |
|----------|-------------|
| **Dimensionality** | Fixed-size vectors (e.g., 1536 for text-embedding-3-small) |
| **Semantic Encoding** | Similar meanings → similar vectors |
| **Distance Metrics** | L2 (Euclidean), Cosine similarity |
| **Compositionality** | Can combine/average embeddings |

### Why Embeddings Matter for RAG

```
Traditional Search: "machine learning" ≠ "ML algorithms"
Semantic Search:    "machine learning" ≈ "ML algorithms" (high similarity)
```

---

## 2. OpenAI Embeddings Implementation

### Process Flow

```
Text Input
    │
    ▼
┌─────────────────┐
│  OpenAI API     │
│  Embedding Call │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Output  │
│  [0.1, 0.3, ...]│
│  (1536 dims)    │
└─────────────────┘
```

### Model Comparison

| Model | Dimensions | Cost | Use Case |
|-------|------------|------|----------|
| `text-embedding-3-small` | 1536 | $0.02/1M tokens | General purpose, cost-effective |
| `text-embedding-3-large` | 3072 | $0.13/1M tokens | Higher accuracy, complex tasks |
| `text-embedding-ada-002` | 1536 | $0.10/1M tokens | Legacy, still widely used |

---

## 3. FAISS Vector Store

### What is FAISS?

**Facebook AI Similarity Search** - A library for efficient similarity search and clustering of dense vectors.

### Why FAISS?

- **Speed**: Optimized for large-scale search
- **Memory Efficient**: Various index types for different trade-offs
- **CPU/GPU Support**: Scales with hardware
- **Production Ready**: Used by Meta, widely adopted

### Index Types

| Index Type | Description | Use Case |
|------------|-------------|----------|
| `IndexFlatL2` | Exact L2 distance search | Small datasets, accuracy critical |
| `IndexFlatIP` | Inner product (cosine similarity) | Normalized vectors |
| `IndexIVFFlat` | Inverted file with flat storage | Large datasets, approximate |
| `IndexHNSW` | Hierarchical Navigable Small World | Fast approximate search |

---

## 4. Building the Vector Store

### Process Steps

1. **Create Embeddings**: Convert text chunks to vectors using OpenAI
2. **Convert to NumPy Array**: FAISS requires float32 numpy arrays
3. **Create FAISS Index**: Initialize index with vector dimension
4. **Add Vectors**: Populate index with embeddings
5. **Store Metadata**: Keep track of chunks and metadata

### Visual: Vector Store Creation

```
Text Chunks                    Embeddings                  FAISS Index
┌─────────────┐              ┌────────────┐              ┌────────────┐
│ "RAG is..." │  ──embed──►  │ [0.1, 0.3, │  ──add──►   │  Vector 0  │
└─────────────┘              │  0.2, ...]  │              ├────────────┤
┌─────────────┐              ├────────────┤              │  Vector 1  │
│ "LLMs use..."│  ──embed──► │ [0.4, 0.1, │  ──add──►   ├────────────┤
└─────────────┘              │  0.5, ...]  │              │  Vector 2  │
┌─────────────┐              ├────────────┤              ├────────────┤
│ "Tokens..." │  ──embed──►  │ [0.2, 0.7, │  ──add──►   │    ...     │
└─────────────┘              │  0.1, ...]  │              └────────────┘
```

---

## 5. Semantic Search Implementation

### Search Process Steps

1. **Embed Query**: Convert user query to embedding vector
2. **Search FAISS Index**: Find k most similar vectors using L2 distance
3. **Format Results**: Combine chunks, distances, and metadata
4. **Convert Distance to Similarity**: Make scores intuitive (higher = more similar)

### Visual: Search Process

```
Query: "What is RAG?"
         │
         ▼
┌─────────────────┐
│  Embed Query    │
│  [0.15, 0.35,   │
│   0.22, ...]    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────────────────┐
│  FAISS Search   │────►│  Compare with all vectors   │
│  (k=5)          │     │  using L2 distance          │
└────────┬────────┘     └─────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Results (sorted by similarity):            │
│  1. "RAG is retrieval..." (sim: 0.92)      │
│  2. "RAG combines..."     (sim: 0.87)      │
│  3. "Retrieval augmented" (sim: 0.81)      │
└─────────────────────────────────────────────┘
```

---

## 6. Distance to Similarity Conversion

### L2 Distance vs Similarity

**L2 Distance**: Lower = More Similar (Range: [0, ∞))

**Similarity Score**: Higher = More Similar (Range: (0, 1])

**Conversion Formula**: `similarity = 1 / (1 + distance)`

### Example Conversions

| L2 Distance | Similarity | Interpretation |
|-------------|------------|----------------|
| 0.0 | 1.0 | Identical |
| 0.5 | 0.67 | Very similar |
| 1.0 | 0.5 | Moderately similar |
| 2.0 | 0.33 | Somewhat related |
| 5.0 | 0.17 | Weakly related |

---

## 7. Text Chunking Strategy

### Why Chunk Text?

- **Token Limits**: Embeddings have max input size
- **Precision**: Smaller chunks = more precise retrieval
- **Context**: Need enough context for meaning

### Chunking Process (Using LangChain)

1. **Load Document**: Use LangChain document loaders (TextLoader, UnstructuredMarkdownLoader)
2. **Split Text**: Use RecursiveCharacterTextSplitter
3. **Preserve Context**: Overlap between chunks maintains continuity
4. **Store Chunks**: Keep chunks with metadata for retrieval

### Visual: Chunking with Overlap

```
Original Text (2500 chars):
┌────────────────────────────────────────────────────────────┐
│████████████████████████████████████████████████████████████│
└────────────────────────────────────────────────────────────┘

Chunk 1 (1000 chars):
┌─────────────────────────┐
│█████████████████████████│
└─────────────────────────┘

Chunk 2 (with 200 char overlap):
              ┌─────────────────────────┐
              │█████████████████████████│
              └─────────────────────────┘
              ↑
        Overlap region (200 chars)

Chunk 3:
                            ┌─────────────────────────┐
                            │█████████████████████████│
                            └─────────────────────────┘
```

### LangChain RecursiveCharacterTextSplitter

**Separators** (in order of preference):
1. `\n\n` - Paragraph breaks
2. `\n` - Line breaks
3. ` ` - Word boundaries
4. `""` - Character level (last resort)

**Benefits**:
- Preserves document structure
- Maintains context boundaries
- Handles markdown formatting
- Intelligent splitting

---

## 8. Metadata Tracking

### Why Track Metadata?

- **Citation**: Know where information came from
- **Filtering**: Search within specific sources
- **Ranking**: Use metadata for result ranking

### Metadata Structure

```
Metadata Example:
{
    "chunk_id": 5,
    "file": "my_notes.md",
    "source": "user_notes",
    "week": "W02"
}
```

### Citation Flow

```
Search Result
    │
    ▼
┌─────────────────┐
│  Extract Chunk  │
│  + Metadata     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Citation │
│  • Source file  │
│  • Chunk ID     │
│  • Similarity   │
│  • Excerpt      │
└────────┬────────┘
         │
         ▼
    Display to User
```

---

## 9. Persistence: Save/Load Vector Store

### Save Process

1. **Collect Data**: Vector store, text chunks, metadata
2. **Serialize**: Use pickle to save to disk
3. **Store Path**: Save with descriptive filename

### Load Process

1. **Read File**: Load pickle file from disk
2. **Deserialize**: Restore vector store, chunks, metadata
3. **Restore State**: Rebuild processor state

### Visual: Persistence Flow

```
Active Vector Store
    │
    ▼
┌─────────────────┐
│  Save to Disk   │
│  (pickle)       │
└────────┬────────┘
         │
         ▼
    .pkl File
         │
         ▼
┌─────────────────┐
│  Load from Disk │
│  (pickle)       │
└────────┬────────┘
         │
         ▼
    Restored Vector Store
```

---

## 10. Best Practices Demonstrated

### ✅ Do's

1. **Validate availability** before using FAISS/OpenAI
2. **Track metadata** for citations
3. **Use overlap** in chunking for context
4. **Convert distances** to intuitive similarity scores
5. **Handle edge cases** (empty results, API failures)
6. **Use LangChain** for intelligent text splitting

### ❌ Don'ts

1. Don't embed without checking API key
2. Don't use large chunks (reduces precision)
3. Don't ignore token limits
4. Don't store vectors without corresponding text
5. Don't skip metadata tracking

---

## 11. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **Embeddings** | Dense vectors capture semantic meaning |
| **FAISS** | Efficient similarity search at scale |
| **Chunking** | Overlap preserves context between chunks |
| **L2 Distance** | Lower distance = higher similarity |
| **Metadata** | Essential for citations and filtering |
| **LangChain** | Intelligent text splitting preserves structure |

---

## Related Concepts

- [Tokenization](./01-project-overview.md) - Text preprocessing before embedding
- [RAG Pipeline](./05-rag-pipeline.md) - How embeddings power retrieval
- [Prompt Engineering](./03-prompt-engineering.md) - Using retrieved context
