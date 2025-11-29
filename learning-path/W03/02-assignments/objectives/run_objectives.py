#!/usr/bin/env python3
"""
Runner script to execute objectives sequentially, simulating notebook behavior.
This preserves global state between objectives, just like a Jupyter notebook.

Usage:
    python run_objectives.py              # Run all objectives (0-6)
    python run_objectives.py 0            # Run only Objective 0
    python run_objectives.py 0 1         # Run Objectives 0 and 1
    python run_objectives.py 0 1 2 3 4 5 6  # Run all objectives in sequence
    python run_objectives.py 4            # Run only Objective 4 (requires 0-3 first)
"""

import sys
import os
from pathlib import Path

# Add current directory to path so we can import objective scripts
sys.path.insert(0, str(Path(__file__).parent))

def run_objective(obj_num: int, globals_dict: dict) -> dict:
    """
    Run a single objective script and return updated globals.
    
    Args:
        obj_num: Objective number (0, 1, 2, 3, etc.)
        globals_dict: Current global namespace (shared state)
        
    Returns:
        Updated globals dictionary
    """
    script_name = f"objective_{obj_num}.py"
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ {script_name} not found!")
        return globals_dict
    
    print("\n" + "=" * 80)
    print(f"🚀 RUNNING OBJECTIVE {obj_num}")
    print("=" * 80)
    
    # Read and execute the script
    with open(script_path, 'r') as f:
        code = f.read()
    
    # Execute in the shared namespace
    try:
        exec(compile(code, script_path, 'exec'), globals_dict)
        print(f"\n✅ Objective {obj_num} completed successfully!")
        return globals_dict
    except Exception as e:
        print(f"\n❌ Objective {obj_num} failed: {e}")
        import traceback
        traceback.print_exc()
        return globals_dict


def main():
    """Main entry point."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Run specific objectives
        objectives = []
        for arg in sys.argv[1:]:
            try:
                obj_num = int(arg)
                if obj_num < 0:
                    raise ValueError("Objective number must be >= 0")
                objectives.append(obj_num)
            except ValueError:
                print(f"❌ Invalid objective number: {arg}")
                print("Usage: python run_objectives.py [0] [1] [2] [3] [4] [5] [6] ...")
                sys.exit(1)
    else:
        # Run all objectives in sequence
        objectives = [0, 1, 2, 3, 4, 5, 6]
    
    # Sort objectives to ensure correct order
    objectives = sorted(set(objectives))
    
    # Check prerequisites
    if objectives and objectives[0] != 0:
        print("⚠️  Warning: Starting with Objective 0 is recommended!")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Shared global namespace (simulates notebook globals)
    shared_globals = {
        '__name__': '__main__',
        '__file__': __file__,
    }
    
    # Run each objective in sequence
    for idx, obj_num in enumerate(objectives):
        shared_globals = run_objective(obj_num, shared_globals)
        
        # Check if we should continue (only pause if running interactively)
        if idx < len(objectives) - 1:
            # Check if stdin is a TTY (interactive terminal)
            if sys.stdin.isatty():
                print(f"\n⏸️  Pausing before next objective...")
                print("   (Press Enter to continue, or Ctrl+C to stop)")
                try:
                    input()
                except KeyboardInterrupt:
                    print("\n\n⚠️  Stopped by user.")
                    break
            else:
                # Non-interactive mode - just print separator
                print(f"\n⏭️  Continuing to next objective...\n")
    
    print("\n" + "=" * 80)
    print("✅ ALL OBJECTIVES COMPLETED!")
    print("=" * 80)
    
    # Print summary of what's available
    print("\n📦 Available in global namespace:")
    important_vars = ['env', 'system_prompt', 'inference_engine', 'qa_database', 
                     'embedding_model', 'faiss_index', 'qa_embeddings', 'rag_pipeline',
                     'rag_response', 'evaluation_results']
    for var in important_vars:
        if var in shared_globals:
            print(f"   ✅ {var}")
        else:
            print(f"   ❌ {var} (not set)")


if __name__ == '__main__':
    main()

