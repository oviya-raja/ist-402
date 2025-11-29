# Phase 1.1: Use Cases - Job Fitment Analysis Agent

## 5 Specific Use Cases

### Use Case 1: Search and Filter Jobs from Company Sites by Multiple Criteria

**Description:**
The agent searches company job posting websites (Cisco, SAP, Google, Apple, Amazon, Tesla) and identifies jobs that match the student's profile based on multiple criteria, not just job title.

**User Input:**
- Priority-based company list (Priority 1, 2, 3)
- Student profile (skills, experience, education, location preferences, salary expectations)
- Search criteria (job level, department, location, required skills, experience years, etc.)

**Agent Process:**
1. Access company job posting sites from target companies list
2. Search and filter jobs based on multiple criteria:
   - Skills match (required vs. student's skills)
   - Experience level (entry, mid, senior)
   - Education requirements (degree level, field)
   - Location preferences (remote, hybrid, specific cities)
   - Department/team alignment
   - Salary range (if available)
   - Job type (full-time, internship, contract)
3. Rank results by fitment score
4. Present filtered job list with fitment percentages

**Output:**
- List of matching jobs from each priority company
- Fitment score for each job (0-100%)
- Key matching criteria highlighted
- Jobs ranked by fitment and priority level

**Success Criteria:**
- ✅ Finds relevant jobs beyond just title matching
- ✅ Filters by multiple criteria simultaneously
- ✅ Provides fitment scores for each match
- ✅ Ranks results by relevance and priority
- ✅ Saves time compared to manual search (hours → minutes)

---

### Use Case 2: Analyze Job Posting Fitment Against Student Profile

**Description:**
The agent analyzes a specific job posting (URL or text) against the student's profile and provides detailed fitment assessment.

**User Input:**
- Job posting URL or job description text
- Student profile (skills, experience, education, projects)

**Agent Process:**
1. Extract job requirements from posting
2. Compare against student profile:
   - Required skills vs. student's skills
   - Experience requirements vs. student's experience
   - Education requirements vs. student's education
   - Preferred qualifications assessment
3. Calculate overall fitment percentage
4. Identify matched skills and missing skills
5. Generate detailed fitment report

**Output:**
- Overall fitment percentage (e.g., 75%)
- Matched skills list (what student has)
- Missing skills list (what's needed)
- Experience gap analysis
- Education alignment assessment
- Recommendation (strong match, moderate match, weak match)

**Success Criteria:**
- ✅ Accurate fitment percentage calculation
- ✅ Clear identification of matched vs. missing skills
- ✅ Actionable recommendations
- ✅ Analysis completed in <2 minutes

---

### Use Case 3: Identify Skill Gaps and Improvement Recommendations

**Description:**
The agent identifies specific skill gaps for a target role and provides personalized recommendations for skill development.

**User Input:**
- Target job posting or role description
- Student's current profile
- Priority level (which companies/roles to focus on)

**Agent Process:**
1. Analyze job requirements
2. Compare with student's current skills
3. Identify skill gaps:
   - Critical missing skills (must-have)
   - Preferred missing skills (nice-to-have)
   - Skill level gaps (have skill but need improvement)
4. Prioritize gaps by importance and frequency across target roles
5. Generate improvement recommendations:
   - Specific skills to learn/improve
   - Learning resources or courses
   - Practice projects or exercises
   - Timeline for skill development

**Output:**
- Prioritized skill gap list
- Critical vs. preferred gaps
- Specific improvement recommendations
- Learning resources and timeline
- Impact assessment (how improving this skill increases fitment)

**Success Criteria:**
- ✅ Identifies all relevant skill gaps
- ✅ Prioritizes by importance
- ✅ Provides actionable recommendations
- ✅ Includes learning resources
- ✅ Shows impact of skill improvement

---

### Use Case 4: Compare Multiple Job Postings Side-by-Side

**Description:**
The agent compares multiple job postings (from same or different companies) to help student prioritize applications.

**User Input:**
- Multiple job posting URLs or descriptions
- Student profile
- Company priority levels

**Agent Process:**
1. Analyze each job posting individually
2. Calculate fitment for each
3. Compare across multiple dimensions:
   - Overall fitment percentage
   - Skills match comparison
   - Experience requirements comparison
   - Location and work arrangement
   - Company priority level
   - Growth potential
4. Generate comparative analysis
5. Rank jobs by recommendation priority

**Output:**
- Side-by-side comparison table
- Fitment scores for each job
- Key differences highlighted
- Recommendation ranking (best to apply first)
- Pros and cons for each position

**Success Criteria:**
- ✅ Accurate comparison across multiple jobs
- ✅ Clear ranking and recommendations
- ✅ Highlights key differences
- ✅ Considers company priority levels
- ✅ Helps prioritize application efforts

---

### Use Case 5: Generate Personalized Job Search Strategy

**Description:**
The agent analyzes student's profile across multiple target companies and generates a personalized job search strategy with recommendations.

**User Input:**
- Student profile (complete)
- Priority-based company list
- Career goals and preferences
- Timeline (when need to find job)

**Agent Process:**
1. Analyze profile against all priority companies
2. Identify best-fit roles across companies
3. Assess skill gaps across target roles
4. Generate strategic recommendations:
   - Which companies to focus on first
   - Which roles to target
   - Skills to develop before applying
   - Application timeline
   - Backup options
5. Create action plan

**Output:**
- Personalized job search strategy
- Recommended companies and roles (ranked)
- Skill development roadmap
- Application timeline
- Action items and next steps

**Success Criteria:**
- ✅ Comprehensive strategy covering all priorities
- ✅ Clear action plan
- ✅ Realistic timeline
- ✅ Prioritized recommendations
- ✅ Helps student focus efforts effectively

---

## Use Case Summary Table

| Use Case | Primary Function | Key Feature | Time Saved |
|----------|----------------|-------------|------------|
| 1. Search & Filter Jobs | Find matching jobs from company sites | Multi-criteria filtering | Hours → Minutes |
| 2. Analyze Job Fitment | Single job analysis | Detailed fitment assessment | 30 min → 2 min |
| 3. Identify Skill Gaps | Gap analysis | Personalized recommendations | Manual analysis → Automated |
| 4. Compare Multiple Jobs | Side-by-side comparison | Prioritization support | Hours → 10 min |
| 5. Generate Strategy | Strategic planning | Comprehensive roadmap | Days → 1 hour |

---

## Use Case Priority Mapping

**Priority 1 Companies:**
- Use Cases 1, 2, 3, 4, 5 (all use cases with detailed analysis)

**Priority 2 Companies:**
- Use Cases 1, 2, 3 (search, analysis, skill gaps)

**Priority 3 Companies:**
- Use Cases 1, 2 (search and basic analysis)

---

**Status:** ✅ Completed for TODO-003  
**Date:** 2025-11-29  
**Key Feature:** Use Case 1 includes multi-criteria job search from company sites (not just title matching)

