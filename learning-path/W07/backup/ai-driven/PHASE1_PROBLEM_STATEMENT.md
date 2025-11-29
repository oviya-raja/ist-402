# Phase 1.1: Problem Statement - Job Fitment Analysis Agent

## Problem Statement

**The Problem:**
Final year students struggle to efficiently identify and evaluate job opportunities that match their profile. The manual job search process is time-consuming and requires constant monitoring of multiple company job boards, analyzing job descriptions, and assessing personal fitment.

**Key Challenges:**
1. **Time-Consuming Manual Search:** Hours spent daily checking multiple company websites
2. **Fitment Assessment Difficulty:** Subjective and time-intensive manual comparison
3. **Skill Gap Identification:** Difficulty identifying specific areas to improve
4. **Inconsistent Evaluation:** Varying assessment approaches miss important requirements
5. **Information Overload:** Extensive job descriptions make quick decisions difficult

**The Solution:**
A Job Fitment Analysis Agent powered by OpenAI's Agent Builder that:
- **Searches company job sites** and finds jobs matching student's profile based on:
  - Skills match, experience level, education, location, department, job type
- **Accepts priority-based company lists** (Priority 1, 2, 3) for weighted analysis
- **Analyzes job postings** against student profile with priority-based weighting
- **Provides fitment percentage** and detailed match analysis (more detailed for Priority 1)
- **Identifies skill gaps** and improvement areas
- **Accesses knowledge base** with student profile, skills, experience, and company information
- **Delivers personalized recommendations** for skill development

**Primary Target Company Job Sites:**
1. Cisco - https://careers.cisco.com/global/en
2. SAP - https://jobs.sap.com/
3. Google - https://careers.google.com/jobs/
4. Apple - https://jobs.apple.com/
5. Amazon - https://www.amazon.jobs/
6. Tesla - https://www.tesla.com/careers

**Input Format:**
- **Priority 1:** Highest interest companies (detailed analysis)
- **Priority 2:** Moderate interest companies (standard analysis)
- **Priority 3:** Lower interest companies (summary analysis)

See `AGENT_INPUT_FORMAT.md` for complete input format specification.

**Expected Impact:**
- Reduced job search time from hours to minutes per posting
- Objective, consistent fitment analysis
- Clear identification of skill gaps
- Better targeting of applications to high-fit opportunities
- Improved preparation through focused skill development recommendations

---

**Status:** ✅ Completed  
**Date:** 2025-11-29  
**Focus Area:** Job Fitment Analysis - Matching job postings to student profile and identifying skill gaps
