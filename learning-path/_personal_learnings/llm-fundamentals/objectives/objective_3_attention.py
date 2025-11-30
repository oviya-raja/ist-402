# ============================================================================
# Objective 3: Attention - Vector Relationships
# ============================================================================
# Understanding how attention mechanisms compute relationships between tokens

import torch
import torch.nn.functional as F
import math

print("=" * 80)
print("OBJECTIVE 3: ATTENTION")
print("=" * 80)
print("\n🧠 Learning Goal: Understand how attention computes vector relationships")
print("   Attention allows each token to attend to all other tokens.\n")

# ============================================================================
# Part 1: Understanding Attention Mechanism
# ============================================================================
print("\n" + "-" * 80)
print("Part 1: Understanding Attention Mechanism")
print("-" * 80)

try:
    from transformers import AutoTokenizer, AutoModel
    
    model_name = "gpt2"
    
    # Get model from previous objective if available
    if 'model' in globals() and 'tokenizer' in globals():
        print(f"\n✅ Using model and tokenizer from previous objectives")
    else:
        print(f"\n📥 Loading tokenizer and model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
    
    # Example text
    text = "The cat sat on the mat"
    print(f"\n📝 Text: '{text}'")
    
    # Tokenize and get embeddings
    token_ids = tokenizer.encode(text, return_tensors="pt")
    tokens = tokenizer.tokenize(text)
    
    print(f"🔤 Tokens: {tokens}")
    
    with torch.no_grad():
        outputs = model(token_ids)
        embeddings = outputs.last_hidden_state  # Shape: [batch, seq_len, hidden_dim]
    
    print(f"\n📊 Embeddings shape: {embeddings.shape}")
    print(f"   - Sequence length: {embeddings.shape[1]} tokens")
    print(f"   - Hidden dimension: {embeddings.shape[2]}")
    
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("   Install with: pip install transformers torch")
    embeddings = None
    tokens = None
except Exception as e:
    print(f"❌ Error: {e}")
    embeddings = None
    tokens = None

# ============================================================================
# Part 2: Manual Attention Calculation
# ============================================================================
print("\n" + "-" * 80)
print("Part 2: Manual Attention Calculation")
print("-" * 80)

if embeddings is not None:
    try:
        # Extract a single sequence (remove batch dimension)
        seq_embeddings = embeddings[0]  # Shape: [seq_len, hidden_dim]
        seq_len, hidden_dim = seq_embeddings.shape
        
        print(f"\n🔍 Computing attention for sequence of {seq_len} tokens")
        
        # Create Query, Key, Value matrices
        # In real transformers, these are learned linear layers
        # For demonstration, we'll use the embeddings directly
        Q = seq_embeddings  # Query
        K = seq_embeddings  # Key
        V = seq_embeddings  # Value
        
        print(f"\n📐 Query/Key/Value shape: {Q.shape}")
        
        # Compute attention scores: Q @ K^T
        # This shows how each token relates to every other token
        attention_scores = torch.matmul(Q, K.transpose(0, 1))  # [seq_len, seq_len]
        
        # Scale by sqrt of hidden dimension (standard attention scaling)
        scale_factor = math.sqrt(hidden_dim)
        attention_scores = attention_scores / scale_factor
        
        print(f"\n📊 Attention scores shape: {attention_scores.shape}")
        print(f"   Each row shows how one token attends to all tokens")
        
        # Apply causal mask (for autoregressive models like GPT)
        # Lower triangle = 1, upper triangle = -inf
        mask = torch.tril(torch.ones(seq_len, seq_len))
        attention_scores = attention_scores.masked_fill(mask == 0, float('-inf'))
        
        # Apply softmax to get attention weights
        attention_weights = F.softmax(attention_scores, dim=-1)
        
        print(f"\n🎯 Attention weights (first token attending to all):")
        first_token_attention = attention_weights[0].tolist()
        for i, (token, weight) in enumerate(zip(tokens, first_token_attention)):
            print(f"   '{token}': {weight:.4f}")
        
        # Compute output: attention_weights @ V
        attention_output = torch.matmul(attention_weights, V)
        
        print(f"\n📤 Attention output shape: {attention_output.shape}")
        print(f"   This is the weighted combination of all token values")
        
    except Exception as e:
        print(f"⚠️  Error computing attention: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# Part 3: Multi-Head Attention Concept
# ============================================================================
print("\n" + "-" * 80)
print("Part 3: Multi-Head Attention Concept")
print("-" * 80)

if 'model' in locals():
    try:
        # Access the first transformer layer
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            
            if hasattr(first_layer, 'attn'):
                attn_layer = first_layer.attn
                
                print(f"\n🔍 Multi-Head Attention Layer:")
                print(f"   Type: {type(attn_layer).__name__}")
                
                # Get number of heads
                if hasattr(attn_layer, 'num_heads'):
                    num_heads = attn_layer.num_heads
                    print(f"   Number of heads: {num_heads}")
                    print(f"   Each head learns different attention patterns!")
                
                # Get head dimension
                if hasattr(attn_layer, 'head_dim'):
                    head_dim = attn_layer.head_dim
                    print(f"   Head dimension: {head_dim}")
                
    except Exception as e:
        print(f"⚠️  Could not inspect attention layer: {e}")

# ============================================================================
# Part 4: Attention Visualization
# ============================================================================
print("\n" + "-" * 80)
print("Part 4: Attention Patterns")
print("-" * 80)

if 'attention_weights' in locals() and tokens is not None:
    try:
        print(f"\n📊 Attention Matrix (showing relationships):")
        print(f"   Rows = attending token, Columns = attended token")
        print(f"\n   {'':12}", end="")
        for token in tokens[:5]:  # Show first 5
            print(f"{token[:8]:>10}", end="")
        print()
        
        for i, token in enumerate(tokens[:5]):
            print(f"   {token[:10]:10}", end="")
            for j in range(min(5, len(tokens))):
                weight = attention_weights[i, j].item()
                print(f"{weight:10.3f}", end="")
            print()
        
        print(f"\n💡 Higher values = stronger attention/relationship")
        
    except Exception as e:
        print(f"⚠️  Could not display attention matrix: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ Objective 3 Complete: Attention")
print("=" * 80)
print("\n📚 Key Takeaways:")
print("  1. Attention computes relationships between all token pairs")
print("  2. Query, Key, Value matrices enable flexible attention patterns")
print("  3. Attention weights show which tokens are most relevant")
print("  4. Multi-head attention learns multiple attention patterns")
print("  5. Causal masking ensures autoregressive generation")
print("\n➡️  Next: Objective 4 - Layers (Stacking Attention + Feedforward)")

# Store for next objective
if 'model' in locals():
    globals()['model'] = model
if 'tokenizer' in locals():
    globals()['tokenizer'] = tokenizer
print("\n💾 Model and tokenizer saved for next objective")
