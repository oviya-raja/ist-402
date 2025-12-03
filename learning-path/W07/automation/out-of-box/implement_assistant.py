#!/usr/bin/env python3
"""
OpenAI Assistant Implementation Script - Out-of-Box Tools Only

This script creates a complete assistant using built-in tools:
- Creates assistant with File Search, Code Interpreter, Web Search
- Uploads files to knowledge base
- Creates vector store
- Tests the assistant

Usage:
    # Activate virtual environment first
    source .venv/bin/activate  # or: source venv/bin/activate
    
    # Run script
    python implement_assistant.py

Requirements:
    - Virtual environment activated (.venv or venv)
    - .env file in project root with OPENAI_API_KEY
    - python-dotenv package (installed in venv)
    - openai package (installed in venv)

Note:
    - The .env file will override any existing OPENAI_API_KEY environment variable
    - This ensures .env file is the source of truth for this session
"""

import os
import json
import sys
import time
import requests
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI


# Configuration
ASSISTANT_NAME = "Student Query Response Agent"
ASSISTANT_MODEL = "gpt-4o"
ASSISTANT_INSTRUCTIONS = """You are a helpful assistant that answers student questions using the provided knowledge base.

Guidelines:
- Answer questions based on information in the knowledge base
- If information is not in the knowledge base, say so clearly
- Provide clear, concise answers
- Cite sources when possible
- Be friendly and professional"""

# Built-in tools to enable
TOOLS = [
    {"type": "file_search"},  # File Search tool
    # {"type": "code_interpreter"},  # Uncomment if needed
    # {"type": "web_search"},  # Uncomment if needed
]


def load_api_key() -> str:
    """
    Load OPENAI_API_KEY from .env file in project root.
    
    The .env file will override any existing OPENAI_API_KEY environment variable.
    This ensures the .env file is the source of truth for this session.
    
    Note: python-dotenv automatically ignores:
    - Lines starting with # (comments)
    - Empty lines
    - Whitespace-only lines
    """
    # Get project root (script is in learning-path/W07/automation/out-of-box)
    # Need to go up 5 levels: out-of-box -> automation -> W07 -> learning-path -> ist-402 (project root)
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent.parent.parent.parent
    env_path = project_root / ".env"
    
    # Load from .env file
    # load_dotenv automatically:
    # - Ignores comments (lines starting with #)
    # - Ignores empty lines
    # - Strips whitespace from values
    # override=True: .env values override any existing env vars for this session
    if env_path.exists():
        # Load from specific .env file path
        # This will ignore comments and empty lines automatically
        # override=True ensures .env file values override any existing environment variables
        result = load_dotenv(env_path, override=True, verbose=False)
    else:
        # Also try loading from current directory and parent directories
        # This searches for .env in current dir and parents
        result = load_dotenv(override=True, verbose=False)
    
    # Get API key (from env var or loaded from .env)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        error_msg = (
            f"OPENAI_API_KEY not found in .env file.\n"
            f"  - Checked .env file: {env_path} ({'exists' if env_path.exists() else 'not found'})\n"
            "Please ensure .env file exists in project root with OPENAI_API_KEY set.\n"
            "Note: Comments (lines starting with #) in .env are automatically ignored."
        )
        raise ValueError(error_msg)
    
    return api_key


def get_client(api_key: str) -> OpenAI:
    """Create and return OpenAI client."""
    return OpenAI(api_key=api_key)


def upload_files(client: OpenAI, file_paths: List[str]) -> List[str]:
    """Upload files to OpenAI and return file IDs."""
    print("📤 Uploading files...")
    file_ids = []
    
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"   ⚠️  File not found: {file_path}")
            continue
        
        try:
            with open(path, 'rb') as f:
                file = client.files.create(
                    file=f,
                    purpose="assistants"
                )
                file_ids.append(file.id)
                print(f"   ✅ Uploaded: {path.name} (ID: {file.id})")
        except Exception as e:
            print(f"   ❌ Error uploading {path.name}: {e}")
    
    return file_ids


def create_vector_store(client: OpenAI, name: str, file_ids: List[str]) -> str:
    """Create vector store and add files using direct API call."""
    print(f"\n📦 Creating vector store: {name}...")
    
    import requests
    
    try:
        # Use direct API call since vector_stores might not be in SDK beta namespace
        api_key = client.api_key
        url = "https://api.openai.com/v1/vector_stores"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "assistants=v2",
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "file_ids": file_ids
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        vector_store = response.json()
        vector_store_id = vector_store["id"]
        
        print(f"   ✅ Vector store created: {vector_store_id}")
        
        # Wait for files to be processed
        print("   ⏳ Waiting for files to be processed...")
        while True:
            vs_url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}"
            vs_response = requests.get(vs_url, headers=headers)
            vs_response.raise_for_status()
            vs_data = vs_response.json()
            
            file_counts = vs_data.get("file_counts", {})
            in_progress = file_counts.get("in_progress", 0)
            completed = file_counts.get("completed", 0)
            
            if in_progress == 0:
                print(f"   ✅ Files processed: {completed} completed")
                break
            
            print(f"   ⏳ Processing: {completed} completed, {in_progress} in progress...")
            time.sleep(2)
        
        return vector_store_id
    except Exception as e:
        print(f"   ❌ Error creating vector store: {e}")
        raise


