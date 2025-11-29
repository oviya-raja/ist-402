#!/usr/bin/env python3
"""
Verify which account/project the assistant belongs to
"""
from openai import OpenAI
import httpx

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)

print("=" * 70)
print("🔍 ACCOUNT VERIFICATION")
print("=" * 70)
print()

# Check API key info
print("📋 API Key Information:")
print(f"   Key prefix: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else 'short'}")
print()

# List all assistants in this account
print("📋 All Assistants in API Account:")
assistants = client.beta.assistants.list(limit=20)
print(f"   Total: {len(assistants.data)}")
for asst in assistants.data:
    print(f"   - {asst.name} ({asst.id})")
    print(f"     Created: {asst.created_at}")
print()

# Check specific assistant
assistant_id = get_assistant_id()
print(f"🔍 Checking Assistant: {assistant_id}")
try:
    asst = client.beta.assistants.retrieve(assistant_id)
    print(f"   ✅ EXISTS in API account")
    print(f"   Name: {asst.name}")
    print(f"   Model: {asst.model}")
    print(f"   Created: {asst.created_at}")
    
    # Check vector store
    if asst.tool_resources and asst.tool_resources.file_search:
        vs_ids = asst.tool_resources.file_search.vector_store_ids
        if vs_ids:
            print(f"   Vector Store: {vs_ids[0]}")
            
            # Check files
            headers = {
                "Authorization": f"Bearer {api_key}",
                "OpenAI-Beta": "assistants=v2"
            }
            response = httpx.get(
                f"https://api.openai.com/v1/vector_stores/{vs_ids[0]}/files",
                headers=headers,
                timeout=30.0
            )
            if response.status_code == 200:
                files = response.json().get("data", [])
                print(f"   Files: {len(files)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("=" * 70)
print("⚠️  IMPORTANT:")
print("=" * 70)
print()
print("The assistant EXISTS via API but NOT visible in browser.")
print("This means:")
print("  1. Browser is logged into a DIFFERENT account than the API key")
print("  2. OR assistant is in a DIFFERENT project/workspace")
print()
print("To fix:")
print("  1. Check which email is logged into the browser")
print("  2. Check which email the API key belongs to")
print("  3. Either:")
print("     - Log into the correct account in browser, OR")
print("     - Use the API key from the account logged in browser")
print()
print(f"🌐 Direct link (may not work if wrong account):")
print(f"   https://platform.openai.com/assistants/{assistant_id}")



