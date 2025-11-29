#!/usr/bin/env python3
"""
Update .env file with new API key
Run this after you get the new API key from browser
"""
import sys
from utils import get_env_path

env_path = get_env_path()

if len(sys.argv) < 2:
    print("Usage: python3 update_env_with_new_key.py <new_api_key>")
    print()
    print("Example:")
    print("  python3 update_env_with_new_key.py sk-proj-abc123...")
    sys.exit(1)

new_key = sys.argv[1].strip()

# Read current .env
if env_path.exists():
    content = env_path.read_text()
    lines = content.split('\n')
    
    # Update or add OPENAI_API_KEY
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith('OPENAI_API_KEY='):
            new_lines.append(f'OPENAI_API_KEY={new_key}')
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f'OPENAI_API_KEY={new_key}')
    
    env_path.write_text('\n'.join(new_lines))
    print(f"✅ Updated .env file with new API key")
    print(f"   Key prefix: {new_key[:15]}...{new_key[-8:]}")
else:
    # Create new .env
    env_path.write_text(f'OPENAI_API_KEY={new_key}\n')
    print(f"✅ Created .env file with new API key")

print()
print("Next step: Run 'python3 create_agent.py' to recreate assistant in browser account")



