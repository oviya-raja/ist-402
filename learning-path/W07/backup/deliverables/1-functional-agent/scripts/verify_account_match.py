#!/usr/bin/env python3
"""
Verify if API key matches browser account
Check which account the API key belongs to and compare with browser account
"""
import os
import sys
from openai import OpenAI
from utils import load_env, get_api_key

def main():
    load_env()
    api_key = get_api_key()
    browser_email = os.getenv("OPENAI_EMAIL", "NOT SET")
    
    print("=" * 70)
    print("🔍 VERIFYING API KEY ACCOUNT MATCH")
    print("=" * 70)
    print()
    
    print(f"📧 Browser Account (from .env): {browser_email}")
    print(f"🔑 API Key (first 20 chars): {api_key[:20]}...")
    print()
    
    client = OpenAI(api_key=api_key)
    
    # Check assistants in this account
    print("📋 Checking assistants in API key account...")
    try:
        assistants = client.beta.assistants.list(limit=20)
        print(f"   ✅ Found {len(assistants.data)} assistant(s) in this account")
        print()
        
        if len(assistants.data) > 0:
            print("   Assistants in API key account:")
            for asst in assistants.data:
                print(f"      - {asst.name} ({asst.id})")
            print()
        else:
            print("   ⚠️  No assistants found in API key account")
            print()
        
        # Check target assistant
        target_id = "asst_iwUluQrtuJR3Rsk7Yxs24BLi"
        target_found = any(a.id == target_id for a in assistants.data)
        
        if target_found:
            print(f"   ✅ Target assistant FOUND: {target_id}")
            print(f"      This means the assistant EXISTS in the API key account")
        else:
            print(f"   ❌ Target assistant NOT FOUND: {target_id}")
            print(f"      This means the assistant is in a DIFFERENT account")
        
        print()
        
        # Try to get account/organization info
        print("📋 Attempting to identify account...")
        try:
            # Try models endpoint
            models = client.models.list()
            print(f"   ✅ API key is valid and active")
            print(f"   ℹ️  To verify account match:")
            print(f"      1. Go to: https://platform.openai.com/api-keys")
            print(f"      2. Find API key starting with: {api_key[:9]}")
            print(f"      3. Check which account/email that key belongs to")
            print(f"      4. Compare with browser account: {browser_email}")
        except Exception as e:
            print(f"   ⚠️  Could not verify account: {e}")
        
        print()
        print("=" * 70)
        print("🔍 DIAGNOSIS")
        print("=" * 70)
        print()
        
        if target_found:
            print("✅ Assistant EXISTS in API key account")
            print("⚠️  But browser shows 'No assistants found'")
            print()
            print("Possible causes:")
            print("  1. Browser is logged into DIFFERENT account than API key")
            print("  2. Browser is in DIFFERENT project/organization")
            print("  3. Browser cache needs to be cleared")
            print()
            print("Solution:")
            print(f"  - Verify API key belongs to account: {browser_email}")
            print("  - If different, either:")
            print("    a) Log into correct account in browser")
            print("    b) Update .env with API key from browser account")
        else:
            print("❌ Assistant NOT FOUND in API key account")
            print("   This means the assistant was created in a different account")
            print("   Need to create assistant in the correct account")
        
    except Exception as e:
        print(f"❌ Error checking account: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

