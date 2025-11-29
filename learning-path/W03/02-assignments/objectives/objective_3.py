# ============================================================================
# OBJECTIVE 3: IMPLEMENT VECTOR DATABASES USING FAISS
# ============================================================================
#
# LEARNING OBJECTIVES DEMONSTRATED:
#   1. Text Embeddings - Converting text to numerical vectors that capture semantic meaning
#   2. Semantic Search - Finding relevant documents by meaning rather than keyword matching
#   3. Vector Databases - Using FAISS for efficient similarity search in high-dimensional spaces
#   4. Index Design - Choosing appropriate index types (IndexFlatL2) for dataset size
#   5. RAG Retrieval - Implementing the retrieval component of RAG systems
#
# PREREQUISITES: Run Objective 1 and Objective 2 first
#   - system_prompt (from Objective 1) - for validation
#   - qa_database (from Objective 2) - 21 Q&A pairs to convert to embeddings
#
# ============================================================================

# ============================================================================
# SECTION 1: IMPORTS & VALIDATION
# ============================================================================

import os
from typing import List, Dict, Tuple

try:
    import numpy as np
    import pandas as pd
    import faiss
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    raise ImportError(f"Missing: {e}. Run: pip install faiss-cpu sentence-transformers numpy pandas")

# Import ObjectiveSupport for DRY (optional - graceful fallback)
try:
    from objective_support import ObjectiveSupport
    _support = ObjectiveSupport()
except ImportError:
    # Fallback if not available (for notebook extraction)
    _support = None


def validate_prerequisites():
    """Ensure Objective 1 and 2 were run first."""
    required = ['system_prompt', 'qa_database']
    missing = [r for r in required if r not in globals()]
    if missing:
        raise RuntimeError(f"Missing: {missing}. Run Objective 1 and 2 first.")
    print("✅ Prerequisites validated")
    print(f"   • System prompt: {len(globals()['system_prompt'])} chars")
    print(f"   • Q&A database: {len(globals()['qa_database'])} pairs")
    return True


# ============================================================================
# SECTION 2: CONFIGURATION
# ============================================================================

# Output directory for FAISS index and embeddings (using ObjectiveSupport if available)
OUTPUT_DIR = "data/vector_database"
if _support:
    OUTPUT_DIR = _support.setup_output_dir(OUTPUT_DIR)
else:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Embedding model - lightweight and efficient
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval settings
TOP_K = 3  # Number of similar documents to retrieve

# Expected Q&A count (from Objective 2)
EXPECTED_QA_COUNT = 21  # Total Q&A pairs: 18 answerable + 3 unanswerable
EMBEDDING_DIM = 384  # Dimension for all-MiniLM-L6-v2 model


# ============================================================================
# SECTION 3: EMBEDDING FUNCTIONS
# ============================================================================

