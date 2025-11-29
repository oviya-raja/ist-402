# Agent Build Checklist
## Job Fitment Analysis Agent - Step-by-Step Build Guide

**Status:** Ready to Build  
**Estimated Time:** 30-45 minutes  
**Prerequisites:** OpenAI Platform account, all files prepared

---

## ✅ PRE-BUILD CHECKLIST

Before starting, verify you have:

- [x] System prompt ready (`system-prompt.txt`)
- [x] 10 knowledge base files ready (`knowledge-base/` folder)
- [x] Test cases ready (`test-cases.txt`)
- [x] Setup guide ready (`AGENT_SETUP_GUIDE.md`)
- [x] Verification checklist ready (`VERIFICATION_CHECKLIST.md`)

---

## 🚀 BUILD STEPS

### Step 1: Access OpenAI Platform (2 min)

- [ ] Go to: https://platform.openai.com
- [ ] Log in with your OpenAI account
- [ ] Navigate to "Assistants" or "Agent Builder" section
- [ ] 📸 **SCREENSHOT:** Platform dashboard

**Note:** If you don't see "Assistants" or "Agent Builder", you may need to enable it in your account settings.

---

### Step 2: Create New Agent (3 min)

- [ ] Click "Create" or "New Assistant" button
- [ ] 📸 **SCREENSHOT:** Agent creation screen
- [ ] Set agent name: **"Job Fitment Analysis Agent"**
- [ ] (Optional) Add description: "Helps final-year students analyze job fitment and identify skill gaps"

---

### Step 3: Configure System Prompt (5 min)

- [ ] Open `deliverables/1-functional-agent/system-prompt.txt`
- [ ] Copy entire content (137 lines)
- [ ] Paste into "Instructions" or "System Prompt" field
- [ ] 📸 **SCREENSHOT:** System instructions configuration
- [ ] Verify all content pasted correctly

**Key Sections in Prompt:**
- Core purpose and mental health focus
- 5 use cases definition
- Input format (Priority 1, 2, 3)
- Processing steps
- Response format guidelines
- Personality and tone
- Error handling

---

### Step 4: Select Model (1 min)

- [ ] Select model: **GPT-4o** (recommended) or GPT-4 Turbo
- [ ] 📸 **SCREENSHOT:** Model selection
- [ ] Verify model is selected

**Why GPT-4o:**
- Best performance for complex reasoning
- Handles knowledge base retrieval well
- Good at following detailed instructions

---

### Step 5: Enable File Search Tool (2 min)

- [ ] Find "Tools" or "Capabilities" section
- [ ] Enable "File Search" or "Retrieval" tool
- [ ] 📸 **SCREENSHOT:** Tools configuration panel
- [ ] Verify File Search is enabled

**This is the PRIMARY tool** - required for knowledge base access.

---

### Step 6: Upload Knowledge Base Files (10 min)

**Files to Upload (10 files):**

1. `knowledge-base/01-student-profiles/profile-template.txt`
2. `knowledge-base/01-student-profiles/skills-taxonomy.txt`
3. `knowledge-base/01-student-profiles/experience-levels.txt`
4. `knowledge-base/02-job-analysis/job-posting-structure.txt`
5. `knowledge-base/03-company-info/target-companies.txt`
6. `knowledge-base/04-fitment-analysis/calculation-methodology.txt`
7. `knowledge-base/04-fitment-analysis/interpretation-guide.txt`
8. `knowledge-base/05-skill-gaps/gap-identification.txt`
9. `knowledge-base/05-skill-gaps/learning-resources.txt`
10. `knowledge-base/06-use-case-examples/use-case-1-example.txt`

**Upload Process:**
- [ ] Click "Upload Files" or "Add Files" button
- [ ] Select all 10 files (or upload one by one)
- [ ] 📸 **SCREENSHOT:** File upload interface
- [ ] Wait for files to process (may take 1-2 minutes)
- [ ] 📸 **SCREENSHOT:** Uploaded files list
- [ ] Verify all 10 files show as "Processed" or "Ready"

**Troubleshooting:**
- If files don't process, try uploading one at a time
- Ensure files are .txt format
- Check file sizes (should be < 512MB each)

---

### Step 7: Configure Additional Settings (3 min)

**Memory/Context:**
- [ ] Review conversation memory settings (default is usually fine)
- [ ] Set context window if available (default recommended)
- [ ] 📸 **SCREENSHOT:** Memory/context settings (if visible)

