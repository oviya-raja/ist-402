#!/usr/bin/env python3
"""
Test script to execute notebook cells in sequence and verify the agent fix works.
This simulates running the notebook cells and checks if the agent properly calls tools.
"""

import json
import sys
import os
import asyncio
from pathlib import Path
from io import StringIO
import contextlib
import traceback

# Capture stdout/stderr for analysis
class OutputCapture:
    def __init__(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def __enter__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self
    
    def __exit__(self, *args):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def get_output(self):
        return self.stdout.getvalue() + self.stderr.getvalue()

def extract_cell_code(notebook_path, cell_indices):
    """Extract code from specific notebook cells."""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    codes = []
    for idx in cell_indices:
        if idx < len(nb['cells']):
            cell = nb['cells'][idx]
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                codes.append((idx, source))
    return codes

def find_cells_by_pattern(notebook_path, patterns):
    """Find cells matching patterns."""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    found = {}
    for name, (pattern1, pattern2) in patterns.items():
        for i, cell in enumerate(nb['cells']):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if pattern1 in source:
                    if pattern2 is None or pattern2 in source:
                        found[name] = i
                        break
    return found

def execute_cell_code(code, globals_dict, cell_name):
    """Execute a cell's code in the given namespace."""
    try:
        exec(compile(code, f'<cell {cell_name}>', 'exec'), globals_dict)
        return True, None
    except Exception as e:
        return False, e

def check_agent_output(output_text):
    """Check if agent output indicates successful tool usage."""
    output_lower = output_text.lower()
    checks = {
        'has_selfrag': ('self-rag' in output_lower or 'selfrag' in output_lower) and ('framework' in output_lower or 'enhances' in output_lower or 'quality' in output_lower),
        'has_longlora': 'longlora' in output_lower and ('method' in output_lower or 'extends' in output_lower or 'approach' in output_lower),
        'no_error': 'cannot retrieve' not in output_lower and 'unable' not in output_lower and 'apologize' not in output_lower,
        'has_content': len(output_text.strip()) > 50,  # Not just empty or minimal
    }
    return checks

def main():
    notebook_path = 'W9_Building_Agentic_RAG_LlamaIndex_3_4.ipynb'
    
    if not os.path.exists(notebook_path):
        print(f"❌ Notebook not found: {notebook_path}")
        sys.exit(1)
    
    print("🚀 Testing Agent Fix - Executing Notebook Cells")
    print("=" * 70)
    print()
    
    # Find key cells - need to find all prerequisite cells
    patterns = {
        'API Key Setup': ('OPENAI_API_KEY', 'userdata'),
        'Settings Config': ('Settings.llm = OpenAI', None),
        'Get Doc Tools Function': ('def get_doc_tools(', None),
        'Papers List': ('papers = [', 'metagpt.pdf'),
        'Paper Download': ('Download papers', 'wget'),
        'Paper Processing': ('paper_to_tools_dict = {}', None),
        'Initial Tools': ('initial_tools = [t for paper', None),
        'LLM Variable': ('llm = OpenAI(model="gpt-3.5-turbo")', 'Number of tools'),
        'Agent Creation': ('agent = FunctionAgent', 'initial_tools'),
        'Tool Test': ('Testing tool callability', None),
        'Main Query': ('Give me a summary of both Self-RAG and LongLoRA', 'asyncio.run'),
    }
    
    print("📍 Finding key cells...")
    cell_indices = find_cells_by_pattern(notebook_path, patterns)
    
    for name, idx in cell_indices.items():
        print(f"   ✅ {name}: Cell {idx}")
    
    if not cell_indices:
        print("❌ Could not find required cells")
        sys.exit(1)
    
    print("\n📋 Execution Plan:")
    execution_order = [
        ('API Key Setup', 'Setup OpenAI API key'),
        ('Settings Config', 'Configure LlamaIndex settings'),
        ('Get Doc Tools Function', 'Define get_doc_tools function'),
        ('Papers List', 'Define papers list'),
        ('Paper Download', 'Download papers (skip if files exist)'),
        ('Paper Processing', 'Process papers and create tools'),
        ('Initial Tools', 'Create initial_tools list'),
        ('LLM Variable', 'Create llm variable'),
        ('Agent Creation', 'Create agent with tools'),
        ('Tool Test', 'Test tool callability'),
        ('Main Query', 'Test agent with query'),
    ]
    
    for step_name, description in execution_order:
        if step_name in cell_indices:
            print(f"   {step_name}: {description}")
    
    print("\n" + "=" * 70)
    print("🔧 Executing Cells...")
    print("=" * 70)
    
    # Global namespace (simulates notebook execution)
    globals_dict = {
        '__name__': '__main__',
        '__file__': notebook_path,
    }
    
    # Add necessary imports and setup to globals
    try:
        exec("import os", globals_dict)
        exec("import sys", globals_dict)
        exec("import asyncio", globals_dict)
        exec("from pathlib import Path", globals_dict)
        exec("import nest_asyncio", globals_dict)
        exec("nest_asyncio.apply()", globals_dict)
        
        # Ensure we have a running event loop for async operations
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Create data directory if it doesn't exist
        exec("os.makedirs('data', exist_ok=True)", globals_dict)
        
        # Mock wget for paper download (skip actual download in test)
        exec("""
def mock_wget(url, output):
    # Skip actual download - assume files exist or will be created
    print(f"   ⏭️  Skipping download (test mode): {output}")
    return True
""", globals_dict)
        
    except Exception as e:
        print(f"⚠️  Warning: Could not set up environment: {e}")
    
    results = {}
    output_captures = {}
    
    # Execute cells in order
    for step_name, description in execution_order:
        if step_name not in cell_indices:
            print(f"\n⏭️  Skipping {step_name} (cell not found)")
            continue
        
        cell_idx = cell_indices[step_name]
        print(f"\n{'─' * 70}")
        print(f"📝 Step: {step_name} (Cell {cell_idx})")
        print(f"   {description}")
        print(f"{'─' * 70}")
        
        # Extract cell code
        codes = extract_cell_code(notebook_path, [cell_idx])
        if not codes:
            print(f"   ❌ Could not extract code from cell {cell_idx}")
            continue
        
        _, code = codes[0]
        
        # Skip paper download step (assume files exist or skip)
        if step_name == 'Paper Download':
            print(f"   ⏭️  Skipping download step (assuming papers exist)")
            results[step_name] = {'success': True, 'output': 'Skipped in test mode'}
            continue
        
        # Replace !wget commands with mock
        if '!wget' in code:
            code = code.replace('!wget', '# !wget  # Skipped in test')
            print(f"   ⚠️  Note: Download commands skipped (test mode)")
        
        # For async agent.run() calls, wrap properly
        if 'asyncio.run(' in code and 'agent.run(' in code:
            # Extract the user_msg and create a proper async wrapper
            import re
            user_msg_match = re.search(r'user_msg=["\']([^"\']+)["\']', code)
            if user_msg_match:
                user_msg = user_msg_match.group(1)
                # Replace with a simpler async execution
                code = f"""
import nest_asyncio
nest_asyncio.apply()
import asyncio

async def _test_agent():
    response = await agent.run(user_msg="{user_msg}")
    return response

response = asyncio.run(_test_agent())
print(str(response))
"""
                print(f"   ⚠️  Note: Using simplified async wrapper for testing")
        
        # Execute with output capture
        with OutputCapture() as capture:
            success, error = execute_cell_code(code, globals_dict, step_name)
            output = capture.get_output()
            output_captures[step_name] = output
        
        if success:
            print(f"   ✅ Executed successfully")
            if output.strip():
                # Show first few lines of output
                lines = output.strip().split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"      {line[:70]}")
                if len(output.strip().split('\n')) > 5:
                    print(f"      ... ({len(output.strip().split('\n')) - 5} more lines)")
            
            results[step_name] = {'success': True, 'output': output}
        else:
            print(f"   ❌ Execution failed: {error}")
            print(f"   {traceback.format_exc()}")
            results[step_name] = {'success': False, 'error': str(error)}
            
            # Don't continue if critical step failed
            if step_name in ['Paper Processing', 'Agent Creation']:
                print(f"\n❌ Critical step failed. Stopping execution.")
                print(f"   Error details: {error}")
                if hasattr(error, '__traceback__'):
                    import traceback
                    traceback.print_exception(type(error), error, error.__traceback__)
                break
    
    print("\n" + "=" * 70)
    print("📊 Verification Results")
    print("=" * 70)
    
    # Check if agent was created
    if 'Agent Creation' in results and results['Agent Creation']['success']:
        agent_output = output_captures.get('Agent Creation', '')
        if 'Creating agent with' in agent_output:
            # Extract tool count
            import re
            match = re.search(r'Creating agent with (\d+) tools', agent_output)
            if match:
                tool_count = int(match.group(1))
                print(f"\n✅ Agent created with {tool_count} tools")
                if tool_count == 6:
                    print("   ✓ Expected number of tools (6)")
                else:
                    print(f"   ⚠️  Expected 6 tools, got {tool_count}")
        else:
            print("\n⚠️  Could not verify agent creation")
    else:
        print("\n❌ Agent creation failed or was not executed")
    
    # Check tool test
    if 'Tool Test' in results and results['Tool Test']['success']:
        tool_output = output_captures.get('Tool Test', '')
        if 'Tool is callable' in tool_output:
            print("\n✅ Tool test passed - tools are callable")
        else:
            print("\n⚠️  Tool test did not show expected success message")
    
    # Check main query result
    if 'Main Query' in results and results['Main Query']['success']:
        query_output = output_captures.get('Main Query', '')
        checks = check_agent_output(query_output)
        
        print("\n📋 Query Result Analysis:")
        print(f"   Contains Self-RAG summary: {'✅' if checks['has_selfrag'] else '❌'}")
        print(f"   Contains LongLoRA summary: {'✅' if checks['has_longlora'] else '❌'}")
        print(f"   No error messages: {'✅' if checks['no_error'] else '❌'}")
        print(f"   Has substantial content: {'✅' if checks['has_content'] else '❌'}")
        
        if all(checks.values()):
            print("\n🎉 SUCCESS! The fix is working correctly!")
            print("   ✓ Agent successfully called tools")
            print("   ✓ Agent retrieved summaries for both papers")
            print("   ✓ No error messages")
            
            # Show preview (case-insensitive)
            import re
            selfrag_match = re.search(r'(?i)(self-rag|selfrag).{0,50}(framework|enhances|quality)', query_output)
            if selfrag_match:
                start = max(0, selfrag_match.start() - 20)
                preview = query_output[start:start+150]
                print(f"\n   Self-RAG preview: {preview}...")
            
            longlora_match = re.search(r'(?i)longlora.{0,50}(method|extends|approach)', query_output)
            if longlora_match:
                start = max(0, longlora_match.start() - 20)
                preview = query_output[start:start+150]
                print(f"   LongLoRA preview: {preview}...")
            
            return True
        else:
            print("\n⚠️  The agent may not be working correctly")
            print("   Check the output above for issues")
            
            if query_output:
                print(f"\n   Output preview: {query_output[:300]}...")
            
            return False
    else:
        print("\n❌ Main query was not executed or failed")
        if 'Main Query' in results:
            print(f"   Error: {results['Main Query'].get('error', 'Unknown error')}")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
