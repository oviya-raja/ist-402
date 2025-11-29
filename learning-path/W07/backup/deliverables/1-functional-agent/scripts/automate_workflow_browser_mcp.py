#!/usr/bin/env python3
"""
Automated Workflow Creation using Browser MCP
Provides step-by-step instructions for browser automation
"""
import os
import sys
from pathlib import Path
from utils import load_env, get_assistant_id, get_vector_store_id

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def generate_workflow_instructions():
    """Generate detailed instructions for workflow creation"""
    load_env()
    assistant_id = get_assistant_id()
    vector_store_id = get_vector_store_id()
    
    print_header("AUTOMATED WORKFLOW CREATION INSTRUCTIONS")
    
    instructions = f"""
# Automated Workflow Creation Steps

## Current Status
✅ Browser is at: https://platform.openai.com/agent-builder/edit
✅ Workflow editor is open
✅ Start node and "My agent" node are already on canvas

## Next Steps (Automated via Browser MCP):

### Step 1: Configure "My agent" Node
1. Click on the "My agent" node on the canvas
2. In the configuration panel (right side), select assistant:
   Assistant ID: {assistant_id}
   Name: "Job Fitment Analysis Agent"

### Step 2: Add File Search Node
1. In the left sidebar, find "Tools" section
2. Click and drag "File search" node to canvas (to the right of "My agent")
3. Configure File search node:
   Vector Store ID: {vector_store_id}
   Name: "Knowledge Base Search"

### Step 3: Add End Node
1. In the left sidebar, find "Core" section
2. Click and drag "End" node to canvas (to the right of File search)
3. End node doesn't need configuration

### Step 4: Connect Nodes
1. Connect Start → My agent (already connected)
2. Connect My agent → File search:
   - Click output port (right side) of "My agent" node
   - Drag to input port (left side) of "File search" node
3. Connect File search → End:
   - Click output port of "File search" node
   - Drag to input port of "End" node

### Step 5: Name and Publish
1. Click on workflow title "New workflow" at top
2. Rename to: "Job Fitment Analysis Workflow"
3. Click "Publish" button (top right)
4. Confirm publication

### Step 6: Capture Screenshots
1. Take screenshot of complete workflow canvas
2. Save to: deliverables/4-screenshots/agent-builder-workflow-complete.png
3. Take screenshot of each node configuration
4. Save to: deliverables/4-screenshots/agent-builder-workflow-nodes.png

## Automation Script
The browser MCP tools will execute these steps programmatically.
"""
    
    print(instructions)
    
    # Save instructions
    output_file = Path(__file__).parent.parent / "WORKFLOW_CREATION_STEPS.md"
    with open(output_file, 'w') as f:
        f.write(instructions)
    print(f"\n💾 Instructions saved to: {output_file}")
    
    return {
        "assistant_id": assistant_id,
        "vector_store_id": vector_store_id,
        "steps": [
            "Configure My agent node",
            "Add File search node",
            "Add End node",
            "Connect all nodes",
            "Publish workflow",
            "Capture screenshots"
        ]
    }

def main():
    """Main function"""
    print_header("WORKFLOW CREATION AUTOMATION GUIDE")
    
    workflow_info = generate_workflow_instructions()
    
    print("\n✅ Instructions generated!")
    print("\n📋 Summary:")
    print(f"   Assistant ID: {workflow_info['assistant_id']}")
    print(f"   Vector Store ID: {workflow_info['vector_store_id']}")
    print(f"   Steps: {len(workflow_info['steps'])}")
    
    print("\n🚀 Ready for browser automation!")
    print("   The browser MCP tools will execute these steps.")

if __name__ == "__main__":
    main()

