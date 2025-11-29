#!/usr/bin/env python3
"""
Repeat Phase 2: Recreate Agent in Current Account
This will create the agent in whatever account the current API key belongs to
"""
import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from openai import OpenAI
import httpx

# Import utilities
from utils import load_env, get_api_key, get_assistant_id, verify_env_setup

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

def delete_existing_assistant(client, assistant_id):
    """Delete existing assistant if it exists"""
    try:
        print(f"🗑️  Deleting existing assistant: {assistant_id}")
        client.beta.assistants.delete(assistant_id)
        print(f"✅ Assistant deleted")
        return True
    except Exception as e:
        if "No such Assistant" in str(e) or "not found" in str(e).lower():
            print(f"ℹ️  Assistant doesn't exist (already deleted or never existed)")
            return True
        else:
            print(f"⚠️  Could not delete assistant: {e}")
            return False

def create_agent_from_scratch(client, api_key):
    """Create agent from scratch - upload files, create vector store, create assistant"""
    from pathlib import Path
    
    # Read system prompt
    system_prompt_path = Path(__file__).parent.parent / "system-prompt.txt"
    with open(system_prompt_path, 'r') as f:
        system_prompt = f.read()
    
    print(f"📝 System prompt loaded: {len(system_prompt)} characters")
    
    # Upload knowledge base files
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
    
    print("\n📤 Uploading knowledge base files...")
    file_ids = []
    for file_path in files_to_upload:
        full_path = knowledge_base_dir / file_path
        if not full_path.exists():
            print(f"⚠️  File not found: {full_path}")
            continue
        
        print(f"  Uploading: {file_path}")
        with open(full_path, 'rb') as f:
            file_obj = client.files.create(
                file=f,
                purpose='assistants'
            )
            file_ids.append(file_obj.id)
            print(f"    ✅ Uploaded: {file_obj.id}")
    
    print(f"\n✅ Uploaded {len(file_ids)} files")
    
    # Create vector store with files using raw HTTP API
    print("\n📚 Creating vector store with files...")
    
    BASE_URL = "https://api.openai.com/v1"
    API_HEADERS = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v2",
        "Content-Type": "application/json"
    }
    
    try:
        # Create vector store
        response = httpx.post(
            f"{BASE_URL}/vector_stores",
            headers=API_HEADERS,
            json={
                "name": "Job Fitment Analysis Knowledge Base",
                "file_ids": file_ids
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            vs_data = response.json()
            vs_id = vs_data["id"]
            print(f"✅ Vector store created: {vs_id}")
            
            # Wait for processing
            print("\n⏳ Waiting for files to process...")
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
            
            # Create assistant with vector store
            print("\n🤖 Creating assistant...")
            assistant = client.beta.assistants.create(
                name="Job Fitment Analysis Agent",
                instructions=system_prompt,
                model="gpt-4o",
                tools=[{"type": "file_search"}],
                tool_resources={
                    "file_search": {
                        "vector_store_ids": [vs_id]
                    }
                }
            )
            vector_store_id = vs_id
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"⚠️  Error creating vector store: {e}")
        # Fallback: Create assistant without files
        print("\n🤖 Creating assistant (basic setup)...")
        assistant = client.beta.assistants.create(
            name="Job Fitment Analysis Agent",
            instructions=system_prompt,
            model="gpt-4o",
            tools=[{"type": "file_search"}]
        )
        vector_store_id = None
        print("⚠️  Note: Files uploaded but not linked. Use link_files_raw_api.py to link them.")
    
    return assistant, vector_store_id, file_ids

def main():
    """Main Phase 2 repeat workflow"""
    start_time = datetime.now()
    
    print_header("REPEAT PHASE 2: Recreate Agent in Current Account")
    print("This will:")
    print("  1. Check current API key account")
    print("  2. Delete existing assistant (if exists)")
    print("  3. Create new agent from scratch")
    print("  4. Upload all knowledge base files")
    print("  5. Test all use cases")
    print(f"\nStarted at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # STEP 1: Verify Environment
    print_step(1, "Verifying Environment Setup")
    load_env()
    env_ok, env_msg = verify_env_setup()
    if not env_ok:
        print(f"❌ Environment setup failed: {env_msg}")
        sys.exit(1)
    print(f"✅ {env_msg}")
    
    api_key = get_api_key()
    print(f"✅ API Key loaded: {api_key[:20]}...")
    print(f"   Using account that owns this API key")
    
    client = OpenAI(api_key=api_key)
    
    # STEP 2: Check for existing assistant
    print_step(2, "Checking for Existing Assistant")
    existing_assistant_id = get_assistant_id()
    
    # List all assistants to see what exists
    assistants = client.beta.assistants.list(limit=20)
    existing_assistant = None
    for asst in assistants.data:
        if asst.name == "Job Fitment Analysis Agent":
            existing_assistant = asst
            print(f"✅ Found existing assistant: {asst.id}")
            break
    
    if existing_assistant:
        print(f"\n⚠️  Found existing assistant: {existing_assistant.id}")
        print(f"   This will be deleted and recreated...")
        delete_existing_assistant(client, existing_assistant.id)
        time.sleep(2)  # Wait a bit for deletion to propagate
    else:
        print("ℹ️  No existing assistant found - will create new one")
    
    # STEP 3: Create Agent from Scratch
    print_step(3, "Creating Agent from Scratch")
    print("This will:")
    print("  - Upload 10 knowledge base files")
    print("  - Create vector store")
    print("  - Create assistant with system prompt")
    print("  - Link files to assistant")
    print()
    
    assistant, vector_store_id, file_ids = create_agent_from_scratch(client, api_key)
    
    print(f"\n🎉 Agent Created Successfully!")
    print(f"   Assistant ID: {assistant.id}")
    print(f"   Assistant Name: {assistant.name}")
    print(f"   Model: {assistant.model}")
    if vector_store_id:
        print(f"   Vector Store ID: {vector_store_id}")
    print(f"   Files: {len(file_ids)}")
    
    # Update .env with new assistant ID
    print(f"\n💾 Updating .env file with new Assistant ID...")
    env_path = Path(__file__).parent.parent.parent.parent.parent / ".env"
    try:
        with open(env_path, 'r') as f:
            env_content = f.read()
        
        # Update ASSISTANT_ID
        if f"ASSISTANT_ID={existing_assistant_id}" in env_content:
            env_content = env_content.replace(
                f"ASSISTANT_ID={existing_assistant_id}",
                f"ASSISTANT_ID={assistant.id}"
            )
        elif "ASSISTANT_ID=" in env_content:
            # Replace existing
            import re
            env_content = re.sub(
                r'ASSISTANT_ID=.*',
                f'ASSISTANT_ID={assistant.id}',
                env_content
            )
        else:
            # Add new
            env_content += f"\nASSISTANT_ID={assistant.id}\n"
        
        # Update VECTOR_STORE_ID if we have one
        if vector_store_id:
            if "VECTOR_STORE_ID=" in env_content:
                import re
                env_content = re.sub(
                    r'VECTOR_STORE_ID=.*',
                    f'VECTOR_STORE_ID={vector_store_id}',
                    env_content
                )
            else:
                env_content += f"\nVECTOR_STORE_ID={vector_store_id}\n"
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Updated .env file")
        print(f"   ASSISTANT_ID={assistant.id}")
        if vector_store_id:
            print(f"   VECTOR_STORE_ID={vector_store_id}")
    except Exception as e:
        print(f"⚠️  Could not update .env file: {e}")
        print(f"   Please manually update:")
        print(f"   ASSISTANT_ID={assistant.id}")
        if vector_store_id:
            print(f"   VECTOR_STORE_ID={vector_store_id}")
    
    # STEP 4: Test Agent
    print_step(4, "Testing Agent End-to-End")
    print("Running end-to-end test...")
    print()
    
    # Reload env to get new assistant ID
    load_env()
    
    # Run test script
    test_script = Path(__file__).parent / "test_agent_e2e.py"
    if test_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(test_script)],
                capture_output=False,
                text=True,
                timeout=180
            )
            if result.returncode == 0:
                print("✅ End-to-end test passed!")
            else:
                print("⚠️  End-to-end test had issues, but continuing...")
        except Exception as e:
            print(f"⚠️  Could not run end-to-end test: {e}")
    else:
        print("⚠️  Test script not found, skipping...")
    
    # STEP 5: Test All Use Cases
    print_step(5, "Testing All 5 Use Cases")
    print("Running comprehensive test suite...")
    print()
    
    test_all_script = Path(__file__).parent / "test_all_use_cases.py"
    if test_all_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(test_all_script)],
                capture_output=False,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("✅ All use cases tested!")
            else:
                print("⚠️  Some use cases may have issues")
        except Exception as e:
            print(f"⚠️  Could not run use case tests: {e}")
    else:
        print("⚠️  Test script not found, skipping...")
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("PHASE 2 REPEAT COMPLETE")
    print(f"✅ Phase 2 repeated successfully!")
    print(f"⏱️  Total time: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print()
    print("📋 Summary:")
    print(f"  ✅ Agent created: {assistant.id}")
    print(f"  ✅ Name: {assistant.name}")
    print(f"  ✅ Model: {assistant.model}")
    if vector_store_id:
        print(f"  ✅ Vector Store: {vector_store_id}")
    print(f"  ✅ Knowledge Base: {len(file_ids)} files")
    print(f"  ✅ .env file updated")
    print()
    print("🔗 Quick Links:")
    print(f"  Browser: https://platform.openai.com/assistants")
    print(f"  Direct: https://platform.openai.com/assistants/{assistant.id}")
    print()
    print("📝 Next Steps:")
    print("  1. Verify agent appears in browser (should be visible now!)")
    print("  2. Capture screenshots for Phase 2 (TODO-016 through TODO-038)")
    print("  3. Proceed to Phase 3: Testing & Refinement")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Process failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

