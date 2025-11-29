# AI-Driven Assignment Management System

This folder contains all the AI-driven system files that work together to manage assignments. These files are **templates** that can be reused for any assignment.

## 📁 Folder Structure

```
ai-driven/
├── README.md (this file)
│
├── state_tracker.json              # Real-time state tracking
├── verification_checklists.md      # Quality gates
├── QUICK_START_GUIDE.md           # Quick reference
├── TEMPLATE_SETUP_INSTRUCTIONS.md  # Setup guide
├── TEMPLATE_SUMMARY.md             # System overview
│
├── episodic_memory/               # Complete event history
│   ├── event_log.md
│   ├── task_history.md
│   ├── decision_log.md
│   └── context_snapshots/
│
├── learnings/                      # Assignment-specific learnings
│   ├── feedback_learnings.md
│   ├── quality_improvements.md
│   ├── error_patterns.md
│   └── success_patterns.md
│
├── evaluations/                    # Evaluation forms
│   ├── task_evaluations.md
│   ├── phase_evaluations.md
│   └── rubric_alignment.md
│
├── self_feedback/                  # AI self-assessments
│   ├── self_assessments.md
│   ├── improvement_suggestions.md
│   └── feedback_loops.md
│
└── docs/
    └── screenshots/                # Screenshot storage
```

## 🎯 Purpose

This folder separates:
- **Assignment-specific content** (in root: `Assignment_Analysis_Prompt.md`, `Assignment_TODO_Tracker.md`)
- **AI system files** (in `ai-driven/`: all tracking, learning, evaluation systems)

## ✅ Benefits

1. **Clear Separation:** Assignment content vs. AI system
2. **Easy Reuse:** Copy entire `ai-driven/` folder for new assignments
3. **Better Organization:** All AI-related files in one place
4. **Template Clarity:** Makes it obvious what's reusable

## 📋 Usage

### For Current Assignment:
- All files are automatically used by the system
- No changes needed - system references these paths

### For New Assignments:
1. Copy entire `ai-driven/` folder to new assignment
2. All files stay the same (template)
3. Only assignment files in root change

## 🔄 How It Works

The `.cursorrules` file references all paths with `ai-driven/` prefix:
- `ai-driven/state_tracker.json`
- `ai-driven/episodic_memory/`
- `ai-driven/learnings/`
- `ai-driven/evaluations/`
- `ai-driven/self_feedback/`
- `ai-driven/verification_checklists.md`

---

*This folder is the "engine" that drives assignment management. Copy it as-is for any new assignment.*



