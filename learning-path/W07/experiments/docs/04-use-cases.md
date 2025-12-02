# Use Cases

## Use Case 1: Find Matching Jobs

**Description:** Search company sites by skills/experience and get ranked job list with fitment scores

**Input:**
- Student profile (skills, experience, education)
- Target companies (with priority levels)

**Output:**
- Ranked list of matching jobs
- Fitment percentage for each job
- Skill match details

**Example:**
- **Input:** 
  - Skills: Python, Java, AWS
  - Experience: Entry-level
  - Education: BS Computer Science
  - Priority 1: Cisco, Google
- **Output:** 
  - Cisco Software Engineer - New Grad (85% fit) ✅
    - Matched: Python (3 years), Java (2 years), AWS (1 year)
    - Missing: Networking basics (preferred)
  - Google Software Engineer I (88% fit) ✅
    - Matched: Python (3 years), Java (2 years), Cloud experience
    - Missing: System design experience (preferred)

---

## Use Case 2: Check Qualification

**Description:** Analyze specific job posting to get fitment percentage and skill gaps

**Input:**
- Job posting URL
- Student profile

**Output:**
- Fitment percentage
- Matched skills
- Missing qualifications
- Application recommendation

**Example:**
- **Input:** 
  - Job URL: https://jobs.apple.com/en-us/details/...
  - Profile: Python (2 years), Swift (6 months), iOS projects (2)
- **Output:** 
  - **Fitment: 78%** ✅ Good match, worth applying
  - **Matched Skills:**
    - Python (required) - 2 years experience ✅
    - Swift (required) - 6 months experience ✅
    - iOS development (required) - 2 projects ✅
    - CS degree (required) - BS Computer Science ✅
  - **Missing Skills:**
    - Objective-C (preferred) - Not critical ⚠️
    - 3+ years experience (preferred) - You have 2 years ⚠️
    - Published apps (preferred) - You have projects but no published apps ⚠️
  - **Recommendation:** Apply! Learn basic Objective-C before interview

---

## Use Case 3: Compare Jobs

**Description:** Compare multiple job postings to get ranked recommendations

**Input:**
- Multiple job URLs
- Student profile
- Company priority list

**Output:**
- Ranked job list
- Side-by-side comparison
- Prioritized recommendations

**Example:**
- **Input:** 
  - 4 job URLs: 2 Google, 1 Cisco, 1 Apple
  - Profile: Python, Java, AWS | Entry-level
  - Priority: Google (Priority 1), Cisco (Priority 1), Apple (Priority 2)
- **Output:** 
  - **#1: Google - Software Engineer I (92% fit)** ✅ APPLY FIRST
    - Skills match: 95%, Location: Remote ✅, Company: Priority 1
  - **#2: Cisco - Software Engineer - New Grad (85% fit)** ✅ APPLY
    - Skills match: 88%, Location: Hybrid ⚠️, Company: Priority 1
  - **#3: Google - Associate SE (78% fit)** ⚠️ MAYBE
    - Skills match: 80%, Location: On-site ❌, Company: Priority 1
  - **#4: Apple - iOS Engineer (72% fit)** ❌ SKIP FOR NOW
    - Skills match: 70%, Location: On-site ❌, Company: Priority 2

---

**Status:** ✅ Complete  
**Last Updated:** 2025-11-29

