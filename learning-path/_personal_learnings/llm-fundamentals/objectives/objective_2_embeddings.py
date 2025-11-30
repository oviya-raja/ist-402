# ============================================================================
# Objective 2: Embeddings - Tokens → Vectors
# ============================================================================
# Understanding how tokens are converted to numerical vectors (embeddings)

from llm_fundamentals_support import (
    LLMFundamentalsSupport, ModelLoader, TextProcessor, EmbeddingExtractor,
    Formatter, StateManager
)
import torch
import torch.nn.functional as F

support = LLMFundamentalsSupport()
formatter = Formatter()
state_mgr = StateManager()

print(formatter.header("OBJECTIVE 2: EMBEDDINGS"))
print(formatter.learning_intro(
    concept="Embeddings",
    description="Tokens are converted to dense vector representations (embeddings) that capture semantic meaning in continuous space. Each token becomes a high-dimensional vector.",
    what_we_learn=[
        "How tokens become numerical vectors (embeddings)",
        "Embedding dimensions and their meaning",
        "Embedding layer architecture in transformers",
        "Semantic relationships in vector space (similarity)"
    ],
    what_we_do=[
        "Load a model and extract embeddings for tokens",
        "Inspect embedding layer structure",
        "Calculate similarity between token embeddings",
        "Analyze embedding statistics"
    ],
    hands_on=[
        "Load GPT-2 model and tokenizer",
        "Get embeddings for text: 'Hello world!'",
        "See embedding shape: [batch=1, seq_len=3, hidden_dim=768]",
        "Extract embedding layer and inspect vocabulary size",
        "Calculate cosine similarity between token embeddings",
        "Analyze mean, std, min, max of embeddings"
    ]
))

# ============================================================================
# Part 1: Basic Embeddings
# ============================================================================
print(formatter.section("Part 1: Basic Embeddings - Hands-On Code"))

loader = ModelLoader()
try:
    tokenizer, model = loader.load_both(globals())
    if 'tokenizer' in globals():
        print("   ✅ Using tokenizer from Objective 1")
    else:
        print(f"   📥 Loaded tokenizer and model: {loader.model_name}")
    
    processor = TextProcessor(tokenizer)
    extractor = EmbeddingExtractor(model, tokenizer)
    
    text = "Hello world!"
    print(f"\n📝 Text: '{text}'")
    
    tokens = processor.tokenize(text)
    token_ids = processor.encode(text, return_tensors="pt")
    
    print(f"🔤 Tokens: {tokens}")
    print(f"🔢 Token IDs shape: {token_ids.shape}")
    
    embeddings = extractor.get_embeddings(text)
    
    print(f"\n📊 Embedding shape: {embeddings.shape}")
    print(f"   - Batch size: {embeddings.shape[0]}")
    print(f"   - Sequence length: {embeddings.shape[1]}")
    print(f"   - Embedding dimension: {embeddings.shape[2]}")
    print(f"\n💡 Each token is now represented as a {embeddings.shape[2]}-dimensional vector!")
    
    print(formatter.output_summary([
        f"Text '{text}' with {len(tokens)} tokens → embeddings shape {embeddings.shape}",
        f"Each token is now a {embeddings.shape[2]}-dimensional vector",
        f"Embeddings capture semantic meaning in continuous space",
        "Shape: [batch_size, sequence_length, hidden_dimension]"
    ]))
    
except Exception as e:
    print(f"❌ Error: {e}")
    embeddings = None

# ============================================================================
# Part 2: Embedding Layer
# ============================================================================
print(formatter.section("Part 2: Embedding Layer - Architecture Inspection"))

if 'model' in locals():
    try:
        embedding_layer = model.get_input_embeddings()
        print(f"\n🔍 Embedding Layer:")
        print(f"   Type: {type(embedding_layer)}")
        print(f"   Vocabulary size: {embedding_layer.num_embeddings}")
        print(f"   Embedding dimension: {embedding_layer.embedding_dim}")
        
        token_id = tokenizer.encode("hello")[0]
        token_embedding = embedding_layer(torch.tensor([[token_id]]))
        
        print(f"\n📊 Example embedding for token 'hello' (ID: {token_id}):")
        print(f"   Shape: {token_embedding.shape}")
        print(f"   First 10 values: {token_embedding[0, 0, :10].tolist()}")
        
        print(formatter.output_summary([
            f"Embedding layer maps {embedding_layer.num_embeddings} tokens to {embedding_layer.embedding_dim}D vectors",
            "Each token ID directly maps to a learned embedding vector",
            "Embeddings are learned during model training",
            "Similar tokens have similar embeddings (closer in vector space)"
        ]))
    except Exception as e:
        print(f"⚠️  Could not access embedding layer: {e}")

# ============================================================================
# Part 3: Embedding Properties
# ============================================================================
print(formatter.section("Part 3: Embedding Properties - Similarity Analysis"))

if 'embeddings' in locals() and embeddings is not None:
    try:
        token1_emb = embeddings[0, 0, :]
        token2_emb = embeddings[0, 1, :]
        
        similarity = F.cosine_similarity(
            token1_emb.unsqueeze(0),
            token2_emb.unsqueeze(0)
        ).item()
        
        print(f"\n🔗 Cosine similarity between first two tokens:")
        print(f"   Token 1: '{tokens[0]}'")
        print(f"   Token 2: '{tokens[1]}'")
        print(f"   Similarity: {similarity:.4f}")
        
        stats = extractor.get_embedding_stats(embeddings)
        print(f"\n📊 Embedding Statistics:")
        for key, value in stats.items():
            print(f"   {key.capitalize()}: {value:.4f}")
        
        print(formatter.output_summary([
            f"Cosine similarity between '{tokens[0]}' and '{tokens[1]}': {similarity:.4f}",
            f"Embedding statistics: mean={stats['mean']:.4f}, std={stats['std']:.4f}",
            "Similar words have higher cosine similarity (closer to 1.0)",
            "Embeddings are typically normalized or centered around zero"
        ]))
    except Exception as e:
        print(f"⚠️  Could not analyze embeddings: {e}")

# ============================================================================
# Summary
# ============================================================================
takeaways = [
    "Tokens are converted to dense vector representations",
    "Embeddings capture semantic meaning in continuous space",
    "Similar words have similar embeddings (closer in vector space)",
    "Embedding dimension is a hyperparameter of the model"
]
print(formatter.summary("Objective 2 Complete: Embeddings", takeaways, "Objective 3 - Attention (Vector Relationships)"))

# Save state
if 'model' in locals() and 'embeddings' in locals():
    state_mgr.save_to_globals(globals(), model=model, embeddings=embeddings)
    print("\n💾 Model and embeddings saved for next objective")
