#!/usr/bin/env python3
"""
OpenAI Assistant Export Script

This script retrieves complete assistant configuration including:
- Assistant details (model, temperature, tools, function schemas)
- Vector store details and associated files
- All tool resources and configurations

Usage:
    python export_assistant.py

Requirements:
    - .env file in project root with OPENAI_API_KEY
    - python-dotenv package
"""

import os
import json
import sys
import argparse
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI


# Configuration
ASSISTANT_ID = "asst_49u4HKGefgKxQwtNo87x4UnA"
VECTOR_STORE_ID = "vs_692b699176c481919d2df4d95a0dfa44"


def load_api_key() -> str:
    """
    Load OPENAI_API_KEY using python-dotenv.
    
    The .env file will override any existing OPENAI_API_KEY environment variable.
    This ensures the .env file is the source of truth for this session.
    
    Note: python-dotenv automatically ignores:
    - Lines starting with # (comments)
    - Empty lines
    - Whitespace-only lines
    """
    # Get project root (assuming script is in learning-path/W07/automation)
    script_path = Path(__file__)
    project_root = script_path.parent.parent.parent.parent
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


def list_assistants(client: OpenAI) -> None:
    """List all assistants for the user to find the correct ID."""
    print("📋 Listing all assistants...")
    try:
        assistants = client.beta.assistants.list()
        if not assistants.data:
            print("   No assistants found.")
            return
        
        print(f"   Found {len(assistants.data)} assistant(s):\n")
        for i, assistant in enumerate(assistants.data, 1):
            print(f"   {i}. {assistant.name or 'Unnamed'}")
            print(f"      ID: {assistant.id}")
            print(f"      Model: {assistant.model}")
            print(f"      Created: {assistant.created_at}")
            print()
    except Exception as e:
        print(f"   ❌ Error listing assistants: {e}")


def step1_retrieve_assistant(client: OpenAI, assistant_id: str) -> Dict[str, Any]:
    """
    STEP 1: Retrieve complete assistant configuration.
    
    Returns full JSON including:
    - tool_resources with all vector stores
    - exact file IDs inside the vector store
    - full function schema
    - model, temperature, top-p, response_format
    - code interpreter settings
    - all configurations
    """
    print("📋 STEP 1: Retrieving assistant details...")
    print(f"   Assistant ID: {assistant_id}")
    
    assistant = client.beta.assistants.retrieve(assistant_id)
    # Convert to dict for JSON serialization
    assistant_data = assistant.model_dump()
    
    print("✅ Assistant retrieved successfully")
    print(f"   Model: {assistant_data.get('model', 'N/A')}")
    print(f"   Temperature: {assistant_data.get('temperature', 'N/A')}")
    print(f"   Top-p: {assistant_data.get('top_p', 'N/A')}")
    print(f"   Response Format: {assistant_data.get('response_format', 'N/A')}")
    
    # Check for tools
    tools = assistant_data.get('tools', [])
    print(f"   Tools: {len(tools)} tool(s) configured")
    for i, tool in enumerate(tools, 1):
        tool_type = tool.get('type', 'unknown')
        if tool_type == 'function':
            func_name = tool.get('function', {}).get('name', 'unknown')
            print(f"      {i}. Function: {func_name}")
        else:
            print(f"      {i}. {tool_type}")
    
    # Check for tool_resources (vector stores)
    tool_resources = assistant_data.get('tool_resources', {})
    if tool_resources:
        file_search = tool_resources.get('file_search', {})
        vector_store_ids = file_search.get('vector_store_ids', [])
        if vector_store_ids:
            print(f"   Vector Stores: {len(vector_store_ids)} store(s)")
            for vs_id in vector_store_ids:
                print(f"      - {vs_id}")
    
    return assistant_data


def step2_retrieve_vector_store(client: OpenAI, vector_store_id: str) -> Dict[str, Any]:
    """
    STEP 2: Retrieve vector store details.
    
    Returns vector store configuration and metadata.
    Uses direct API call since vector_stores is not in the SDK beta namespace.
    """
    print(f"\n📦 STEP 2: Retrieving vector store details...")
    print(f"   Vector Store ID: {vector_store_id}")
    
    # Use direct API call since vector_stores is not available in SDK
    api_key = client.api_key
    url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v2"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    vector_store_data = response.json()
    
    print("✅ Vector store retrieved successfully")
    print(f"   Name: {vector_store_data.get('name', 'N/A')}")
    print(f"   Status: {vector_store_data.get('status', 'N/A')}")
    file_counts = vector_store_data.get('file_counts', {})
    total_files = file_counts.get('in_progress', 0) + file_counts.get('completed', 0)
    print(f"   File Count: {total_files}")
    
    return vector_store_data


def step2_retrieve_vector_store_files(client: OpenAI, vector_store_id: str) -> Dict[str, Any]:
    """
    STEP 2 (continued): Retrieve files inside the vector store.
    
    Returns list of files with IDs, filenames, and metadata.
    Uses direct API call since vector_stores is not in the SDK beta namespace.
    """
    print(f"\n📁 STEP 2 (continued): Retrieving files in vector store...")
    
    # Use direct API call since vector_stores is not available in SDK
    api_key = client.api_key
    url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}/files"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v2"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files_data = response.json()
    
    files = files_data.get('data', [])
    print(f"✅ Retrieved {len(files)} file(s)")
    
    for i, file_info in enumerate(files, 1):
        file_id = file_info.get('id', 'N/A')
        # Get filename from the file object if available
        file_obj = file_info.get('file', {})
        filename = file_obj.get('filename', 'N/A') if isinstance(file_obj, dict) else 'N/A'
        bytes_size = file_obj.get('bytes', 0) if isinstance(file_obj, dict) else 0
        status = file_info.get('status', 'N/A')
        print(f"   {i}. {filename}")
        print(f"      ID: {file_id}")
        print(f"      Size: {bytes_size:,} bytes")
        print(f"      Status: {status}")
    
    return files_data


