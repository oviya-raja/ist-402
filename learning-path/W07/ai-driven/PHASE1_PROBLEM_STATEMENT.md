# Phase 1.1: Problem Statement - Job Fitment Analysis Agent

## Problem Statement

**The Problem:**
Final year students face significant challenges in efficiently identifying and evaluating job opportunities that match their profile. The job search process is time-consuming and requires constant monitoring of multiple company job boards, analyzing job descriptions, and assessing personal fitment. Students struggle with:
- Identifying which job postings align with their skills and experience
- Understanding skill gaps and areas that need improvement for specific roles
- Efficiently tracking job postings from their target companies
- Determining their fitment percentage for each position

**Current Challenges:**
1. **Time-Consuming Manual Search:** Students spend hours daily checking multiple company websites and job boards for new postings that match their profile.
2. **Fitment Assessment Difficulty:** Manually comparing job requirements with personal skills and experience is subjective and time-intensive.
3. **Skill Gap Identification:** Students struggle to identify specific areas they need to refresh or improve to qualify for desired positions.
4. **Inconsistent Evaluation:** Without a systematic approach, fitment assessment varies and may miss important requirements.
5. **Information Overload:** Job descriptions contain extensive information that needs to be analyzed against personal profile, making quick decisions difficult.

**The Solution:**
A Job Fitment Analysis Agent powered by OpenAI's Agent Builder that:
- Accepts company lists organized by priority levels (Priority 1, Priority 2, Priority 3, etc.) - see `AGENT_INPUT_FORMAT.md` for format specification
- Analyzes job postings from target companies against student profile with priority-based weighting
- Searches within publicly available company job posting websites (see `TARGET_COMPANIES_JOB_SITES.md` for list)
- Provides fitment percentage and detailed match analysis (more detailed for Priority 1 companies)
- Identifies specific skill gaps and areas requiring improvement
- Accesses a knowledge base containing student profile, skills, experience, and target company information
- Delivers personalized recommendations for skill development prioritized by company interest level

**Primary Target Company Job Sites:**
The agent will search within these publicly available job posting sites:
1. **Cisco** - https://careers.cisco.com/global/en
2. **SAP** - https://jobs.sap.com/
3. **Google** - https://careers.google.com/jobs/
4. **Apple** - https://jobs.apple.com/
5. **Amazon** - https://www.amazon.jobs/
6. **Tesla** - https://www.tesla.com/careers

**Input Format:**
Students provide company lists organized by priority:
- **Priority 1:** Highest interest companies (detailed analysis)
- **Priority 2:** Moderate interest companies (standard analysis)
- **Priority 3:** Lower interest companies (summary analysis)

See `AGENT_INPUT_FORMAT.md` for complete input format specification.

**Additional Companies:**
The knowledge base also includes 40+ other major companies (full list in `TARGET_COMPANIES_JOB_SITES.md`) for comprehensive coverage.

**Expected Impact:**
- Reduced job search time from hours to minutes per posting
- Objective, consistent fitment analysis for each position
- Clear identification of skill gaps and improvement areas
- Better targeting of applications to high-fit opportunities
- Improved preparation through focused skill development recommendations

---

**Status:** ✅ Completed for TODO-001 (Updated based on user feedback)  
**Date:** 2025-11-29  
**Focus Area:** Job Fitment Analysis - Matching job postings to student profile and identifying skill gaps

