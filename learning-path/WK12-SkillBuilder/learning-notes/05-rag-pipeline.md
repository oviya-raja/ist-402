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

## 3. RAG Implementation in the Project

### Complete RAG Flow (From `app.py`)

The Concept Explainer demonstrates a full RAG pipeline:

```python
# STEP 1: RETRIEVAL - Vector search on IST concepts
if st.session_state.data_processor.vector_store:
    search_results = st.session_state.data_processor.search_vectors(
        query=f"{selected_concept} concept explanation learning objectives",
        k=5,
        model="text-embedding-3-small"
    )
    
    # Extract related concepts
    related_concepts = []
    for result in search_results:
        concept_name = result.get('metadata', {}).get('concept_name', '')
        if concept_name and concept_name.lower() != selected_concept.lower():
            related_concepts.append(concept_name)

# STEP 2: RETRIEVAL - Search user notes (second knowledge base)
if st.session_state.user_notes_processor.vector_store:
    user_notes_results = st.session_state.user_notes_processor.search_vectors(
        query=f"{selected_concept} explanation notes learning",
        k=3,
        model="text-embedding-3-small"
    )
    
    # Extract relevant chunks for augmentation
    user_notes_chunks = []
    for result in user_notes_results:
        if result.get('similarity', 0) > 0.3:  # Relevance threshold
            user_notes_chunks.append(result.get('chunk', '')[:500])

# STEP 3: AUGMENTATION - Combine all context
description = concept_info.get('description', '')
if related_concepts:
    description += f"\n\nRelated concepts: {', '.join(related_concepts)}"
if user_notes_chunks:
    description += f"\n\nFrom your notes:\n" + "\n".join(user_notes_chunks)

# STEP 4: GENERATION - Generate with enhanced context
result = st.session_state.generator.generate_with_prompt_type(
    prompt_type=PromptType.IST_CONCEPT_EXPLANATION,
    concept_name=concept_info.get('concept_name'),
    description=description,  # Augmented with retrieved context
    # ... other parameters
)
```

---

## 4. Multi-Source Retrieval

### The Project Uses Two Vector Stores

```
┌─────────────────────────────────────────────────────────────┐
│                    RETRIEVAL SOURCES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │  IST Concepts DB    │    │  User Notes         │        │
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

```python
# Basic approach
enhanced_prompt = f"{original_query}\n\nContext:\n{retrieved_text}"
```

### Strategy 2: Structured Context (Used in Project)

```python
# More organized approach
description = concept_info.get('description', '')

# Add related concepts
if related_concepts:
    description += f"\n\nRelated concepts found via vector search: {', '.join(related_concepts)}"

# Add user notes
if user_notes_context:
    description += f"\n\nRelevant information from your learning notes:\n{user_notes_context}"

# Pass to prompt template
prompt_kwargs = {
    'concept_name': concept_name,
    'description': description,  # Contains all augmented context
    # ...
}
```

### Strategy 3: Explicit Context Sections

```python
prompt = f"""
CONCEPT: {concept_name}

BASE INFORMATION:
{base_description}

RELATED CONCEPTS (from knowledge base):
{related_concepts_text}

YOUR NOTES (relevant excerpts):
{user_notes_text}

Based on all the above, provide a comprehensive explanation...
"""
```

---

## 6. Relevance Filtering

### Similarity Threshold

```python
# From the project: Filter by similarity score
for result in user_notes_results:
    similarity = result.get('similarity', 0)
    
    # Only include if similarity is reasonable
    if similarity > 0.3:  # Threshold for relevance
        user_notes_chunks.append(result.get('chunk', '')[:500])
```

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

```python
# From the project: Build citation data during retrieval
user_notes_citations = []
for idx, result in enumerate(user_notes_results, 1):
    chunk_text = result.get('chunk', '')
    similarity = result.get('similarity', 0)
    metadata = result.get('metadata', {})
    
    if similarity > 0.3:
        user_notes_citations.append({
            'source': metadata.get('file', 'Your Notes'),
            'chunk_id': metadata.get('chunk_id', idx),
            'similarity': similarity,
            'excerpt': chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
        })
```

### Displaying Citations

```python
# From app.py: Show citations after response
if user_notes_citations:
    st.subheader("📚 References from Your Learning Notes")
    
    for idx, citation in enumerate(user_notes_citations, 1):
        with st.expander(f"📝 Reference {idx}: {citation['source']}"):
            st.markdown(f"**Source:** {citation['source']}")
            st.markdown(f"**Chunk ID:** {citation['chunk_id']}")
            st.markdown(f"**Relevance Score:** {citation['similarity']:.1%}")
            st.markdown("**Excerpt:**")
            st.text(citation['excerpt'])
