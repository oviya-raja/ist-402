#!/usr/bin/env python3
"""
Test Assistant Script

Quick script to test your assistant via API.

Usage:
    python3 test_assistant.py
"""

import os
import sys
import time
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
        raise ValueError("OPENAI_API_KEY not found in .env file")
    return api_key


def test_assistant(client: OpenAI, assistant_id: str, question: str) -> str:
    """Test assistant with a question."""
    print(f"🧪 Testing assistant: {assistant_id}")
    print(f"📝 Question: {question}\n")
    
    # Create thread
    thread = client.beta.threads.create()
    
    # Add message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )
    
    # Run assistant
    print("⏳ Running assistant...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    # Wait for completion
    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == 'in_progress':
            print("   ⏳ Processing...")
    
    # Get response
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_message = messages.data[0]
        if assistant_message.role == 'assistant':
            answer = assistant_message.content[0].text.value
            print("✅ Answer received:\n")
            print("=" * 70)
            print(answer)
            print("=" * 70)
            return answer
        else:
            print(f"❌ Unexpected message role: {assistant_message.role}")
            return ""
    else:
        print(f"❌ Run failed with status: {run.status}")
        if hasattr(run, 'last_error'):
            print(f"   Error: {run.last_error}")
        return ""


def main():
    """Main execution function."""
    ASSISTANT_ID = "asst_HhWz11KVfZgudaIxXlqXHLt2"
    
    print("=" * 70)
    print("Test Assistant - Student Query Response Agent")
    print("=" * 70)
    print()
    
    # Load API key
    try:
        api_key = load_api_key()
        print("✅ API key loaded\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Initialize client
    client = OpenAI(api_key=api_key)
    
    # Test questions
    test_questions = [
        "What are the course requirements?",
        "How do I submit assignments?",
        "What is the grading policy?",
        "When are office hours?",
        "What are the assignment deliverables?"
    ]
    
    print("📋 Test Questions:")
    for i, q in enumerate(test_questions, 1):
        print(f"   {i}. {q}")
    print()
    
    # Run tests
    results = []
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}/{len(test_questions)}")
        print('=' * 70)
        answer = test_assistant(client, ASSISTANT_ID, question)
        results.append({
            "question": question,
            "answer": answer,
            "status": "✅ Pass" if answer else "❌ Fail"
        })
        print()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['status']} - {result['question']}")
    
    passed = sum(1 for r in results if "✅" in r['status'])
    print(f"\n✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {len(results) - passed}/{len(results)}")


if __name__ == "__main__":
    main()

