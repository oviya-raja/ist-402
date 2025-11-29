#!/usr/bin/env python3
"""
Check which API key is active in .env and help identify the account
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get .env path
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent.parent.parent.parent
env_path = project_root / ".env"

print("=" * 70)
print("🔑 CHECKING .ENV API KEY")
print("=" * 70)
print()

if not env_path.exists():
    print(f"❌ .env file not found at: {env_path}")
    exit(1)

print(f"📁 .env file location: {env_path}")
print()

# Read .env file
with open(env_path, 'r') as f:
    lines = f.readlines()

print("📋 API Keys found in .env:")
print()

active_key = None
commented_keys = []

for i, line in enumerate(lines, 1):
    line = line.strip()
    if 'OPENAI_API_KEY' in line:
        if line.startswith('#'):
            # Commented out
            key_part = line.split('=')[-1] if '=' in line else 'N/A'
            if key_part and key_part.startswith('sk-'):
                commented_keys.append((i, key_part[:20] + '...'))
                print(f"   Line {i}: ⚪ COMMENTED OUT")
                print(f"            {key_part[:25]}...")
        else:
            # Active
            key_part = line.split('=')[-1] if '=' in line else 'N/A'
            if key_part and key_part.startswith('sk-'):
                active_key = key_part
                print(f"   Line {i}: ✅ ACTIVE")
                print(f"            {key_part[:25]}...")
                print(f"            Full key: {key_part[:50]}...")

print()

if active_key:
    print("✅ Active API Key Identified:")
    print(f"   First 8-9 chars: {active_key[:9]}")
    print(f"   First 20 chars: {active_key[:20]}")
    print()
    print("📝 To identify which account this key belongs to:")
    print("   1. Go to: https://platform.openai.com/api-keys")
    print("   2. Look for a key starting with: " + active_key[:9])
    print("   3. Check which account/organization that key is under")
    print("   4. Log into that same account in the browser")
    print()
    print("🔗 Quick Links:")
    print("   - API Keys: https://platform.openai.com/api-keys")
    print("   - Assistants: https://platform.openai.com/assistants")
    print("   - Direct Assistant: https://platform.openai.com/assistants/asst_jPS7NmMYqh3QPxxl1nyCI7Yj")
else:
    print("❌ No active API key found in .env")
    print("   Please add: OPENAI_API_KEY=sk-proj-...")

print()
print("=" * 70)

