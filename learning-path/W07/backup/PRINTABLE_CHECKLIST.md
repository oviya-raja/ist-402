# Printable Build Checklist
## Job Fitment Analysis Agent - Follow Along Checklist

**Print this page and check off each item as you complete it.**

---

## ✅ PRE-BUILD CHECKLIST

- [ ] Computer with internet
- [ ] Web browser open
- [ ] OpenAI account (or ready to create one)
- [ ] 30-45 minutes available
- [ ] All files ready (they are!)

---

## STEP 1: ACCESS OPENAI PLATFORM (2 min)

- [ ] Open web browser
- [ ] Go to: https://platform.openai.com
- [ ] Log in (or create account)
- [ ] Navigate to "Assistants" or "Agent Builder"
- [ ] 📸 **SCREENSHOT 1:** Platform dashboard

---

## STEP 2: CREATE NEW AGENT (3 min)

- [ ] Click "Create" or "New Assistant" button
- [ ] 📸 **SCREENSHOT 2:** Agent creation screen
- [ ] Set name: "Job Fitment Analysis Agent"
- [ ] Verify name is set

---

## STEP 3: COPY SYSTEM PROMPT (5 min)

- [ ] Open file: `deliverables/1-functional-agent/system-prompt.txt`
- [ ] Select all text (Cmd+A or Ctrl+A)
- [ ] Copy text (Cmd+C or Ctrl+C)
- [ ] Go back to OpenAI Platform
- [ ] Find "Instructions" or "System prompt" field
- [ ] Paste text (Cmd+V or Ctrl+V)
- [ ] Verify text pasted (should be 137 lines)
- [ ] 📸 **SCREENSHOT 3:** System prompt pasted

---

## STEP 4: SELECT MODEL (1 min)

- [ ] Find "Model" dropdown
- [ ] Select "GPT-4o" (or GPT-4 Turbo)
- [ ] Verify selection
- [ ] 📸 **SCREENSHOT 4:** Model selection

---

## STEP 5: ENABLE FILE SEARCH (2 min)

- [ ] Find "Tools" section
- [ ] Look for "File Search" or "Retrieval"
- [ ] Enable it (check box or toggle ON)
- [ ] Verify it's enabled
- [ ] 📸 **SCREENSHOT 5:** Tools configuration

---

## STEP 6: UPLOAD FILES (10 min)

- [ ] Find "Upload Files" or "Add Files" button
- [ ] Navigate to `knowledge-base/` folder
- [ ] Upload all 10 files:
  - [ ] `01-student-profiles/profile-template.txt`
  - [ ] `01-student-profiles/skills-taxonomy.txt`
  - [ ] `01-student-profiles/experience-levels.txt`
  - [ ] `02-job-analysis/job-posting-structure.txt`
  - [ ] `03-company-info/target-companies.txt`
  - [ ] `04-fitment-analysis/calculation-methodology.txt`
  - [ ] `04-fitment-analysis/interpretation-guide.txt`
  - [ ] `05-skill-gaps/gap-identification.txt`
  - [ ] `05-skill-gaps/learning-resources.txt`
  - [ ] `06-use-case-examples/use-case-1-example.txt`
- [ ] Wait for files to process (1-2 minutes)
- [ ] Verify all 10 files show as "Processed"
- [ ] 📸 **SCREENSHOT 6:** File upload interface
- [ ] 📸 **SCREENSHOT 7:** Uploaded files list

---

## STEP 7: SAVE AGENT (2 min)

- [ ] Find "Save" or "Create" button
- [ ] Click to save
- [ ] Wait for confirmation
- [ ] Note agent ID (optional)
- [ ] 📸 **SCREENSHOT 8:** Complete configuration

---

## STEP 8: TEST AGENT (5 min)

- [ ] Open agent chat/playground
- [ ] Enter test query:
  ```
  Priority 1:
  - Cisco
  - Google
  
  My profile: Computer Science student, Python, Java, AWS, 2 internships
  ```
- [ ] Send query
- [ ] Wait for response
- [ ] Verify agent responds
- [ ] Check agent uses knowledge base
- [ ] 📸 **SCREENSHOT 9:** First test interaction

---

## STEP 9: VERIFY (3 min)

- [ ] Agent name correct
- [ ] Model is GPT-4o
- [ ] File Search enabled
- [ ] All 10 files uploaded
- [ ] All files processed
- [ ] System prompt complete
- [ ] Agent responds correctly
- [ ] Knowledge base accessed

---

## ✅ BUILD COMPLETE!

**If all items checked:** ✅ **Your agent is ready!**

---

## 📸 SCREENSHOTS CHECKLIST

- [ ] Screenshot 1: Platform dashboard
- [ ] Screenshot 2: Agent creation screen
- [ ] Screenshot 3: System prompt
- [ ] Screenshot 4: Model selection
- [ ] Screenshot 5: Tools configuration
- [ ] Screenshot 6: File upload interface
- [ ] Screenshot 7: Uploaded files
- [ ] Screenshot 8: Complete configuration
- [ ] Screenshot 9: Test interaction

**Save all to:** `deliverables/4-screenshots/` folder

---

## 🎯 NEXT STEPS

- [ ] Run test cases (1-2 hours)
- [ ] Complete documentation (1 hour)
- [ ] Fill final report (3-4 hours)

---

**Time to Build:** 30-45 minutes  
**Status:** Ready to Start  
**Guide:** `COMPLETE_BUILD_INSTRUCTIONS.md`



