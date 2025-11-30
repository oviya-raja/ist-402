# ============================================================================
# Objective 4: Layers - Transformer Layers
# ============================================================================
# Understanding transformer layer architecture

from llm_fundamentals_support import (
    LLMFundamentalsSupport, ModelLoader, Formatter, StateManager
)
import torch
import torch.nn as nn

support = LLMFundamentalsSupport()
formatter = Formatter()
state_mgr = StateManager()

print(formatter.header("OBJECTIVE 4: LAYERS"))
print(formatter.learning_intro(
    concept="Transformer Layers",
    description="Transformer layers stack attention and feedforward blocks with residual connections and layer normalization. Multiple layers process information sequentially.",
    what_we_learn=[
        "Transformer block structure (Attention + MLP + Residuals)",
        "Layer normalization and its role",
        "Feedforward network (MLP) architecture",
        "Residual connections and gradient flow",
        "How multiple layers process information sequentially"
    ],
    what_we_do=[
        "Inspect transformer layer architecture in the model",
        "Examine LayerNorm components and their placement",
        "Analyze feedforward MLP structure",
        "Understand residual connection patterns",
        "Count parameters per layer and total"
    ],
    hands_on=[
        "Access model.transformer.h to see all layers",
        "Inspect first layer: ln_1 → attn → ln_2 → mlp",
        "Examine LayerNorm parameters (normalized_shape, epsilon)",
        "Analyze MLP structure (Linear → GELU → Linear)",
        "Count parameters: ~{X}M per layer × {N} layers"
    ]
))

# Part 1: Transformer Block Structure
print(formatter.section("Part 1: Transformer Block Structure - Architecture Inspection"))

loader = ModelLoader()
try:
    tokenizer, model = loader.load_both(globals())
    if 'model' in globals() and 'tokenizer' in globals():
        print("✅ Using model and tokenizer from previous objectives")
    else:
        print(f"📥 Loaded tokenizer and model: {loader.model_name}")
    
    if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
        layers = model.transformer.h
        num_layers = len(layers)
        
        print(f"\n📊 Model Architecture:")
        print(f"   Number of transformer layers: {num_layers}")
        
        first_layer = layers[0]
        print(f"\n🔍 First Layer Structure:")
        print(f"   Type: {type(first_layer).__name__}")
        
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
        
        print(formatter.output_summary([
            f"Model has {num_layers} transformer layers stacked sequentially",
            f"Each layer contains: {' → '.join(components)}",
            "Layers process embeddings from previous layer",
            "Output of last layer is the final representation"
        ]))
        
except Exception as e:
    print(f"❌ Error: {e}")
    model = None

# Part 2: Layer Normalization
print(formatter.section("Part 2: Layer Normalization - Stabilization Mechanism"))

if model is not None and hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
    try:
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
        
        print(formatter.output_summary([
            "LayerNorm normalizes activations to mean=0, std=1",
            "Applied before attention and before MLP (pre-norm architecture)",
            "Enables training of very deep networks (100+ layers)",
            "Epsilon prevents division by zero in normalization"
        ]))
    except Exception as e:
        print(f"⚠️  Could not inspect layer normalization: {e}")

# Part 3: Feedforward Network (MLP)
print(formatter.section("Part 3: Feedforward Network (MLP) - Expansion & Contraction"))

if model is not None and hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
    try:
        first_layer = model.transformer.h[0]
        if hasattr(first_layer, 'mlp'):
            mlp = first_layer.mlp
            print(f"\n🔍 Feedforward MLP:")
            print(f"   Type: {type(mlp).__name__}")
            
            if isinstance(mlp, nn.Module):
                print(f"   Structure:")
                for name, module in mlp.named_children():
                    if isinstance(module, nn.Linear):
                        print(f"     {name}: Linear({module.in_features} → {module.out_features})")
                    elif isinstance(module, (nn.GELU, nn.ReLU)):
                        print(f"     {name}: {type(module).__name__} activation")
            
            print(f"\n💡 MLP typically: Linear → Activation → Linear")
            print(f"   Expands dimension (e.g., 768 → 3072 → 768)")
            
            print(formatter.output_summary([
                "MLP expands then contracts dimensions (e.g., 768 → 3072 → 768)",
                "First linear layer expands (4x typical)",
                "Activation function (GELU/ReLU) adds non-linearity",
                "Second linear layer contracts back to original dimension",
                "This allows model to learn complex transformations"
            ]))
    except Exception as e:
        print(f"⚠️  Could not inspect MLP: {e}")

# Part 4: Residual Connections
print(formatter.section("Part 4: Residual Connections - Gradient Flow"))

print("\n📚 Residual Connection Pattern:")
print("   x → LayerNorm → Attention → + x (residual)")
print("   x → LayerNorm → MLP → + x (residual)")
print("\n💡 Benefits:")
print("   1. Enables gradient flow through deep networks")
print("   2. Allows identity mapping (skip connection)")
print("   3. Makes training of deep networks possible")

print(formatter.output_summary([
    "Residual connections add input to output: output = f(x) + x",
    "Enables gradient to flow directly through skip connection",
    "Allows model to learn identity function (if needed)",
    "Critical for training deep networks (50+ layers)",
    "Prevents vanishing gradient problem"
]))

# Part 5: Stacking Multiple Layers
print(formatter.section("Part 5: Stacking Multiple Layers - Sequential Processing"))

if model is not None and hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
    try:
        layers = model.transformer.h
        num_layers = len(layers)
        
        print(f"\n📊 Layer Stacking:")
        print(f"   Total layers: {num_layers}")
        print(f"   Each layer processes the output of the previous layer")
        
        print(f"\n🔄 Data Flow Through Layers:")
        print(f"   Input embeddings")
        for i in range(min(3, num_layers)):
            print(f"   ↓ Layer {i+1}: Attention + MLP")
        if num_layers > 3:
            print(f"   ↓ ... ({num_layers - 3} more layers)")
        print(f"   ↓ Final LayerNorm")
        print(f"   ↓ Output embeddings")
        
        if num_layers > 0:
            first_layer_params = sum(p.numel() for p in layers[0].parameters())
            print(f"\n📈 Parameters per layer: ~{first_layer_params:,}")
            print(f"   Total transformer parameters: ~{first_layer_params * num_layers:,}")
        
        print(formatter.output_summary([
            f"Information flows sequentially through {num_layers} layers",
            f"Each layer refines the representation from previous layer",
            f"Early layers learn low-level features, later layers learn high-level",
            f"Total parameters: ~{first_layer_params * num_layers:,} across all layers",
            "More layers = more capacity but also more computation"
        ]))
    except Exception as e:
        print(f"⚠️  Could not analyze layer stacking: {e}")

# Summary
takeaways = [
    "Transformer layers = Attention + Feedforward + Residuals",
    "LayerNorm stabilizes training and enables deep networks",
    "MLP expands and contracts dimensions (e.g., 768 → 3072 → 768)",
    "Residual connections enable gradient flow",
    "Multiple layers process information sequentially"
]
print(formatter.summary("Objective 4 Complete: Layers", takeaways, "Objective 5 - Tensors (Data Representation)"))

# Save state
if 'model' in locals() and 'tokenizer' in locals():
    state_mgr.save_to_globals(globals(), model=model, tokenizer=tokenizer)
    print("\n💾 Model and tokenizer saved for next objective")
