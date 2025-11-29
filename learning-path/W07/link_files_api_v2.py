#!/usr/bin/env python3
"""
Link files to assistant using OpenAI API - Updated approach
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

# File IDs
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
print(f"SDK Version: {client.__class__.__module__}")

# Check what's available in client.beta
print("\n📋 Checking API capabilities...")
print(f"  client.beta attributes: {[attr for attr in dir(client.beta) if not attr.startswith('_')]}")

# Try to access vector_stores
try:
    # Method 1: Direct access
    print("\n📚 Method 1: Creating vector store with files...")
    vector_store = client.beta.vector_stores.create(
        name="Job Fitment Analysis Knowledge Base",
        file_ids=file_ids
    )
    print(f"✅ Vector store created: {vector_store.id}")
    
    # Wait for processing
    print("\n⏳ Waiting for files to process...")
    max_wait = 120
    waited = 0
    while waited < max_wait:
        vs = client.beta.vector_stores.retrieve(vector_store.id)
        status = vs.status
        print(f"   Status: {status} ({waited}s)")
        
        if status == 'completed':
            print(f"✅ Files processed!")
            break
        
        time.sleep(3)
        waited += 3
    
    # Link to assistant
    print("\n🔗 Linking vector store to assistant...")
    assistant = client.beta.assistants.update(
        ASSISTANT_ID,
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        }
    )
    
    print(f"✅ SUCCESS!")
    print(f"   Assistant ID: {assistant.id}")
    print(f"   Vector Store ID: {vector_store.id}")
    print(f"   Files linked: {len(file_ids)}")
    
    # Final verification
    print("\n✅ Verification:")
    asst = client.beta.assistants.retrieve(ASSISTANT_ID)
    if asst.tool_resources and asst.tool_resources.file_search:
        vs_ids = asst.tool_resources.file_search.vector_store_ids
        if vs_ids:
            print(f"   ✅ Vector store linked: {vs_ids[0]}")
            
            # Check files in vector store
            try:
                vs_files = client.beta.vector_stores.files.list(vector_store_id=vs_ids[0])
                file_count = len(vs_files.data) if hasattr(vs_files, 'data') else 0
                print(f"   ✅ Files in vector store: {file_count}")
            except Exception as e:
                print(f"   ⚠️  Could not list files: {e}")
        else:
            print(f"   ⚠️  No vector store IDs")
    else:
        print(f"   ⚠️  No file_search resources")
    
    print(f"\n🎉 COMPLETE! Agent is ready to use!")
    print(f"🌐 View: https://platform.openai.com/assistants/{ASSISTANT_ID}")
    
except AttributeError as e:
    print(f"❌ AttributeError: {e}")
    print("\n💡 Trying alternative import...")
    
    # Try importing directly
    try:
        from openai import Beta
        beta = Beta(client=client)
        print(f"Beta object: {dir(beta)}")
    except Exception as e2:
        print(f"❌ Alternative import failed: {e2}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Type: {type(e)}")
    import traceback
    traceback.print_exc()



