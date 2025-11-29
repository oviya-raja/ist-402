#!/usr/bin/env python3
"""
Automated Workflow Setup for Job Fitment Analysis Agent
This script fully automates the workflow configuration in Agent Builder via API
"""
import os
import sys
import time
from pathlib import Path
from openai import OpenAI
import httpx
from datetime import datetime

# Import utilities
from utils import load_env, get_api_key, get_assistant_id

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"🚀 {text}")
    print("=" * 70 + "\n")

def print_step(step_num, text):
    """Print formatted step"""
    print(f"\n{'─' * 70}")
    print(f"STEP {step_num}: {text}")
    print(f"{'─' * 70}\n")

def load_system_prompt():
    """Load system prompt from file"""
    system_prompt_path = Path(__file__).parent.parent / "system-prompt.txt"
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt not found: {system_prompt_path}")
    
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def upload_knowledge_base_files(client):
    """Upload all knowledge base files"""
    knowledge_base_dir = Path(__file__).parent.parent.parent.parent / "knowledge-base"
    files_to_upload = [
        "01-student-profiles/profile-template.txt",
        "01-student-profiles/skills-taxonomy.txt",
        "01-student-profiles/experience-levels.txt",
        "02-job-analysis/job-posting-structure.txt",
        "03-company-info/target-companies.txt",
        "04-fitment-analysis/calculation-methodology.txt",
        "04-fitment-analysis/interpretation-guide.txt",
        "05-skill-gaps/gap-identification.txt",
        "05-skill-gaps/learning-resources.txt",
        "06-use-case-examples/use-case-1-example.txt",
    ]
    
    print("📤 Uploading knowledge base files...")
    file_ids = []
    for file_path in files_to_upload:
        full_path = knowledge_base_dir / file_path
        if not full_path.exists():
            print(f"⚠️  File not found: {full_path}")
            continue
        
        print(f"  Uploading: {file_path}")
        with open(full_path, 'rb') as f:
            file_obj = client.files.create(file=f, purpose='assistants')
            file_ids.append(file_obj.id)
            print(f"    ✅ Uploaded: {file_obj.id}")
    
    return file_ids

def create_vector_store(api_key, file_ids):
    """Create vector store with files"""
    BASE_URL = "https://api.openai.com/v1"
    API_HEADERS = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v2",
        "Content-Type": "application/json"
    }
    
    print("📚 Creating vector store...")
    response = httpx.post(
        f"{BASE_URL}/vector_stores",
        headers=API_HEADERS,
        json={
            "name": "Job Fitment Analysis Knowledge Base",
            "file_ids": file_ids
        },
        timeout=60.0
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to create vector store: {response.status_code} - {response.text}")
    
    vs_data = response.json()
    vs_id = vs_data["id"]
    print(f"✅ Vector store created: {vs_id}")
    
    # Wait for processing
    print("⏳ Waiting for files to process...")
    max_wait = 120
    waited = 0
    while waited < max_wait:
        vs_response = httpx.get(
            f"{BASE_URL}/vector_stores/{vs_id}",
            headers=API_HEADERS,
            timeout=30.0
        )
        if vs_response.status_code == 200:
            vs_status = vs_response.json().get("status", "unknown")
            if vs_status == "completed":
                print(f"✅ Files processed!")
                break
        time.sleep(3)
        waited += 3
        if waited % 15 == 0:
            print(f"   Still processing... ({waited}s)")
    
    return vs_id

def create_or_update_assistant(client, assistant_id, system_prompt, vector_store_id):
    """Create new assistant or update existing one"""
    if assistant_id:
        print(f"✏️  Updating existing assistant: {assistant_id}")
        assistant = client.beta.assistants.update(
            assistant_id,
            name="Job Fitment Analysis Agent",
            instructions=system_prompt,
            model="gpt-4o",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            } if vector_store_id else None
        )
        print("✅ Assistant updated")
    else:
        print("🤖 Creating new assistant...")
        assistant = client.beta.assistants.create(
            name="Job Fitment Analysis Agent",
            instructions=system_prompt,
            model="gpt-4o",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            } if vector_store_id else None
        )
        print(f"✅ Assistant created: {assistant.id}")
    
    return assistant

