# File Creation Policy - AI System

## 🚨 CRITICAL RULE

**ALL intermediate files, logs, tracking, and system files MUST stay within `ai-driven/` folder.**

## ✅ What You CAN Do

### Use Existing Files
- ✅ Update `ai-driven/state_tracker.json`
- ✅ Append to `ai-driven/episodic_memory/event_log.md`
- ✅ Append to `ai-driven/episodic_memory/task_history.md`
- ✅ Append to `ai-driven/episodic_memory/decision_log.md`
- ✅ Update `ai-driven/learnings/` files
- ✅ Update `ai-driven/evaluations/` files
- ✅ Update `ai-driven/self_feedback/` files
- ✅ Update `Assignment_TODO_Tracker.md` (assignment file)

### Create Context Snapshots
- ✅ Save to `ai-driven/episodic_memory/context_snapshots/`
- ✅ Use format: `snapshot_YYYY-MM-DD_HH-MM-SS.md`

## ❌ What You CANNOT Do

### Do NOT Create Files Outside `ai-driven/`
- ❌ No new markdown files in root directory
- ❌ No temporary files
- ❌ No intermediate documentation files
- ❌ No new folders outside `ai-driven/`
- ❌ No duplicate tracking files
- ❌ No one-off log files

### Do NOT Create New Files Unless:
- User explicitly requests a file in a specific location
- Creating assignment deliverables (in root or specified location)
- Absolutely necessary and no existing file can serve the purpose

## 📋 File Organization

### When You Need to Log Something:

**Events/Activities:**
→ Use `ai-driven/episodic_memory/event_log.md`

**Task Completions:**
→ Use `ai-driven/episodic_memory/task_history.md`

**Decisions:**
→ Use `ai-driven/episodic_memory/decision_log.md`

**Learnings:**
→ Use appropriate file in `ai-driven/learnings/`

**Evaluations:**
→ Use appropriate file in `ai-driven/evaluations/`

**Self-Assessments:**
→ Use appropriate file in `ai-driven/self_feedback/`

**State Tracking:**
→ Use `ai-driven/state_tracker.json`

## 🔍 Before Creating ANY File

Ask yourself:
1. ✅ Does an existing file in `ai-driven/` serve this purpose?
2. ✅ Can I append to an existing file instead?
3. ✅ Is this truly necessary?
4. ✅ Can I consolidate with existing information?

**If answer to #1 or #2 is YES → Use existing file**
**If answer to #3 or #4 is NO → Don't create the file**

## 📁 Assignment Deliverables Exception

**Assignment deliverables** (like reports, documentation, code) can be created in root or specified locations, but:
- These are explicit deliverables, not system files
- User will specify where these should go
- These are not intermediate/tracking files

## 🎯 Principle

**Consolidate, don't proliferate.**
**Use existing structure, don't create new files.**
**Stay within `ai-driven/`, don't scatter files.**

---

*This policy ensures clean organization and prevents file proliferation.*



