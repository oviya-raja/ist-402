#!/usr/bin/env python3
"""
Delete All Assistants Script

This script deletes all assistants for the OpenAI account.
Use with caution!

Usage:
    python delete_all_assistants.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def load_api_key() -> str:
    """Load OPENAI_API_KEY from .env file in project root."""
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent.parent.parent.parent
    env_path = project_root / ".env"
    
    if env_path.exists():
        load_dotenv(env_path, override=True, verbose=False)
    else:
        load_dotenv(override=True, verbose=False)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            f"OPENAI_API_KEY not found in .env file.\n"
            f"  - Checked: {env_path}\n"
            "Please ensure .env file exists in project root with OPENAI_API_KEY set."
        )
    return api_key


def delete_all_assistants(client: OpenAI) -> None:
    """Delete all assistants."""
    print("📋 Listing all assistants...")
    try:
        assistants = client.beta.assistants.list()
        
        if not assistants.data:
            print("   ✅ No assistants found.")
            return
        
        print(f"   Found {len(assistants.data)} assistant(s):\n")
        
        deleted_count = 0
        for assistant in assistants.data:
            try:
                print(f"   🗑️  Deleting: {assistant.name or 'Unnamed'} (ID: {assistant.id})")
                client.beta.assistants.delete(assistant.id)
                deleted_count += 1
                print(f"      ✅ Deleted")
            except Exception as e:
                print(f"      ❌ Error: {e}")
        
        print(f"\n✅ Deleted {deleted_count} assistant(s)")
        
    except Exception as e:
        print(f"❌ Error listing/deleting assistants: {e}")
        raise


def main():
    """Main execution function."""
    print("=" * 70)
    print("Delete All Assistants")
    print("=" * 70)
    print()
    
    # Load API key
    try:
        api_key = load_api_key()
        print("✅ API key loaded")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Initialize client
    client = OpenAI(api_key=api_key)
    
    # Confirm deletion
    print("⚠️  WARNING: This will delete ALL assistants!")
    confirm = input("   Type 'DELETE ALL' to confirm: ")
    
    if confirm != "DELETE ALL":
        print("❌ Cancelled. No assistants were deleted.")
        sys.exit(0)
    
    # Delete all assistants
    try:
        delete_all_assistants(client)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✅ All assistants deleted!")
    print("=" * 70)


if __name__ == "__main__":
    main()

