#!/usr/bin/env python3
"""
Run LLM Fundamentals Objectives Sequentially

This script runs objectives in sequence, preserving state between them
(like a notebook would).

Usage:
    python run_objectives.py              # Run all objectives
    python run_objectives.py 1            # Run only objective 1
    python run_objectives.py 1 2 3        # Run objectives 1, 2, 3
"""

import sys
from pathlib import Path
from llm_fundamentals_support import Formatter

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()

# Objective mapping
OBJECTIVES = {
    1: {
        'file': 'objective_1_tokens.py',
        'name': 'Tokens',
        'description': 'Text → Tokens'
    },
    2: {
        'file': 'objective_2_embeddings.py',
        'name': 'Embeddings',
        'description': 'Tokens → Vectors'
    },
    3: {
        'file': 'objective_3_attention.py',
        'name': 'Attention',
        'description': 'Vector Relationships'
    },
    4: {
        'file': 'objective_4_layers.py',
        'name': 'Layers',
        'description': 'Transformer Layers'
    },
    5: {
        'file': 'objective_5_tensors.py',
        'name': 'Tensors',
        'description': 'Working with Tensors'
    },
    6: {
        'file': 'objective_6_parameters.py',
        'name': 'Parameters',
        'description': 'Model Weights & Config'
    },
}


def run_objective(obj_num: int, global_namespace: dict):
    """Run a single objective script."""
    if obj_num not in OBJECTIVES:
        print(f"❌ Unknown objective: {obj_num}")
        print(f"   Available: {list(OBJECTIVES.keys())}")
        return False
    
    obj_info = OBJECTIVES[obj_num]
    obj_file = SCRIPT_DIR / obj_info['file']
    
    if not obj_file.exists():
        print(f"⚠️  Objective {obj_num} file not found: {obj_file}")
        print(f"   Skipping...")
        return False
    
    formatter = Formatter()
    print(formatter.header(f"🚀 RUNNING OBJECTIVE {obj_num}: {obj_info['name']}"))
    print(f"   {obj_info['description']}\n")
    
    try:
        # Read and execute the objective script
        with open(obj_file, 'r') as f:
            code = f.read()
        
        # Execute in the global namespace to preserve state
        exec(code, global_namespace)
        
        print(f"\n✅ Objective {obj_num} completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error running objective {obj_num}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to run objectives."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            obj_numbers = [int(arg) for arg in sys.argv[1:]]
        except ValueError:
            print("❌ Invalid objective numbers. Use integers like: 1 2 3")
            sys.exit(1)
    else:
        # Run all objectives
        obj_numbers = list(OBJECTIVES.keys())
    
    # Validate objective numbers
    invalid = [n for n in obj_numbers if n not in OBJECTIVES]
    if invalid:
        print(f"❌ Invalid objective numbers: {invalid}")
        print(f"   Available: {list(OBJECTIVES.keys())}")
        sys.exit(1)
    
    # Sort to run in order
    obj_numbers = sorted(set(obj_numbers))
    
    formatter = Formatter()
    print(formatter.header("LLM FUNDAMENTALS - OBJECTIVES RUNNER"))
    print(f"\n📋 Objectives to run: {obj_numbers}")
    print(f"   Total: {len(obj_numbers)} objective(s)\n")
    
    # Create global namespace to preserve state between objectives
    global_namespace = {
        '__name__': '__main__',
        '__file__': str(SCRIPT_DIR),
    }
    
    # Run objectives
    results = {}
    for obj_num in obj_numbers:
        success = run_objective(obj_num, global_namespace)
        results[obj_num] = success
        
        # Pause between objectives (except for the last one)
        if obj_num != obj_numbers[-1]:
            print(formatter.section(""))
            input("⏸️  Press Enter to continue to next objective (or Ctrl+C to stop)...")
    
    # Summary
    print(formatter.header("📊 SUMMARY"))
    
    successful = [n for n, s in results.items() if s]
    failed = [n for n, s in results.items() if not s]
    
    if successful:
        print(f"\n✅ Successful: {successful}")
    if failed:
        print(f"\n❌ Failed: {failed}")
    
    print(f"\n🎯 Completed {len(successful)}/{len(results)} objectives")
    
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

