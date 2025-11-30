# ============================================================================
# Objective 6: Parameters - Model Weights & Configuration
# ============================================================================
# Understanding model parameters, weights, and configuration

from llm_fundamentals_support import (
    LLMFundamentalsSupport, ModelLoader, Formatter, StateManager
)
import torch

support = LLMFundamentalsSupport()
formatter = Formatter()
state_mgr = StateManager()

print(formatter.header("OBJECTIVE 6: PARAMETERS"))
print(formatter.learning_intro(
    concept="Model Parameters",
    description="Parameters are learned weights stored in tensors that define model behavior. Model configuration specifies architecture (layers, heads, dimensions).",
    what_we_learn=[
        "Model configuration (architecture hyperparameters)",
        "Parameter counting and memory usage",
        "Weight initialization and statistics",
        "Model architecture inspection",
        "Parameter sharing and efficiency techniques"
    ],
    what_we_do=[
        "Inspect model configuration (layers, heads, dimensions)",
        "Count total and trainable parameters",
        "Analyze parameters by component (embeddings, attention, MLP)",
        "Inspect weight statistics (mean, std, min, max)",
        "Check for parameter sharing between layers"
    ],
    hands_on=[
        "Access model.config to see architecture parameters",
        "Count parameters: sum(p.numel() for p in model.parameters())",
        "Break down parameters by component type",
        "Inspect embedding layer weights",
        "Calculate memory usage (float32 vs float16)",
        "Check if embedding and output layers share weights"
    ]
))

# Part 1: Model Configuration
print(formatter.section("Part 1: Model Configuration - Architecture Parameters"))

loader = ModelLoader()
try:
    tokenizer, model = loader.load_both(globals())
    if 'model' in globals() and 'tokenizer' in globals():
        print("✅ Using model and tokenizer from previous objectives")
    else:
        print(f"📥 Loaded tokenizer and model: {loader.model_name}")
    
    if hasattr(model, 'config'):
        config = model.config
        print(f"\n📋 Model Configuration:")
        print(f"   Model type: {config.model_type}")
        
        attrs = ['n_layer', 'n_head', 'n_embd', 'n_positions', 'vocab_size']
        config_values = {}
        for attr in attrs:
            if hasattr(config, attr):
                value = getattr(config, attr)
                config_values[attr] = value
                label = attr.replace('n_', '').replace('_', ' ').title()
                print(f"   {label}: {value}")
        
        if hasattr(config, 'activation_function'):
            print(f"   Activation: {config.activation_function}")
        if hasattr(config, 'layer_norm_epsilon'):
            print(f"   LayerNorm epsilon: {config.layer_norm_epsilon}")
        
        print(formatter.output_summary([
            f"Model architecture: {config_values.get('n_layer', 'N/A')} layers, {config_values.get('n_head', 'N/A')} heads",
            f"Hidden dimension: {config_values.get('n_embd', 'N/A')}, Vocabulary: {config_values.get('vocab_size', 'N/A')}",
            "Configuration defines model capacity and behavior",
            "All hyperparameters are set before training"
        ]))
except Exception as e:
    print(f"❌ Error: {e}")
    model = None

# Part 2: Parameter Counting
print(formatter.section("Part 2: Parameter Counting - Model Size Analysis"))

if model is not None:
    try:
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"\n📊 Parameter Statistics:")
        print(f"   Total parameters: {total_params:,}")
        print(f"   Trainable parameters: {trainable_params:,}")
        print(f"   Memory (float32): ~{total_params * 4 / 1024 / 1024:.2f} MB")
        print(f"   Memory (float16): ~{total_params * 2 / 1024 / 1024:.2f} MB")
        
        print(f"\n🔍 Parameters by Component:")
        component_params = {'embedding': 0, 'attention': 0, 'mlp': 0, 'norm': 0, 'other': 0}
        
        for name, param in model.named_parameters():
            num_params = param.numel()
            if 'embed' in name.lower():
                component_params['embedding'] += num_params
            elif 'attn' in name.lower():
                component_params['attention'] += num_params
            elif 'mlp' in name.lower() or 'c_fc' in name.lower() or 'c_proj' in name.lower():
                component_params['mlp'] += num_params
            elif 'ln' in name.lower() or 'norm' in name.lower():
                component_params['norm'] += num_params
            else:
                component_params['other'] += num_params
        
        for comp, count in component_params.items():
            if count > 0:
                pct = count / total_params * 100
                print(f"   {comp.capitalize()}: {count:,} ({pct:.1f}%)")
        
        print(formatter.output_summary([
            f"Total parameters: {total_params:,} (defines model capacity)",
            f"Memory: ~{total_params * 4 / 1024 / 1024:.2f} MB (float32) or ~{total_params * 2 / 1024 / 1024:.2f} MB (float16)",
            f"Largest component: {max(component_params.items(), key=lambda x: x[1])[0]} ({max(component_params.values())/total_params*100:.1f}%)",
            "More parameters = more capacity but also more memory and computation"
        ]))
    except Exception as e:
        print(f"⚠️  Error counting parameters: {e}")

