#!/usr/bin/env python3
"""
Create Job Fitment Analysis Agent using OpenAI API
"""
import os
import sys
import time
from pathlib import Path
from openai import OpenAI
import httpx

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)

# Check for existing assistant first
TARGET_NAME = "Job Fitment Analysis Agent"
print("🔍 Checking for existing assistant...")
assistants = client.beta.assistants.list(limit=20)
existing_assistant = None
for asst in assistants.data:
    if asst.name == TARGET_NAME:
        existing_assistant = asst
        print(f"✅ Found existing assistant: {asst.id}")
        break

if existing_assistant:
    print(f"\n⚠️  Assistant '{TARGET_NAME}' already exists!")
    print(f"   ID: {existing_assistant.id}")
    print(f"   Use this assistant or delete it first if you want to recreate.")
    print(f"\n🌐 View in browser: https://platform.openai.com/assistants/{existing_assistant.id}")
    sys.exit(0)

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
        file_obj = client.files.create(
            file=f,
            purpose='assistants'
        )
        file_ids.append(file_obj.id)
        print(f"    ✅ Uploaded: {file_obj.id}")

print(f"\n✅ Uploaded {len(file_ids)} files")

# Create vector store with files using raw HTTP API
# (SDK doesn't expose vector_stores directly, so we use HTTP)
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

print(f"\n🎉 SUCCESS!")
print(f"   Assistant ID: {assistant.id}")
print(f"   Assistant Name: {assistant.name}")
print(f"   Model: {assistant.model}")
if vector_store_id:
    print(f"   Vector Store ID: {vector_store_id}")
print(f"   Files: {len(file_ids)}")
print(f"\n🌐 View in browser: https://platform.openai.com/assistants/{assistant.id}")

