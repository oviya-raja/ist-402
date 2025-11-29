# What to Expect When Building Your Agent
## A Guide to the Build Process

**This guide tells you what to expect at each step.**

---

## ⏱️ TIME BREAKDOWN

**Total Time:** 30-45 minutes

- Step 1: Access Platform (2 min)
- Step 2: Create Agent (3 min)
- Step 3: System Prompt (5 min)
- Step 4: Select Model (1 min)
- Step 5: Enable File Search (2 min)
- Step 6: Upload Files (10 min)
- Step 7: Save Agent (2 min)
- Step 8: Test Agent (5 min)
- Step 9: Verify (3 min)

---

## 🎯 STEP-BY-STEP EXPECTATIONS

### Step 1: Access OpenAI Platform

**What You'll See:**
- OpenAI Platform login page
- Dashboard with various options
- "Assistants" or "Agent Builder" in sidebar

**What to Do:**
- Log in (or create account)
- Click "Assistants" or "Agent Builder"

**Expected Time:** 2 minutes

**Possible Issues:**
- Need to create account (adds 2-3 minutes)
- Can't find "Assistants" (look for "Playground" or "Build")

---

### Step 2: Create New Agent

**What You'll See:**
- A form with fields to fill
- Fields like "Name", "Instructions", "Model"
- Various configuration options

**What to Do:**
- Click "Create" or "New Assistant"
- Enter name: "Job Fitment Analysis Agent"

**Expected Time:** 3 minutes

**What It Looks Like:**
- Form with text fields
- Dropdown menus
- Checkboxes for tools

---

### Step 3: Copy System Prompt

**What You'll See:**
- Text file with 137 lines
- Starts with "You are a Job Fitment Analysis Agent..."
- Large text box in OpenAI Platform

**What to Do:**
- Open `system-prompt.txt`
- Select all text
- Copy
- Paste into "Instructions" field

**Expected Time:** 5 minutes

**What It Looks Like:**
- Large text area filled with instructions
- Should see text about "Job Fitment Analysis Agent"
- About 137 lines of text

**Possible Issues:**
- Text doesn't paste (try Ctrl+V or Cmd+V)
- Text is cut off (check if all 137 lines pasted)

---

### Step 4: Select Model

**What You'll See:**
- Dropdown menu with model options
- Options like "GPT-4o", "GPT-4 Turbo", "GPT-3.5"

**What to Do:**
- Click dropdown
- Select "GPT-4o"

**Expected Time:** 1 minute

**What It Looks Like:**
- Dropdown showing "GPT-4o" selected

**Possible Issues:**
- GPT-4o not available (use GPT-4 Turbo instead)

---

### Step 5: Enable File Search

**What You'll See:**
- Section labeled "Tools" or "Capabilities"
- Checkboxes or toggles for different tools
- "File Search" or "Retrieval" option

**What to Do:**
- Find "File Search" or "Retrieval"
- Check the box or toggle ON

**Expected Time:** 2 minutes

**What It Looks Like:**
- Checkbox checked or toggle showing "ON"
- Green indicator or checkmark

**Possible Issues:**
- Can't find File Search (make sure GPT-4o is selected)
- Tool not available (check account permissions)

---

### Step 6: Upload Knowledge Base Files

**What You'll See:**
- "Upload Files" button
- File picker window
- List of uploaded files
- Processing status indicators

**What to Do:**
- Click "Upload Files"
- Select all 10 files from `knowledge-base/` folder
- Wait for processing

**Expected Time:** 10 minutes (including processing)

**What It Looks Like:**
- List of 10 files
- Status showing "Processing..." then "Processed" or "Ready"
- Checkmarks next to each file

**Possible Issues:**
- Files won't upload (try one at a time)
- Files stuck on "Processing" (wait 2-3 minutes)
- Wrong file format (must be .txt)

---

### Step 7: Save Agent

**What You'll See:**
- "Save" or "Create" button
- Success message or page refresh
- Agent appears in your list

**What to Do:**
- Click "Save" or "Create"
- Wait for confirmation

**Expected Time:** 2 minutes

**What It Looks Like:**
- Success message
- OR page refreshes showing your agent
- Agent name: "Job Fitment Analysis Agent"

**Possible Issues:**
- Save button doesn't work (check all required fields)
- Error message (read error and fix issue)

---

### Step 8: Test Agent

**What You'll See:**
- Chat interface or playground
- Text input box
- Response area

**What to Do:**
- Enter test query
- Press Enter or click "Send"
- Wait for response

**Expected Time:** 5 minutes

**What It Looks Like:**
- Your query appears
- Agent response appears (10-30 seconds)
- Response includes analysis, recommendations

**Expected Response:**
- Acknowledges your input
- References knowledge base
- Provides fitment analysis
- Gives recommendations

**Possible Issues:**
- No response (check File Search is enabled)
- Error message (check files are processed)
- Generic response (check system prompt is complete)

---

### Step 9: Verify

**What You'll See:**
- Agent configuration page
- List of uploaded files
- Tools enabled
- Test response

**What to Do:**
- Check each item in verification checklist
- Ensure everything works

**Expected Time:** 3 minutes

**What It Looks Like:**
- All checkboxes checked
- Everything working correctly

---

## ✅ SUCCESS INDICATORS

**Your agent is working if:**

- ✅ Agent responds to queries
- ✅ Response references knowledge base
- ✅ Response includes fitment analysis
- ✅ Response provides recommendations
- ✅ File Search tool is enabled
- ✅ All 10 files are processed
- ✅ System prompt is complete

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### Issue: Can't find "Assistants"
**Solution:** Look for "Playground" or "Build" section

### Issue: Files won't upload
**Solution:** Upload one at a time, check file format

### Issue: File Search not available
**Solution:** Make sure GPT-4o is selected

### Issue: Agent not responding
**Solution:** Check File Search enabled, files processed

### Issue: Response doesn't use knowledge base
**Solution:** Verify files are processed (not just uploaded)

---

## 🎉 WHEN YOU'RE DONE

**You'll have:**
- ✅ Working agent
- ✅ 9 screenshots
- ✅ Tested functionality
- ✅ Ready for next steps

**Next Steps:**
1. Run test cases (1-2 hours)
2. Complete documentation (1 hour)
3. Fill final report (3-4 hours)

---

## 📸 SCREENSHOTS TO CAPTURE

Capture these 9 screenshots:

1. Platform dashboard
2. Agent creation screen
3. System prompt pasted
4. Model selection
5. Tools configuration
6. File upload interface
7. Uploaded files list
8. Complete configuration
9. Test interaction

**Save to:** `deliverables/4-screenshots/` folder

---

## 💡 TIPS FOR SUCCESS

1. **Take your time** - Don't rush
2. **Follow instructions** - Step by step
3. **Take screenshots** - As you go
4. **Verify each step** - Before moving on
5. **Read error messages** - They help
6. **Be patient** - File processing takes time

---

**Status:** Ready to Build  
**Time:** 30-45 minutes  
**Difficulty:** Easy - Just follow steps

**You've got this!** 🚀

