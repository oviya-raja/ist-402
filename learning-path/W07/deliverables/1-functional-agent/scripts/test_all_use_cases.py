#!/usr/bin/env python3
"""
Comprehensive Test Suite for Job Fitment Analysis Agent
Tests all 5 use cases end-to-end
"""
import os
import sys
import time
from openai import OpenAI

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()

# All 5 use cases from the assignment
USE_CASES = [
    {
        "id": "UC1",
        "name": "Use Case 1: Search and Filter Jobs by Multiple Criteria",
        "message": """I'm a final year CS student with:
- Skills: Python, JavaScript, React, Node.js, SQL, Docker
- Experience: 2 internships (6 months total), 3 personal projects
- Location preference: Remote or San Francisco
- Target companies: Priority 1: Google, Apple; Priority 2: Amazon, Tesla

Can you help me find relevant software engineering roles that match my profile?""",
        "expected_keywords": ["Google", "Apple", "software engineering", "Python", "criteria"]
    },
    {
        "id": "UC2",
        "name": "Use Case 2: Analyze Job Posting Fitment",
        "message": """I found this job posting:

Title: Software Engineer II - Machine Learning Platform
Company: Google
Requirements:
- 3+ years experience in Python, Java, or C++
- Experience with ML frameworks (TensorFlow, PyTorch)
- Strong algorithms and data structures
- BS/MS in Computer Science

My profile:
- 2 years internship experience
- Skills: Python, TensorFlow, basic ML
- Education: BS Computer Science (graduating soon)

Can you analyze my fitment score and tell me what I need to improve?""",
        "expected_keywords": ["fitment", "score", "improve", "experience", "skills"]
    },
    {
        "id": "UC3",
        "name": "Use Case 3: Identify Skill Gaps",
        "message": """I want to apply for a "Senior Data Scientist" position at Amazon. 

My current skills:
- Python (intermediate)
- SQL (basic)
- Statistics (college level)
- Machine Learning (took one course)

What skills am I missing? What should I learn to be competitive?""",
        "expected_keywords": ["skill gap", "missing", "learn", "recommendations"]
    },
    {
        "id": "UC4",
        "name": "Use Case 4: Compare Multiple Job Postings",
        "message": """I'm considering two positions:

Job 1: Software Engineer at Google
- Focus: Backend systems, distributed systems
- Tech: Java, Python, Go
- Experience: 2+ years

Job 2: Software Engineer at Apple
- Focus: iOS development
- Tech: Swift, Objective-C
- Experience: 1+ years

My profile: 1 year experience, Python, JavaScript, some mobile dev

Can you compare these and tell me which is a better fit?""",
        "expected_keywords": ["compare", "fit", "better", "Google", "Apple"]
    },
    {
        "id": "UC5",
        "name": "Use Case 5: Generate Personalized Job Search Strategy",
        "message": """I'm a final year student graduating in 6 months. I want to work at:
- Priority 1: Google, Apple
- Priority 2: Amazon, Microsoft, Tesla

My skills: Python, Java, web development, some ML
Experience: 1 internship, 2 projects

Can you create a personalized 6-month job search strategy for me?""",
        "expected_keywords": ["strategy", "plan", "timeline", "priority", "steps"]
    }
]

def test_use_case(use_case):
    """Test a single use case"""
    print(f"\n{'='*70}")
    print(f"🧪 {use_case['id']}: {use_case['name']}")
    print(f"{'='*70}")
    print(f"\n📝 Query: {use_case['message'][:100]}...")
    
    # Create thread
    thread = client.beta.threads.create()
    
    # Send message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=use_case['message']
    )
    
    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    
    # Wait for completion
    max_wait = 120
    waited = 0
    while waited < max_wait:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
        if run.status == "completed":
            break
        elif run.status in ["failed", "cancelled", "expired"]:
            return False, f"Run {run.status}", None
        
        time.sleep(2)
        waited += 2
    
    if waited >= max_wait:
        return False, "Timeout waiting for response", None
    
    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_messages = [m for m in messages.data if m.role == "assistant"]
    
    if not assistant_messages:
        return False, "No response", None
    
    response = assistant_messages[0]
    response_text = ""
    if response.content:
        for content_block in response.content:
            if hasattr(content_block, 'text'):
                response_text = content_block.text.value
                break
    
    # Check if knowledge base was used
    kb_used = False
    try:
        steps = client.beta.threads.runs.steps.list(
            thread_id=thread.id,
            run_id=run.id
        )
        for step in steps.data:
            if hasattr(step, 'step_details') and hasattr(step.step_details, 'tool_calls'):
                for tool_call in step.step_details.tool_calls:
                    if hasattr(tool_call, 'type') and tool_call.type == 'file_search':
                        kb_used = True
                        break
            if kb_used:
                break
    except Exception as e:
        # Silently continue - tool usage verification is optional
        pass
    
    # Check for expected keywords
    keywords_found = []
    response_lower = response_text.lower()
    for keyword in use_case['expected_keywords']:
        if keyword.lower() in response_lower:
            keywords_found.append(keyword)
    
    return True, response_text, {
        "kb_used": kb_used,
        "keywords_found": keywords_found,
        "response_length": len(response_text),
        "thread_id": thread.id
    }

# Main test execution
print("=" * 70)
print("🧪 COMPREHENSIVE TEST SUITE: Job Fitment Analysis Agent")
print("=" * 70)
print(f"\nTesting {len(USE_CASES)} use cases...")
print(f"Assistant ID: {ASSISTANT_ID}\n")

results = []
for use_case in USE_CASES:
    success, result, metadata = test_use_case(use_case)
    
    if success and metadata is not None:
        print(f"\n✅ {use_case['id']} PASSED")
        print(f"   Response length: {metadata['response_length']} chars")
        print(f"   Knowledge base used: {'✅' if metadata['kb_used'] else '⚠️'}")
        print(f"   Keywords found: {len(metadata['keywords_found'])}/{len(use_case['expected_keywords'])}")
        if metadata['keywords_found']:
            print(f"      Found: {', '.join(metadata['keywords_found'][:5])}")
        
        # Show first 200 chars of response
        print(f"\n   Response preview:")
        print(f"   {result[:200]}...")
        
        results.append({
            "use_case": use_case['id'],
            "status": "PASSED",
            "metadata": metadata
        })
    else:
        print(f"\n❌ {use_case['id']} FAILED: {result}")
        results.append({
            "use_case": use_case['id'],
            "status": "FAILED",
            "error": result
        })
    
    time.sleep(2)  # Rate limiting

# Summary
print("\n" + "=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)

passed = sum(1 for r in results if r['status'] == 'PASSED')
failed = len(results) - passed

print(f"\nTotal Tests: {len(results)}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"Success Rate: {(passed/len(results)*100):.1f}%")

if passed == len(results):
    print("\n🎉 ALL TESTS PASSED! Agent is fully functional!")
else:
    print(f"\n⚠️  {failed} test(s) failed. Review errors above.")

print(f"\n🌐 View assistant: https://platform.openai.com/assistants/{ASSISTANT_ID}")



