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

### From the Project: `data_processor.py`

```python
def create_embeddings(self, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """
    Create embeddings for a list of texts using OpenAI.
    
    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model to use
        
    Returns:
        List of embedding vectors
    """
    # OpenAI embeddings API call
    response = self.embeddings_model.embeddings.create(
        model=model,
        input=texts
    )
    
    embeddings = [item.embedding for item in response.data]
    return embeddings
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

### From the Project: `data_processor.py`

```python
def build_vector_store(self, chunks: List[str], metadata: Optional[List[Dict]] = None, 
                       model: str = "text-embedding-3-small"):
    """
    Build a vector store from text chunks using OpenAI embeddings and FAISS.
    """
    # Step 1: Create embeddings for all chunks
    embeddings = self.create_embeddings(chunks, model)
    
    # Step 2: Convert to numpy array (FAISS requirement)
    embeddings_array = np.array(embeddings).astype('float32')
    dimension = embeddings_array.shape[1]
    
    # Step 3: Create FAISS index (using L2 distance)
    index = faiss.IndexFlatL2(dimension)
    
    # Step 4: Add vectors to index
    index.add(embeddings_array)
    
    # Step 5: Store index, chunks, and metadata
    self.vector_store = index
    self.text_chunks = chunks
    self.metadata = metadata if metadata else [{"chunk_id": i} for i in range(len(chunks))]
```

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

### From the Project: `data_processor.py`

```python
def search_vectors(self, query: str, k: int = 5, 
                   model: str = "text-embedding-3-small") -> List[Dict[str, Any]]:
    """
    Search the vector store for similar chunks.
    """
    # Step 1: Create embedding for query
    query_embedding = self.create_embeddings([query], model)[0]
    query_vector = np.array([query_embedding]).astype('float32')
    
    # Step 2: Search FAISS index
    k = min(k, self.vector_store.ntotal)  # Don't exceed available vectors
    distances, indices = self.vector_store.search(query_vector, k)
    
    # Step 3: Format results with similarity scores
    results = []
    for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
        results.append({
            'chunk': self.text_chunks[idx],
            'score': float(distance),
            'similarity': float(1 / (1 + distance)),  # Convert distance to similarity
            'metadata': self.metadata[idx],
            'rank': i + 1
        })
    
    return results
```

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

```python
# L2 Distance: Lower = More Similar
# Range: [0, ∞)

# Conversion to Similarity Score
similarity = 1 / (1 + distance)
# Range: (0, 1]
# Higher = More Similar
```

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

### From the Project: `data_processor.py`

```python
def chunk_text(self, text: str, chunk_size: int = 1000, 
               overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap for context preservation.
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Overlap preserves context
    
    return chunks
```

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

---

## 8. Metadata Tracking

### Why Track Metadata?

- **Citation**: Know where information came from
- **Filtering**: Search within specific sources
- **Ranking**: Use metadata for result ranking

### From the Project: `app.py`

```python
# Creating metadata for user notes
metadata = [
    {
        "chunk_id": i, 
        "file": uploaded_file.name, 
        "source": "user_notes"
    } 
    for i in range(len(chunks))
]

# Later, in search results:
for result in search_results:
    citation = {
        'source': result['metadata'].get('file', 'Unknown'),
        'chunk_id': result['metadata'].get('chunk_id'),
        'similarity': result['similarity'],
        'excerpt': result['chunk'][:200]
    }
```

---

## 9. Persistence: Save/Load Vector Store

### From the Project: `data_processor.py`

```python
def save_vector_store(self, file_path: str):
    """Save vector store to disk using pickle."""
    save_data = {
        'vector_store': self.vector_store,
        'text_chunks': self.text_chunks,
        'metadata': self.metadata
    }
    
    with open(file_path, 'wb') as f:
        pickle.dump(save_data, f)

def load_vector_store(self, file_path: str):
    """Load vector store from disk."""
    with open(file_path, 'rb') as f:
        save_data = pickle.load(f)
    
    self.vector_store = save_data['vector_store']
    self.text_chunks = save_data['text_chunks']
    self.metadata = save_data.get('metadata', [])
```

---

## 10. Best Practices Demonstrated

### ✅ Do's

1. **Validate availability** before using FAISS/OpenAI
2. **Track metadata** for citations
3. **Use overlap** in chunking for context
4. **Convert distances** to intuitive similarity scores
5. **Handle edge cases** (empty results, API failures)

### ❌ Don'ts

1. Don't embed without checking API key
2. Don't use large chunks (reduces precision)
3. Don't ignore token limits
4. Don't store vectors without corresponding text

---

## 11. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **Embeddings** | Dense vectors capture semantic meaning |
| **FAISS** | Efficient similarity search at scale |
| **Chunking** | Overlap preserves context between chunks |
| **L2 Distance** | Lower distance = higher similarity |
| **Metadata** | Essential for citations and filtering |

---

## Related Concepts

- [Tokenization](./01-project-overview.md) - Text preprocessing before embedding
- [RAG Pipeline](./05-rag-pipeline.md) - How embeddings power retrieval
- [Prompt Engineering](./03-prompt-engineering.md) - Using retrieved context
