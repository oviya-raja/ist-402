# ============================================================================
# OBJECTIVE 4: BUILD COMPLETE RAG PIPELINE
# ============================================================================
#
# PIPELINE COMPONENTS:
#   1. Query Processing - Convert user question to embedding
#   2. Retrieval - Use FAISS to find top-k most similar Q&A pairs
#   3. Augmentation - Combine user question with retrieved context
#   4. Generation - Use Mistral to generate answer from augmented context
#
# WHY THIS ARCHITECTURE:
#   - RAG combines retrieval (accurate, up-to-date info) with generation (natural responses)
#   - Grounds answers in knowledge base, reducing hallucinations
#   - Allows easy updates to knowledge base without retraining models
#
# 100% REUSE FROM PREVIOUS OBJECTIVES:
#   - env (Objective 0) - Environment configuration and timing
#   - inference_engine, system_prompt (Objective 1) - Model and prompt
#   - qa_database (Objective 2) - Knowledge base
#   - embedding_model, faiss_index, embed_query (Objective 3) - Vector search
#
# PREREQUISITES: Run Objectives 0, 1, 2, and 3 first
#
# ============================================================================


# ============================================================================
# SECTION 1: IMPORTS & VALIDATION
# ============================================================================

import os
from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    import numpy as np
    import pandas as pd
    import torch
except ImportError as e:
    raise ImportError(f"Missing: {e}. Run: pip install numpy pandas torch")


def validate_prerequisites():
    """Ensure Objectives 0, 1, 2, and 3 were run first."""
    required = {
        'Objective 0': ['env'],
        'Objective 1': ['system_prompt', 'inference_engine'],
        'Objective 2': ['qa_database'],
        'Objective 3': ['embedding_model', 'faiss_index', 'embed_query']
    }
    
    all_missing = []
    for objective, items in required.items():
        missing = [item for item in items if item not in globals()]
        if missing:
            all_missing.append(f"{objective}: {missing}")
    
    if all_missing:
        raise RuntimeError(f"Missing prerequisites:\n" + "\n".join(all_missing))
    
    print("✅ All prerequisites validated")
    print(f"   • env: EnvironmentConfig (from Objective 0)")
    print(f"   • System prompt: {len(globals()['system_prompt'])} chars")
    print(f"   • InferenceEngine: Ready (from Objective 1)")
    print(f"   • Q&A database: {len(globals()['qa_database'])} pairs")
    print(f"   • FAISS index: {globals()['faiss_index'].ntotal} vectors")
    print(f"   • embed_query(): Ready (from Objective 3)")
    return True


# ============================================================================
# SECTION 2: CONFIGURATION
# ============================================================================

# Output directory
OUTPUT_DIR = "data/rag_pipeline"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# RAG CONFIGURATION PARAMETERS EXPLAINED
# ============================================================================
#
# top_k: Number of documents to retrieve from FAISS
#   - Higher value (5-10): More context, better coverage, but may include noise
#   - Lower value (1-3): More focused, less noise, but may miss relevant info
#   - Default 3: Good balance for small knowledge bases (21 Q&A pairs)
#
# max_new_tokens: Maximum tokens the model can generate in response
#   - Higher value (500+): Longer, more detailed responses
#   - Lower value (100-200): Concise responses, faster generation
#   - Default 300: Allows comprehensive answers without being verbose
#
# temperature: Controls randomness/creativity in generation (0.0 - 1.0)
#   - 0.0: Deterministic, always picks most likely token (factual tasks)
#   - 0.5-0.7: Balanced creativity and coherence (recommended for QA)
#   - 1.0+: More random/creative (creative writing, brainstorming)
#   - Default 0.7: Allows natural variation while staying on-topic
#
# similarity_threshold: Minimum similarity score to include a document (0.0 - 1.0)
#   - Higher value (0.5+): Only very relevant documents, may return few/none
#   - Lower value (0.1-0.3): More documents included, may have lower relevance
#   - Default 0.3: Filters out clearly irrelevant results while being inclusive
#
# ============================================================================

RAG_CONFIG = {
    "top_k": 3,                    # Number of documents to retrieve
    "max_new_tokens": 300,         # Max tokens for generation
    "temperature": 0.7,            # Generation temperature
    "similarity_threshold": 0.3,   # Minimum similarity score (0-1)
}


# ============================================================================
# SECTION 3: RAG RESULT DATA CLASS
# ============================================================================

@dataclass
class RAGResult:
    """Container for RAG pipeline results."""
    query: str
    response: str
    retrieved_context: List[Dict]
    success: bool
    error_message: Optional[str] = None

