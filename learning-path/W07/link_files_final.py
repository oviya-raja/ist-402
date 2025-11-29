#!/usr/bin/env python3
"""
Link files using the assistants API directly
Based on OpenAI API v2 structure
"""
import os
import sys
import time
from openai import OpenAI

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()

file_ids = [
    "file-Qjz8NYSYmKhf5SgFymKsN9",
    "file-K9bMtGGJeATSEQDkaEfg8D",
    "file-Pbxfs2Q5XzDxwdiqcVmUMT",
    "file-PAiR8gHkNaDXERKWuTkv6i",
    "file-QULV4KsH7Xs8p6guEZ2qsx",
    "file-Ext59zodCpWLsXYHUq95yh",
    "file-AUyPijrBAptgTDZD5DyhaX",
    "file-P5WeXb6Meg2uTDSitF9TSd",
    "file-VijAPn2YQ8v3TvEq28XP9e",
    "file-APxyU6Nk6VYSjCon2Ki8oh",
]

print("🔗 Linking files via OpenAI API...\n")

# Retrieve current assistant state
print("📋 Checking current assistant state...")
asst = client.beta.assistants.retrieve(ASSISTANT_ID)
print(f"   Name: {asst.name}")
print(f"   Tools: {asst.tools}")
print(f"   Tool Resources: {asst.tool_resources}")

# Try creating vector store through assistants API
# In newer API versions, vector stores might be created differently
print("\n📚 Attempting to create and link vector store...")

try:
    # Check if we can access vector_stores through a different path
    # Some SDK versions have it nested differently
    
    # Try: client.beta.assistants.vector_stores (if it exists)
    if hasattr(client.beta.assistants, 'vector_stores'):
        print("   Found vector_stores in assistants")
        vs = client.beta.assistants.vector_stores.create(
            name="Job Fitment Analysis Knowledge Base",
            file_ids=file_ids
        )
    # Try: Direct HTTP call approach
    else:
        print("   Using direct API call method...")
        import json
        
        # Create vector store via raw API using httpx (more reliable)
        import httpx
        headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "assistants=v2",
            "Content-Type": "application/json"
        }
        response = httpx.post(
            "https://api.openai.com/v1/vector_stores",
            headers=headers,
            json={
                "name": "Job Fitment Analysis Knowledge Base",
                "file_ids": file_ids
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            vs_data = response.json()
            vs_id = vs_data["id"]
            print(f"   ✅ Vector store created: {vs_id}")
            
            # Wait for processing
            print("\n⏳ Waiting for processing...")
            max_wait = 120
            waited = 0
            while waited < max_wait:
                vs_status = httpx.get(
                    f"https://api.openai.com/v1/vector_stores/{vs_id}",
                    headers=headers,
                    timeout=30.0
                )
                if vs_status.status_code == 200:
                    status = vs_status.json().get("status")
                    if status == "completed":
                        print("   ✅ Processing complete!")
                        break
                time.sleep(3)
                waited += 3
            
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
                print(f"\n✅ SUCCESS! Files linked!")
                print(f"   Vector Store ID: {vs_id}")
                print(f"   Files: {len(file_ids)}")
                sys.exit(0)
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            
except Exception as e:
    print(f"   ⚠️  Method failed: {e}")
    import traceback
    traceback.print_exc()

# Final fallback: Try updating assistant with files directly
print("\n📝 Final attempt: Direct assistant update...")
try:
    # Some API versions allow direct file assignment
    assistant = client.beta.assistants.update(
        ASSISTANT_ID,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": []  # Empty, will be created
            }
        }
    )
    
    # Then try to add files
    # This might require a separate API call
    print("   Assistant updated, but files may need separate linking")
    
except Exception as e:
    print(f"   ❌ Failed: {e}")

print(f"\n📝 Note: If all API methods fail, files are uploaded and ready.")
print(f"   They may need to be linked via the web UI.")
print(f"   Assistant ID: {ASSISTANT_ID}")
print(f"   File IDs: {file_ids}")



