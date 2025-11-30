# ============================================================================
# Objective 6: Parameters - Model Weights & Configuration
# ============================================================================
# Understanding model parameters, weights, and configuration

import torch

print("=" * 80)
print("OBJECTIVE 6: PARAMETERS")
print("=" * 80)
print("\n🧠 Learning Goal: Understand model parameters and configuration")
print("   Parameters are learned weights that define model behavior.\n")

# ============================================================================
# Part 1: Model Configuration
# ============================================================================
print("\n" + "-" * 80)
print("Part 1: Model Configuration")
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
    
    # Access model configuration
    if hasattr(model, 'config'):
        config = model.config
        
        print(f"\n📋 Model Configuration:")
        print(f"   Model type: {config.model_type}")
        
        # Architecture parameters
        if hasattr(config, 'n_layer'):
            print(f"   Number of layers: {config.n_layer}")
        if hasattr(config, 'n_head'):
            print(f"   Number of attention heads: {config.n_head}")
        if hasattr(config, 'n_embd'):
            print(f"   Embedding dimension: {config.n_embd}")
        if hasattr(config, 'n_positions'):
            print(f"   Max sequence length: {config.n_positions}")
        if hasattr(config, 'vocab_size'):
            print(f"   Vocabulary size: {config.vocab_size}")
        
        # Activation and other settings
        if hasattr(config, 'activation_function'):
            print(f"   Activation: {config.activation_function}")
        if hasattr(config, 'layer_norm_epsilon'):
            print(f"   LayerNorm epsilon: {config.layer_norm_epsilon}")
        
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("   Install with: pip install transformers torch")
    model = None
except Exception as e:
    print(f"❌ Error: {e}")
    model = None

# ============================================================================
# Part 2: Parameter Counting
# ============================================================================
print("\n" + "-" * 80)
print("Part 2: Parameter Counting")
print("-" * 80)

if model is not None:
    try:
        # Count total parameters
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"\n📊 Parameter Statistics:")
        print(f"   Total parameters: {total_params:,}")
        print(f"   Trainable parameters: {trainable_params:,}")
        print(f"   Memory (float32): ~{total_params * 4 / 1024 / 1024:.2f} MB")
        print(f"   Memory (float16): ~{total_params * 2 / 1024 / 1024:.2f} MB")
        
        # Count by layer type
        print(f"\n🔍 Parameters by Component:")
        embedding_params = 0
        attention_params = 0
        mlp_params = 0
        norm_params = 0
        other_params = 0
        
        for name, param in model.named_parameters():
            num_params = param.numel()
            if 'embed' in name.lower():
                embedding_params += num_params
            elif 'attn' in name.lower():
                attention_params += num_params
            elif 'mlp' in name.lower() or 'c_fc' in name.lower() or 'c_proj' in name.lower():
                mlp_params += num_params
            elif 'ln' in name.lower() or 'norm' in name.lower():
                norm_params += num_params
            else:
                other_params += num_params
        
        print(f"   Embeddings: {embedding_params:,} ({embedding_params/total_params*100:.1f}%)")
        print(f"   Attention: {attention_params:,} ({attention_params/total_params*100:.1f}%)")
        print(f"   MLP/Feedforward: {mlp_params:,} ({mlp_params/total_params*100:.1f}%)")
        print(f"   LayerNorm: {norm_params:,} ({norm_params/total_params*100:.1f}%)")
        print(f"   Other: {other_params:,} ({other_params/total_params*100:.1f}%)")
        
    except Exception as e:
        print(f"⚠️  Error counting parameters: {e}")

# ============================================================================
# Part 3: Weight Inspection
# ============================================================================
print("\n" + "-" * 80)
print("Part 3: Weight Inspection")
print("-" * 80)

