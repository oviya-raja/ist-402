# Complete Build Instructions - Step by Step
## Build Your Agent - No Assumptions, Every Detail Covered

**This guide assumes NOTHING. Follow step-by-step.**

---

## 🎯 WHAT YOU'RE BUILDING

**Agent Name:** Job Fitment Analysis Agent  
**Purpose:** Helps students analyze job fitment and identify skill gaps  
**Time Required:** 30-45 minutes  
**Difficulty:** Easy (just follow steps)

---

## ✅ BEFORE YOU START - CHECKLIST

Make sure you have:

- [ ] Computer with internet connection
- [ ] Web browser (Chrome, Firefox, Safari, or Edge)
- [ ] OpenAI account (if you don't have one, we'll create it)
- [ ] 30-45 minutes of uninterrupted time
- [ ] All files ready (they are - we've prepared everything)

**If you have all of the above, continue to Step 1.**

---

## STEP 1: ACCESS OPENAI PLATFORM (2 minutes)

### 1.1 Open Your Web Browser
- Open Chrome, Firefox, Safari, or Edge
- Make sure you have internet connection

### 1.2 Go to OpenAI Platform
- Type this in your browser address bar: `https://platform.openai.com`
- Press Enter

### 1.3 Log In
- **If you have an account:**
  - Click "Log in" or "Sign in"
  - Enter your email and password
  - Click "Log in"

- **If you DON'T have an account:**
  - Click "Sign up" or "Get started"
  - Enter your email
  - Create a password
  - Verify your email (check your inbox)
  - Complete signup process

### 1.4 Navigate to Assistants
- Once logged in, look for "Assistants" in the left sidebar
- Click on "Assistants"
- **OR** look for "Agent Builder" and click that

**If you don't see "Assistants" or "Agent Builder":**
- Look for "Playground" or "Build" in the menu
- The interface may vary - look for anything related to "Assistants" or "Agents"

**✅ Checkpoint:** You should see a page with options to create or manage assistants/agents.

**📸 SCREENSHOT 1:** Take a screenshot of this page (Platform dashboard)

---

## STEP 2: CREATE NEW ASSISTANT/AGENT (3 minutes)

### 2.1 Find the Create Button
- Look for a button that says:
  - "Create" or
  - "New Assistant" or
  - "New Agent" or
  - "+" (plus sign) or
  - "Create Assistant"

### 2.2 Click Create
- Click the button you found

### 2.3 You Should See a Form
- You should now see a form or page with fields to fill in
- This is the agent creation screen

**📸 SCREENSHOT 2:** Take a screenshot of this creation screen

### 2.4 Set the Name
- Find a field labeled "Name" or "Assistant name" or "Agent name"
- Type exactly this: `Job Fitment Analysis Agent`
- Press Tab or click next field

**✅ Checkpoint:** Name field should show "Job Fitment Analysis Agent"

---

## STEP 3: COPY AND PASTE SYSTEM PROMPT (5 minutes)

### 3.1 Open the System Prompt File
- On your computer, navigate to this folder: `W07/deliverables/1-functional-agent/`
- Find the file named: `system-prompt.txt`
- Double-click to open it (it will open in a text editor)

**If you can't find the file:**
- The full path is: `/Users/rajasoun/workspace/personal/oviya/ist-402/learning-path/W07/deliverables/1-functional-agent/system-prompt.txt`
- Or search your computer for "system-prompt.txt"

### 3.2 Select All Text
- Click anywhere in the text file
- Press `Cmd+A` (Mac) or `Ctrl+A` (Windows) to select all
- **OR** click and drag from the very beginning to the very end

### 3.3 Copy the Text
- Press `Cmd+C` (Mac) or `Ctrl+C` (Windows) to copy
- **OR** Right-click and select "Copy"
- **Verify:** The text should be copied (you won't see anything, but it's copied)

### 3.4 Go Back to OpenAI Platform
- Switch back to your browser (the OpenAI Platform tab)
- Find the field labeled:
  - "Instructions" or
  - "System prompt" or
  - "System instructions" or
  - "Assistant instructions" or
  - A large text box

### 3.5 Paste the Text
- Click inside that field
- Press `Cmd+V` (Mac) or `Ctrl+V` (Windows) to paste
- **OR** Right-click and select "Paste"

### 3.6 Verify It Pasted
- Scroll through the pasted text
- You should see text starting with "You are a Job Fitment Analysis Agent..."
- The text should be about 137 lines long
- **If it's not all there, go back and copy again**

**📸 SCREENSHOT 3:** Take a screenshot showing the system prompt pasted

**✅ Checkpoint:** System prompt field should contain the full instructions (137 lines)

---

## STEP 4: SELECT THE MODEL (1 minute)

### 4.1 Find Model Selection
- Look for a dropdown or field labeled:
  - "Model" or
  - "GPT Model" or
  - "Model selection" or
  - "Choose model"

### 4.2 Select GPT-4o
- Click the dropdown
- Look for "GPT-4o" in the list
- Click on "GPT-4o"

**If GPT-4o is not available:**
- Select "GPT-4 Turbo" (second choice)
- **OR** "gpt-4" (third choice)
- **Avoid:** GPT-3.5 (not recommended)

### 4.3 Verify Selection
- The dropdown should now show "GPT-4o" (or your selected model)

**📸 SCREENSHOT 4:** Take a screenshot showing the model selection

**✅ Checkpoint:** Model should be set to GPT-4o (or GPT-4 Turbo)

---

## STEP 5: ENABLE FILE SEARCH TOOL (2 minutes)

### 5.1 Find Tools Section
- Look for a section labeled:
  - "Tools" or
  - "Capabilities" or
  - "Functions" or
  - "Add tools"

### 5.2 Look for File Search
- In the tools section, look for:
  - "File Search" or
  - "Retrieval" or
  - "Knowledge Base" or
  - A checkbox with "File Search" or "Retrieval"

### 5.3 Enable File Search
- **If it's a checkbox:** Click to check it (put a checkmark)
- **If it's a toggle:** Click to turn it ON
- **If it's a button:** Click "Add" or "Enable"

### 5.4 Verify It's Enabled
- You should see File Search/Retrieval is now enabled/checked
- There might be a green checkmark or "ON" indicator

**📸 SCREENSHOT 5:** Take a screenshot of the tools configuration showing File Search enabled

**✅ Checkpoint:** File Search/Retrieval tool should be enabled/checked

**⚠️ IMPORTANT:** This tool is REQUIRED. Without it, the agent cannot access the knowledge base.

---

## STEP 6: UPLOAD KNOWLEDGE BASE FILES (10 minutes)

### 6.1 Find File Upload Section
- Look for:
  - "Files" or
  - "Knowledge Base" or
  - "Upload Files" or
  - "Add Files" or
  - A button that says "Upload" or "Add"

### 6.2 Locate Knowledge Base Files on Your Computer
- Navigate to: `W07/knowledge-base/` folder
- You should see 6 folders:
  - `01-student-profiles/`
  - `02-job-analysis/`
  - `03-company-info/`
  - `04-fitment-analysis/`
  - `05-skill-gaps/`
  - `06-use-case-examples/`

### 6.3 Files to Upload (10 files total):

**From `01-student-profiles/` folder:**
1. `profile-template.txt`
2. `skills-taxonomy.txt`
3. `experience-levels.txt`

**From `02-job-analysis/` folder:**
4. `job-posting-structure.txt`

**From `03-company-info/` folder:**
5. `target-companies.txt`

**From `04-fitment-analysis/` folder:**
6. `calculation-methodology.txt`
7. `interpretation-guide.txt`

**From `05-skill-gaps/` folder:**
8. `gap-identification.txt`
9. `learning-resources.txt`

**From `06-use-case-examples/` folder:**
10. `use-case-1-example.txt`

### 6.4 Upload Method 1: Upload All at Once (Easier)
1. Click "Upload Files" or "Add Files" button
2. A file picker window will open
3. Navigate to `knowledge-base/` folder
4. **Select all 10 files at once:**
   - Hold `Cmd` (Mac) or `Ctrl` (Windows)
   - Click each of the 10 files
   - OR select the first file, hold Shift, click the last file
5. Click "Open" or "Select"
6. Files should start uploading

### 6.5 Upload Method 2: Upload One by One (If Method 1 Fails)
1. Click "Upload Files" or "Add Files"
2. Navigate to first file: `01-student-profiles/profile-template.txt`
3. Select it and click "Open"
4. Wait for it to upload
5. Repeat for each of the 10 files

### 6.6 Wait for Processing
- After uploading, files need to be processed
- You'll see status like "Processing..." or "Uploading..."
- **Wait 1-2 minutes** for all files to process
- Status should change to "Processed" or "Ready" or show a checkmark

**📸 SCREENSHOT 6:** Take a screenshot of the file upload interface (before uploading)

**📸 SCREENSHOT 7:** Take a screenshot showing all 10 files uploaded and processed

**✅ Checkpoint:** All 10 files should show as "Processed" or "Ready"

**⚠️ TROUBLESHOOTING:**
- **Files won't upload?** Try uploading one at a time
- **Files stuck on "Processing"?** Wait 2-3 minutes, refresh page
- **Wrong file format?** Make sure files are .txt format
- **File too large?** Files should be small (< 1MB each)

---

## STEP 7: SAVE THE AGENT (2 minutes)

### 7.1 Find Save Button
- Look for a button that says:
  - "Save" or
  - "Create" or
  - "Save Assistant" or
  - "Create Agent"

### 7.2 Click Save
- Click the save/create button
- Wait a few seconds

### 7.3 Agent Created
- You should see a success message
- OR the page will refresh showing your agent
- OR you'll be taken to the agent's page

### 7.4 Note the Agent ID (Optional but Recommended)
- Look for an ID like: `asst_xxxxxxxxxxxxx`
- Copy it and save it somewhere (you might need it later)
- **OR** just note the agent name: "Job Fitment Analysis Agent"

**📸 SCREENSHOT 8:** Take a screenshot of the complete agent configuration (after saving)

**✅ Checkpoint:** Agent should be saved and visible in your assistants list

---

## STEP 8: TEST THE AGENT (5 minutes)

### 8.1 Open the Agent
- Find your agent in the list (named "Job Fitment Analysis Agent")
- Click on it to open

### 8.2 Find the Chat/Test Interface
- Look for:
  - "Playground" or
  - "Test" or
  - "Chat" or
  - A text input box at the bottom

### 8.3 Enter Test Query
- Click in the text input box
- Type or paste this EXACT text:

```
Priority 1:
- Cisco
- Google

My profile: Computer Science student, Python, Java, AWS, 2 internships
```

### 8.4 Send the Query
- Press Enter
- OR click "Send" button
- Wait for response (may take 10-30 seconds)

### 8.5 Check the Response
- The agent should respond with:
  - Acknowledgment of your input
  - Analysis of fitment
  - References to knowledge base (you might see file names)
  - Recommendations

**If the response looks good:**
- ✅ Agent is working!

**If the response is empty or error:**
- Check that File Search tool is enabled
- Check that files are processed
- Try a simpler query: "Hello, can you help me?"

**📸 SCREENSHOT 9:** Take a screenshot of the first successful test interaction

**✅ Checkpoint:** Agent should respond with relevant analysis

---

## STEP 9: VERIFY EVERYTHING WORKS (3 minutes)

### 9.1 Quick Verification Checklist

Check each item:

- [ ] Agent name is "Job Fitment Analysis Agent"
- [ ] Model is GPT-4o (or GPT-4 Turbo)
- [ ] File Search tool is enabled
- [ ] All 10 knowledge base files are uploaded
- [ ] All files show as "Processed" or "Ready"
- [ ] System prompt is complete (137 lines)
- [ ] Agent responds to test queries
- [ ] Agent references knowledge base in responses

**If all checked:**
- ✅ **Your agent is ready!**

**If any unchecked:**
- Go back to that step and fix it

---

## ✅ CONGRATULATIONS!

**Your agent is built and ready!**

### What You've Accomplished:
- ✅ Created Job Fitment Analysis Agent
- ✅ Configured system prompt
- ✅ Uploaded knowledge base (10 files)
- ✅ Enabled File Search tool
- ✅ Tested and verified functionality

### Next Steps:
1. **Run Test Cases** (1-2 hours)
   - Open: `deliverables/1-functional-agent/test-cases.txt`
   - Test all 10 test cases
   - Capture screenshots

2. **Complete Documentation** (1 hour)
   - Insert workflow diagrams
   - Complete workflow docs

3. **Final Report** (3-4 hours)
   - Fill report template
   - Include screenshots
   - Export to PDF

---

## 📸 SCREENSHOTS SUMMARY

You should have 9 screenshots:

1. ✅ Platform dashboard
2. ✅ Agent creation screen
3. ✅ System instructions configuration
4. ✅ Model selection
5. ✅ Tools configuration (File Search enabled)
6. ✅ File upload interface
7. ✅ Uploaded files list (all 10 files processed)
8. ✅ Complete agent configuration
9. ✅ First successful test interaction

**Save all screenshots to:** `deliverables/4-screenshots/` folder (create if needed)

---

## 🐛 TROUBLESHOOTING GUIDE

### Problem: Can't find "Assistants" in OpenAI Platform
**Solution:**
- Look for "Playground" instead
- OR "Build" section
- OR check if you need to enable beta features
- OR try: https://platform.openai.com/assistants

### Problem: Files won't upload
**Solution:**
- Try uploading one file at a time
- Check file format (must be .txt)
- Check file size (should be < 1MB each)
- Refresh page and try again

### Problem: File Search tool not available
**Solution:**
- Make sure you're using GPT-4o or GPT-4 Turbo (not GPT-3.5)
- Check if your account has access to File Search
- Try refreshing the page

### Problem: Agent not responding
**Solution:**
- Check that File Search is enabled
- Verify files are processed (not just uploaded)
- Try a simpler query first
- Check system prompt is complete

### Problem: Agent responds but doesn't use knowledge base
**Solution:**
- Verify File Search tool is enabled
- Check that files are processed (status should be "Processed")
- Try asking: "What information do you have about student profiles?"

---

## 📝 NOTES SECTION

**Agent Name:** Job Fitment Analysis Agent  
**Agent ID:** _________________________ (if you saved it)  
**Build Date:** _________________________  
**Model Used:** GPT-4o (or _________________)  
**Files Uploaded:** 10/10  

**Issues Encountered:**
- 
- 

**Solutions Applied:**
- 
- 

---

## ✅ FINAL CHECKLIST

Before considering the build complete:

- [ ] Agent created successfully
- [ ] System prompt pasted (137 lines)
- [ ] Model selected (GPT-4o)
- [ ] File Search tool enabled
- [ ] All 10 files uploaded
- [ ] All files processed
- [ ] Agent responds to queries
- [ ] Agent uses knowledge base
- [ ] 9 screenshots captured
- [ ] Everything verified

**If all checked:** ✅ **BUILD COMPLETE!**

---

**Status:** Ready to Build  
**Time Required:** 30-45 minutes  
**Difficulty:** Easy (just follow steps)  
**Last Updated:** 2025-11-29

**You can do this! Follow each step carefully. Good luck!** 🚀



