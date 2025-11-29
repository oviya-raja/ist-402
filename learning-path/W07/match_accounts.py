#!/usr/bin/env python3
"""
Match API account with Browser account
Shows what account each is using and how to sync them
"""
from openai import OpenAI

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)

print("=" * 70)
print("🔍 ACCOUNT MATCHING TOOL")
print("=" * 70)
print()

# Check API Account
print("📋 API KEY ACCOUNT (from .env file):")
print(f"   Key prefix: {api_key[:15]}...{api_key[-8:]}")
print()

# List what's in this API account
print("   Resources in this API account:")
assistants = client.beta.assistants.list(limit=10)
print(f"   - Assistants: {len(assistants.data)}")
for asst in assistants.data:
    print(f"     • {asst.name} ({asst.id})")

# Check files
files = client.files.list(limit=10)
print(f"   - Files: {len(files.data)}")
if files.data:
    for f in files.data[:5]:
        print(f"     • {f.filename or f.id} ({f.id})")

print()
print("=" * 70)
print("🌐 BROWSER ACCOUNT:")
print("=" * 70)
print()
print("   To check browser account:")
print("   1. Look at the top-left of OpenAI Platform")
print("      - Click on 'Personal' dropdown")
print("      - See the email address")
print()
print("   2. Or check API Keys page:")
print("      - Go to: https://platform.openai.com/api-keys")
print("      - See which account you're logged into")
print()
print("   3. Check Assistants page:")
print("      - Go to: https://platform.openai.com/assistants")
print("      - See if 'Job Fitment Analysis Agent' appears")
print()

print("=" * 70)
print("✅ HOW TO MATCH ACCOUNTS:")
print("=" * 70)
print()

# Check if assistant exists
assistant_id = get_assistant_id()
try:
    asst = client.beta.assistants.retrieve(assistant_id)
    print(f"✅ Assistant EXISTS in API account:")
    print(f"   Name: {asst.name}")
    print(f"   ID: {asst.id}")
    print()
    print("📝 OPTIONS TO SYNC:")
    print()
    print("   Option 1: Use API Key from Browser Account")
    print("   ──────────────────────────────────────────")
    print("   1. In browser, go to: https://platform.openai.com/api-keys")
    print("   2. Click 'Create new secret key'")
    print("   3. Copy the new API key")
    print("   4. Update .env file:")
    print("      OPENAI_API_KEY=your_new_key_here")
    print("   5. Recreate assistant in browser account")
    print()
    print("   Option 2: Log into API Key Account in Browser")
    print("   ────────────────────────────────────────────")
    print("   1. Log out of current browser session")
    print("   2. Log into the account that owns the API key")
    print("   3. Assistant will be visible in browser")
    print()
    print("   Option 3: Continue with API (Recommended)")
    print("   ──────────────────────────────────────────")
    print("   The assistant works perfectly via API!")
    print("   You can test it with: python3 test_agent_e2e.py")
    print("   Browser visibility is optional for testing.")
    print()
    
except Exception as e:
    print(f"❌ Assistant not found: {e}")
    print()
    print("   The assistant needs to be created.")
    print("   Run: python3 create_agent.py")

print("=" * 70)
print("🔑 QUICK CHECK:")
print("=" * 70)
print()
print("Run this command to see browser account email:")
print("   (Check the 'Personal' dropdown in browser)")
print()
print("Or check API keys page in browser:")
print("   https://platform.openai.com/api-keys")
print()



