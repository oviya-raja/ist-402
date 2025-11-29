# OpenAI Agent Builder - Setup Guide
## Job Fitment Analysis Agent

This guide provides step-by-step instructions for setting up the Job Fitment Analysis Agent in OpenAI Agent Builder.

---

## Prerequisites

1. **OpenAI Account** with access to Agent Builder
   - Sign up at: https://platform.openai.com
   - Ensure you have API access or Agent Builder access

2. **Knowledge Base Files Ready**
   - All 10 knowledge base files in `knowledge-base/` folder
   - Files should be in .txt format

3. **System Prompt Ready**
   - System prompt in `system-prompt.txt`

---

## Step-by-Step Setup

### STEP 1: Access OpenAI Platform

1. Go to: https://platform.openai.com
2. Log in with your OpenAI account
3. Navigate to **Assistants** or **Agent Builder** section
4. 📸 **TAKE SCREENSHOT:** Platform dashboard

---

### STEP 2: Create New Assistant/Agent

1. Click **"Create"** or **"New Assistant"** button
2. Choose **"Assistant"** or **"Agent"** type
3. 📸 **TAKE SCREENSHOT:** Agent creation screen

---

### STEP 3: Configure Basic Settings

1. **Agent Name:** 
   ```
   Job Fitment Analysis Agent
   ```

2. **Description:**
   ```
   Helps final-year students and recent graduates analyze job fitment, 
   identify skill gaps, and create personalized job search strategies. 
   Reduces job search stress by providing focused, actionable guidance.
   ```

3. **Model Selection:**
   - Select: **GPT-4o** (recommended) or **GPT-4 Turbo**
   - Reason: Best performance for complex analysis tasks
   - 📸 **TAKE SCREENSHOT:** Model selection

---

### STEP 4: Configure System Instructions

1. Click on **"Instructions"** or **"System Prompt"** section
2. Copy the entire content from `system-prompt.txt`
3. Paste into the instructions field
4. Review for accuracy
5. 📸 **TAKE SCREENSHOT:** System instructions configuration

**System Prompt Location:** `deliverables/1-functional-agent/system-prompt.txt`

---

### STEP 5: Enable File Search (Retrieval) Tool

1. Navigate to **"Tools"** or **"Capabilities"** section
2. Enable **"File Search"** or **"Retrieval"** tool
   - This is CRITICAL - this is your primary tool
3. 📸 **TAKE SCREENSHOT:** Tools configuration showing File Search enabled

---

### STEP 6: Upload Knowledge Base Files

1. Navigate to **"Files"** or **"Knowledge Base"** section
2. Click **"Upload File"** or **"Add File"**
3. Upload ALL 10 knowledge base files:

   **From `knowledge-base/01-student-profiles/`:**
   - `profile-template.txt`
   - `skills-taxonomy.txt`
   - `experience-levels.txt`

   **From `knowledge-base/02-job-analysis/`:**
   - `job-posting-structure.txt`

   **From `knowledge-base/03-company-info/`:**
   - `target-companies.txt`

   **From `knowledge-base/04-fitment-analysis/`:**
   - `calculation-methodology.txt`
   - `interpretation-guide.txt`

   **From `knowledge-base/05-skill-gaps/`:**
   - `gap-identification.txt`
   - `learning-resources.txt`

   **From `knowledge-base/06-use-case-examples/`:**
   - `use-case-1-example.txt`

4. Wait for files to process (may take a few minutes)
5. Verify all files show as "Processed" or "Ready"
6. 📸 **TAKE SCREENSHOT:** File upload interface
7. 📸 **TAKE SCREENSHOT:** Uploaded files list showing all 10 files

---

### STEP 7: Configure Memory Settings (Optional)

1. Navigate to **"Memory"** or **"Context"** settings
2. Enable conversation memory (if available)
3. Set context window preferences
4. 📸 **TAKE SCREENSHOT:** Memory/context settings

---

### STEP 8: Save and Verify Configuration

1. Click **"Save"** or **"Create"** to save the agent
2. Review all settings:
   - ✅ Name: Job Fitment Analysis Agent
   - ✅ Model: GPT-4o
   - ✅ System prompt: Complete
   - ✅ File Search: Enabled
   - ✅ Knowledge base: 10 files uploaded
   - ✅ Memory: Configured
3. 📸 **TAKE SCREENSHOT:** Complete agent configuration overview
4. Note the **Assistant ID** or **Agent ID** for documentation

---

### STEP 9: Test Basic Functionality

1. Open the **"Playground"** or **"Test"** interface
2. Test Use Case 1 with this input:

```
I'm a Computer Science student graduating in May 2025. 
I have experience with Python, Java, AWS, and SQL. 
I'm looking for software engineering roles at Cisco and Google. 
I prefer remote work and entry-level positions.

Priority 1:
- Cisco
- Google
```

3. Verify agent:
   - ✅ Responds appropriately
   - ✅ References knowledge base
   - ✅ Provides fitment analysis
   - ✅ Uses supportive, student-friendly tone
   - ✅ Includes mental health benefits messaging
4. 📸 **TAKE SCREENSHOT:** Test conversation

---

## Configuration Checklist

Before proceeding to testing, verify:

- [ ] Agent name set correctly
- [ ] Model selected (GPT-4o)
- [ ] System prompt complete and accurate
- [ ] File Search (Retrieval) tool enabled
- [ ] All 10 knowledge base files uploaded and processed
- [ ] Memory settings configured
- [ ] Agent saved successfully
- [ ] Assistant/Agent ID noted
- [ ] Basic test completed successfully

---

## Screenshots Required

For Deliverable 4 (Screenshots), ensure you capture:

1. ✅ Platform dashboard
2. ✅ Agent creation screen
3. ✅ System instructions configuration
4. ✅ Model selection
5. ✅ File upload interface
6. ✅ Uploaded files list (all 10 files visible)
7. ✅ Tools configuration panel (File Search enabled)
8. ✅ Memory/context settings
9. ✅ Complete agent configuration overview
10. ✅ Test conversation (Use Case 1)

---

## Troubleshooting

### Issue: Files not processing
**Solution:** 
- Wait a few minutes
- Check file format (should be .txt)
- Try re-uploading individual files
- Check file size limits

### Issue: File Search not working
**Solution:**
- Verify File Search tool is enabled
- Ensure files are fully processed
- Check that files are in supported format (.txt)
- Try a simple query to test retrieval

### Issue: Agent not following system prompt
**Solution:**
- Verify system prompt is complete (check for truncation)
- Ensure model is GPT-4o or GPT-4 Turbo
- Test with simple queries first
- Review prompt for clarity

---

## Next Steps

After setup is complete:

1. Proceed to **Phase 3: Testing & Refinement**
2. Test all 5 use cases
3. Document test results
4. Capture screenshots of all tests
5. Refine based on testing

---

**Setup Date:** ___________  
**Agent ID:** ___________  
**Status:** ✅ Ready for Testing