def save_json(data: Dict[str, Any], filename: str, output_dir: Path) -> Path:
    """Save JSON data to file with pretty formatting."""
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to: {output_path}")
    return output_path


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Export OpenAI Assistant configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python export_assistant.py
  python export_assistant.py --assistant-id asst_xxxxx
  python export_assistant.py --list-assistants
        """
    )
    parser.add_argument(
        "--assistant-id",
        type=str,
        default=ASSISTANT_ID,
        help=f"Assistant ID to export (default: {ASSISTANT_ID})"
    )
    parser.add_argument(
        "--vector-store-id",
        type=str,
        default=VECTOR_STORE_ID,
        help=f"Vector Store ID (default: {VECTOR_STORE_ID})"
    )
    parser.add_argument(
        "--list-assistants",
        action="store_true",
        help="List all assistants and exit"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("OpenAI Assistant Export Script")
    print("=" * 70)
    print()
    
    # Load API key
    try:
        api_key = load_api_key()
        print("✅ API key loaded from .env file")
    except Exception as e:
        print(f"❌ Error loading API key: {e}")
        sys.exit(1)
    
    # Initialize OpenAI client
    client = get_client(api_key)
    
    # List assistants if requested
    if args.list_assistants:
        list_assistants(client)
        sys.exit(0)
    
    # Create output directory
    script_dir = Path(__file__).parent
    output_dir = script_dir / "assistant_export"
    output_dir.mkdir(exist_ok=True)
    print(f"📂 Output directory: {output_dir}\n")
    
    try:
        # STEP 1: Retrieve assistant
        assistant_data = step1_retrieve_assistant(client, args.assistant_id)
        assistant_file = save_json(
            assistant_data,
            "assistant_export.json",
            output_dir
        )
        
        # STEP 2: Retrieve vector store details (if vector store ID is provided)
        vector_store_id = args.vector_store_id
        if vector_store_id:
            vector_store_data = step2_retrieve_vector_store(client, vector_store_id)
            save_json(
                vector_store_data,
                "vector_store_details.json",
                output_dir
            )
            
            # STEP 2 (continued): Retrieve vector store files
            vector_store_files = step2_retrieve_vector_store_files(client, vector_store_id)
        else:
            # Try to get vector store ID from assistant data
            tool_resources = assistant_data.get('tool_resources', {})
            file_search = tool_resources.get('file_search', {})
            vector_store_ids = file_search.get('vector_store_ids', [])
            
            if vector_store_ids:
                vector_store_id = vector_store_ids[0]
                print(f"\n📦 Using vector store from assistant: {vector_store_id}")
                vector_store_data = step2_retrieve_vector_store(client, vector_store_id)
                save_json(
                    vector_store_data,
                    "vector_store_details.json",
                    output_dir
                )
                
                vector_store_files = step2_retrieve_vector_store_files(client, vector_store_id)
            else:
                print("\n⚠️  No vector store found in assistant configuration")
                vector_store_files = {"data": []}
                vector_store_id = None
        save_json(
            vector_store_files,
            "vector_store_files.json",
            output_dir
        )
        
        # Create a summary document
        summary = {
            "export_timestamp": assistant_data.get('created_at', 'N/A'),
            "assistant_id": args.assistant_id,
            "assistant_name": assistant_data.get('name', 'N/A'),
            "model": assistant_data.get('model', 'N/A'),
            "temperature": assistant_data.get('temperature', 'N/A'),
            "top_p": assistant_data.get('top_p', 'N/A'),
            "response_format": assistant_data.get('response_format', 'N/A'),
            "tools_count": len(assistant_data.get('tools', [])),
            "vector_store_id": vector_store_id or "N/A",
            "files_count": len(vector_store_files.get('data', [])),
            "export_files": {
                "assistant": "assistant_export.json",
                "vector_store": "vector_store_details.json",
                "vector_store_files": "vector_store_files.json"
            },
            "recreate_command": (
                "curl https://api.openai.com/v1/assistants \\\n"
                "  -H \"Authorization: Bearer $OPENAI_API_KEY\" \\\n"
                "  -H \"Content-Type: application/json\" \\\n"
                "  -d @assistant_export.json"
            )
        }
        
        save_json(summary, "export_summary.json", output_dir)
        
        print("\n" + "=" * 70)
        print("✅ Export completed successfully!")
        print("=" * 70)
        print(f"\n📋 Summary:")
        print(f"   - Assistant configuration: assistant_export.json")
        print(f"   - Vector store details: vector_store_details.json")
        print(f"   - Vector store files: vector_store_files.json")
        print(f"   - Export summary: export_summary.json")
        print(f"\n💡 To recreate this assistant, use the command in export_summary.json")
        print(f"   or use the assistant_export.json file with the OpenAI API.")
        
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

