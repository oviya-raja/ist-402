# Quick Reference Card
## Job Fitment Analysis Agent - Build & Test

**Print this page for quick reference during build!**

---

## 🔑 KEY INFORMATION

**Agent Name:** Job Fitment Analysis Agent  
**Model:** GPT-4o  
**Primary Tool:** File Search (Retrieval)  
**Knowledge Base Files:** 10 files  
**Build Time:** 30-45 minutes

---

## 📋 BUILD CHECKLIST (Quick)

- [ ] Log into OpenAI Platform
- [ ] Create new Assistant
- [ ] Copy system prompt (137 lines)
- [ ] Select GPT-4o model
- [ ] Enable File Search tool
- [ ] Upload 10 knowledge base files
- [ ] Save agent
- [ ] Test with sample query
- [ ] Verify knowledge base access

---

## 📁 FILE PATHS

**System Prompt:**
```
deliverables/1-functional-agent/system-prompt.txt
```

**Knowledge Base:**
```
knowledge-base/
├── 01-student-profiles/ (3 files)
├── 02-job-analysis/ (1 file)
├── 03-company-info/ (1 file)
├── 04-fitment-analysis/ (2 files)
├── 05-skill-gaps/ (2 files)
└── 06-use-case-examples/ (1 file)
```

**Test Cases:**
```
deliverables/1-functional-agent/test-cases.txt
```

---

## 🧪 QUICK TEST QUERY

```
Priority 1:
- Cisco
- Google

My profile: Computer Science student, Python, Java, AWS, 2 internships
```

**Expected:** Fitment analysis with skill gaps and recommendations

---

## 📸 SCREENSHOTS NEEDED (9)

1. Platform dashboard
2. Agent creation screen
3. System instructions
4. Model selection
5. File upload interface
6. Uploaded files list
7. Tools configuration
8. Complete configuration
9. First test interaction

---

## 🐛 QUICK TROUBLESHOOTING

**Files won't upload?**
→ Upload one at a time

**File Search not working?**
→ Enable tool, wait for processing

**Agent not responding?**
→ Check system prompt is complete

---

## 📞 DETAILED GUIDES

**Build Checklist:**
`deliverables/1-functional-agent/BUILD_CHECKLIST.md`

**Setup Guide:**
`deliverables/1-functional-agent/AGENT_SETUP_GUIDE.md`

**Test Cases:**
`deliverables/1-functional-agent/test-cases.txt`

**Verification:**
`deliverables/1-functional-agent/VERIFICATION_CHECKLIST.md`

---

## ✅ POST-BUILD CHECK

- [ ] Agent responds
- [ ] Knowledge base accessed
- [ ] All 10 files uploaded
- [ ] File Search enabled
- [ ] Test query works
- [ ] Screenshots captured

---

**Status:** Ready to Build  
**Time:** 30-45 minutes



