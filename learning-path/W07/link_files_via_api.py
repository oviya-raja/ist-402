#!/usr/bin/env python3
"""
Link uploaded files to assistant using OpenAI API
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

# File IDs from previous upload
file_ids = [
    "file-Qjz8NYSYmKhf5SgFymKsN9",  # profile-template.txt
    "file-K9bMtGGJeATSEQDkaEfg8D",  # skills-taxonomy.txt
    "file-Pbxfs2Q5XzDxwdiqcVmUMT",  # experience-levels.txt
    "file-PAiR8gHkNaDXERKWuTkv6i",  # job-posting-structure.txt
    "file-QULV4KsH7Xs8p6guEZ2qsx",  # target-companies.txt
    "file-Ext59zodCpWLsXYHUq95yh",  # calculation-methodology.txt
    "file-AUyPijrBAptgTDZD5DyhaX",  # interpretation-guide.txt
    "file-P5WeXb6Meg2uTDSitF9TSd",  # gap-identification.txt
    "file-VijAPn2YQ8v3TvEq28XP9e",  # learning-resources.txt
    "file-APxyU6Nk6VYSjCon2Ki8oh",  # use-case-1-example.txt
]

print("🔗 Linking files to assistant via API...\n")

# Method 1: Try using vector_stores if available
try:
    print("📚 Method 1: Creating vector store...")
    
    # Check if vector_stores attribute exists
    if hasattr(client.beta, 'vector_stores'):
        # Create vector store
        vector_store = client.beta.vector_stores.create(
            name="Job Fitment Analysis Knowledge Base"
        )
        print(f"✅ Vector store created: {vector_store.id}")
        
        # Add files to vector store
        print("\n📎 Adding files to vector store...")
        for file_id in file_ids:
            try:
                client.beta.vector_stores.files.create(
                    vector_store_id=vector_store.id,
                    file_id=file_id
                )
                print(f"  ✅ Added: {file_id}")
            except Exception as e:
                print(f"  ⚠️  Error adding {file_id}: {e}")
        
        # Wait for processing
        print("\n⏳ Waiting for files to process...")
        max_wait = 120
        waited = 0
        while waited < max_wait:
            vs = client.beta.vector_stores.retrieve(vector_store.id)
            if vs.status == 'completed':
                print(f"✅ Files processed!")
                break
            time.sleep(3)
            waited += 3
            if waited % 15 == 0:
                print(f"   Still processing... ({waited}s)")
        
        # Update assistant with vector store
        print("\n🔗 Linking vector store to assistant...")
        assistant = client.beta.assistants.update(
            ASSISTANT_ID,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store.id]
                }
            }
        )
        print(f"✅ Vector store linked to assistant!")
        print(f"   Vector Store ID: {vector_store.id}")
        print(f"   Files: {len(file_ids)}")
        
        # Verify
        print("\n✅ Verification:")
        asst = client.beta.assistants.retrieve(ASSISTANT_ID)
        if asst.tool_resources and asst.tool_resources.file_search:
            vs_ids = asst.tool_resources.file_search.vector_store_ids
            if vs_ids:
                print(f"   ✅ Assistant has vector store: {vs_ids[0]}")
            else:
                print(f"   ⚠️  No vector store IDs found")
        else:
            print(f"   ⚠️  No file_search tool resources found")
        
        print(f"\n🎉 SUCCESS! Files linked via API!")
        sys.exit(0)
    else:
        raise AttributeError("vector_stores not available in client.beta")
        
except AttributeError as e:
    print(f"⚠️  Method 1 failed: {e}")
    print("\n📚 Method 2: Trying direct file_ids in tool_resources...")
    
    # Method 2: Try using file_ids directly (older API)
    try:
        assistant = client.beta.assistants.update(
            ASSISTANT_ID,
            tool_resources={
                "file_search": {
                    "file_ids": file_ids
                }
            }
        )
        print(f"✅ Files linked directly!")
        print(f"   Files: {len(file_ids)}")
        sys.exit(0)
    except Exception as e2:
        print(f"⚠️  Method 2 failed: {e2}")
        
except Exception as e:
    print(f"⚠️  Error: {e}")
    print("\n📝 Trying alternative approach...")
    
    # Method 3: Check API version and try different approach
    try:
        print("Checking API capabilities...")
        # Try to retrieve assistant to see current state
        asst = client.beta.assistants.retrieve(ASSISTANT_ID)
        print(f"Current assistant tools: {asst.tools}")
        print(f"Current tool_resources: {asst.tool_resources}")
        
        # Try updating with files directly
        print("\nAttempting direct update...")
        assistant = client.beta.assistants.update(
            ASSISTANT_ID,
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": []  # Will create new one
                }
            }
        )
        print("Update successful, but may need manual file linking")
        
    except Exception as e3:
        print(f"⚠️  All methods failed: {e3}")
        print("\n📝 Manual step required via browser UI")
        print(f"   Assistant ID: {ASSISTANT_ID}")
        print(f"   File IDs: {file_ids}")

print(f"\n🌐 View assistant: https://platform.openai.com/assistants/{ASSISTANT_ID}")



