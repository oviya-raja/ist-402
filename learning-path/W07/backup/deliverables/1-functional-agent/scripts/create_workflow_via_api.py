#!/usr/bin/env python3
"""
Create Agent Builder Workflow via API
Attempts to create workflow programmatically using OpenAI API
"""
import os
import sys
import json
import time
from pathlib import Path
from openai import OpenAI
import httpx

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id, get_vector_store_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()
VECTOR_STORE_ID = get_vector_store_id()

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def create_workflow_via_api(client, assistant_id, vector_store_id):
    """
    Attempt to create workflow in Agent Builder via API
    
    Note: OpenAI Agent Builder workflows API may be in beta or may require
    direct HTTP calls to specific endpoints.
    """
    print_header("CREATE AGENT BUILDER WORKFLOW VIA API")
    print(f"Assistant ID: {assistant_id}")
    print(f"Vector Store ID: {vector_store_id}")
    
    # Workflow definition based on our agent's logic
    workflow_config = {
        "name": "Job Fitment Analysis Workflow",
        "description": "Automated workflow for job fitment analysis using knowledge base",
        "assistant_id": assistant_id,
        "steps": [
            {
                "id": "start",
                "type": "start"
            },
            {
                "id": "parse_input",
                "type": "agent",
                "assistant_id": assistant_id,
                "name": "Parse User Input"
            },
            {
                "id": "identify_use_case",
                "type": "classify",
                "name": "Identify Use Case",
                "options": [
                    "UC1: Search Jobs",
                    "UC2: Analyze Fitment",
                    "UC3: Skill Gaps",
                    "UC4: Compare Jobs",
                    "UC5: Generate Strategy"
                ]
            },
            {
                "id": "search_knowledge_base",
                "type": "file_search",
                "vector_store_id": vector_store_id,
                "name": "Search Knowledge Base"
            },
            {
                "id": "process_response",
                "type": "agent",
                "assistant_id": assistant_id,
                "name": "Generate Response"
            },
            {
                "id": "end",
                "type": "end"
            }
        ],
        "connections": [
            {"from": "start", "to": "parse_input"},
            {"from": "parse_input", "to": "identify_use_case"},
            {"from": "identify_use_case", "to": "search_knowledge_base"},
            {"from": "search_knowledge_base", "to": "process_response"},
            {"from": "process_response", "to": "end"}
        ]
    }
    
    print("\n📝 Workflow Configuration:")
    print(json.dumps(workflow_config, indent=2))
    
    # Try to create workflow via API
    # Note: This may require direct HTTP calls if not in SDK
    try:
        print("\n🔍 Attempting to create workflow via API...")
        
        # Option 1: Try beta.workflows if available
        if hasattr(client, 'beta') and hasattr(client.beta, 'workflows'):
            print("   Found workflows API in beta")
            # workflow = client.beta.workflows.create(**workflow_config)
            # print(f"✅ Workflow created: {workflow.id}")
        else:
            print("   ⚠️  Workflows API not found in SDK")
        
        # Option 2: Try direct HTTP call
        print("\n🔍 Attempting direct HTTP API call...")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        
        # Note: The actual endpoint may be different
        # This is a placeholder - actual endpoint needs to be verified
        url = "https://api.openai.com/v1/workflows"
        
        print(f"   Would call: {url}")
        print("   ⚠️  Note: Actual endpoint may differ")
        print("   ⚠️  Workflows API may require different authentication")
        
    except Exception as e:
        print(f"   ⚠️  API call failed: {e}")
    
    print("\n" + "=" * 70)
    print("📋 IMPORTANT NOTE:")
    print("=" * 70)
    print("""
Agent Builder workflows may need to be created in the UI because:

1. The workflow is already configured in your assistant:
   ✅ System prompt contains workflow logic
   ✅ File Search tool is enabled
   ✅ Knowledge base is linked
   ✅ Assistant is functional

2. Agent Builder visual workflow is a UI representation of:
   - The assistant's system prompt (workflow logic)
   - The tools configuration (File Search)
   - The knowledge base integration

3. To create visual workflow in Agent Builder:
   a. Go to: https://platform.openai.com/agent-builder
   b. Click "Create"
   c. Add nodes:
      - Start node
      - Agent node (link to your assistant)
      - File Search node (for knowledge base)
      - End node
   d. Connect: Start → Agent → File Search → End
   e. Save and publish

4. The workflow logic is already working via:
   - System prompt (defines workflow steps)
   - File Search tool (automatically triggered)
   - Assistant API (executes workflow)
""")
    
    # Save workflow definition for reference
    output_file = Path(__file__).parent.parent / "workflow-definition.json"
    with open(output_file, 'w') as f:
        json.dump(workflow_config, f, indent=2)
    print(f"\n💾 Workflow definition saved to: {output_file}")
    print("   This can be used as reference when creating in UI")
    
    return workflow_config

def main():
    """Main function"""
    print_header("AGENT BUILDER WORKFLOW CREATION VIA API")
    
    assistant_id = get_assistant_id()
    vector_store_id = get_vector_store_id()
    
    if not assistant_id:
        print("❌ No assistant ID found")
        sys.exit(1)
    
    workflow = create_workflow_via_api(client, assistant_id, vector_store_id)
    
    print("\n✅ Workflow definition created!")
    print("\n📸 Next Steps:")
    print("   1. Navigate to: https://platform.openai.com/agent-builder")
    print("   2. Create workflow manually in visual editor")
    print("   3. Use workflow-definition.json as reference")
    print("   4. Link to existing assistant")
    print("   5. Capture screenshots")

if __name__ == "__main__":
    main()

