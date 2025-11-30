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
# Part 2: Real Attention Calculation Using Model's Learned Weights
# ============================================================================
print(formatter.section("Part 2: Real Attention Calculation - Using Model's Learned Weights"))

if embeddings is not None and 'model' in locals():
    try:
        seq_embeddings = embeddings[0]  # [seq_len, hidden_dim]
        seq_len, hidden_dim = seq_embeddings.shape
        
        print(f"\n🔍 Computing REAL attention for sequence of {seq_len} tokens")
        print(f"   Using the model's learned Q, K, V projection weights")
        
        # Get the first attention layer from the model (works with GPT-2, Qwen2, etc.)
        first_layer = None
        attn_layer = None
        
        # Try different architecture patterns (GPT-2 style)
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            if hasattr(first_layer, 'attn'):
                attn_layer = first_layer.attn
        # Try Qwen2/Llama style (model.model.layers)
        elif hasattr(model, 'model') and hasattr(model.model, 'layers'):
            first_layer = model.model.layers[0]
            if hasattr(first_layer, 'self_attn'):
                attn_layer = first_layer.self_attn
        
        if attn_layer is not None:
            # Try different QKV weight names
            if hasattr(attn_layer, 'c_attn'):  # GPT-2 style (combined QKV)
                # Get Q, K, V projection weights (learned by the model!)
                c_attn = attn_layer.c_attn
                qkv_weight = c_attn.weight  # [3 * hidden_dim, hidden_dim]
                qkv_bias = c_attn.bias if c_attn.bias is not None else torch.zeros(3 * hidden_dim, device=seq_embeddings.device)
                
                # Split into Q, K, V weights
                q_weight = qkv_weight[:hidden_dim, :]  # [hidden_dim, hidden_dim]
                k_weight = qkv_weight[hidden_dim:2*hidden_dim, :]  # [hidden_dim, hidden_dim]
                v_weight = qkv_weight[2*hidden_dim:, :]  # [hidden_dim, hidden_dim]
                
                q_bias = qkv_bias[:hidden_dim]
                k_bias = qkv_bias[hidden_dim:2*hidden_dim]
                v_bias = qkv_bias[2*hidden_dim:]
            elif hasattr(attn_layer, 'q_proj') and hasattr(attn_layer, 'k_proj') and hasattr(attn_layer, 'v_proj'):  # Qwen2/Llama style (separate)
                # Qwen2 uses separate projections
                q_weight = attn_layer.q_proj.weight  # [hidden_dim, hidden_dim]
                k_weight = attn_layer.k_proj.weight  # [hidden_dim, hidden_dim]
                v_weight = attn_layer.v_proj.weight  # [hidden_dim, hidden_dim]
                
                q_bias = attn_layer.q_proj.bias if attn_layer.q_proj.bias is not None else torch.zeros(hidden_dim, device=seq_embeddings.device)
                k_bias = attn_layer.k_proj.bias if attn_layer.k_proj.bias is not None else torch.zeros(hidden_dim, device=seq_embeddings.device)
                v_bias = attn_layer.v_proj.bias if attn_layer.v_proj.bias is not None else torch.zeros(hidden_dim, device=seq_embeddings.device)
            else:
                raise ValueError(f"Unknown attention architecture. Available attributes: {dir(attn_layer)}")
            
            if 'q_weight' in locals():
                
                print(f"\n📐 Learned Q/K/V Projection Weights:")
                print(f"   Q weight shape: {q_weight.shape}")
                print(f"   K weight shape: {k_weight.shape}")
                print(f"   V weight shape: {v_weight.shape}")
                print(f"   These are REAL learned weights from the trained model!")
                
                # Project embeddings to Q, K, V using learned weights
                # Add batch dimension for matrix multiplication
                emb_batch = seq_embeddings.unsqueeze(0)  # [1, seq_len, hidden_dim]
                
                Q = torch.matmul(emb_batch, q_weight.t()) + q_bias  # [1, seq_len, hidden_dim]
                K = torch.matmul(emb_batch, k_weight.t()) + k_bias  # [1, seq_len, hidden_dim]
                V = torch.matmul(emb_batch, v_weight.t()) + v_bias  # [1, seq_len, hidden_dim]
                
                # Remove batch dimension for easier computation
                Q = Q[0]  # [seq_len, hidden_dim]
                K = K[0]  # [seq_len, hidden_dim]
                V = V[0]  # [seq_len, hidden_dim]
                
                print(f"\n📊 Q/K/V after projection: {Q.shape}")
                
                # Compute attention scores: Q @ K^T
                attention_scores = torch.matmul(Q, K.transpose(0, 1))  # [seq_len, seq_len]
                
                # Scale by sqrt(hidden_dim) - standard attention scaling
                scale_factor = math.sqrt(hidden_dim)
                attention_scores = attention_scores / scale_factor
                
                print(f"\n📊 Attention scores shape: {attention_scores.shape}")
                print(f"   Each row shows how one token attends to all tokens")
                print(f"   Scaled by √{hidden_dim} = {scale_factor:.1f}")
                
                # Apply causal mask (lower triangular)
                mask = torch.tril(torch.ones(seq_len, seq_len, device=attention_scores.device))
                attention_scores = attention_scores.masked_fill(mask == 0, float('-inf'))
                
                # Apply softmax to get attention weights
                attention_weights = F.softmax(attention_scores, dim=-1)  # [seq_len, seq_len]
                
                print(f"\n🎯 REAL Attention weights (first token attending to all):")
                first_token_attention = attention_weights[0].cpu().tolist()
                for i, (token, weight) in enumerate(zip(tokens, first_token_attention)):
                    print(f"   '{token}': {weight:.4f}")
                
                # Compute attention output: weights @ V
                attention_output = torch.matmul(attention_weights, V)  # [seq_len, hidden_dim]
                print(f"\n📤 Attention output shape: {attention_output.shape}")
                print(f"   This is the weighted combination of all token values")
                
                max_attn_idx = first_token_attention.index(max(first_token_attention))
                max_attn_token = tokens[max_attn_idx] if tokens and max_attn_idx < len(tokens) else "N/A"
                max_attn_val = max(first_token_attention)
                
                print(formatter.output_summary([
                    f"Using REAL learned Q/K/V weights from the model (not fake embeddings!)",
                    f"Attention scores matrix: {attention_scores.shape} (each token × each token)",
                    f"After softmax: attention weights sum to 1.0 per row",
                    f"First token '{tokens[0] if tokens else 'N/A'}' attends most to: {max_attn_token} ({max_attn_val:.4f})",
                    "Causal mask ensures tokens only attend to previous tokens (autoregressive)",
                    f"Attention output combines all token values weighted by attention: {attention_output.shape}"
                ]))
            else:
                print("⚠️  Could not extract Q/K/V weights from attention layer")
        else:
            print("⚠️  Could not access transformer layers - model architecture not recognized")
        
    except Exception as e:
        print(f"⚠️  Error computing real attention: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# Part 3: Multi-Head Attention - Computing Real Multi-Head Patterns
# ============================================================================
print(formatter.section("Part 3: Multi-Head Attention - Computing Real Multi-Head Patterns"))

if 'model' in locals() and embeddings is not None:
    try:
        # Get first layer and attention module (works with GPT-2, Qwen2, etc.)
        first_layer = None
        attn_layer = None
        
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):  # GPT-2 style
            first_layer = model.transformer.h[0]
            if hasattr(first_layer, 'attn'):
                attn_layer = first_layer.attn
        elif hasattr(model, 'model') and hasattr(model.model, 'layers'):  # Qwen2/Llama style
            first_layer = model.model.layers[0]
            if hasattr(first_layer, 'self_attn'):
                attn_layer = first_layer.self_attn
        
        if attn_layer is not None:
                # Get number of heads (Qwen 2.5-1.5B has 16 heads, but we'll detect dynamically)
            num_heads = getattr(attn_layer, 'num_heads', None)
            if num_heads is None:
                # Try to infer from config
                if hasattr(model, 'config') and hasattr(model.config, 'num_attention_heads'):
                    num_heads = model.config.num_attention_heads
                else:
                    num_heads = hidden_dim // 64  # Default assumption
            head_dim = hidden_dim // num_heads
            
            print(f"\n🔍 Multi-Head Attention Architecture:")
            print(f"   Number of heads: {num_heads}")
            print(f"   Head dimension: {head_dim}")
            print(f"   Total hidden dimension: {hidden_dim}")
            print(f"   Each head computes attention independently!")
            
            # Get QKV weights (handle both GPT-2 and Qwen2 architectures)
            seq_embeddings = embeddings[0]  # [seq_len, hidden_dim]
            emb_batch = seq_embeddings.unsqueeze(0)  # [1, seq_len, hidden_dim]
            
            if hasattr(attn_layer, 'c_attn'):  # GPT-2 style (combined)
                c_attn = attn_layer.c_attn
                qkv_weight = c_attn.weight  # [3 * hidden_dim, hidden_dim]
                qkv_bias = c_attn.bias if c_attn.bias is not None else torch.zeros(3 * hidden_dim, device=emb_batch.device)
                
                # Project to QKV
                qkv = torch.matmul(emb_batch, qkv_weight.t()) + qkv_bias  # [1, seq_len, 3*hidden_dim]
                
                # Split into Q, K, V
                Q = qkv[:, :, :hidden_dim]  # [1, seq_len, hidden_dim]
                K = qkv[:, :, hidden_dim:2*hidden_dim]  # [1, seq_len, hidden_dim]
                V = qkv[:, :, 2*hidden_dim:]  # [1, seq_len, hidden_dim]
            elif hasattr(attn_layer, 'q_proj'):  # Qwen2/Llama style (separate)
                Q = torch.matmul(emb_batch, attn_layer.q_proj.weight.t())
                if attn_layer.q_proj.bias is not None:
                    Q = Q + attn_layer.q_proj.bias
                
                K = torch.matmul(emb_batch, attn_layer.k_proj.weight.t())
                if attn_layer.k_proj.bias is not None:
                    K = K + attn_layer.k_proj.bias
                
                V = torch.matmul(emb_batch, attn_layer.v_proj.weight.t())
                if attn_layer.v_proj.bias is not None:
                    V = V + attn_layer.v_proj.bias
            else:
                raise ValueError(f"Unknown attention architecture for multi-head")
            
            # Reshape for multi-head: [batch, seq_len, num_heads, head_dim]
            Q = Q.view(1, seq_len, num_heads, head_dim).transpose(1, 2)  # [1, num_heads, seq_len, head_dim]
            K = K.view(1, seq_len, num_heads, head_dim).transpose(1, 2)  # [1, num_heads, seq_len, head_dim]
            V = V.view(1, seq_len, num_heads, head_dim).transpose(1, 2)  # [1, num_heads, seq_len, head_dim]
            
            print(f"\n📊 Multi-Head Q/K/V shapes: {Q.shape}")
            print(f"   Each head has its own Q, K, V projections")
            
            # Compute attention for each head
            attention_scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(head_dim)  # [1, num_heads, seq_len, seq_len]
            
            # Apply causal mask
            mask = torch.tril(torch.ones(seq_len, seq_len, device=attention_scores.device))
            attention_scores = attention_scores.masked_fill(mask.unsqueeze(0).unsqueeze(0) == 0, float('-inf'))
            
            # Softmax
            attention_weights_multi = F.softmax(attention_scores, dim=-1)  # [1, num_heads, seq_len, seq_len]
            
            # Show attention patterns for first few heads
            print(f"\n🎯 Attention Patterns Across Heads (first token):")
            if tokens is not None:
                for head_idx in range(min(3, num_heads)):
                    head_weights = attention_weights_multi[0, head_idx, 0].cpu().tolist()
                    max_idx = head_weights.index(max(head_weights))
                    print(f"   Head {head_idx}: attends most to '{tokens[max_idx] if max_idx < len(tokens) else 'N/A'}' ({max(head_weights):.4f})")
            else:
                for head_idx in range(min(3, num_heads)):
                    head_weights = attention_weights_multi[0, head_idx, 0].cpu().tolist()
                    print(f"   Head {head_idx}: max attention weight = {max(head_weights):.4f}")
            
            # Compute attention output per head
            attention_output_multi = torch.matmul(attention_weights_multi, V)  # [1, num_heads, seq_len, head_dim]
            
            # Concatenate heads
            attention_output_multi = attention_output_multi.transpose(1, 2).contiguous()  # [1, seq_len, num_heads, head_dim]
            attention_output_multi = attention_output_multi.view(1, seq_len, hidden_dim)  # [1, seq_len, hidden_dim]
            
            print(f"\n📤 Multi-head attention output shape: {attention_output_multi.shape}")
            print(f"   All {num_heads} heads concatenated together")
            
            head0_max_idx = attention_weights_multi[0, 0, 0].argmax().item()
            head0_token = tokens[head0_max_idx] if tokens and head0_max_idx < len(tokens) else 'N/A'
            
            print(formatter.output_summary([
                f"Model uses {num_heads} attention heads, each with dimension {head_dim}",
                "Each head computes attention independently using different learned patterns",
                f"Head 0 attends most to: '{head0_token}'",
                "Heads are concatenated and projected to final dimension",
                "Multi-head allows model to attend to different types of relationships simultaneously"
            ]))
        else:
            print("⚠️  Could not access attention layer")
    except Exception as e:
        print(f"⚠️  Could not compute multi-head attention: {e}")
        import traceback
        traceback.print_exc()

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