# Export RAGResult globally
globals()['RAGResult'] = RAGResult


# ============================================================================
# SECTION 4: RAG PIPELINE CORE FUNCTIONS
# ============================================================================
#
# These functions form the complete RAG pipeline:
#   1. search_faiss()       - Search FAISS for similar Q&A pairs
#   2. format_context()     - Format retrieved Q&A as context string
#   3. build_prompt()       - Build augmented prompt
#   4. generate_response()  - Generate response with Mistral
#
# NOTE: embed_query() is REUSED from Objective 3 (not redefined here)
#
# ============================================================================

def search_faiss(query_embedding: np.ndarray, top_k: int = None) -> List[Dict]:
    """
    STEP 2: Search FAISS index for similar Q&A pairs.
    
    Reuses: faiss_index from Objective 3, qa_database from Objective 2
    
    Args:
        query_embedding: Query vector from embed_query()
        top_k: Number of results to retrieve
    
    Returns:
        List of Q&A dicts with similarity scores
    """
    if top_k is None:
        top_k = RAG_CONFIG["top_k"]
    
    faiss_index = globals()['faiss_index']
    qa_database = globals()['qa_database']
    
    # Ensure proper shape for FAISS search
    if len(query_embedding.shape) == 1:
        query_embedding = query_embedding.reshape(1, -1)
    
    # Search FAISS index
    distances, indices = faiss_index.search(query_embedding, top_k)
    
    # Get Q&A pairs with similarity scores
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(qa_database):
            similarity = 1 / (1 + float(dist))  # Convert distance to similarity
            if similarity >= RAG_CONFIG["similarity_threshold"]:
                qa = qa_database[idx].copy()
                qa['similarity_score'] = similarity
                qa['distance'] = float(dist)
                results.append(qa)
    
    return results


def format_context(retrieved_qa: List[Dict]) -> str:
    """
    STEP 3: Format retrieved Q&A pairs as context string.
    
    Args:
        retrieved_qa: List of Q&A dicts from search_faiss()
    
    Returns:
        Formatted context string for prompt
    """
    if not retrieved_qa:
        return "No relevant information found in knowledge base."
    
    context_parts = ["RELEVANT INFORMATION FROM KNOWLEDGE BASE:", "-" * 40]
    
    for i, qa in enumerate(retrieved_qa, 1):
        similarity_pct = qa.get('similarity_score', 0) * 100
        context_parts.append(f"\n[Source {i}] (Relevance: {similarity_pct:.0f}%)")
        context_parts.append(f"Q: {qa['question']}")
        context_parts.append(f"A: {qa['answer']}")
    
    context_parts.append("-" * 40)
    return "\n".join(context_parts)


def build_prompt(query: str, context: str) -> str:
    """
    STEP 4: Build augmented prompt combining system prompt, context, and query.
    
    Reuses: system_prompt from Objective 1
    
    Args:
        query: User's question
        context: Formatted context from format_context()
    
    Returns:
        Complete augmented prompt
    """
    system_prompt = globals()['system_prompt']
    
    augmented_prompt = f"""{system_prompt}

{context}

INSTRUCTIONS:
- Answer using ONLY the information provided above
- If information is not available, politely say so
- Be helpful, accurate, and concise

CUSTOMER QUESTION: {query}

ASSISTANT RESPONSE:"""
    
    return augmented_prompt


def generate_response(augmented_prompt: str) -> str:
    """
    STEP 5: Generate response with Mistral model.
    
    Reuses: inference_engine from Objective 1 (100% reuse!)
    
    Args:
        augmented_prompt: Complete prompt from build_prompt()
    
    Returns:
        Generated response string
    """
    # REUSE: inference_engine from Objective 1
    inference_engine = globals()['inference_engine']
    
    # Get model and tokenizer from inference_engine (cached from Objective 1)
    # Use the same model name as Objective 1
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    tokenizer, model = inference_engine.load_model(model_name)
    
    # Format for Mistral Instruct (using SystemPromptEngineer from Objective 1)
    if 'SystemPromptEngineer' in globals():
        # Reuse format_template from Objective 1
        formatted = SystemPromptEngineer.format_template(augmented_prompt)
    else:
        # Fallback if SystemPromptEngineer not available
        formatted = f"<s>[INST] {augmented_prompt} [/INST]"
    
    # REUSE: inference_engine.generate_response() from Objective 1
    response = inference_engine.generate_response(
        tokenizer, model, formatted,
        max_new_tokens=RAG_CONFIG["max_new_tokens"],
        temperature=RAG_CONFIG["temperature"],
        top_p=0.9
    )
    
    return response