# Part 3: Weight Inspection
print(formatter.section("Part 3: Weight Inspection - Learned Values"))

if model is not None:
    try:
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'wte'):
            embedding_layer = model.transformer.wte
            
            print(f"\n🔍 Embedding Layer Weights:")
            print(f"   Shape: {embedding_layer.weight.shape}")
            print(f"   Dtype: {embedding_layer.weight.dtype}")
            print(f"   Requires grad: {embedding_layer.weight.requires_grad}")
            
            weight = embedding_layer.weight.data
            print(f"\n📊 Weight Statistics:")
            print(f"   Mean: {weight.mean().item():.6f}")
            print(f"   Std: {weight.std().item():.6f}")
            print(f"   Min: {weight.min().item():.6f}")
            print(f"   Max: {weight.max().item():.6f}")
            
            print(formatter.output_summary([
                f"Embedding weights shape: {embedding_layer.weight.shape}",
                f"Weight distribution: mean={weight.mean().item():.6f}, std={weight.std().item():.6f}",
                "Weights are learned during training (not random after training)",
                "Weight initialization affects training stability"
            ]))
        
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            first_layer = model.transformer.h[0]
            if hasattr(first_layer, 'attn') and hasattr(first_layer.attn, 'c_attn'):
                attn_weights = first_layer.attn.c_attn.weight
                print(f"\n🔍 Attention Weights (QKV projection):")
                print(f"   Shape: {attn_weights.shape}")
                print(f"   This projects embeddings to Q, K, V")
    except Exception as e:
        print(f"⚠️  Error inspecting weights: {e}")

# Part 4: Model Architecture Inspection
print(formatter.section("Part 4: Model Architecture Inspection - Component Analysis"))

if model is not None:
    try:
        print(f"\n🏗️  Model Structure:")
        print(f"   Type: {type(model).__name__}")
        
        print(f"\n📦 Main Components:")
        for name, module in model.named_children():
            num_params = sum(p.numel() for p in module.parameters())
            print(f"   {name}: {type(module).__name__} ({num_params:,} params)")
        
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'h'):
            num_layers = len(model.transformer.h)
            print(f"\n🔢 Layer Details:")
            print(f"   Number of transformer blocks: {num_layers}")
            
            if num_layers > 0:
                first_block = model.transformer.h[0]
                block_params = sum(p.numel() for p in first_block.parameters())
                print(f"   Parameters per block: ~{block_params:,}")
                print(f"   Total block parameters: ~{block_params * num_layers:,}")
        
        print(formatter.output_summary([
            "Model is composed of main components (transformer, embeddings, etc.)",
            f"Each transformer block has ~{block_params if num_layers > 0 else 'N/A':,} parameters",
            "Architecture determines how parameters are organized",
            "Understanding architecture helps optimize and debug models"
        ]))
    except Exception as e:
        print(f"⚠️  Error inspecting architecture: {e}")

# Part 5: Parameter Sharing and Efficiency
print(formatter.section("Part 5: Parameter Sharing and Efficiency - Optimization Techniques"))

print(f"\n💡 Parameter Efficiency Techniques:")
print(f"   1. Weight Sharing: Same weights used in multiple places")
print(f"   2. LoRA: Low-Rank Adaptation (train small matrices)")
print(f"   3. Quantization: Use fewer bits (float16, int8)")
print(f"   4. Pruning: Remove less important parameters")
print(f"   5. Distillation: Smaller model learns from larger")

if model is not None:
    try:
        if hasattr(model, 'transformer') and hasattr(model, 'lm_head'):
            wte = model.transformer.wte
            lm_head = model.lm_head
            
            if hasattr(wte, 'weight') and hasattr(lm_head, 'weight'):
                if wte.weight.data_ptr() == lm_head.weight.data_ptr():
                    print(f"\n✅ Weight Sharing Detected:")
                    print(f"   Embedding and output layers share weights!")
                    print(f"   Saves: {wte.weight.numel() * 4 / 1024 / 1024:.2f} MB")
                else:
                    print(f"\n📊 No weight sharing between embeddings and output")
        
        print(formatter.output_summary([
            "Weight sharing reduces parameters and memory",
            "LoRA allows fine-tuning with fewer parameters",
            "Quantization (float16/int8) reduces memory by 2-4x",
            "Pruning removes unimportant parameters",
            "Efficiency techniques enable running large models on smaller hardware"
        ]))
    except Exception as e:
        print(f"⚠️  Could not check parameter sharing: {e}")

# Summary
takeaways = [
    "Model config defines architecture (layers, heads, dimensions)",
    "Parameters are learned weights (millions to billions)",
    "Different components use different parameter amounts",
    "Weight sharing can reduce memory and parameters",
    "Parameters define model capacity and behavior"
]
print(formatter.summary("Objective 6 Complete: Parameters", takeaways))

print(formatter.header("🎉 ALL OBJECTIVES COMPLETE!"))
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
