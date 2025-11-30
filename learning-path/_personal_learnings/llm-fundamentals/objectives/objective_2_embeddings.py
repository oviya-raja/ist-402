# ============================================================================
# Objective 2: Embeddings - Tokens → Vectors
# ============================================================================
# Understanding how tokens are converted to numerical vectors (embeddings)

print("=" * 80)
print("OBJECTIVE 2: EMBEDDINGS")
print("=" * 80)
print("\n🧠 Learning Goal: Understand how tokens become vectors")
print("   Embeddings convert discrete tokens into continuous vector space.\n")

# ============================================================================
# Part 1: Basic Embeddings
# ============================================================================
print("\n" + "-" * 80)
print("Part 1: Basic Embeddings")
print("-" * 80)

try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    
    model_name = "gpt2"
    
    print(f"\n📥 Loading tokenizer and model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    # Get tokenizer from previous objective if available
    if 'tokenizer' in globals():
        print("   ✅ Using tokenizer from Objective 1")
    else:
        print("   ℹ️  Loading new tokenizer")
    
    # Example text
    text = "Hello world!"
    print(f"\n📝 Text: '{text}'")
    
    # Tokenize
    tokens = tokenizer.tokenize(text)
    token_ids = tokenizer.encode(text, return_tensors="pt")
    
    print(f"🔤 Tokens: {tokens}")
    print(f"🔢 Token IDs shape: {token_ids.shape}")
    
    # Get embeddings
    with torch.no_grad():
        outputs = model(token_ids)
        embeddings = outputs.last_hidden_state
    
    print(f"\n📊 Embedding shape: {embeddings.shape}")
    print(f"   - Batch size: {embeddings.shape[0]}")
    print(f"   - Sequence length: {embeddings.shape[1]}")
    print(f"   - Embedding dimension: {embeddings.shape[2]}")
    
    print(f"\n💡 Each token is now represented as a {embeddings.shape[2]}-dimensional vector!")
    
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("   Install with: pip install transformers torch")
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 2: Embedding Layer
# ============================================================================
print("\n" + "-" * 80)
print("Part 2: Embedding Layer")
print("-" * 80)

if 'model' in locals():
    try:
        # Access the embedding layer
        embedding_layer = model.get_input_embeddings()
        
        print(f"\n🔍 Embedding Layer:")
        print(f"   Type: {type(embedding_layer)}")
        print(f"   Vocabulary size: {embedding_layer.num_embeddings}")
        print(f"   Embedding dimension: {embedding_layer.embedding_dim}")
        
        # Get embedding for a specific token
        token_id = tokenizer.encode("hello")[0]
        token_embedding = embedding_layer(torch.tensor([[token_id]]))
        
        print(f"\n📊 Example embedding for token 'hello' (ID: {token_id}):")
        print(f"   Shape: {token_embedding.shape}")
        print(f"   First 10 values: {token_embedding[0, 0, :10].tolist()}")
        
    except Exception as e:
        print(f"⚠️  Could not access embedding layer: {e}")

# ============================================================================
# Part 3: Visualizing Embeddings
# ============================================================================
print("\n" + "-" * 80)
print("Part 3: Embedding Properties")
print("-" * 80)

if 'embeddings' in locals():
    try:
        import torch.nn.functional as F
        
        # Calculate similarity between token embeddings
        token1_emb = embeddings[0, 0, :]  # First token
        token2_emb = embeddings[0, 1, :]  # Second token
        
        # Cosine similarity
        similarity = F.cosine_similarity(
            token1_emb.unsqueeze(0),
            token2_emb.unsqueeze(0)
        ).item()
        
        print(f"\n🔗 Cosine similarity between first two tokens:")
        print(f"   Token 1: '{tokens[0]}'")
        print(f"   Token 2: '{tokens[1]}'")
        print(f"   Similarity: {similarity:.4f}")
        
        # Embedding statistics
        print(f"\n📊 Embedding Statistics:")
        print(f"   Mean: {embeddings.mean().item():.4f}")
        print(f"   Std: {embeddings.std().item():.4f}")
        print(f"   Min: {embeddings.min().item():.4f}")
        print(f"   Max: {embeddings.max().item():.4f}")
        
    except Exception as e:
        print(f"⚠️  Could not analyze embeddings: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ Objective 2 Complete: Embeddings")
print("=" * 80)
print("\n📚 Key Takeaways:")
print("  1. Tokens are converted to dense vector representations")
print("  2. Embeddings capture semantic meaning in continuous space")
print("  3. Similar words have similar embeddings (closer in vector space)")
print("  4. Embedding dimension is a hyperparameter of the model")
print("\n➡️  Next: Objective 3 - Attention (Vector Relationships)")

# Store for next objective
if 'model' in locals():
    globals()['model'] = model
    globals()['embeddings'] = embeddings
    print("\n💾 Model and embeddings saved for next objective")

