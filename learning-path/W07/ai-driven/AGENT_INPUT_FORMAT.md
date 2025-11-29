# Agent Input Format Specification

## Company Priority Input Format

The Job Fitment Analysis Agent accepts company lists organized by priority levels. This allows students to specify which companies they're most interested in, enabling the agent to focus analysis accordingly.

### Input Format Structure

```
Priority 1:
- Company Name 1
- Company Name 2
- Company Name 3

Priority 2:
- Company Name 4
- Company Name 5

Priority 3:
- Company Name 6
- Company Name 7
- Company Name 8
```

### Example Input

```
Priority 1:
- Cisco
- Google
- Apple

Priority 2:
- Amazon
- Tesla

Priority 3:
- SAP
```

### Format Rules

1. **Priority Levels:** Use "Priority 1", "Priority 2", "Priority 3", etc.
2. **Company Names:** Use exact company names as they appear in the target companies list
3. **Case Sensitivity:** Company names are case-insensitive (Cisco = cisco = CISCO)
4. **Multiple Companies:** Can list multiple companies per priority level
5. **Flexible Priority Levels:** Can use Priority 1, 2, 3, or more levels as needed

### Agent Processing

**How the Agent Handles Priority:**

1. **Priority 1 Companies:**
   - Highest focus for job matching
   - Detailed fitment analysis
   - Comprehensive skill gap identification
   - Priority in search results

2. **Priority 2 Companies:**
   - Moderate focus
   - Standard fitment analysis
   - Skill gap identification included

3. **Priority 3 Companies:**
   - Lower focus
   - Basic fitment analysis
   - Summary-level skill gap identification

### Alternative Input Formats

**Simple List (No Priority):**
If no priority is specified, agent treats all companies equally:
```
Companies:
- Cisco
- Google
- Apple
- Amazon
- Tesla
- SAP
```

**Single Priority:**
If only one priority level is provided:
```
Priority 1:
- Cisco
- Google
- Apple
```

### Input Validation

The agent will:
- ✅ Validate company names against known target companies list
- ✅ Suggest corrections for misspelled company names
- ✅ Warn if company is not in the target list
- ✅ Accept partial matches (e.g., "Google" matches "Google Inc.")

### Integration with Knowledge Base

The agent's knowledge base should include:
- Complete list of target companies with job posting URLs
- Company-specific information (industry, size, culture)
- Common job roles and requirements per company
- Historical job posting patterns

### Example Agent Interaction

**User Input:**
```
I want to analyze job fitment for these companies:

Priority 1:
- Cisco
- Google

Priority 2:
- Apple
- Amazon

Priority 3:
- Tesla
- SAP
```

**Agent Response:**
```
I'll analyze job fitment for your prioritized company list:

Priority 1 (High Focus):
- Cisco (https://careers.cisco.com/global/en)
- Google (https://careers.google.com/jobs/)

Priority 2 (Moderate Focus):
- Apple (https://jobs.apple.com/)
- Amazon (https://www.amazon.jobs/)

Priority 3 (Standard Focus):
- Tesla (https://www.tesla.com/careers)
- SAP (https://jobs.sap.com/)

Please provide:
1. Your job posting URL or job description text
2. Your profile (skills, experience, education)

I'll provide detailed fitment analysis with priority weighting.
```

---

**Last Updated:** 2025-11-29  
**Purpose:** Define input format for Job Fitment Analysis Agent

