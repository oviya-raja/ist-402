# ============================================================================
# Objective 3: Attention - Vector Relationships
# ============================================================================
# Understanding how attention mechanisms compute relationships between tokens

from llm_fundamentals_support import (
    LLMFundamentalsSupport, ModelLoader, TextProcessor, EmbeddingExtractor,
    Formatter, StateManager
)
import torch
import torch.nn.functional as F
import math

support = LLMFundamentalsSupport()
formatter = Formatter()
state_mgr = StateManager()

print(formatter.header("OBJECTIVE 3: ATTENTION"))
print(formatter.learning_intro(
    concept="Attention Mechanism",
    description="Attention computes relationships between all token pairs. Each token can attend to (focus on) all other tokens, creating a relationship matrix.",
    what_we_learn=[
        "How attention computes relationships between tokens",
        "Query, Key, Value (QKV) matrices and their roles",
        "Attention scores and weights (softmax probabilities)",
        "Multi-head attention and different attention patterns",
        "Causal masking for autoregressive models"
    ],
    what_we_do=[
        "Manually compute attention scores from embeddings",
        "Create Q, K, V matrices and compute attention",
        "Apply causal masking and softmax",
        "Visualize attention patterns between tokens",
        "Inspect multi-head attention in the model"
    ],
    hands_on=[
        "Use embeddings from Objective 2",
        "Compute Q @ K^T to get attention scores",
        "Scale by sqrt(hidden_dim) and apply causal mask",
        "Apply softmax to get attention weights",
        "Compute attention output: weights @ V",
        "Visualize attention matrix showing token relationships"
    ]
))

# ============================================================================
# Part 1: Understanding Attention Mechanism
# ============================================================================
print(formatter.section("Part 1: Understanding Attention Mechanism - Setup"))

loader = ModelLoader()
try:
    tokenizer, model = loader.load_both(globals())
    if 'model' in globals() and 'tokenizer' in globals():
        print("✅ Using model and tokenizer from previous objectives")
    else:
        print(f"📥 Loaded tokenizer and model: {loader.model_name}")
    
    processor = TextProcessor(tokenizer)
    extractor = EmbeddingExtractor(model, tokenizer)
    
    text = "The cat sat on the mat"
    print(f"\n📝 Text: '{text}'")
    
    tokens = processor.tokenize(text)
    embeddings = extractor.get_embeddings(text)
    
    print(f"🔤 Tokens: {tokens}")
    print(f"\n📊 Embeddings shape: {embeddings.shape}")
    print(f"   - Sequence length: {embeddings.shape[1]} tokens")
    print(f"   - Hidden dimension: {embeddings.shape[2]}")
    
    print(formatter.output_summary([
        f"Text '{text}' → {len(tokens)} tokens → embeddings shape {embeddings.shape}",
        "Embeddings are the input to attention mechanism",
        "Each token's embedding will be used to compute relationships"
    ]))
    
except Exception as e:
    print(f"❌ Error: {e}")
    embeddings = None
    tokens = None

# ============================================================================
# Part 2: Manual Attention Calculation
# ============================================================================
print(formatter.section("Part 2: Manual Attention Calculation - Hands-On Code"))

