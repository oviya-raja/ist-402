#!/usr/bin/env python3
"""
Add files to existing vector store
"""
import os
import sys
import time
import httpx

# Import common utilities
from utils import load_env, get_api_key, get_vector_store_id

# Load environment variables
load_env()
API_KEY = get_api_key()
VS_ID = get_vector_store_id()

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

print("📎 Adding files to vector store...\n")

# Check current files
print("📋 Checking current files in vector store...")
try:
    response = httpx.get(
        f"{BASE_URL}/vector_stores/{VS_ID}/files",
        headers=HEADERS,
        timeout=30.0
    )
    if response.status_code == 200:
        current_files = response.json().get("data", [])
        current_file_ids = [f["id"] for f in current_files]
        print(f"   Current files: {len(current_file_ids)}")
        if current_file_ids:
            print(f"   File IDs: {current_file_ids[:3]}...")
    else:
        current_file_ids = []
        print(f"   ⚠️  Could not check: {response.status_code}")
except Exception as e:
    current_file_ids = []
    print(f"   ⚠️  Error: {e}")

# Add files that aren't already there
files_to_add = [fid for fid in file_ids if fid not in current_file_ids]
if not files_to_add:
    print(f"\n✅ All files already in vector store!")
    sys.exit(0)

print(f"\n📤 Adding {len(files_to_add)} files...")
for file_id in files_to_add:
    try:
        response = httpx.post(
            f"{BASE_URL}/vector_stores/{VS_ID}/files",
            headers=HEADERS,
            json={"file_id": file_id},
            timeout=30.0
        )
        
        if response.status_code == 200:
            print(f"  ✅ Added: {file_id}")
        else:
            print(f"  ⚠️  Error adding {file_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"  ⚠️  Error: {e}")

# Wait for processing
print("\n⏳ Waiting for files to process...")
time.sleep(5)

# Verify
print("\n✅ Verification:")
try:
    response = httpx.get(
        f"{BASE_URL}/vector_stores/{VS_ID}/files",
        headers=HEADERS,
        timeout=30.0
    )
    if response.status_code == 200:
        files = response.json().get("data", [])
        print(f"   Total files in vector store: {len(files)}")
        if len(files) == len(file_ids):
            print(f"   ✅ All {len(file_ids)} files are in the vector store!")
        else:
            print(f"   ⚠️  Expected {len(file_ids)}, found {len(files)}")
except Exception as e:
    print(f"   ⚠️  Error verifying: {e}")

print(f"\n🎉 Complete!")
print(f"   Vector Store ID: {VS_ID}")
print(f"   Files: {len(file_ids)}")



