# ============================================================================
# Objective 4: Layers - Transformer Layers
# ============================================================================
# Understanding transformer layer architecture

import torch
import torch.nn as nn

print("=" * 80)
print("OBJECTIVE 4: LAYERS")
print("=" * 80)
print("\n🧠 Learning Goal: Understand transformer layer architecture")
print("   Layers stack attention and feedforward blocks.\n")

# ============================================================================
# Part 1: Transformer Block Structure
# ============================================================================
print("\n" + "-" * 80)
print("Part 1: Transformer Block Structure")
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
    
    # Access transformer layers
    if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
        layers = model.transformer.h
        num_layers = len(layers)
        
        print(f"\n📊 Model Architecture:")
        print(f"   Number of transformer layers: {num_layers}")
        
        # Inspect first layer
        first_layer = layers[0]
        print(f"\n🔍 First Layer Structure:")
        print(f"   Type: {type(first_layer).__name__}")
        
        # List components
        components = []
        if hasattr(first_layer, 'ln_1'):
            components.append("LayerNorm 1")
        if hasattr(first_layer, 'attn'):
            components.append("Multi-Head Attention")
        if hasattr(first_layer, 'ln_2'):
            components.append("LayerNorm 2")
        if hasattr(first_layer, 'mlp'):
            components.append("Feedforward MLP")
        
        print(f"   Components: {' → '.join(components)}")
        
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("   Install with: pip install transformers torch")
    model = None
except Exception as e:
    print(f"❌ Error: {e}")
    model = None

# ============================================================================
# Part 2: Layer Normalization
# ============================================================================
print("\n" + "-" * 80)
print("Part 2: Layer Normalization")
print("-" * 80)

if model is not None and 'model' in locals():
    try:
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            
            if hasattr(first_layer, 'ln_1'):
                ln1 = first_layer.ln_1
                print(f"\n🔍 LayerNorm 1:")
                print(f"   Type: {type(ln1).__name__}")
                if isinstance(ln1, nn.LayerNorm):
                    print(f"   Normalized shape: {ln1.normalized_shape}")
                    print(f"   Epsilon: {ln1.eps}")
                    print(f"   Purpose: Stabilize training, enable deeper networks")
            
            if hasattr(first_layer, 'ln_2'):
                ln2 = first_layer.ln_2
                print(f"\n🔍 LayerNorm 2:")
                print(f"   Type: {type(ln2).__name__}")
                print(f"   Applied after attention, before feedforward")
                
    except Exception as e:
        print(f"⚠️  Could not inspect layer normalization: {e}")

# ============================================================================
# Part 3: Feedforward Network (MLP)
# ============================================================================
print("\n" + "-" * 80)
print("Part 3: Feedforward Network (MLP)")
print("-" * 80)

if model is not None and 'model' in locals():
    try:
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            
            if hasattr(first_layer, 'mlp'):
                mlp = first_layer.mlp
                print(f"\n🔍 Feedforward MLP:")
                print(f"   Type: {type(mlp).__name__}")
                
                # Inspect MLP structure
                if isinstance(mlp, nn.Module):
                    print(f"   Structure:")
                    for name, module in mlp.named_children():
                        if isinstance(module, nn.Linear):
                            print(f"     {name}: Linear({module.in_features} → {module.out_features})")
                        elif isinstance(module, nn.GELU) or isinstance(module, nn.ReLU):
                            print(f"     {name}: {type(module).__name__} activation")
                
                print(f"\n💡 MLP typically: Linear → Activation → Linear")
                print(f"   Expands dimension (e.g., 768 → 3072 → 768)")
                
    except Exception as e:
        print(f"⚠️  Could not inspect MLP: {e}")

# ============================================================================
# Part 4: Residual Connections
# ============================================================================
print("\n" + "-" * 80)
print("Part 4: Residual Connections")
print("-" * 80)

print("\n📚 Residual Connection Pattern:")
print("   x → LayerNorm → Attention → + x (residual)")
print("   x → LayerNorm → MLP → + x (residual)")
print("\n💡 Benefits:")
print("   1. Enables gradient flow through deep networks")
print("   2. Allows identity mapping (skip connection)")
print("   3. Makes training of deep networks possible")

# ============================================================================
# Part 5: Stacking Multiple Layers
# ============================================================================
print("\n" + "-" * 80)
print("Part 5: Stacking Multiple Layers")
print("-" * 80)

if model is not None and 'model' in locals():
    try:
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            layers = model.transformer.h
            num_layers = len(layers)
            
            print(f"\n📊 Layer Stacking:")
            print(f"   Total layers: {num_layers}")
            print(f"   Each layer processes the output of the previous layer")
            
            # Show layer progression
            print(f"\n🔄 Data Flow Through Layers:")
            print(f"   Input embeddings")
            for i in range(min(3, num_layers)):
                print(f"   ↓ Layer {i+1}: Attention + MLP")
            if num_layers > 3:
                print(f"   ↓ ... ({num_layers - 3} more layers)")
            print(f"   ↓ Final LayerNorm")
            print(f"   ↓ Output embeddings")
            
            # Count parameters per layer
            if num_layers > 0:
                first_layer_params = sum(p.numel() for p in layers[0].parameters())
                print(f"\n📈 Parameters per layer: ~{first_layer_params:,}")
                print(f"   Total transformer parameters: ~{first_layer_params * num_layers:,}")
                
    except Exception as e:
        print(f"⚠️  Could not analyze layer stacking: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ Objective 4 Complete: Layers")
print("=" * 80)
print("\n📚 Key Takeaways:")
print("  1. Transformer layers = Attention + Feedforward + Residuals")
print("  2. LayerNorm stabilizes training and enables deep networks")
print("  3. MLP expands and contracts dimensions (e.g., 768 → 3072 → 768)")
print("  4. Residual connections enable gradient flow")
print("  5. Multiple layers process information sequentially")
print("\n➡️  Next: Objective 5 - Tensors (Data Representation)")

# Store for next objective
if 'model' in locals():
    globals()['model'] = model
if 'tokenizer' in locals():
    globals()['tokenizer'] = tokenizer
print("\n💾 Model and tokenizer saved for next objective")