if model is not None:
    try:
        # Inspect a specific weight matrix
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'wte'):
            embedding_layer = model.transformer.wte
            
            print(f"\n🔍 Embedding Layer Weights:")
            print(f"   Shape: {embedding_layer.weight.shape}")
            print(f"   Dtype: {embedding_layer.weight.dtype}")
            print(f"   Requires grad: {embedding_layer.weight.requires_grad}")
            
            # Weight statistics
            weight = embedding_layer.weight.data
            print(f"\n📊 Weight Statistics:")
            print(f"   Mean: {weight.mean().item():.6f}")
            print(f"   Std: {weight.std().item():.6f}")
            print(f"   Min: {weight.min().item():.6f}")
            print(f"   Max: {weight.max().item():.6f}")
        
        # Inspect attention weights
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            if hasattr(first_layer, 'attn') and hasattr(first_layer.attn, 'c_attn'):
                attn_weights = first_layer.attn.c_attn.weight
                print(f"\n🔍 Attention Weights (QKV projection):")
                print(f"   Shape: {attn_weights.shape}")
                print(f"   This projects embeddings to Q, K, V")
                
    except Exception as e:
        print(f"⚠️  Error inspecting weights: {e}")

# ============================================================================
# Part 4: Model Architecture Inspection
# ============================================================================
print("\n" + "-" * 80)
print("Part 4: Model Architecture Inspection")
print("-" * 80)

if model is not None:
    try:
        print(f"\n🏗️  Model Structure:")
        print(f"   Type: {type(model).__name__}")
        
        # List main components
        print(f"\n📦 Main Components:")
        for name, module in model.named_children():
            num_params = sum(p.numel() for p in module.parameters())
            print(f"   {name}: {type(module).__name__} ({num_params:,} params)")
        
        # Layer structure
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            num_layers = len(model.transformer.h)
            print(f"\n🔢 Layer Details:")
            print(f"   Number of transformer blocks: {num_layers}")
            
            if num_layers > 0:
                first_block = model.transformer.h[0]
                block_params = sum(p.numel() for p in first_block.parameters())
                print(f"   Parameters per block: ~{block_params:,}")
                print(f"   Total block parameters: ~{block_params * num_layers:,}")
        
    except Exception as e:
        print(f"⚠️  Error inspecting architecture: {e}")

# ============================================================================
# Part 5: Parameter Sharing and Efficiency
# ============================================================================
print("\n" + "-" * 80)
print("Part 5: Parameter Sharing and Efficiency")
print("-" * 80)

print(f"\n💡 Parameter Efficiency Techniques:")
print(f"   1. Weight Sharing: Same weights used in multiple places")
print(f"   2. LoRA: Low-Rank Adaptation (train small matrices)")
print(f"   3. Quantization: Use fewer bits (float16, int8)")
print(f"   4. Pruning: Remove less important parameters")
print(f"   5. Distillation: Smaller model learns from larger")

if model is not None:
    try:
        # Check for shared embeddings
        if hasattr(model, 'transformer'):
            if hasattr(model.transformer, 'wte') and hasattr(model, 'lm_head'):
                wte = model.transformer.wte
                lm_head = model.lm_head
                
                # Check if weights are shared
                if hasattr(wte, 'weight') and hasattr(lm_head, 'weight'):
                    if wte.weight.data_ptr() == lm_head.weight.data_ptr():
                        print(f"\n✅ Weight Sharing Detected:")
                        print(f"   Embedding and output layers share weights!")
                        print(f"   Saves: {wte.weight.numel() * 4 / 1024 / 1024:.2f} MB")
                    else:
                        print(f"\n📊 No weight sharing between embeddings and output")
        
    except Exception as e:
        print(f"⚠️  Could not check parameter sharing: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ Objective 6 Complete: Parameters")
print("=" * 80)
print("\n📚 Key Takeaways:")
print("  1. Model config defines architecture (layers, heads, dimensions)")
print("  2. Parameters are learned weights (millions to billions)")
print("  3. Different components use different parameter amounts")
print("  4. Weight sharing can reduce memory and parameters")
print("  5. Parameters define model capacity and behavior")
print("\n" + "=" * 80)
print("🎉 ALL OBJECTIVES COMPLETE!")
print("=" * 80)
print("\n📚 You now understand the complete LLM pipeline:")
print("   1. Tokens → Text split into subword units")
print("   2. Embeddings → Tokens converted to vectors")
print("   3. Attention → Computing relationships between tokens")
print("   4. Layers → Stacking attention + feedforward blocks")
print("   5. Tensors → Multi-dimensional data representation")
print("   6. Parameters → Learned weights that define behavior")
print("\n🔗 Complete Flow:")
print("   Text → Tokens → Embeddings → Attention → Layers → Tensors → Parameters")
print("\n✅ You're ready to build and understand LLMs!")
