#!/usr/bin/env python3
"""
Create Agent Builder Workflow via Direct HTTP API
Attempts to create workflow using direct HTTP calls to OpenAI API
"""
import os
import sys
import json
import httpx
from pathlib import Path

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id, get_vector_store_id

# Load environment variables
load_env()
api_key = get_api_key()
ASSISTANT_ID = get_assistant_id()
VECTOR_STORE_ID = get_vector_store_id()

BASE_URL = "https://api.openai.com/v1"
API_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"
}

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def create_workflow_via_http(assistant_id, vector_store_id):
    """
    Attempt to create workflow via direct HTTP API calls
    """
    print_header("CREATE WORKFLOW VIA HTTP API")
    print(f"Assistant ID: {assistant_id}")
    print(f"Vector Store ID: {vector_store_id}")
    
    # Workflow definition
    workflow_payload = {
        "name": "Job Fitment Analysis Workflow",
        "description": "Workflow for job fitment analysis with knowledge base",
        "steps": [
            {
                "id": "start",
                "type": "start"
            },
            {
                "id": "main_agent",
                "type": "agent",
                "assistant_id": assistant_id,
                "name": "Job Fitment Analysis Agent"
            },
            {
                "id": "file_search",
                "type": "file_search",
                "vector_store_id": vector_store_id,
                "name": "Knowledge Base Search"
            },
            {
                "id": "end",
                "type": "end"
            }
        ],
        "connections": [
            {"from": "start", "to": "main_agent"},
            {"from": "main_agent", "to": "file_search"},
            {"from": "file_search", "to": "end"}
        ]
    }
    
    print("\n📝 Workflow Payload:")
    print(json.dumps(workflow_payload, indent=2))
    
    # Try different possible endpoints
    endpoints_to_try = [
        "/workflows",
        "/beta/workflows",
        "/agent-builder/workflows",
        "/assistants/workflows"
    ]
    
    workflow_created = False
    for endpoint in endpoints_to_try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 Trying endpoint: {url}")
        
        try:
            response = httpx.post(
                url,
                headers=API_HEADERS,
                json=workflow_payload,
                timeout=30.0
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                workflow_data = response.json()
                print(f"✅ Workflow created successfully!")
                print(f"   Workflow ID: {workflow_data.get('id', 'N/A')}")
                workflow_created = True
                return workflow_data
            elif response.status_code == 404:
                print(f"   ⚠️  Endpoint not found")
            elif response.status_code == 401:
                print(f"   ⚠️  Authentication failed")
            else:
                print(f"   ⚠️  Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ⚠️  Exception: {str(e)[:200]}")
    
    if not workflow_created:
        print("\n" + "=" * 70)
        print("⚠️  WORKFLOW API NOT AVAILABLE")
        print("=" * 70)
        print("""
The workflows API endpoint is not available or requires different authentication.

ALTERNATIVE APPROACH:
The workflow is already configured in your assistant:
  ✅ System prompt = workflow logic
  ✅ File Search tool = knowledge base access
  ✅ Assistant = workflow executor

To create visual workflow in Agent Builder UI:
  1. Go to: https://platform.openai.com/agent-builder
  2. Click "Create"
  3. Add nodes manually:
     - Start → Agent → File Search → End
  4. Link Agent node to: {assistant_id}
  5. Configure File Search with vector store
  6. Save and publish

The workflow definition has been saved to workflow-definition.json
Use it as a reference when creating in UI.
""".format(assistant_id=assistant_id))
    
    return None

def main():
    """Main function"""
    print_header("AGENT BUILDER WORKFLOW CREATION (HTTP API)")
    
    workflow = create_workflow_via_http(ASSISTANT_ID, VECTOR_STORE_ID)
    
    # Save workflow definition regardless
    workflow_def = {
        "name": "Job Fitment Analysis Workflow",
        "assistant_id": ASSISTANT_ID,
        "vector_store_id": VECTOR_STORE_ID,
        "steps": ["Start", "Agent", "File Search", "End"],
        "description": "Workflow for job fitment analysis"
    }
    
    output_file = Path(__file__).parent.parent / "workflow-definition.json"
    with open(output_file, 'w') as f:
        json.dump(workflow_def, f, indent=2)
    print(f"\n💾 Workflow definition saved: {output_file}")
    
    if workflow:
        print("\n✅ Workflow created via API!")
    else:
        print("\n⚠️  Workflow needs to be created in Agent Builder UI")
        print("   See instructions above")

if __name__ == "__main__":
    main()