**Temperature (Optional):**
- [ ] Set temperature to 0.7-0.8 (for balanced creativity/consistency)
- [ ] Or leave default

---

### Step 8: Save Agent Configuration (2 min)

- [ ] Click "Save" or "Create" button
- [ ] Wait for agent to be created
- [ ] 📸 **SCREENSHOT:** Complete agent configuration overview
- [ ] Note the Agent/Assistant ID (for documentation)
- [ ] Copy agent URL or ID for reference

**Agent ID Format:** Usually looks like `asst_xxxxxxxxxxxxx`

---

### Step 9: Initial Test (5 min)

**Quick Test:**
- [ ] Open agent playground or chat interface
- [ ] Test with simple query:
  ```
  Priority 1:
  - Cisco
  - Google
  
  My profile: Computer Science student, Python, Java, AWS, 2 internships
  ```
- [ ] Verify agent responds appropriately
- [ ] Check if knowledge base is accessed (should reference files)
- [ ] 📸 **SCREENSHOT:** First successful test interaction

**Expected Behavior:**
- Agent should acknowledge input
- Should reference knowledge base content
- Should provide fitment analysis
- Should be supportive and clear

---

### Step 10: Verify Configuration (5 min)

**Run Verification Checklist:**
- [ ] Open `VERIFICATION_CHECKLIST.md`
- [ ] Check each item:
  - [ ] System prompt is complete
  - [ ] Model is GPT-4o (or GPT-4 Turbo)
  - [ ] File Search tool is enabled
  - [ ] All 10 knowledge base files uploaded
  - [ ] Files show as processed
  - [ ] Agent responds to test queries
  - [ ] Knowledge base is being accessed

**If any item fails:**
- Review setup guide
- Check troubleshooting section
- Re-upload files if needed
- Verify system prompt is complete

---

## ✅ POST-BUILD CHECKLIST

After building, verify:

- [ ] Agent is accessible and functional
- [ ] All 10 knowledge base files are uploaded and processed
- [ ] File Search tool is enabled and working
- [ ] System prompt is complete and correct
- [ ] Test query returns appropriate response
- [ ] Agent references knowledge base content
- [ ] Screenshots captured (at least 5-7 key screenshots)
- [ ] Agent ID/URL saved for documentation

---

## 📸 REQUIRED SCREENSHOTS

Capture these screenshots during build:

1. ✅ Platform dashboard
2. ✅ Agent creation screen
3. ✅ System instructions configuration
4. ✅ Model selection
5. ✅ File upload interface
6. ✅ Uploaded files list
7. ✅ Tools configuration panel
8. ✅ Complete agent configuration overview
9. ✅ First successful test interaction

**Total:** 9 screenshots minimum

---

## 🐛 TROUBLESHOOTING

### Files Won't Upload
- **Solution:** Try uploading one file at a time
- **Solution:** Check file format (must be .txt)
- **Solution:** Verify file size (< 512MB)

### File Search Not Working
- **Solution:** Ensure File Search tool is enabled
- **Solution:** Wait for files to finish processing (may take 2-3 minutes)
- **Solution:** Re-upload files if needed

### Agent Not Responding Correctly
- **Solution:** Verify system prompt is complete (check for truncation)
- **Solution:** Test with simpler query first
- **Solution:** Check if knowledge base files are processed

### Knowledge Base Not Accessed
- **Solution:** Verify File Search tool is enabled
- **Solution:** Check file upload status (should be "Processed")
- **Solution:** Try re-uploading files

---

## 📝 NOTES SECTION

**Agent ID:** _________________________

**Agent URL:** _________________________

**Build Date:** _________________________

**Issues Encountered:**
- 
- 
- 

**Solutions Applied:**
- 
- 
- 

---

## 🎯 NEXT STEPS

After successful build:

1. **Run Test Cases** (1-2 hours)
   - Use `test-cases.txt`
   - Test all 5 use cases
   - Capture screenshots

2. **Complete Verification** (30 min)
   - Run full verification checklist
   - Document any issues

3. **Capture Screenshots** (1 hour)
   - All required screenshots
   - Test case screenshots
   - Workflow screenshots

4. **Document Workflow** (1 hour)
   - Insert diagrams
   - Complete workflow documentation

5. **Final Report** (3-4 hours)
   - Fill report template
   - Include all screenshots
   - Export to PDF

---

**Status:** Ready to Build  
**Last Updated:** 2025-11-29  
**Estimated Total Build Time:** 30-45 minutes

