#!/usr/bin/env python3
"""
List Local Cached Models

This script lists all models available in the Hugging Face cache directory
and optionally exports the information to a CSV file.

Usage:
    python list_models.py                    # List models to console
    python list_models.py output.csv         # Export to CSV file
"""

import sys
from pathlib import Path

# Add objectives directory to path so script can be run from parent directory
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from llm_fundamentals_support import ModelLoader, Formatter

def main():
    """Main function to list cached models with all core-concepts.md details."""
    formatter = Formatter()
    print(formatter.header("LOCAL CACHED MODELS"))
    print("\n📚 Includes all details from core-concepts.md:")
    print("   1️⃣  Tokens (vocab_size)")
    print("   2️⃣  Embeddings (embedding_size)")
    print("   3️⃣  Vector Relationships/Attention (num_attention_heads, attention_type)")
    print("   4️⃣  Layers (num_layers, intermediate_size)")
    print("   5️⃣  Tensors (hidden_size, tensor shapes)")
    print("   6️⃣  Parameters (estimated_parameters)")
    print("\n   Plus: activation_function, position_embedding_type, and more!")
    
    # Get output CSV path from command line if provided
    output_csv = sys.argv[1] if len(sys.argv) > 1 else None
    
    if output_csv:
        print(f"\n📊 Scanning cache and exporting to: {output_csv}\n")
    else:
        print(f"\n📊 Scanning cache directory...\n")
    
    # List models (includes all core-concepts.md details)
    models = ModelLoader.list_local_models(output_csv=output_csv)
    
    # Summary
    if models:
        total_size_gb = sum(m['total_size_gb'] for m in models)
        total_size_mb = sum(m['total_size_mb'] for m in models)
        total_params = sum(m['estimated_parameters_billions'] or 0 for m in models)
        
        print(formatter.section("Summary"))
        print(f"  Total models: {len(models)}")
        print(f"  Total cache size: {total_size_gb:.2f} GB ({total_size_mb:.2f} MB)")
        print(f"  Total files: {sum(m['file_count'] for m in models)}")
        if total_params > 0:
            print(f"  Estimated total parameters: ~{total_params:.2f}B")
        
        # Show models with complete config
        models_with_config = [m for m in models if m.get('vocab_size') and m.get('hidden_size')]
        if models_with_config:
            print(f"  Models with full config: {len(models_with_config)}/{len(models)}")
        
        if output_csv:
            print(f"\n✅ Model details exported to: {output_csv}")
            print(f"   CSV includes all 6 core components from core-concepts.md")
    else:
        print("\n⚠️  No cached models found in the cache directory.")
        print("   Models will be downloaded automatically on first use.")

if __name__ == "__main__":
    main()

