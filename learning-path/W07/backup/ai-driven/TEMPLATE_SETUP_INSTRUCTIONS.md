# Assignment Management Template - Setup Instructions

## 🎯 Overview

This is a **reusable template system** for managing any assignment. The same structure, verification system, learning database, and tracking mechanisms work for **every assignment**. Only two files change per assignment.

---

## 📋 What Changes Per Assignment

### ✅ Files You Create/Update (Assignment-Specific):
1. **`Assignment_Analysis_Prompt.md`**
   - Contains assignment requirements
   - Rubrics and grading criteria
   - Deliverables and expectations
   - **Create this for each new assignment**

2. **`Assignment_TODO_Tracker.md`**
   - All tasks broken down by phases
   - Progress tracking tables
   - Screenshot checklists
   - **Create this for each new assignment**

### ❌ Files That Stay The Same (Template Files):
- `.cursorrules` - **Copy as-is, no changes needed**
- `verification_checklists.md` - **Copy as-is, no changes needed**
- Directory structure - **Same for all assignments**
- All tracking/learning systems - **Same for all assignments**

---

## 🚀 Setting Up a New Assignment

### Step 1: Create Assignment Folder
```bash
mkdir W08_Assignment_Name
cd W08_Assignment_Name
```

### Step 2: Copy Template Files
Copy these files from a previous assignment (or template):
- `.cursorrules`
- `verification_checklists.md`
- `TEMPLATE_SETUP_INSTRUCTIONS.md` (this file)

### Step 3: Create Assignment-Specific Files
Create these two files with your assignment details:
- `Assignment_Analysis_Prompt.md` - Assignment requirements
- `Assignment_TODO_Tracker.md` - Task breakdown

### Step 4: Create Directory Structure
```bash
mkdir -p episodic_memory/context_snapshots
mkdir -p learnings
mkdir -p evaluations
mkdir -p self_feedback
mkdir -p docs/screenshots
```

### Step 5: Initialize State Tracker
Create `state_tracker.json`:
```json
{
  "current_state": {
    "phase": "Phase 1: [Phase Name]",
    "phase_number": 1,
    "current_task": "TODO-001",
    "task_description": "[First task description]",
    "status": "not_started",
    "session_id": "[YYYY-MM-DD-session-1]",
    "timestamp": "[ISO timestamp]"
  },
  "progress": {
    "overall_completion": 0,
    "phase_1_completion": 0,
    "tasks_completed": 0,
    "tasks_total": 0
  },
  "recent_activity": [],
  "blockers": [],
  "next_steps": ["TODO-001: [First task]"],
  "evaluation_status": {
    "last_task_evaluation": null,
    "last_phase_evaluation": null,
    "pending_approvals": 0
  }
}
```

### Step 6: Set Up Global Learnings (First Time Only)
If this is your first assignment, create global learnings directory:
```bash
cd ..
mkdir -p _global_learnings
```

Create initial files:
- `_global_learnings/quality_standards.md`
- `_global_learnings/common_errors.md`
- `_global_learnings/best_practices.md`
- `_global_learnings/success_patterns.md`

### Step 7: Start Working
Begin with Phase 1, Task 1. The system will guide you through everything.

---

## 📁 Complete Directory Structure

```
[Assignment_Folder]/
├── .cursorrules                          # Template - copy as-is
├── Assignment_Analysis_Prompt.md         # CREATE per assignment
├── Assignment_TODO_Tracker.md            # CREATE per assignment
├── verification_checklists.md            # Template - copy as-is
├── TEMPLATE_SETUP_INSTRUCTIONS.md        # Template - copy as-is
├── state_tracker.json                    # Auto-generated/updated
│
├── episodic_memory/
│   ├── event_log.md                      # Auto-generated
│   ├── task_history.md                   # Auto-generated
│   ├── decision_log.md                   # Auto-generated
│   └── context_snapshots/                # Auto-generated
│       └── snapshot_[timestamp].md
│
├── learnings/
│   ├── feedback_learnings.md             # Auto-generated
│   ├── quality_improvements.md           # Auto-generated
│   ├── error_patterns.md                 # Auto-generated
│   └── success_patterns.md               # Auto-generated
│
├── evaluations/
│   ├── task_evaluations.md               # Auto-generated
│   ├── phase_evaluations.md              # Auto-generated
│   └── rubric_alignment.md               # Auto-generated
│
├── self_feedback/
│   ├── self_assessments.md               # Auto-generated
│   ├── improvement_suggestions.md        # Auto-generated
│   └── feedback_loops.md                 # Auto-generated
│
└── docs/
    └── screenshots/                      # Manual - save screenshots here
        └── [screenshot files]

[Parent_Directory]/
└── _global_learnings/                    # Shared across ALL assignments
    ├── quality_standards.md
    ├── common_errors.md
    ├── best_practices.md
    ├── process_improvements.md
    └── success_patterns.md
```

---

## 🔄 How The System Learns

### During Assignment:
1. **Feedback Capture:** All human feedback stored in `learnings/`
2. **Pattern Recognition:** System identifies common issues/successes
3. **Immediate Application:** Learnings applied to current assignment