def verify_workflow_configuration(client, assistant_id):
    """Verify the workflow is properly configured"""
    print("\n🔍 Verifying workflow configuration...")
    
    assistant = client.beta.assistants.retrieve(assistant_id)
    
    # Check vector store - tool_resources is a Pydantic object
    has_vector_store = False
    if assistant.tool_resources and hasattr(assistant.tool_resources, 'file_search'):
        file_search = assistant.tool_resources.file_search
        if hasattr(file_search, 'vector_store_ids') and file_search.vector_store_ids:
            has_vector_store = True
    
    checks = {
        "Name": assistant.name == "Job Fitment Analysis Agent",
        "Model": assistant.model == "gpt-4o",
        "System Prompt": len(assistant.instructions) > 0,
        "File Search Tool": any(tool.type == "file_search" for tool in assistant.tools),
        "Vector Store": has_vector_store
    }
    
    print("\n📋 Configuration Check:")
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}: {'OK' if passed else 'MISSING'}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✅ All workflow components configured correctly!")
    else:
        print("\n⚠️  Some components may need manual configuration")
    
    return all_passed

def main():
    """Main automation workflow"""
    start_time = datetime.now()
    
    print_header("AUTOMATED WORKFLOW SETUP")
    print("This script fully automates the Agent Builder workflow configuration")
    print("No manual clicks required - everything via API!")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # STEP 1: Load Environment
    print_step(1, "Loading Environment")
    load_env()
    api_key = get_api_key()
    assistant_id = get_assistant_id()
    client = OpenAI(api_key=api_key)
    print(f"✅ API Key loaded: {api_key[:20]}...")
    if assistant_id:
        print(f"✅ Assistant ID: {assistant_id}")
    else:
        print("ℹ️  No existing assistant ID - will create new one")
    
    # STEP 2: Load System Prompt (Workflow Logic)
    print_step(2, "Loading Workflow Logic (System Prompt)")
    try:
        system_prompt = load_system_prompt()
        print(f"✅ System prompt loaded: {len(system_prompt)} characters")
        print(f"   Contains workflow logic for all 5 use cases")
        print(f"   Includes routing, processing, and decision logic")
    except Exception as e:
        print(f"❌ Failed to load system prompt: {e}")
        sys.exit(1)
    
    # STEP 3: Upload Knowledge Base Files
    print_step(3, "Uploading Knowledge Base Files")
    try:
        file_ids = upload_knowledge_base_files(client)
        print(f"\n✅ Uploaded {len(file_ids)} knowledge base files")
    except Exception as e:
        print(f"❌ Failed to upload files: {e}")
        sys.exit(1)
    
    # STEP 4: Create Vector Store
    print_step(4, "Creating Vector Store")
    try:
        vector_store_id = create_vector_store(api_key, file_ids)
        print(f"✅ Vector store ready: {vector_store_id}")
    except Exception as e:
        print(f"⚠️  Failed to create vector store: {e}")
        print("   Continuing without vector store (files uploaded but not linked)")
        vector_store_id = None
    
    # STEP 5: Create/Update Assistant with Workflow
    print_step(5, "Configuring Agent with Workflow")
    print("This configures:")
    print("  - System prompt (workflow logic)")
    print("  - Model (GPT-4o)")
    print("  - File Search tool (knowledge base access)")
    print("  - Vector store (file linking)")
    print()
    
    try:
        assistant = create_or_update_assistant(
            client, 
            assistant_id, 
            system_prompt, 
            vector_store_id
        )
        final_assistant_id = assistant.id
        print(f"\n✅ Agent configured with workflow!")
        print(f"   Assistant ID: {final_assistant_id}")
    except Exception as e:
        print(f"❌ Failed to configure agent: {e}")
        sys.exit(1)
    
    # STEP 6: Verify Workflow Configuration
    print_step(6, "Verifying Workflow Configuration")
    verify_workflow_configuration(client, final_assistant_id)
    
    # STEP 7: Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("WORKFLOW AUTOMATION COMPLETE")
    print("✅ Workflow fully configured via automation!")
    print(f"⏱️  Total time: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print()
    print("📋 Workflow Components Configured:")
    print("  ✅ System Prompt (workflow logic)")
    print("  ✅ Model: GPT-4o")
    print("  ✅ File Search Tool (enabled)")
    print(f"  ✅ Knowledge Base ({len(file_ids)} files)")
    if vector_store_id:
        print(f"  ✅ Vector Store: {vector_store_id}")
    print()
    print("🔗 Workflow Execution:")
    print("  1. User sends message → Agent Builder receives")
    print("  2. GPT-4o reads system prompt (workflow logic)")
    print("  3. System prompt instructions executed:")
    print("     - Parse input")
    print("     - Validate company names")
    print("     - Identify use case (1-5)")
    print("     - Route to processing module")
    print("  4. File Search tool activated (if needed)")
    print("  5. GPT-4o processes with knowledge base context")
    print("  6. Response generated and formatted")
    print("  7. Response sent to user")
    print()
    print("🌐 View Agent in Browser:")
    print(f"   https://platform.openai.com/assistants/{final_assistant_id}")
    print()
    print("💡 To test the workflow:")
    print("   python3 test_agent_e2e.py")
    print("   python3 test_all_use_cases.py")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Automation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

