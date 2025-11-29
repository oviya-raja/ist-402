#!/usr/bin/env python3
"""
Test individual use case and save detailed results
Usage: python3 test_use_case_individual.py <UC1|UC2|UC3|UC4|UC5>
"""
import os
import sys
import time
import json
from datetime import datetime
from openai import OpenAI

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id

# Load environment variables
load_env()
api_key = get_api_key()
client = OpenAI(api_key=api_key)
ASSISTANT_ID = get_assistant_id()

# All 5 use cases
USE_CASES = {
    "UC1": {
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
    "UC2": {
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
    "UC3": {
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
    "UC4": {
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
- Experience: 2+ years

My profile: 2 years experience, Python, Java, some iOS projects. Which one fits me better?""",
        "expected_keywords": ["compare", "fit", "better", "Google", "Apple"]
    },
    "UC5": {
        "id": "UC5",
        "name": "Use Case 5: Generate Personalized Job Search Strategy",
        "message": """I'm a final year student graduating in 6 months. I want to work at:
- Priority 1: Google, Apple
- Priority 2: Amazon, Microsoft, Tesla

My skills: Python, Java, React, SQL
Experience: 1 internship, 2 projects

Can you create a 6-month strategy to land a job at these companies?""",
        "expected_keywords": ["strategy", "plan", "priority", "steps", "timeline"]
    }
}

def test_use_case(uc_id):
    """Test a single use case and return detailed results"""
    if uc_id not in USE_CASES:
        print(f"❌ Invalid use case ID: {uc_id}")
        print(f"Available: {', '.join(USE_CASES.keys())}")
        sys.exit(1)
    
    uc = USE_CASES[uc_id]
    print(f"\n{'='*70}")
    print(f"🧪 {uc['name']}")
    print(f"{'='*70}\n")
    print(f"📝 Query: {uc['message'][:100]}...")
    print(f"\n⏳ Testing...")
    
    # Create thread
    thread = client.beta.threads.create()
    
    # Send message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=uc['message']
    )
    
    # Create run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    
    # Wait for completion
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    if run.status != 'completed':
        print(f"❌ Run failed with status: {run.status}")
        if hasattr(run, 'last_error'):
            print(f"   Error: {run.last_error}")
        return None
    
    # Get messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_message = messages.data[0]
    response_text = assistant_message.content[0].text.value
    
    # Check for knowledge base usage
    steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )
    
    knowledge_base_used = False
    for step in steps.data:
        if step.type == 'tool_calls':
            for tool_call in step.step_details.tool_calls:
                if tool_call.type == 'file_search':
                    knowledge_base_used = True
                    break
    
    # Check keywords
    found_keywords = []
    for keyword in uc['expected_keywords']:
        if keyword.lower() in response_text.lower():
            found_keywords.append(keyword)
    
    # Results
    result = {
        "use_case_id": uc_id,
        "use_case_name": uc['name'],
        "query": uc['message'],
        "response": response_text,
        "response_length": len(response_text),
        "knowledge_base_used": knowledge_base_used,
        "expected_keywords": uc['expected_keywords'],
        "found_keywords": found_keywords,
        "keywords_found_count": len(found_keywords),
        "keywords_total": len(uc['expected_keywords']),
        "thread_id": thread.id,
        "run_id": run.id,
        "timestamp": datetime.now().isoformat(),
        "status": "passed" if len(found_keywords) >= len(uc['expected_keywords']) * 0.6 else "partial"
    }
    
    print(f"\n✅ {uc_id} {'PASSED' if result['status'] == 'passed' else 'PARTIAL'}")
    print(f"   Response length: {result['response_length']} chars")
    print(f"   Knowledge base used: {'✅' if knowledge_base_used else '⚠️'}")
    print(f"   Keywords found: {result['keywords_found_count']}/{result['keywords_total']}")
    if found_keywords:
        print(f"      Found: {', '.join(found_keywords)}")
    print(f"\n   Response preview:")
    print(f"   {response_text[:200]}...")
    print(f"\n   Thread ID: {thread.id}")
    print(f"   Run ID: {run.id}")
    
    # Save to file
    output_dir = Path(__file__).parent.parent / "test-results"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{uc_id}_test_result.json"
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return result

if __name__ == "__main__":
    from pathlib import Path
    
    if len(sys.argv) < 2:
        print("Usage: python3 test_use_case_individual.py <UC1|UC2|UC3|UC4|UC5>")
        sys.exit(1)
    
    uc_id = sys.argv[1].upper()
    test_use_case(uc_id)

