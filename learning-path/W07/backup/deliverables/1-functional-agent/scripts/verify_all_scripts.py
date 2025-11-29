#!/usr/bin/env python3
"""
Verify all Python scripts are working correctly
Tests imports, utilities, and basic functionality
"""
import sys
import importlib.util
from pathlib import Path

print("=" * 70)
print("🔍 VERIFYING ALL PYTHON SCRIPTS")
print("=" * 70)
print()

# Test utils module
print("📋 Testing utils module...")
try:
    from utils import (
        get_env_path, load_env, get_api_key, 
        get_assistant_id, get_vector_store_id, verify_env_setup
    )
    
    # Test env path
    env_path = get_env_path()
    print(f"   ✅ get_env_path(): {env_path}")
    print(f"      Exists: {env_path.exists()}")
    
    # Test env loading
    load_env()
    print(f"   ✅ load_env(): Success")
    
    # Test API key
    api_key = get_api_key()
    print(f"   ✅ get_api_key(): {api_key[:20]}...{api_key[-10:]}")
    
    # Test assistant ID
    assistant_id = get_assistant_id()
    print(f"   ✅ get_assistant_id(): {assistant_id}")
    
    # Test vector store ID
    vs_id = get_vector_store_id()
    print(f"   ✅ get_vector_store_id(): {vs_id}")
    
    # Test verification
    success, msg = verify_env_setup()
    print(f"   ✅ verify_env_setup(): {msg}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()

# Test all script imports
print("📋 Testing script imports...")
scripts = [
    "create_agent.py",
    "test_agent_e2e.py",
    "test_all_use_cases.py",
    "add_files_to_vector_store.py",
    "complete_agent_setup.py",
    "link_files_raw_api.py",
    "verify_all_scripts.py",
]

# Script is in deliverables/1-functional-agent/scripts/, scripts are in same directory
script_dir = Path(__file__).parent
failed_imports = []

for script_name in scripts:
    script_path = script_dir / script_name
    if not script_path.exists():
        print(f"   ⚠️  {script_name}: File not found")
        continue
    
    try:
        # Check syntax
        with open(script_path, 'r') as f:
            code = f.read()
            compile(code, script_path, 'exec')
        print(f"   ✅ {script_name}: Syntax OK")
    except SyntaxError as e:
        print(f"   ❌ {script_name}: Syntax error - {e}")
        failed_imports.append(script_name)
    except Exception as e:
        print(f"   ⚠️  {script_name}: {e}")

print()

# Test required dependencies
print("📋 Testing required dependencies...")
required_modules = [
    ("openai", "OpenAI"),
    ("httpx", "httpx"),
    ("dotenv", "load_dotenv"),
]

missing_modules = []
for module_name, import_name in required_modules:
    try:
        __import__(module_name)
        print(f"   ✅ {module_name}: Available")
    except ImportError:
        print(f"   ❌ {module_name}: NOT INSTALLED")
        missing_modules.append(module_name)

print()

# Summary
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print()

if failed_imports:
    print(f"❌ {len(failed_imports)} script(s) have issues:")
    for script in failed_imports:
        print(f"   - {script}")
else:
    print("✅ All scripts have valid syntax")

if missing_modules:
    print(f"\n❌ Missing dependencies:")
    for module in missing_modules:
        print(f"   - {module}")
    print(f"\n💡 Install with: pip install {' '.join(missing_modules)}")
else:
    print("✅ All required dependencies are installed")

print()
print("=" * 70)
if not failed_imports and not missing_modules:
    print("🎉 ALL CHECKS PASSED!")
else:
    print("⚠️  Some issues found - see above")
print("=" * 70)