def create_assistant(
    client: OpenAI,
    name: str,
    instructions: str,
    model: str,
    tools: List[dict],
    vector_store_id: Optional[str] = None
) -> str:
    """Create assistant with built-in tools."""
    print(f"\n🤖 Creating assistant: {name}...")
    
    tool_resources = {}
    if vector_store_id:
        tool_resources = {
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        }
    
    try:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools,
            tool_resources=tool_resources
        )
        print(f"   ✅ Assistant created: {assistant.id}")
        print(f"   📋 Model: {assistant.model}")
        print(f"   🛠️  Tools: {len(assistant.tools)} tool(s)")
        return assistant.id
    except Exception as e:
        print(f"   ❌ Error creating assistant: {e}")
        raise


def test_assistant(client: OpenAI, assistant_id: str, test_questions: List[str]) -> None:
    """Test assistant with sample questions."""
    print(f"\n🧪 Testing assistant...")
    
    thread = client.beta.threads.create()
    print(f"   ✅ Thread created: {thread.id}")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Question {i}: {question}")
        
        # Add message to thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )
        
        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        # Wait for completion
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_message = messages.data[0]
            if assistant_message.role == 'assistant':
                content = assistant_message.content[0].text.value
                print(f"   ✅ Answer: {content[:200]}...")
        else:
            print(f"   ❌ Run failed with status: {run.status}")


def check_venv() -> bool:
    """Check if virtual environment is activated."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )


def main():
    """Main execution function."""
    print("=" * 70)
    print("OpenAI Assistant Implementation - Out-of-Box Tools")
    print("=" * 70)
    print()
    
    # Check virtual environment
    if not check_venv():
        print("⚠️  Warning: Virtual environment may not be activated")
        print("   Recommended: source .venv/bin/activate")
        print()
    
    # Load API key (will override any existing env vars)
    try:
        api_key = load_api_key()
        print("✅ API key loaded from .env file (overrides existing env vars)")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Initialize client
    client = get_client(api_key)
    
    # Step 1: Upload files (optional - provide file paths)
    script_dir = Path(__file__).parent
    knowledge_base_dir = script_dir / "sample_knowledge_base"
    
    # Auto-detect files in sample_knowledge_base directory
    file_paths = []
    if knowledge_base_dir.exists():
        for file_path in knowledge_base_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in ['.txt', '.pdf', '.docx', '.md']:
                file_paths.append(str(file_path))
    
    if not file_paths:
        print("⚠️  No files found in sample_knowledge_base/")
        print("   Creating assistant without knowledge base")
        print("   You can add files later via Agent Builder UI")
    
    vector_store_id = None
    if file_paths:
        file_ids = upload_files(client, file_paths)
        if file_ids:
            vector_store_id = create_vector_store(
                client,
                "Student Knowledge Base",
                file_ids
            )
    else:
        print("\n⚠️  No files provided - creating assistant without knowledge base")
        print("   You can add files later via Agent Builder UI")
    
    # Step 2: Create assistant
    assistant_id = create_assistant(
        client=client,
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        model=ASSISTANT_MODEL,
        tools=TOOLS,
        vector_store_id=vector_store_id
    )
    
    # Step 3: Test assistant (optional)
    test_questions = [
        "What are the course requirements?",
        "How do I submit assignments?",
        "What is the grading policy?"
    ]
    
    # Handle interactive input (skip if non-interactive)
    try:
        test_choice = input("\n🧪 Test assistant? (y/n): ").lower()
        if test_choice == 'y':
            test_assistant(client, assistant_id, test_questions)
    except (EOFError, KeyboardInterrupt):
        print("\n⚠️  Skipping interactive test (non-interactive mode)")
        print("   You can test the assistant in Agent Builder UI")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Implementation Complete!")
    print("=" * 70)
    print(f"\n📋 Assistant ID: {assistant_id}")
    print(f"🌐 View in UI: https://platform.openai.com/assistants/{assistant_id}")
    print(f"\n💡 Next Steps:")
    print(f"   1. Go to Agent Builder UI to configure additional settings")
    print(f"   2. Upload more files if needed")
    print(f"   3. Test in Agent Builder chat interface")
    print(f"   4. Capture screenshots for documentation")
    print(f"\n📝 Note:")
    print(f"   - API key loaded from .env file (overrides existing env vars)")
    print(f"   - Virtual environment: {'✅ Activated' if check_venv() else '⚠️  Not detected'}")


if __name__ == "__main__":
    main()