# ============================================================================
# SECTION 5: COMPLETE RAG PIPELINE FUNCTION
# ============================================================================

def rag_query(query: str, top_k: int = None, verbose: bool = True) -> RAGResult:
    """
    Complete RAG Pipeline: Query → Retrieve → Augment → Generate
    
    This is the main entry point for the RAG system.
    Orchestrates all pipeline functions in sequence.
    
    Args:
        query: User's question
        top_k: Number of documents to retrieve (default: from config)
        verbose: Print step-by-step progress
    
    Returns:
        RAGResult with response and metadata
    
    Example:
        result = rag_query("What is your return policy?")
        print(result.response)
    """
    if top_k is None:
        top_k = RAG_CONFIG["top_k"]
    
    # Get embed_query from Objective 3
    embed_query_func = globals()['embed_query']
    
    try:
        # ============================================================
        # STEP 1: QUERY PROCESSING - Convert to embedding
        # ============================================================
        if verbose:
            print(f"   Step 1: embed_query() - Converting query to embedding...")
        query_embedding = embed_query_func(query)
        
        # Ensure proper shape
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # ============================================================
        # STEP 2: RETRIEVAL - Search FAISS for similar Q&A
        # ============================================================
        if verbose:
            print(f"   Step 2: search_faiss() - Searching for similar Q&A pairs...")
        retrieved_qa = search_faiss(query_embedding, top_k)
        if verbose:
            print(f"           → Found {len(retrieved_qa)} relevant documents")
        
        # ============================================================
        # STEP 3: AUGMENTATION (Part 1) - Format context
        # ============================================================
        if verbose:
            print(f"   Step 3: format_context() - Formatting retrieved context...")
        context = format_context(retrieved_qa)
        
        # ============================================================
        # STEP 4: AUGMENTATION (Part 2) - Build prompt
        # ============================================================
        if verbose:
            print(f"   Step 4: build_prompt() - Building augmented prompt...")
        augmented_prompt = build_prompt(query, context)
        
        # ============================================================
        # STEP 5: GENERATION - Generate response with Mistral
        # ============================================================
        if verbose:
            print(f"   Step 5: generate_response() - Generating response with Mistral...")
        response = generate_response(augmented_prompt)
        if verbose:
            print(f"           → Response generated: {len(response)} chars")
        
        return RAGResult(
            query=query,
            response=response,
            retrieved_context=retrieved_qa,
            success=True
        )
        
    except Exception as e:
        return RAGResult(
            query=query,
            response="I apologize, but I encountered an error processing your request.",
            retrieved_context=[],
            success=False,
            error_message=str(e)
        )


# ============================================================================
# SECTION 6: DISPLAY & STORAGE FUNCTIONS
# ============================================================================

def display_rag_result(result: RAGResult):
    """Display RAG result in formatted way."""
    print("\n" + "="*70)
    print("🤖 RAG PIPELINE RESULT")
    print("="*70)
    
    print(f"\n📥 USER QUERY:")
    print(f"   {result.query}")
    
    print(f"\n📚 RETRIEVED CONTEXT ({len(result.retrieved_context)} sources):")
    for i, ctx in enumerate(result.retrieved_context, 1):
        similarity = ctx.get('similarity_score', 0) * 100
        answerable = '📗' if ctx.get('answerable', True) else '📕'
        print(f"   {answerable} [{i}] {ctx.get('category', 'N/A')} (Similarity: {similarity:.0f}%)")
        print(f"       Q: {ctx['question'][:60]}...")
    
    print(f"\n📤 GENERATED RESPONSE:")
    print("-"*70)
    print(result.response)
    print("-"*70)
    
    if not result.success:
        print(f"\n⚠️  Error: {result.error_message}")
    
    print("="*70)


def save_rag_results(results: List[RAGResult], filename: str = "rag_test_results.csv"):
    """Save RAG test results to CSV."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    rows = []
    for result in results:
        rows.append({
            'query': result.query,
            'response': result.response[:500],
            'num_sources': len(result.retrieved_context),
            'top_source_similarity': result.retrieved_context[0]['similarity_score'] if result.retrieved_context else 0,
            'success': result.success,
            'error': result.error_message
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    print(f"✅ RAG results saved to: {filepath}")
    return filepath


def save_pipeline_config(filename: str = "pipeline_config.txt"):
    """Save pipeline configuration."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    config_text = f"""RAG PIPELINE CONFIGURATION
