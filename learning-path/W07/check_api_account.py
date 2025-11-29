#!/usr/bin/env python3
"""
Check which account the API key belongs to
"""
from openai import OpenAI
import httpx

# Import common utilities
from utils import load_env, get_api_key

# Load environment variables
load_env()
api_key = get_api_key()

print("=" * 70)
print("🔍 CHECKING API KEY ACCOUNT")
print("=" * 70)
print()

# Method 1: Try to get account info from API
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("📋 Attempting to identify API key account...")
print()

# Try billing/subscription endpoint (often shows account info)
try:
    response = httpx.get(
        "https://api.openai.com/v1/dashboard/billing/subscription",
        headers=headers,
        timeout=10.0
    )
    if response.status_code == 200:
        data = response.json()
        print("✅ Account Information Found:")
        print(f"   Account ID: {data.get('id', 'N/A')}")
        print(f"   Account Type: {data.get('object', 'N/A')}")
        if 'organization_id' in data:
            print(f"   Organization ID: {data.get('organization_id', 'N/A')}")
        print()
except Exception as e:
    print(f"   ⚠️  Could not get subscription info: {e}")

# Try usage endpoint
try:
    response = httpx.get(
        "https://api.openai.com/v1/usage",
        headers=headers,
        timeout=10.0
    )
    if response.status_code == 200:
        print("✅ Usage endpoint accessible")
    else:
        print(f"   Usage endpoint: {response.status_code}")
except Exception as e:
    print(f"   Usage endpoint error: {e}")

# List assistants to confirm account
print("\n📋 Assistants in this API account:")
client = OpenAI(api_key=api_key)
assistants = client.beta.assistants.list(limit=5)
print(f"   Total: {len(assistants.data)}")
for asst in assistants.data:
    print(f"   - {asst.name} ({asst.id})")

print()
print("=" * 70)
print("📝 HOW TO MATCH ACCOUNTS:")
print("=" * 70)
print()
print("1. Check browser account:")
print("   - Look at the email in the top-right of OpenAI Platform")
print("   - Or click on 'Personal' dropdown in browser")
print()
print("2. Check API key account:")
print("   - Go to: https://platform.openai.com/api-keys")
print("   - See which account the API key belongs to")
print()
print("3. Match them:")
print("   - If different: Either change API key OR log into correct account")
print()



