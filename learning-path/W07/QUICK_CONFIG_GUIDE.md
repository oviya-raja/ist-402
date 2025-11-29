# Quick Configuration Guide - Agent Builder

## Current Status
✅ Workflow created with "My agent" node  
✅ All files ready  
⏳ Need to configure the agent node

## Steps to Complete Configuration

### 1. Open Agent Configuration
- **Click on the "My agent" node** in the workflow canvas
- A **right-side panel** should open with configuration options

### 2. Configure Agent Name
- Find field: **"Name"** or **"Agent name"**
- Enter: `Job Fitment Analysis Agent`

### 3. Paste System Prompt
- Find field: **"Instructions"** or **"System Prompt"** or **"Prompt"**
- Open file: `deliverables/1-functional-agent/system-prompt.txt`
- **Copy entire content** (138 lines)
- **Paste** into the field

### 4. Select Model
- Find dropdown: **"Model"** or **"AI Model"**
- Select: **GPT-4o** (or GPT-4 Turbo if GPT-4o not available)

### 5. Enable File Search Tool
- Find section: **"Tools"** or **"Capabilities"**
- **Enable/Check:** "File Search" or "Retrieval" or "File Search and Retrieval"
- This is CRITICAL - enables knowledge base access

### 6. Upload Knowledge Base Files
- Find button: **"Upload Files"** or **"Add Files"** or **"Files"**
- Upload these 10 files (in order):

```
knowledge-base/01-student-profiles/profile-template.txt
knowledge-base/01-student-profiles/skills-taxonomy.txt
knowledge-base/01-student-profiles/experience-levels.txt
knowledge-base/02-job-analysis/job-posting-structure.txt
knowledge-base/03-company-info/target-companies.txt
knowledge-base/04-fitment-analysis/calculation-methodology.txt
knowledge-base/04-fitment-analysis/interpretation-guide.txt
knowledge-base/05-skill-gaps/gap-identification.txt
knowledge-base/05-skill-gaps/learning-resources.txt
knowledge-base/06-use-case-examples/use-case-1-example.txt
```

- Wait for all files to show as **"Processed"** or **"Ready"**

### 7. Save Configuration
- Click **"Save"** or **"Done"** button
- Configuration should be saved

### 8. Test Agent
- Click **"Preview"** or **"Test"** button (play icon in header)
- Try this test query:
  ```
  Priority 1:
  - Cisco
  - Google
  
  My profile: Computer Science student, Python, Java, AWS, 2 internships
  ```
- Verify agent responds and references knowledge base

## Troubleshooting

**If configuration panel doesn't open:**
- Try double-clicking the "My agent" node
- Look for a settings/gear icon on the node
- Check if there's a right-side panel that's collapsed

**If File Search not available:**
- Make sure you're using Agent Builder (not Assistants API)
- Check Tools section carefully
- May be labeled as "Retrieval" or "File Search and Retrieval"

**If files won't upload:**
- Try uploading one at a time
- Check file format (must be .txt)
- Verify file sizes (< 512MB each)

## What's Ready
- ✅ System prompt: `deliverables/1-functional-agent/system-prompt.txt` (138 lines)
- ✅ 10 knowledge base files in `knowledge-base/` folder
- ✅ Test cases: `deliverables/1-functional-agent/test-cases.txt`
- ✅ Build checklist: `deliverables/1-functional-agent/BUILD_CHECKLIST.md`

## Next Steps After Configuration
1. Test all 5 use cases
2. Capture screenshots
3. Complete workflow documentation
4. Prepare final report