### After Assignment Completion:
1. **Learning Extraction:** Review all learnings from assignment
2. **Global Update:** Save universal patterns to `../_global_learnings/`
3. **Template Improvement:** Update templates if process improvements found

### Before Next Assignment:
1. **Load Global Learnings:** System reads `../_global_learnings/`
2. **Apply Patterns:** Relevant learnings applied automatically
3. **Avoid Pitfalls:** Known error patterns avoided
4. **Replicate Success:** Success patterns replicated

---

## 📝 Assignment File Templates

### Assignment_Analysis_Prompt.md Template Structure:
```markdown
# [Assignment Name] - Analysis Prompt

## Assignment Objective
[What the assignment is about]

## Project Goals
1. [Goal 1]
2. [Goal 2]
...

## Deliverables
### 1. [Deliverable 1] (X pts)
Requirements:
- [Requirement 1]
- [Requirement 2]
...

### 2. [Deliverable 2] (X pts)
...

## Rubric Checklist
[Detailed rubric breakdown]

## Suggested Workflow Options
[If applicable]

## Pro Tips
[Helpful tips]
```

### Assignment_TODO_Tracker.md Template Structure:
```markdown
# [Assignment Name] - TODO Tracker

**Project:** [Project Name]
**Total Points:** [X]
**Status:** 🔴 Not Started | 🟡 In Progress | 🟢 Complete

## PROGRESS OVERVIEW
[Progress table]

## PHASE 1: [Phase Name]
**Status:** 🔴
- [ ] **TODO-001:** [Task description]
- [ ] **TODO-002:** [Task description]
...

## PHASE 2: [Phase Name]
...

[Continue for all phases]

## SCREENSHOT CHECKLIST
[Screenshot tracking table]

## FINAL STATS
**Total Tasks:** [X]
**Completed:** ___/[X]
```

---

## 🎓 Learning System Details

### What Gets Learned:

1. **Quality Standards:**
   - What quality level is expected
   - Common quality issues to avoid
   - How to improve quality

2. **Error Patterns:**
   - Common mistakes made
   - How to avoid them
   - What to check before submission

3. **Success Patterns:**
   - What works well
   - Best practices identified
   - Approaches that get approved quickly

4. **Process Improvements:**
   - Better ways to organize work
   - More efficient workflows
   - Verification improvements

### How Learnings Are Applied:

1. **Automatic Application:**
   - System checks learnings before starting tasks
   - Applies relevant patterns automatically
   - Avoids known pitfalls

2. **Verification Integration:**
   - Learnings update verification checklists
   - Quality standards evolve
   - Error checks become more comprehensive

3. **Continuous Improvement:**
   - Each assignment improves the system
   - Templates get refined
   - Process becomes more efficient

---

## 💬 Using The System

### Starting Work:
1. Say: "Start working on [assignment name]"
2. System reads assignment files
3. System loads learnings
4. System checks current state
5. System begins with next task

### Checking Status:
1. Ask: "Where are you?" or "Status" or "Current state"
2. System reads state_tracker.json
3. System reads recent episodic memory
4. System generates comprehensive status report

### Requesting Approval:
1. System completes task
2. System runs self-assessment
3. System generates evaluation form
4. System presents work for approval
5. **You approve or provide feedback**
6. System captures feedback and learns

### After Approval/Feedback:
1. If approved: System updates trackers and proceeds
2. If feedback: System learns, improves, resubmits

---

## ✅ Verification Workflow

### Task Level:
1. Complete task
2. Run task verification checklist
3. Self-assess
4. Generate evaluation form
5. **Request human approval**
6. If approved: Update and proceed
7. If feedback: Learn, improve, resubmit

### Phase Level:
1. Complete all phase tasks
2. Run phase verification checklist
3. Self-assess phase
4. Generate phase evaluation
5. **Request human approval**
6. If approved: Unlock next phase
7. If feedback: Address issues, resubmit

---

## 🎯 Key Benefits

1. **Consistency:** Same process for every assignment
2. **Quality:** Verification at every step
3. **Learning:** System improves with each assignment
4. **Tracking:** Always know where you are
5. **Efficiency:** Learnings applied automatically
6. **Accountability:** Human approval required
7. **Documentation:** Complete audit trail

---

## ⚠️ Important Notes

1. **Never skip verification** - Always check before approval
2. **Always wait for approval** - Don't proceed without human OK
3. **Always capture learnings** - Every feedback is valuable
4. **Always update state** - Keep trackers current
5. **Always check rubric** - Align with requirements
6. **Always apply learnings** - Use accumulated knowledge

---

## 🔧 Troubleshooting

### System doesn't know where to start:
- Check if `state_tracker.json` exists
- If not, initialize it (see Step 5)
- Start with Phase 1, Task 1

### Learnings not being applied:
- Check if `../_global_learnings/` exists
- Check if learnings files are readable
- System should load automatically

### Status query not working:
- Ensure `state_tracker.json` exists and is valid JSON
- Check episodic memory files exist
- System should read and report

---

*This template system works for ANY assignment. Just create the two assignment-specific files and you're ready to go!*

