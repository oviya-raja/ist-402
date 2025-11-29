#!/usr/bin/env python3
"""
Complete agent setup: Upload files and link to existing assistant
"""
import os
import sys
import time
from pathlib import Path
from openai import OpenAI

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()

# Read system prompt
system_prompt_path = Path(__file__).parent / "deliverables/1-functional-agent/system-prompt.txt"
with open(system_prompt_path, 'r') as f:
    system_prompt = f.read()

print("📝 System prompt loaded:", len(system_prompt), "characters")

# Upload knowledge base files
knowledge_base_dir = Path(__file__).parent / "knowledge-base"
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
        file_obj = client.files.create(file=f, purpose='assistants')
        file_ids.append(file_obj.id)
        print(f"    ✅ Uploaded: {file_obj.id}")

print(f"\n✅ Uploaded {len(file_ids)} files")

# Update assistant with system prompt
print("\n✏️  Updating assistant...")
assistant = client.beta.assistants.update(
    ASSISTANT_ID,
    instructions=system_prompt,
    model="gpt-4o",
    tools=[{"type": "file_search"}]
)
print(f"✅ Assistant updated")

# Try to create vector store and link files
print("\n📚 Attempting to link files...")
try:
    # Check if we can use vector stores
    if hasattr(client.beta, 'vector_stores'):
        # Create vector store
        vector_store = client.beta.vector_stores.create(
            name="Job Fitment Analysis Knowledge Base",
            file_ids=file_ids
        )
        print(f"✅ Vector store created: {vector_store.id}")
        
        # Wait for processing
        print("\n⏳ Waiting for files to process...")
        max_wait = 60
        waited = 0
        while waited < max_wait:
            vs = client.beta.vector_stores.retrieve(vector_store.id)
            if vs.status == 'completed':
                print(f"✅ Files processed!")
                break
            time.sleep(2)
            waited += 2
            if waited % 10 == 0:
                print(f"   Still processing... ({waited}s)")
        
        # Update assistant with vector store
        assistant = client.beta.assistants.update(
            ASSISTANT_ID,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store.id]
                }
            }
        )
        print(f"✅ Files linked to assistant!")
        print(f"   Vector Store ID: {vector_store.id}")
    else:
        raise AttributeError("vector_stores not available")
except Exception as e:
    print(f"⚠️  Could not link files automatically: {e}")
    print(f"\n💡 Trying alternative method with raw HTTP API...")
    try:
        import httpx
        headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "assistants=v2",
            "Content-Type": "application/json"
        }
        # Create vector store
        vs_response = httpx.post(
            "https://api.openai.com/v1/vector_stores",
            headers=headers,
            json={
                "name": "Job Fitment Analysis Knowledge Base",
                "file_ids": file_ids
            },
            timeout=60.0
        )
        if vs_response.status_code == 200:
            vs_id = vs_response.json()["id"]
            # Update assistant
            update_response = httpx.post(
                f"https://api.openai.com/v1/assistants/{ASSISTANT_ID}",
                headers=headers,
                json={
                    "tool_resources": {
                        "file_search": {
                            "vector_store_ids": [vs_id]
                        }
                    }
                },
                timeout=30.0
            )
            if update_response.status_code == 200:
                print(f"✅ Files linked using raw HTTP API!")
                print(f"   Vector Store ID: {vs_id}")
            else:
                raise Exception(f"Failed to update assistant: {update_response.status_code}")
        else:
            raise Exception(f"Failed to create vector store: {vs_response.status_code}")
    except Exception as e2:
        print(f"⚠️  Alternative method also failed: {e2}")
        print(f"\n📝 Manual step required:")
        print(f"   1. Go to: https://platform.openai.com/assistants/{ASSISTANT_ID}")
        print(f"   2. Enable 'File Search' tool")
        print(f"   3. Upload these file IDs:")
        for fid in file_ids:
            print(f"      - {fid}")

print(f"\n🎉 Setup complete!")
print(f"   Assistant ID: {ASSISTANT_ID}")
print(f"   Assistant Name: {assistant.name}")
print(f"   Model: {assistant.model}")
print(f"   Files uploaded: {len(file_ids)}")
print(f"\n🌐 View in browser: https://platform.openai.com/assistants/{ASSISTANT_ID}")