def load_embedding_model(model_name: str = EMBEDDING_MODEL) -> SentenceTransformer:
    """
    Load sentence transformer model for generating embeddings.
    
    Model: all-MiniLM-L6-v2
    - Dimensions: 384
    - Speed: Fast (good for real-time applications)
    - Quality: Good semantic understanding
    - Memory: Low (suitable for CPU-based environments)
    
    Returns:
        SentenceTransformer model ready for encoding
    """
    print(f"   Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"   ✅ Model loaded (embedding dim: {model.get_sentence_embedding_dimension()})")
    return model


def generate_embeddings(texts: List[str], model: SentenceTransformer) -> np.ndarray:
    """
    if not texts:
        raise ValueError("Texts list cannot be empty")
    
    Generate embeddings for a list of texts.
    
    Converts text to 384-dimensional float32 vectors using sentence-transformers.
    These embeddings capture semantic meaning, enabling similarity search.
    
    Args:
        texts: List of strings to embed
        model: SentenceTransformer model
    
    Returns:
        numpy array of shape (n_texts, 384) with float32 dtype
    """
    # Encode all texts - model handles batching internally
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    # FAISS requires float32 dtype
    return embeddings.astype('float32')


# ============================================================================
# SECTION 4: FAISS INDEX FUNCTIONS
# ============================================================================

def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Create FAISS index from embeddings.
    
    Uses IndexFlatL2 for exact search with L2 (Euclidean) distance.
    Ideal for small-medium datasets (<100k vectors).
    
    Args:
        embeddings: numpy array of shape (n_vectors, embedding_dim)
    
    Returns:
        FAISS IndexFlatL2 index with all vectors indexed
    """
    # Step 1: Get embedding dimension
    if embeddings.size == 0:
        raise ValueError("Embeddings array cannot be empty")
    
    if len(embeddings.shape) != 2:
        raise ValueError(f"Embeddings must be 2D array, got shape {embeddings.shape}")
    
    if embeddings.dtype != np.float32:
        raise TypeError(f"Embeddings must be float32, got {embeddings.dtype}")
    
    dimension = embeddings.shape[1]
    
    # Step 2: Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    
    # Step 3: Add vectors to index
    index.add(embeddings)
    
    # Step 4: Return the populated index
    return index


def search_index(
    query_embedding: np.ndarray,
    index: faiss.IndexFlatL2,
    top_k: int = TOP_K
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Search FAISS index for most similar vectors.
    
    Args:
        query_embedding: Query vector (1, embedding_dim)
        index: FAISS index
        top_k: Number of results to return
    
    Returns:
        distances: Distance scores (lower = more similar for L2)
        indices: Indices of matched documents
    """
    if len(query_embedding.shape) == 1:
        query_embedding = query_embedding.reshape(1, -1)
    
    # Validate dimension match
    if query_embedding.shape[1] != index.d:
        raise ValueError(f"Query embedding dimension {query_embedding.shape[1]} doesn't match index dimension {index.d}")
    
    
    distances, indices = index.search(query_embedding, top_k)
    return distances[0], indices[0]


def retrieve_context(
    query: str,
    model: SentenceTransformer,
    index: faiss.IndexFlatL2,
    qa_database: List[Dict],
    top_k: int = TOP_K
) -> List[Dict]:
    """
    Retrieve most relevant Q&A pairs for a query.
    
    This is the core RAG retrieval function:
    1. Convert query to embedding
    2. Search FAISS index for similar embeddings
    3. Return corresponding Q&A pairs as context
    
    Args:
        query: User's question
        model: Embedding model
        index: FAISS index
        qa_database: Original Q&A database
        top_k: Number of results to return
    
    Returns:
        List of relevant Q&A pairs with distance scores
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if not qa_database:
        raise ValueError("Q&A database cannot be empty")
    
    # Generate query embedding
    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    
    # Search index
    distances, indices = search_index(query_embedding, index, top_k)
    
    # Get corresponding Q&A pairs
    results = []
    for dist, idx in zip(distances, indices):
        if idx < len(qa_database):  # Safety check
            qa = qa_database[idx].copy()
            qa['distance'] = float(dist)
            qa['similarity_score'] = 1 / (1 + float(dist))  # Convert distance to similarity
            results.append(qa)
    
    return results


def format_context_for_llm(retrieved_qa: List[Dict]) -> str:
    """
    Format retrieved Q&A pairs as context for LLM.
    
    This context will be injected into the prompt for RAG.
    """
    if not retrieved_qa:
        return "No relevant information found in knowledge base."
    
    context_parts = []
    for i, qa in enumerate(retrieved_qa, 1):
        context_parts.append(f"[Context {i}]")
        context_parts.append(f"Q: {qa['question']}")
        context_parts.append(f"A: {qa['answer']}")
        context_parts.append("")
    
    return "\n".join(context_parts)


# ============================================================================
# SECTION 5: DISPLAY & STORAGE FUNCTIONS
# ============================================================================

def display_retrieval_results(query: str, results: List[Dict]):
    """Display retrieval results in a formatted way."""
    print("\n" + "="*70)
    print(f"🔍 RETRIEVAL RESULTS FOR: \"{query}\"")
    print("="*70)
    
    for i, qa in enumerate(results, 1):
        similarity = qa.get('similarity_score', 0) * 100
        answerable = '📗' if qa.get('answerable', True) else '📕'
        
        print(f"\n{answerable} Result {i} (Similarity: {similarity:.1f}%)")
        print(f"   Category: {qa.get('category', 'N/A')}")
        print(f"   Question: {qa.get('question', 'N/A')}")
        print(f"   Answer: {qa.get('answer', 'N/A')[:100]}...")
    
    print("\n" + "="*70)


def save_embeddings(embeddings: np.ndarray, filename: str = "qa_embeddings.npy"):
    """Save embeddings to numpy file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    np.save(filepath, embeddings)
    print(f"✅ Embeddings saved to: {filepath}")
    return filepath


def save_faiss_index(index: faiss.IndexFlatL2, filename: str = "qa_index.faiss"):
    """Save FAISS index to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    faiss.write_index(index, filepath)
    print(f"✅ FAISS index saved to: {filepath}")
    return filepath


def save_retrieval_test_results(test_results: List[Dict], filename: str = "retrieval_test_results.csv"):
    """Save retrieval test results to CSV."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Flatten results for CSV
    rows = []
    for result in test_results:
        for i, retrieved in enumerate(result['retrieved'], 1):
            rows.append({
                'query': result['query'],
                'rank': i,
                'category': retrieved.get('category', ''),
                'answerable': retrieved.get('answerable', True),
                'question': retrieved.get('question', ''),
                'answer': retrieved.get('answer', '')[:200],
                'similarity_score': retrieved.get('similarity_score', 0)
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    print(f"✅ Retrieval test results saved to: {filepath}")
    return filepath


# ============================================================================
# SECTION 6: VERIFICATION FUNCTION
# ============================================================================

def verify_objective3():
    """
    Verify that Objective 3 completed successfully.
    Checks all variables, embeddings, FAISS index, and files.
    """
    print("="*70)
    print("🔍 OBJECTIVE 3 VERIFICATION")
    print("="*70)
    
    errors = []

    # Check if variables exist
    if 'embedding_model' not in globals():
        errors.append("❌ embedding_model not found")
    if 'qa_embeddings' not in globals():
        errors.append("❌ qa_embeddings not found")
    if 'faiss_index' not in globals():
        errors.append("❌ faiss_index not found")
    if 'embed_query' not in globals():
        errors.append("❌ embed_query function not found")

    if errors:
        print("\n".join(errors))
        print("="*70)
        return False

    # Check embeddings shape
    if qa_embeddings.shape[0] != EXPECTED_QA_COUNT:
        errors.append(f"❌ Expected EXPECTED_QA_COUNT embeddings, got {qa_embeddings.shape[0]}")
    if qa_embeddings.shape[1] != EMBEDDING_DIM:
        errors.append(f"❌ Expected EMBEDDING_DIM dimensions, got {qa_embeddings.shape[1]}")
    if qa_embeddings.dtype != 'float32':
        errors.append(f"❌ Expected float32 dtype, got {qa_embeddings.dtype}")

    # Check FAISS index
    if faiss_index.ntotal != EXPECTED_QA_COUNT:
        errors.append(f"❌ Expected EXPECTED_QA_COUNT vectors in index, got {faiss_index.ntotal}")
    if faiss_index.d != EMBEDDING_DIM:
        errors.append(f"❌ Expected EMBEDDING_DIM dimensions in index, got {faiss_index.d}")

    # Check files exist
    if not os.path.exists("data/vector_database/qa_embeddings.npy"):
        errors.append("❌ qa_embeddings.npy not found")
    if not os.path.exists("data/vector_database/qa_index.faiss"):
        errors.append("❌ qa_index.faiss not found")

    # Test embed_query function
    try:
        test_embedding = embed_query("test query")
        if test_embedding.shape != (EMBEDDING_DIM,):
            errors.append(f"❌ embed_query() returned wrong shape: {test_embedding.shape}")
    except Exception as e:
        errors.append(f"❌ embed_query() test failed: {e}")

    # Print results
    if errors:
        print("\n❌ VERIFICATION FAILED:")
        print("\n".join(errors))
        print("="*70)
        return False
    else:
        print("\n✅ Objective 3 Complete - All variables and files verified")
        print(f"   • Embedding Model: {embedding_model.get_sentence_embedding_dimension()} dimensions")
        print(f"   • Embeddings: {qa_embeddings.shape[0]} vectors × {qa_embeddings.shape[1]} dimensions")
        print(f"   • FAISS Index: {faiss_index.ntotal} vectors indexed")
        print(f"   • embed_query(): Ready")
        print(f"   • Files: Saved to data/vector_database/")
        print("="*70)
        return True


# ============================================================================
# EXECUTION - Uses env from Objective 0, wrapped with timing
# ============================================================================

# Verify prerequisites using ObjectiveSupport (DRY)
if _support:
    _support.ensure_prerequisites({
        'env': 'Objective 0 (Prerequisites & Setup)',
        'system_prompt': 'Objective 1',
        'qa_database': 'Objective 2'
    }, globals())
    print("✅ Prerequisites validated (env, system_prompt, qa_database)")
else:
    # Fallback to manual checking if ObjectiveSupport not available
    if 'env' not in globals():
        raise RuntimeError("❌ 'env' not found! Please run Objective 0 (Prerequisites & Setup) first.")
    if 'system_prompt' not in globals():
        raise RuntimeError("❌ 'system_prompt' not found! Please run Objective 1 first.")
    if 'qa_database' not in globals():
        raise RuntimeError("❌ 'qa_database' not found! Please run Objective 2 first.")
    print("✅ Prerequisites validated (env, system_prompt, qa_database)")

# ============================================================================
# EXECUTION - Orchestrates Objective 3 workflow with timing
# ============================================================================

with env.timer.objective(ObjectiveNames.OBJECTIVE_3):
    print("Objective 3: Implementing Vector Database\n")

    # ============================================================================
    # SECTION 7: EXECUTION
    # ============================================================================

    print("="*70)

    # --- Step 1: Validate Prerequisites ---
    print("-"*70)

    qa_database = globals()['qa_database']

    # --- Step 2: Load Embedding Model ---
    print("\n🤖 STEP 2: Load Embedding Model")
    print("-"*70)

    embedding_model = load_embedding_model()
    globals()['embedding_model'] = embedding_model

    # --- Step 3: Generate Embeddings for Q&A Database ---
    print("\n📊 STEP 3: Generate Embeddings for Q&A Database")
    print("-"*70)

    # Combine question and answer for richer embeddings
    qa_texts = [f"{qa['question']} {qa['answer']}" for qa in qa_database]
    print(f"   Generating embeddings for {len(qa_texts)} Q&A pairs...")

    qa_embeddings = generate_embeddings(qa_texts, embedding_model)
    globals()['qa_embeddings'] = qa_embeddings

    print(f"   ✅ Embeddings shape: {qa_embeddings.shape}")

    # --- Step 4: Create FAISS Index ---
    print("\n🗄️  STEP 4: Create FAISS Index")
    print("-"*70)

    # Create FAISS index and add embeddings
    faiss_index = create_faiss_index(qa_embeddings)
    globals()['faiss_index'] = faiss_index

    # Create embed_query function for RAG pipeline (used in Objective 4)
    def embed_query(query: str) -> np.ndarray:
        """Convert query text to embedding vector for FAISS search."""
        return embedding_model.encode([query], convert_to_numpy=True).astype('float32')[0]

    globals()['embed_query'] = embed_query

    print(f"   ✅ FAISS index created")
    print(f"   • Index type: IndexFlatL2 (exact search)")
    print(f"   • Vectors indexed: {faiss_index.ntotal}")
    print(f"   • Embedding dimension: {qa_embeddings.shape[1]}")

    # --- Step 5: Test Retrieval ---
    print("\n🧪 STEP 5: Test Retrieval with Sample Queries")
    print("-"*70)

    test_queries = [
        "How long does shipping take?",
        "Can I return a product?",
        "What are your business hours?",
        "Do you price match with competitors?",  # Unanswerable
    ]

    test_results = []

    for query in test_queries:
        print(f"\n   Testing: \"{query}\"")

        retrieved = retrieve_context(
            query=query,
            model=embedding_model,
            index=faiss_index,
            qa_database=qa_database,
            top_k=TOP_K
        )

        test_results.append({
            'query': query,
            'retrieved': retrieved
        })

        display_retrieval_results(query, retrieved)

    # --- Step 6: Show Formatted Context for LLM ---
    print("\n📝 STEP 6: Example - Formatted Context for LLM")
    print("-"*70)

    sample_query = "What is your return policy?"
    sample_retrieved = retrieve_context(sample_query, embedding_model, faiss_index, qa_database, TOP_K)
    formatted_context = format_context_for_llm(sample_retrieved)

    print(f"Query: \"{sample_query}\"\n")
    print("Formatted Context for LLM:")
    print("-"*70)
    print(formatted_context)
    print("-"*70)

    # --- Step 7: Save All Artifacts ---
    print("\n💾 STEP 7: Save Files to data/vector_database/")
    print("-"*70)

    save_embeddings(qa_embeddings)
    save_faiss_index(faiss_index)
    save_retrieval_test_results(test_results)

    # --- Step 8: Verify Objective 3 ---
    print("\n✅ STEP 8: Verify Objective 3")
    print("-"*70)
    verify_objective3()

    # --- Summary ---
    print("\n" + "="*70)
    print("✅ OBJECTIVE 3 COMPLETE")
    print(f"""
    Key Concepts Demonstrated:
      1. Embeddings - Text to vector conversion using sentence-transformers
      2. FAISS Index - Efficient similarity search with IndexFlatL2
      3. RAG Retrieval - Finding relevant context for user queries

    📦 FILES SAVED (for submission):
      • {OUTPUT_DIR}/qa_embeddings.npy - Embedding vectors
      • {OUTPUT_DIR}/qa_index.faiss - FAISS index
      • {OUTPUT_DIR}/retrieval_test_results.csv - Test results

    📦 GLOBAL VARIABLES:
      • embedding_model: SentenceTransformer model
      • qa_embeddings: numpy array ({qa_embeddings.shape})
      • faiss_index: FAISS IndexFlatL2 ({faiss_index.ntotal} vectors)

    🔜 READY FOR OBJECTIVE 4: RAG Pipeline Integration
    """)
    print("="*70)