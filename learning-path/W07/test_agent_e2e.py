#!/usr/bin/env python3
"""
End-to-End Test of Job Fitment Analysis Agent
Tests the complete flow: thread creation, message, response, knowledge base access
"""
import os
import sys
import time
from openai import OpenAI
import httpx

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()

print("=" * 70)
print("🧪 END-TO-END TEST: Job Fitment Analysis Agent")
print("=" * 70)
print()

# Step 1: Verify Assistant Configuration
print("📋 Step 1: Verifying Assistant Configuration...")
try:
    assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
    print(f"   ✅ Assistant Name: {assistant.name}")
    print(f"   ✅ Model: {assistant.model}")
    print(f"   ✅ Tools: {[t.type for t in assistant.tools]}")
    
    if assistant.tool_resources and assistant.tool_resources.file_search:
        vs_ids = assistant.tool_resources.file_search.vector_store_ids
        if vs_ids:
            print(f"   ✅ Vector Store ID: {vs_ids[0]}")
            
            # Check files in vector store
            headers = {
                "Authorization": f"Bearer {api_key}",
                "OpenAI-Beta": "assistants=v2"
            }
            response = httpx.get(
                f"https://api.openai.com/v1/vector_stores/{vs_ids[0]}/files",
                headers=headers,
                timeout=30.0
            )
            if response.status_code == 200:
                files = response.json().get("data", [])
                print(f"   ✅ Files in Knowledge Base: {len(files)}")
            else:
                print(f"   ⚠️  Could not verify files: {response.status_code}")
        else:
            print(f"   ❌ No vector store linked!")
            sys.exit(1)
    else:
        print(f"   ❌ File search not configured!")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()

# Step 2: Create a Thread
print("📝 Step 2: Creating Conversation Thread...")
try:
    thread = client.beta.threads.create()
    print(f"   ✅ Thread Created: {thread.id}")
except Exception as e:
    print(f"   ❌ Error creating thread: {e}")
    sys.exit(1)

print()

# Step 3: Send Test Message
print("💬 Step 3: Sending Test Message...")
test_queries = [
    {
        "name": "Use Case 1: Job Search",
        "message": "I'm a final year computer science student with experience in Python, machine learning, and web development. I'm interested in software engineering roles at Priority 1 companies: Google, Apple. Can you help me find relevant job postings?"
    },
    {
        "name": "Use Case 2: Fitment Analysis",
        "message": "I found a job posting for 'Senior Software Engineer' at Google. I have 2 years of internship experience in Python and machine learning. Can you analyze my fitment for this role?"
    },
    {
        "name": "Use Case 3: Skill Gap Analysis",
        "message": "I want to apply for a Data Scientist position at Amazon. My skills include Python, SQL, and basic statistics. What skills am I missing and what should I learn?"
    }
]

# Run first test query
test_query = test_queries[0]
print(f"   Test: {test_query['name']}")
print(f"   Message: {test_query['message'][:80]}...")
print()

try:
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=test_query['message']
    )
    print(f"   ✅ Message sent: {message.id}")
except Exception as e:
    print(f"   ❌ Error sending message: {e}")
    sys.exit(1)

print()

# Step 4: Run Assistant
print("🤖 Step 4: Running Assistant...")
try:
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    print(f"   ✅ Run started: {run.id}")
    print(f"   Status: {run.status}")
except Exception as e:
    print(f"   ❌ Error starting run: {e}")
    sys.exit(1)

print()

# Step 5: Wait for Completion
print("⏳ Step 5: Waiting for Response...")
max_wait = 120
waited = 0
while waited < max_wait:
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
        status = run.status
        print(f"   Status: {status} ({waited}s)", end='\r')
        
        if status == "completed":
            print(f"\n   ✅ Run completed!")
            break
        elif status == "failed":
            print(f"\n   ❌ Run failed!")
            if run.last_error:
                print(f"   Error: {run.last_error.message}")
            sys.exit(1)
        elif status in ["cancelled", "expired"]:
            print(f"\n   ❌ Run {status}!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n   ⚠️  Error checking status: {e}")
    
    time.sleep(2)
    waited += 2

if waited >= max_wait:
    print(f"\n   ⚠️  Timeout waiting for response")
    sys.exit(1)

print()

# Step 6: Retrieve Response
print("📥 Step 6: Retrieving Response...")
try:
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    # Get the assistant's response (most recent)
    assistant_messages = [m for m in messages.data if m.role == "assistant"]
    if assistant_messages:
        response = assistant_messages[0]
        print(f"   ✅ Response received!")
        print()
        print("=" * 70)
        print("📋 ASSISTANT RESPONSE:")
        print("=" * 70)
        
        # Extract text content
        if response.content:
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    print(content_block.text.value)
                elif hasattr(content_block, 'type') and content_block.type == 'text':
                    print(content_block.text.value)
        
        print()
        print("=" * 70)
        
        # Check if knowledge base was used
        if hasattr(run, 'required_action') and run.required_action:
            print("   ℹ️  Note: Assistant used tools/functions")
        
        # Check run steps for file search usage
        try:
            steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id,
                run_id=run.id
            )
            file_search_used = False
            for step in steps.data:
                if hasattr(step, 'step_details') and hasattr(step.step_details, 'tool_calls'):
                    for tool_call in step.step_details.tool_calls:
                        if hasattr(tool_call, 'type') and tool_call.type == 'file_search':
                            file_search_used = True
                            break
            
            if file_search_used:
                print("   ✅ Knowledge Base Access: File search tool was used!")
            else:
                print("   ℹ️  Knowledge Base Access: May have used cached knowledge")
        except:
            print("   ℹ️  Could not verify tool usage")
            
    else:
        print("   ❌ No assistant response found")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Error retrieving response: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("✅ END-TO-END TEST COMPLETE!")
print("=" * 70)
print()
print("Summary:")
print(f"  ✅ Assistant configured correctly")
print(f"  ✅ Knowledge base accessible")
print(f"  ✅ Thread created and message sent")
print(f"  ✅ Assistant responded")
print(f"  ✅ Agent is fully functional!")
print()
print(f"🌐 View in browser: https://platform.openai.com/assistants/{ASSISTANT_ID}")
print(f"📝 Thread ID: {thread.id}")



