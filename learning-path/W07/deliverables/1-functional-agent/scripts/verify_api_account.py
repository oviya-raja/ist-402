#!/usr/bin/env python3
"""
Verify which OpenAI account the API key belongs to
and help match it with the browser account
"""
import os
import sys
from openai import OpenAI
from utils import load_env, get_api_key, get_assistant_id

# Load environment
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()

print("=" * 70)
print("🔍 VERIFYING API ACCOUNT")
print("=" * 70)
print()

# Try to get account/organization info
print("📋 Step 1: Checking API Key Account...")
try:
    # List assistants to see what account this key belongs to
    assistants = client.beta.assistants.list(limit=10)
    
    print(f"   ✅ API Key is valid")
    print(f"   ✅ Found {len(assistants.data)} assistant(s) in this account")
    print()
    
    if len(assistants.data) > 0:
        print("   📋 Assistants in this API account:")
        for asst in assistants.data:
            marker = " ⭐" if asst.id == ASSISTANT_ID else ""
            print(f"      - {asst.name} ({asst.id}){marker}")
        print()
        
        # Check if our target assistant exists
        target_found = any(asst.id == ASSISTANT_ID for asst in assistants.data)
        if target_found:
            print(f"   ✅ Target assistant found: {ASSISTANT_ID}")
            print(f"      Name: {[a.name for a in assistants.data if a.id == ASSISTANT_ID][0]}")
        else:
            print(f"   ⚠️  Target assistant NOT found: {ASSISTANT_ID}")
            print(f"      This means the assistant is in a different account!")
    else:
        print("   ⚠️  No assistants found in this API account")
        print("      This could mean:")
        print("      1. You're using a different account in the browser")
        print("      2. The assistant was created in a different account")
        print()
    
    # Try to get organization info
    print("📋 Step 2: Getting Organization Info...")
    try:
        # Use models endpoint to get org info
        models = client.models.list()
        print(f"   ✅ API access confirmed")
        print(f"   ℹ️  Organization: (check in browser at https://platform.openai.com/account/org-settings)")
    except Exception as e:
        print(f"   ⚠️  Could not get organization info: {e}")
    
    print()
    print("=" * 70)
    print("📝 ACCOUNT MATCHING INSTRUCTIONS")
    print("=" * 70)
    print()
    print("To match your browser account with the API key:")
    print()
    print("OPTION 1: Use the same account in browser")
    print("  1. Go to: https://platform.openai.com")
    print("  2. Check which account you're logged into (top right)")
    print("  3. If different, log out and log into the account that matches the API key")
    print("  4. The assistant should appear in the browser")
    print()
    print("OPTION 2: Update API key to match browser account")
    print("  1. In browser, go to: https://platform.openai.com/api-keys")
    print("  2. Create a new API key (or copy existing one)")
    print("  3. Update .env file with the new key:")
    print(f"     OPENAI_API_KEY=sk-proj-...")
    print("  4. Re-run this script to verify")
    print()
    print("OPTION 3: Check project/organization")
    print("  1. In browser, check the project dropdown (top left)")
    print("  2. Make sure you're in the correct project/organization")
    print("  3. Different projects may have different assistants")
    print()
    print("=" * 70)
    print("🔗 QUICK LINKS")
    print("=" * 70)
    print()
    print(f"  Browser: https://platform.openai.com/assistants")
    print(f"  API Keys: https://platform.openai.com/api-keys")
    print(f"  Org Settings: https://platform.openai.com/account/org-settings")
    print()
    if ASSISTANT_ID:
        print(f"  Direct Assistant Link: https://platform.openai.com/assistants/{ASSISTANT_ID}")
        print()
    print("=" * 70)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

