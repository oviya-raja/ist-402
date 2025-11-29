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
    # Get the project root (parent of learning-path)
    script_dir = Path(__file__).parent
    # Go up to ist-402 directory
    project_root = script_dir.parent.parent
    env_path = project_root / ".env"
    return env_path


def load_env():
    """Load environment variables from .env file"""
    env_path = get_env_path()
    if not env_path.exists():
        print(f"ERROR: .env file not found at {env_path}")
        print(f"Please create .env file with OPENAI_API_KEY")
        sys.exit(1)
    load_dotenv(env_path)
    return env_path


def get_api_key():
    """Get and validate OpenAI API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        env_path = get_env_path()
        print(f"ERROR: OPENAI_API_KEY not found in .env file")
        print(f"Please add OPENAI_API_KEY to {env_path}")
        sys.exit(1)
    return api_key


def get_assistant_id():
    """Get assistant ID from environment or return default"""
    return os.getenv("ASSISTANT_ID", "asst_jPS7NmMYqh3QPxxl1nyCI7Yj")


def get_vector_store_id():
    """Get vector store ID from environment or return default"""
    return os.getenv("VECTOR_STORE_ID", "vs_692b51c5140c8191aca47cf90d444c0f")

