#!/usr/bin/env python3
"""
Link files using raw HTTP API calls
OpenAI API v2 with proper headers
"""
import os
import sys
import time
import httpx

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
API_KEY = get_api_key()
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

BASE_URL = "https://api.openai.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2",
    "Content-Type": "application/json"
}

print("🔗 Linking files via OpenAI API (raw HTTP)...\n")

# Step 1: Create vector store
print("📚 Step 1: Creating vector store...")
try:
    response = httpx.post(
        f"{BASE_URL}/vector_stores",
        headers=HEADERS,
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
        print(f"   Status: {vs_data.get('status', 'unknown')}")
    else:
        print(f"❌ Error creating vector store: {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 2: Wait for processing
print("\n⏳ Step 2: Waiting for files to process...")
max_wait = 120
waited = 0
while waited < max_wait:
    try:
        response = httpx.get(
            f"{BASE_URL}/vector_stores/{vs_id}",
            headers=HEADERS,
            timeout=30.0
        )
        
        if response.status_code == 200:
            vs_data = response.json()
            status = vs_data.get("status", "unknown")
            file_count = vs_data.get("file_counts", {})
            
            print(f"   Status: {status} ({waited}s)")
            if file_count:
                print(f"   Files: {file_count}")
            
            if status == "completed":
                print(f"✅ Files processed!")
                break
        else:
            print(f"   ⚠️  Error checking status: {response.status_code}")
            
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    time.sleep(3)
    waited += 3

if waited >= max_wait:
    print(f"\n   ⚠️  Timeout waiting for files to process (max {max_wait}s)")
    print(f"   Continuing anyway - files may still be processing...")

# Step 3: Link vector store to assistant
print("\n🔗 Step 3: Linking vector store to assistant...")
try:
    response = httpx.post(
        f"{BASE_URL}/assistants/{ASSISTANT_ID}",
        headers=HEADERS,
        json={
            "tool_resources": {
                "file_search": {
                    "vector_store_ids": [vs_id]
                }
            }
        },
        timeout=30.0
    )
    
    if response.status_code == 200:
        asst_data = response.json()
        print(f"✅ Vector store linked to assistant!")
        print(f"   Assistant: {asst_data.get('name', 'N/A')}")
        
        # Verify
        tool_resources = asst_data.get("tool_resources", {})
        if tool_resources and "file_search" in tool_resources:
            vs_ids = tool_resources["file_search"].get("vector_store_ids", [])
            if vs_id in vs_ids:
                print(f"   ✅ Verified: Vector store {vs_id} is linked")
            else:
                print(f"   ⚠️  Warning: Vector store not found in response")
        
        print(f"\n🎉 SUCCESS! Files linked via API!")
        print(f"   Assistant ID: {ASSISTANT_ID}")
        print(f"   Vector Store ID: {vs_id}")
        print(f"   Files: {len(file_ids)}")
        print(f"\n🌐 View: https://platform.openai.com/assistants/{ASSISTANT_ID}")
        sys.exit(0)
    else:
        print(f"❌ Error linking: {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



