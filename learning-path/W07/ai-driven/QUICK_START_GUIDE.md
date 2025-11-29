# Quick Start Guide - Assignment Management Template

## 🚀 For New Assignments

### Step 1: Copy Template Files
From a completed assignment, copy these files to your new assignment folder:
- `.cursorrules` ✅
- `verification_checklists.md` ✅
- `TEMPLATE_SETUP_INSTRUCTIONS.md` ✅

### Step 2: Create Assignment Files
Create these two files with your assignment details:
- `Assignment_Analysis_Prompt.md` - Requirements, rubrics, deliverables
- `Assignment_TODO_Tracker.md` - Tasks, phases, progress tracking

### Step 3: Create Directories
```bash
mkdir -p episodic_memory/context_snapshots learnings evaluations self_feedback docs/screenshots
```

### Step 4: Initialize State
Create `state_tracker.json` (see TEMPLATE_SETUP_INSTRUCTIONS.md for template)

### Step 5: Start Working
Say: "Start working on [assignment name]"

---

## 📍 Checking Status

**Ask:** "Where are you?" or "Status" or "Current state"

**System will tell you:**
- Current phase and task
- Progress percentages
- Recent activity
- Blockers/issues
- Next steps
- Recent learnings
- Evaluation status

---

## ✅ Task Workflow

1. **Complete task** → System runs self-assessment
2. **System requests approval** → You review
3. **Approve or provide feedback** → System learns
4. **System updates trackers** → Proceeds to next task

---

## 🔄 Learning System

**Automatic Learning:**
- All feedback captured
- Patterns identified
- Applied to future work
- Saved to global learnings

**Cross-Assignment Learning:**
- Learnings from this assignment → Global learnings
- Global learnings → Applied to next assignment
- System improves with each assignment

---

## 📁 Key Files

**Assignment-Specific (Change These):**
- `Assignment_Analysis_Prompt.md`
- `Assignment_TODO_Tracker.md`

**Template Files (Copy As-Is):**
- `.cursorrules`
- `verification_checklists.md`
- All directory structure

**Auto-Generated (System Maintains):**
- `state_tracker.json`
- All files in `episodic_memory/`
- All files in `learnings/`
- All files in `evaluations/`
- All files in `self_feedback/`

---

## 🎯 What The System Does

✅ **Tracks Progress** - Always knows where you are  
✅ **Verifies Quality** - Checks before approval  
✅ **Learns Continuously** - Improves with each assignment  
✅ **Requires Approval** - Human-in-the-loop at every step  
✅ **Maintains Memory** - Complete audit trail  
✅ **Applies Learnings** - Uses past experience  

---

## 💡 Pro Tips

1. **Always check status** before starting work
2. **Review learnings** - System applies them automatically
3. **Provide feedback** - Helps system learn
4. **Check rubric** - System verifies alignment
5. **Trust the process** - System guides you through

---

*This template works for ANY assignment. Just create the two assignment files and you're ready!*