```

---

## 8. Knowledge Base Preparation

### IST Concepts Vector Store (From `app.py`)

```python
def load_ist_concepts():
    """Load IST concepts and build vector store."""
    
    # Load CSV data
    ist_concepts_df = data_processor.load_ist_concepts("data/ist_concepts.csv")
    
    # Create text chunks from concept information
    concept_chunks = []
    concept_metadata = []
    
    for idx, row in ist_concepts_df.iterrows():
        # Combine concept information into searchable text
        concept_text = f"""
        Concept: {row.get('concept_name', '')}
        Week: {row.get('week', '')}
        Description: {row.get('description', '')}
        Learning Objectives: {row.get('learning_objectives', '')}
        Prerequisites: {row.get('prerequisites', 'None')}
        Difficulty: {row.get('difficulty', '')}
        Keywords: {row.get('keywords', '')}
        """.strip()
        
        concept_chunks.append(concept_text)
        concept_metadata.append({
            'concept_name': row.get('concept_name', ''),
            'week': row.get('week', ''),
            'difficulty': row.get('difficulty', ''),
            'chunk_id': idx
        })
    
    # Build vector store
    data_processor.build_vector_store(
        chunks=concept_chunks,
        metadata=concept_metadata,
        model="text-embedding-3-small"
    )
```

### User Notes Vector Store

```python
# User uploads notes -> chunking -> embeddings -> vector store
if uploaded_file.name.endswith('.txt'):
    # Load text
    text = user_notes_processor.load_text_file(file_path)
    
    # Chunk text
    chunks = user_notes_processor.chunk_text(text, chunk_size=1000)
    
    # Create metadata for chunks
    metadata = [
        {"chunk_id": i, "file": uploaded_file.name, "source": "user_notes"} 
        for i in range(len(chunks))
    ]
    
    # Build vector store
    user_notes_processor.build_vector_store(
        chunks=chunks,
        metadata=metadata,
        model="text-embedding-3-small"
    )
```

---

## 9. RAG Query Processing Flow

### Complete Flow with Execution Logging

```python
# From app.py: Step-by-step RAG execution

# Step 1: User action
log_execution("Concept Explainer", "Generate Explanation button clicked", "⏳")

# Step 2: Initialize generator
if not st.session_state.generator:
    initialize_generator()
log_execution("Concept Explainer", "Content generator initialized", "✅")

# Step 3: RETRIEVAL - IST concepts vector store
log_execution("Concept Explainer", "RETRIEVAL - Semantic search on IST concepts", "⏳")
search_results = data_processor.search_vectors(query=..., k=5)
log_execution("Concept Explainer", "RETRIEVAL - Completed", "✅", 
              f"Found {len(related_concepts)} related concepts")

# Step 4: RETRIEVAL - User notes vector store
log_execution("Concept Explainer", "RETRIEVAL - Searching user notes", "⏳")
user_notes_results = user_notes_processor.search_vectors(query=..., k=3)
log_execution("Concept Explainer", "RETRIEVAL - User notes completed", "✅")

# Step 5: Identify related concepts
log_execution("Concept Explainer", "Identifying related concepts", "✅")

# Step 6: Load concept info from database
log_execution("Concept Explainer", "Loading concept from database", "✅")

# Step 7: AUGMENTATION - Combine context
log_execution("Concept Explainer", "AUGMENTATION - Combining context", "⏳")
# ... context combination logic ...
log_execution("Concept Explainer", "AUGMENTATION - Context combined", "✅")

# Step 8: GENERATION - Generate with LLM
log_execution("Concept Explainer", "GENERATION - Generating explanation", "⏳")
result = generator.generate_with_prompt_type(...)
log_execution("Concept Explainer", "GENERATION - Complete", "✅", 
              f"Model: {model}, Tokens: {tokens}")

# Step 9: Display with citations
log_execution("Concept Explainer", "Displaying with citations", "✅")
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

```python
# Try primary source, fallback to alternatives
results = primary_vector_store.search(query, k=5)
if not results or max_similarity < 0.3:
    results = secondary_vector_store.search(query, k=5)
if not results:
    # Generate without RAG context
    results = []
```

### Pattern 2: Query Expansion

```python
# Generate multiple query variations
queries = [
    original_query,
    f"{concept_name} definition",
    f"{concept_name} explanation examples"
]

all_results = []
for q in queries:
    results = vector_store.search(q, k=3)
    all_results.extend(results)

# Deduplicate and rank
unique_results = deduplicate(all_results)
```

### Pattern 3: Context Window Management

```python
# Limit context to avoid token limits
MAX_CONTEXT_TOKENS = 2000

context_chunks = []
total_tokens = 0

for result in sorted_results:
    chunk_tokens = estimate_tokens(result['chunk'])
    if total_tokens + chunk_tokens <= MAX_CONTEXT_TOKENS:
        context_chunks.append(result['chunk'])
        total_tokens += chunk_tokens
    else:
        break  # Stop adding context
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
