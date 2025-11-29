#!/usr/bin/env python3
"""
Common utilities for OpenAI agent scripts
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def get_env_path():
    """Get the path to .env file, relative to project root"""
    # Script is in deliverables/1-functional-agent/scripts/
    # Go up to project root: scripts -> 1-functional-agent -> deliverables -> W07 -> ist-402
    script_dir = Path(__file__).parent
    # Go up 4 levels to get to W07, then up one more to ist-402
    project_root = script_dir.parent.parent.parent.parent.parent
    env_path = project_root / ".env"
    return env_path


def load_env():
    """Load environment variables from .env file, overriding any existing env vars"""
    env_path = get_env_path()
    if not env_path.exists():
        print(f"ERROR: .env file not found at {env_path}")
        print(f"Please create .env file with OPENAI_API_KEY")
        sys.exit(1)
    # Use override=True to ensure .env file values override environment variables
    load_dotenv(env_path, override=True)
    return env_path


def get_api_key():
    """Get and validate OpenAI API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        env_path = get_env_path()
        print(f"ERROR: OPENAI_API_KEY not found in .env file")
        print(f"Please add OPENAI_API_KEY to {env_path}")
        sys.exit(1)
    # Basic validation
    if not api_key.startswith(('sk-', 'sk-proj-')):
        print(f"WARNING: API key format may be incorrect (should start with 'sk-' or 'sk-proj-')")
    return api_key


def get_assistant_id():
    """Get assistant ID from environment or return default"""
    assistant_id = os.getenv("ASSISTANT_ID", "asst_jPS7NmMYqh3QPxxl1nyCI7Yj")
    if not assistant_id.startswith("asst_"):
        print(f"WARNING: Assistant ID format may be incorrect (should start with 'asst_')")
    return assistant_id


def get_vector_store_id():
    """Get vector store ID from environment or return default"""
    vs_id = os.getenv("VECTOR_STORE_ID", "vs_692b51c5140c8191aca47cf90d444c0f")
    if not vs_id.startswith("vs_"):
        print(f"WARNING: Vector store ID format may be incorrect (should start with 'vs_')")
    return vs_id


def verify_env_setup():
    """Verify that .env file is properly set up and accessible"""
    env_path = get_env_path()
    if not env_path.exists():
        return False, f".env file not found at {env_path}"
    
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False, "OPENAI_API_KEY not found in .env file"
    
    return True, f".env file loaded successfully from {env_path}"

