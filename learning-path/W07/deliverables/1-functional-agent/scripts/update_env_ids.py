#!/usr/bin/env python3
"""
Update .env file with new Assistant ID and Vector Store ID
"""
import os
import sys
from pathlib import Path
from utils import get_env_path

def update_env_file(assistant_id, vector_store_id):
    """Update .env file with new IDs"""
    env_path = get_env_path()
    
    if not env_path.exists():
        print(f"❌ .env file not found at: {env_path}")
        return False
    
    # Read current content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update or add ASSISTANT_ID
    assistant_found = False
    vector_found = False
    
    new_lines = []
    for line in lines:
        if line.strip().startswith('ASSISTANT_ID='):
            new_lines.append(f'ASSISTANT_ID={assistant_id}\n')
            assistant_found = True
        elif line.strip().startswith('VECTOR_STORE_ID='):
            new_lines.append(f'VECTOR_STORE_ID={vector_store_id}\n')
            vector_found = True
        else:
            new_lines.append(line)
    
    # Add if not found
    if not assistant_found:
        new_lines.append(f'\nASSISTANT_ID={assistant_id}\n')
    if not vector_found:
        new_lines.append(f'VECTOR_STORE_ID={vector_store_id}\n')
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print(f"✅ Updated .env file:")
    print(f"   ASSISTANT_ID={assistant_id}")
    print(f"   VECTOR_STORE_ID={vector_store_id}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 update_env_ids.py <assistant_id> <vector_store_id>")
        sys.exit(1)
    
    assistant_id = sys.argv[1]
    vector_store_id = sys.argv[2]
    
    update_env_file(assistant_id, vector_store_id)

