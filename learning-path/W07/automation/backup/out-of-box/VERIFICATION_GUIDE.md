# Verification & Testing Guide

## ✅ Current Assistant Status

**Assistant ID:** `asst_HhWz11KVfZgudaIxXlqXHLt2`  
**Name:** Student Query Response Agent  
**Model:** gpt-4o  
**Tools:** File Search (enabled)  
**Vector Store:** `vs_692f102bf28881918bdb3c58aabb8ba6`  
**Knowledge Base:** 2 files uploaded

**View in UI:** https://platform.openai.com/assistants/asst_HhWz11KVfZgudaIxXlqXHLt2

---

## 🔍 How to Verify in OpenAI Dashboard

### Step 1: Access Agent Builder

1. **Go to:** https://platform.openai.com/agent-builder
2. **Login** with your OpenAI account
3. **Find your assistant:** "Student Query Response Agent"

### Step 2: Verify Configuration

**Check these sections:**

1. **Configuration Tab:**
   - ✅ Name: "Student Query Response Agent"
   - ✅ Model: gpt-4o
   - ✅ Description: Should be set
   - ✅ Instructions: Should contain the system prompt

2. **Tools Tab:**
   - ✅ File Search: **Enabled** (this is critical!)
   - ⬜ Code Interpreter: Optional (can enable if needed)
   - ⬜ Web Search: Optional (can enable if needed)

3. **Knowledge Tab:**
   - ✅ Vector Store: "Student Knowledge Base"
   - ✅ Files: Should show 2 files:
     - `course_faq.txt`
     - `assignment_guidelines.txt`
   - ✅ Status: Files should be "Processed" or "Completed"

### Step 3: Verify Vector Store

1. **Click on Vector Store** name
2. **Check:**
   - ✅ Name: "Student Knowledge Base"
   - ✅ Status: "completed"
   - ✅ File Count: 2 files
   - ✅ Files listed: Both files visible

---

## 🧪 How to Test the Assistant

### Method 1: Test in Agent Builder UI (Recommended)

1. **Go to:** Agent Builder → Your Assistant → **Test** tab
2. **Ask test questions:**
   ```
   What are the course requirements?
   ```
   ```
   How do I submit assignments?
   ```
   ```
   What is the grading policy?
   ```
   ```
   When are office hours?
   ```
   ```
   What are the assignment deliverables?
   ```

3. **Verify responses:**
   - ✅ Answers should reference the knowledge base
   - ✅ Answers should be accurate based on uploaded files
   - ✅ Agent should cite sources (if configured)
   - ✅ Agent should say "I don't know" for questions not in knowledge base

### Method 2: Test via Script

```bash
cd learning-path/W07/automation/out-of-box
source ../../../../.venv/bin/activate
python3 implement_assistant.py
# When prompted, type 'y' to test
```

### Method 3: Test via API (Advanced)

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create thread
thread = client.beta.threads.create()

# Add message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What are the course requirements?"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="asst_HhWz11KVfZgudaIxXlqXHLt2"
)

# Wait for completion
import time
while run.status in ['queued', 'in_progress']:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# Get response
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

---

## ✅ Verification Checklist

### Configuration Verification

- [ ] Assistant name is correct
- [ ] Model is gpt-4o
- [ ] Instructions are set
- [ ] File Search tool is enabled
- [ ] Vector store is attached
- [ ] Files are uploaded and processed

### Functionality Verification

- [ ] Assistant responds to questions
- [ ] Answers come from knowledge base
- [ ] Answers are accurate
- [ ] Agent handles questions not in knowledge base
- [ ] File Search tool is being used (check in UI)

### Testing Verification

- [ ] Tested with at least 5 different questions
- [ ] All questions answered correctly
- [ ] Edge cases handled (questions not in KB)
- [ ] Error handling works
- [ ] Response time is reasonable

---

## 📸 Screenshots to Capture

### Required Screenshots (for Rubric - 20 pts)

1. **Agent Configuration**
   - Location: Agent Builder → Configuration tab
   - Show: Name, Model, Description, Instructions

2. **Tools Setup**
   - Location: Agent Builder → Tools tab
   - Show: File Search enabled

3. **Knowledge Base**
   - Location: Agent Builder → Knowledge tab
   - Show: Vector store with files listed

4. **Instructions/Prompt**
   - Location: Agent Builder → Instructions section
   - Show: Full system prompt text

5. **Test Chat - Question 1**
   - Location: Agent Builder → Test tab
   - Show: Question and answer

6. **Test Chat - Question 2**
   - Location: Agent Builder → Test tab
   - Show: Different question and answer

7. **Deployment Evidence**
   - Location: Any view showing agent is active
   - Show: URL bar with platform.openai.com

---

## 🐛 Troubleshooting

### Issue: Assistant doesn't answer questions

**Check:**
- ✅ File Search tool is enabled
- ✅ Vector store is attached to assistant
- ✅ Files are processed (not "in_progress")
- ✅ Instructions are set correctly

**Fix:**
- Re-enable File Search tool
- Re-attach vector store
- Wait for files to finish processing

### Issue: Answers are incorrect

**Check:**
- ✅ Correct files uploaded
- ✅ Files contain relevant information
- ✅ Instructions guide agent correctly

**Fix:**
- Upload correct files
- Update instructions if needed

### Issue: Files not processing

**Check:**
- ✅ Files are valid format (PDF, TXT, DOCX)
- ✅ Files are not too large
- ✅ API key has proper permissions

**Fix:**
- Wait longer (can take 5-10 minutes)
- Re-upload files
- Check file formats

---

## 📊 Test Results Template

```
Test Date: [Date]
Assistant ID: asst_HhWz11KVfZgudaIxXlqXHLt2

Test Questions:
1. "What are the course requirements?"
   Result: ✅ Pass / ❌ Fail
   Response: [Brief summary]

2. "How do I submit assignments?"
   Result: ✅ Pass / ❌ Fail
   Response: [Brief summary]

3. "What is the grading policy?"
   Result: ✅ Pass / ❌ Fail
   Response: [Brief summary]

4. "When are office hours?"
   Result: ✅ Pass / ❌ Fail
   Response: [Brief summary]

5. "What is the capital of Mars?" (Edge case)
   Result: ✅ Pass / ❌ Fail
   Response: [Should say "I don't know" or similar]

Overall: ✅ All tests passed / ⚠️ Some issues
```

---

## 🎯 Success Criteria

Your assistant is ready for submission if:

- ✅ All verification checklist items are complete
- ✅ All test questions answered correctly
- ✅ Screenshots captured (5-7 screenshots)
- ✅ Agent works consistently
- ✅ Documentation complete

---

**Status:** ✅ Ready for verification and testing!