==========================

Retrieval Settings:
- Top-K: {RAG_CONFIG['top_k']}
- Similarity Threshold: {RAG_CONFIG['similarity_threshold']}

Generation Settings:
- Max New Tokens: {RAG_CONFIG['max_new_tokens']}
- Temperature: {RAG_CONFIG['temperature']}

Components:
- Embedding Model: sentence-transformers/all-MiniLM-L6-v2
- Vector Store: FAISS IndexFlatL2
- LLM: Mistral-7B-Instruct-v0.3
- Q&A Database: {len(globals().get('qa_database', []))} pairs
"""
    
    with open(filepath, 'w') as f:
        f.write(config_text)
    
    print(f"✅ Pipeline config saved to: {filepath}")
    return filepath


# ============================================================================
# SECTION 7: VERIFICATION FUNCTION
# ============================================================================

def verify_objective4():
    """
    Verify that Objective 4 completed successfully.
    Checks all functions, files, and test results.
    """
    print("="*70)
    print("🔍 OBJECTIVE 4 VERIFICATION")
    print("="*70)
    
    errors = []
    
    # Check required functions exist
    required_functions = ['rag_query', 'search_faiss', 'format_context', 
                          'build_prompt', 'generate_response', 'embed_query']
    for func_name in required_functions:
        if func_name not in globals() or not callable(globals()[func_name]):
            errors.append(f"❌ Function '{func_name}' not found")
    
    # Check RAGResult dataclass
    if 'RAGResult' not in globals():
        errors.append("❌ RAGResult dataclass not found")
    
    # Check files exist
    if not os.path.exists("data/rag_pipeline/rag_test_results.csv"):
        errors.append("❌ rag_test_results.csv not found")
    if not os.path.exists("data/rag_pipeline/pipeline_config.txt"):
        errors.append("❌ pipeline_config.txt not found")
    
    # Check test results
    if 'rag_results' not in globals():
        errors.append("❌ rag_results not found")
    elif len(globals()['rag_results']) != 10:
        errors.append(f"❌ Expected 10 test results, got {len(globals()['rag_results'])}")
    
    # Test rag_query function
    try:
        test_result = rag_query("test query", verbose=False)
        if not isinstance(test_result, RAGResult):
            errors.append("❌ rag_query() does not return RAGResult")
    except Exception as e:
        errors.append(f"❌ rag_query() test failed: {e}")
    
    # Print results
    if errors:
        print("\n❌ VERIFICATION FAILED:")
        print("\n".join(errors))
        print("="*70)
        return False
    else:
        print("\n✅ Objective 4 Complete - All components verified")
        print(f"   • Pipeline Functions: {len(required_functions)} verified")
        print(f"   • RAGResult: Defined")
        print(f"   • Test Results: {len(globals()['rag_results'])} queries")
        print(f"   • Files: Saved to data/rag_pipeline/")
        print("="*70)
        return True


# ============================================================================
# SECTION 8: EXECUTION - Uses env from Objective 0, wrapped with timing
# ============================================================================

# Verify env is available from Objective 0
if 'env' not in globals():
    raise RuntimeError("❌ 'env' not found! Please run Objective 0 (Prerequisites & Setup) first.")

# Verify prerequisites from Objectives 1, 2, and 3
if 'system_prompt' not in globals():
    raise RuntimeError("❌ 'system_prompt' not found! Please run Objective 1 first.")

if 'inference_engine' not in globals():
    raise RuntimeError("❌ 'inference_engine' not found! Please run Objective 1 first.")

if 'qa_database' not in globals():
    raise RuntimeError("❌ 'qa_database' not found! Please run Objective 2 first.")

if 'embedding_model' not in globals() or 'faiss_index' not in globals() or 'embed_query' not in globals():
    raise RuntimeError("❌ Missing Objective 3 components! Please run Objective 3 first.")

print("✅ Prerequisites validated (env, system_prompt, inference_engine, qa_database, embedding_model, faiss_index, embed_query)")

# ============================================================================
# EXECUTION - Orchestrates Objective 4 workflow with timing
# ============================================================================

with env.timer.objective(ObjectiveNames.OBJECTIVE_4):
    print("Objective 4: Building Complete RAG Pipeline\n")
    
    # --- Step 1: Validate Prerequisites ---
    print("\n🔍 STEP 1: Validate Prerequisites")
    print("-"*70)
    validate_prerequisites()

    # --- Step 2: Show Pipeline Architecture ---
    print("\n📐 STEP 2: RAG Pipeline Architecture")
    print("-"*70)
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query                                                     │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ 1. embed_query()│  Convert query to embedding (from Obj 3)   │
│  └────────┬────────┘                                            │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │ 2. search_faiss()│  Find similar Q&A pairs                   │
│  └────────┬────────┘                                            │
│           ▼                                                     │
│  ┌──────────────────┐                                           │
│  │ 3. format_context()│  Format as context string               │
│  └────────┬─────────┘                                           │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │ 4. build_prompt()│  Combine system + context + query         │
│  └────────┬────────┘                                            │
│           ▼                                                     │
│  ┌─────────────────────┐                                        │
│  │ 5. generate_response()│  Generate with Mistral               │
│  └────────┬────────────┘                                        │
│           ▼                                                     │
│      Response                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    # --- Step 3: Test RAG Pipeline with Answerable Questions ---
    print("\n🧪 STEP 3: Test with ANSWERABLE Questions")
    print("-"*70)
    print("   These questions CAN be answered from our knowledge base")

    answerable_questions = [
        "What is your return policy?",
        "How long does shipping take?",
        "What are your customer service hours?",
        "Do you offer warranty on products?",
        "How can I track my order?",
    ]

    answerable_results = []

    for query in answerable_questions:
        print(f"\n{'='*70}")
        print(f"📗 ANSWERABLE: \"{query}\"")
        print('='*70)
        
        result = rag_query(query, verbose=True)
        answerable_results.append(result)
        display_rag_result(result)

    # --- Step 4: Test RAG Pipeline with Unanswerable Questions ---
    print("\n🧪 STEP 4: Test with UNANSWERABLE Questions")
    print("-"*70)
    print("   These questions CANNOT be answered from our knowledge base")
    print("   Testing system limitations and graceful handling")

    unanswerable_questions = [
        "How do your prices compare to Amazon?",
        "Should I buy solar panels for my house?",
        "Will you have a Black Friday sale this year?",
        "What is the CEO's email address?",
        "Can you recommend a good restaurant nearby?",
    ]

    unanswerable_results = []

    for query in unanswerable_questions:
        print(f"\n{'='*70}")
        print(f"📕 UNANSWERABLE: \"{query}\"")
        print('='*70)
        
        result = rag_query(query, verbose=True)
        unanswerable_results.append(result)
        display_rag_result(result)

    # --- Step 5: Save Results ---
    print("\n💾 STEP 5: Save Results")
    print("-"*70)

    all_results = answerable_results + unanswerable_results
    save_rag_results(all_results)
    save_pipeline_config()

    # Store globally for reuse
    globals()['rag_query'] = rag_query
    globals()['rag_results'] = all_results

    # Export core functions globally
    globals()['search_faiss'] = search_faiss
    globals()['format_context'] = format_context
    globals()['build_prompt'] = build_prompt
    globals()['generate_response'] = generate_response
    globals()['verify_objective4'] = verify_objective4

    # --- Step 6: Verify Objective 4 ---
    print("\n✅ STEP 6: Verify Objective 4")
    print("-"*70)
    verify_objective4()

    # --- Summary ---
    print("\n" + "="*70)
    print("✅ OBJECTIVE 4 COMPLETE")
    print("="*70)

    answerable_success = sum(1 for r in answerable_results if r.success)
    unanswerable_success = sum(1 for r in unanswerable_results if r.success)

    print(f"""
RAG Pipeline Components:
  1. Query Processing: embed_query() - Convert to embedding (from Objective 3)
  2. Retrieval: search_faiss() - FAISS similarity search (top-{RAG_CONFIG['top_k']})
  3. Augmentation: format_context() + build_prompt()
  4. Generation: generate_response() - Uses inference_engine from Objective 1

Test Results:
  📗 Answerable Questions: {answerable_success}/{len(answerable_results)} successful
  📕 Unanswerable Questions: {unanswerable_success}/{len(unanswerable_results)} successful

📦 FILES SAVED:
  • {OUTPUT_DIR}/rag_test_results.csv
  • {OUTPUT_DIR}/pipeline_config.txt

📦 GLOBAL FUNCTIONS:
  • rag_query(query) - Complete RAG pipeline
  • search_faiss(), format_context(), build_prompt(), generate_response()
  • embed_query() - Reused from Objective 3
  • verify_objective4() - Verification function

🔜 READY FOR OBJECTIVE 5: Model Experimentation and Ranking
""")
    print("="*70)