if embeddings is not None:
    try:
        seq_embeddings = embeddings[0]
        seq_len, hidden_dim = seq_embeddings.shape
        
        print(f"\n🔍 Computing attention for sequence of {seq_len} tokens")
        
        Q = K = V = seq_embeddings
        print(f"\n📐 Query/Key/Value shape: {Q.shape}")
        print(f"   (In real transformers, Q/K/V are learned linear projections)")
        
        attention_scores = torch.matmul(Q, K.transpose(0, 1))
        scale_factor = math.sqrt(hidden_dim)
        attention_scores = attention_scores / scale_factor
        
        print(f"\n📊 Attention scores shape: {attention_scores.shape}")
        print(f"   Each row shows how one token attends to all tokens")
        print(f"   Scaled by √{hidden_dim} = {scale_factor:.1f}")
        
        mask = torch.tril(torch.ones(seq_len, seq_len))
        attention_scores = attention_scores.masked_fill(mask == 0, float('-inf'))
        attention_weights = F.softmax(attention_scores, dim=-1)
        
        print(f"\n🎯 Attention weights (first token attending to all):")
        first_token_attention = attention_weights[0].tolist()
        for i, (token, weight) in enumerate(zip(tokens, first_token_attention)):
            print(f"   '{token}': {weight:.4f}")
        
        attention_output = torch.matmul(attention_weights, V)
        print(f"\n📤 Attention output shape: {attention_output.shape}")
        print(f"   This is the weighted combination of all token values")
        
        max_attn_idx = first_token_attention.index(max(first_token_attention))
        max_attn_token = tokens[max_attn_idx] if tokens and max_attn_idx < len(tokens) else "N/A"
        print(formatter.output_summary([
            f"Attention scores matrix: {attention_scores.shape} (each token × each token)",
            f"After softmax: attention weights sum to 1.0 per row",
            f"First token '{tokens[0] if tokens else 'N/A'}' attends most to: {max_attn_token} ({max(first_token_attention):.4f})",
            "Causal mask ensures tokens only attend to previous tokens (autoregressive)",
            f"Attention output combines all token values weighted by attention: {attention_output.shape}"
        ]))
        
    except Exception as e:
        print(f"⚠️  Error computing attention: {e}")

# ============================================================================
# Part 3: Multi-Head Attention Concept
# ============================================================================
print(formatter.section("Part 3: Multi-Head Attention - Model Architecture"))

if 'model' in locals():
    try:
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            if hasattr(first_layer, 'attn'):
                attn_layer = first_layer.attn
                print(f"\n🔍 Multi-Head Attention Layer:")
                print(f"   Type: {type(attn_layer).__name__}")
                if hasattr(attn_layer, 'num_heads'):
                    print(f"   Number of heads: {attn_layer.num_heads}")
                    print(f"   Each head learns different attention patterns!")
                if hasattr(attn_layer, 'head_dim'):
                    print(f"   Head dimension: {attn_layer.head_dim}")
                
                print(formatter.output_summary([
                    f"Model uses {attn_layer.num_heads if hasattr(attn_layer, 'num_heads') else 'multiple'} attention heads",
                    "Each head computes attention independently and learns different patterns",
                    "Heads are concatenated and projected to final dimension",
                    "Multi-head allows model to attend to different types of relationships"
                ]))
    except Exception as e:
        print(f"⚠️  Could not inspect attention layer: {e}")

# ============================================================================
# Part 4: Attention Patterns
# ============================================================================
print(formatter.section("Part 4: Attention Patterns - Visualization"))

if 'attention_weights' in locals() and tokens is not None:
    try:
        print(f"\n📊 Attention Matrix (showing relationships):")
        print(f"   Rows = attending token, Columns = attended token")
        print(f"\n   {'':12}", end="")
        for token in tokens[:5]:
            print(f"{token[:8]:>10}", end="")
        print()
        
        for i, token in enumerate(tokens[:5]):
            print(f"   {token[:10]:10}", end="")
            for j in range(min(5, len(tokens))):
                weight = attention_weights[i, j].item()
                print(f"{weight:10.3f}", end="")
            print()
        print(f"\n💡 Higher values = stronger attention/relationship")
        
        print(formatter.output_summary([
            "Attention matrix shows which tokens attend to which tokens",
            "Diagonal and lower triangle have values (causal masking)",
            "Upper triangle is -inf (future tokens masked out)",
            "Each row sums to 1.0 (softmax normalization)"
        ]))
    except Exception as e:
        print(f"⚠️  Could not display attention matrix: {e}")

# ============================================================================
# Summary
# ============================================================================
takeaways = [
    "Attention computes relationships between all token pairs",
    "Query, Key, Value matrices enable flexible attention patterns",
    "Attention weights show which tokens are most relevant",
    "Multi-head attention learns multiple attention patterns",
    "Causal masking ensures autoregressive generation"
]
print(formatter.summary("Objective 3 Complete: Attention", takeaways, "Objective 4 - Layers (Stacking Attention + Feedforward)"))

# Save state
if 'model' in locals() and 'tokenizer' in locals():
    state_mgr.save_to_globals(globals(), model=model, tokenizer=tokenizer)
    print("\n💾 Model and tokenizer saved for next objective")
