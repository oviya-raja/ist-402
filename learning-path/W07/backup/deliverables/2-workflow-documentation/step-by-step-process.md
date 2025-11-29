# Step-by-Step Automation Process
## Job Fitment Analysis Agent

This document provides a detailed, numbered step-by-step process for the complete automation workflow.

---

## Complete Automation Process

### PHASE 1: Input Reception and Validation

#### Step 1: Receive User Input
- **Action:** Agent receives user query/input
- **Input Types:**
  - Company priorities (Priority 1, 2, 3 format)
  - Student profile (skills, experience, education, location)
  - Job posting (URL or description text)
  - Use case selection (explicit or implicit)

#### Step 2: Parse Input Components
- **Action:** Extract structured information from input
- **Components Extracted:**
  - Company names and priority levels
  - Student skills with proficiency levels
  - Experience details (years, internships, projects)
  - Education information (degree, field, institution)
  - Location preferences
  - Job posting details (if provided)

#### Step 3: Validate Company Names
- **Action:** Check company names against knowledge base
- **Validation Criteria:**
  - Company name exists in knowledge base
  - Company name is spelled correctly
  - Company has job posting information available
- **Decision Point:**
  - **If Valid:** Proceed to Step 4
  - **If Invalid/Typo:** Suggest corrections, ask for confirmation
  - **If Not in Knowledge Base:** Acknowledge limitation, provide general guidance

#### Step 4: Validate Profile Completeness
- **Action:** Check if required profile components are present
- **Required Components:**
  - Skills (at minimum)
  - Experience level
  - Education level
- **Decision Point:**
  - **If Complete:** Proceed to Step 5
  - **If Incomplete:** Request missing information or proceed with partial analysis

#### Step 5: Identify Use Case
- **Action:** Determine which of 5 use cases user needs
- **Use Case Identification:**
  - Use Case 1: Finding jobs (company priorities + profile)
  - Use Case 2: Checking qualification (job posting + profile)
  - Use Case 3: Identifying skill gaps (target role + profile)
  - Use Case 4: Comparing jobs (multiple postings + profile)
  - Use Case 5: Generating strategy (complete profile + priorities + timeline)
- **Decision Point:**
  - **If Clear:** Route to appropriate use case processing
  - **If Unclear:** Ask clarifying questions
  - **If Multiple:** Process sequentially

---

### PHASE 2: Knowledge Base Retrieval

#### Step 6: Activate File Search Tool
- **Action:** Trigger knowledge base retrieval
- **Trigger:** Automatic based on query context
- **Method:** Semantic search via File Search (Retrieval) tool

#### Step 7: Retrieve Company Information
- **Action:** Search for target company information
- **Files Searched:** `target-companies.txt`
- **Information Retrieved:**
  - Company overview
  - Typical job requirements
  - Common roles available
  - Company-specific notes

#### Step 8: Retrieve Job Analysis Framework
- **Action:** Get job posting analysis methodology
- **Files Searched:** `job-posting-structure.txt`
- **Information Retrieved:**
  - How to extract requirements
  - How to parse skills, experience, education
  - How to identify location preferences

#### Step 9: Retrieve Fitment Calculation Methodology
- **Action:** Get fitment calculation framework
- **Files Searched:** `calculation-methodology.txt`
- **Information Retrieved:**
  - Component weights (Required Skills 40%, Preferred 20%, etc.)
  - Calculation formulas
  - Priority-based weighting rules

#### Step 10: Retrieve Skill Gap Analysis Framework
- **Action:** Get skill gap identification methodology
- **Files Searched:** `gap-identification.txt`, `learning-resources.txt`
- **Information Retrieved:**
  - How to identify gaps (Critical, Important, Level)
  - How to prioritize gaps
  - Learning resources for each skill

#### Step 11: Retrieve Relevant Examples
- **Action:** Get use case examples for reference
- **Files Searched:** `use-case-1-example.txt` and other example files
- **Information Retrieved:**
  - Example interactions
  - Response format examples
  - Best practices

---

### PHASE 3: Processing and Analysis

#### Step 12: Extract Job Requirements (If Use Case 2, 4, or 5)
- **Action:** Parse job posting to extract requirements
- **Extraction Process:**
  - Identify required skills
  - Identify preferred skills
  - Extract experience requirements
  - Extract education requirements
  - Identify location and work arrangement
- **Data Transformation:** Unstructured text → Structured requirements

#### Step 13: Compare Student Profile Against Requirements
- **Action:** Match student skills, experience, education against job requirements
- **Comparison Process:**
  - **Skills Match:**
    - Count required skills student has
    - Count preferred skills student has
    - Identify missing skills
    - Assess skill proficiency levels
  - **Experience Match:**
    - Compare student experience vs. required experience
    - Calculate match percentage
  - **Education Match:**
    - Compare degree level
    - Compare field of study
    - Assess alignment
  - **Location Match:**
    - Compare preferences vs. job location
    - Assess work arrangement alignment

#### Step 14: Calculate Fitment Percentage
- **Action:** Apply fitment calculation methodology
- **Calculation Steps:**
  1. Calculate Required Skills Match: (student's required skills / total required) × 100
  2. Calculate Preferred Skills Match: (student's preferred skills / total preferred) × 100
  3. Calculate Experience Match: (student's years / required years) × 100 (capped at 100%)
  4. Calculate Education Match: 100% if match, 50% if lower degree, 75% if related field
  5. Calculate Location Match: 100% if match, 0% if mismatch
  6. Apply weights:
     - Required Skills: × 40%
     - Preferred Skills: × 20%
     - Experience: × 25%
     - Education: × 10%
     - Location: × 5%
  7. Sum weighted scores = Total Fitment Percentage
- **Priority Adjustment:** Apply priority-based weighting if applicable

#### Step 15: Identify Skill Gaps (If Use Case 3 or 5)
- **Action:** Determine what skills student is missing
- **Gap Identification:**
  - **Critical Gaps:** Missing required skills
  - **Important Gaps:** Missing preferred skills
  - **Level Gaps:** Skills at lower proficiency than required
- **Prioritization:**
  - Rank by importance (Critical > Important > Level Gap)
  - Consider frequency across multiple target roles
  - Assess learning difficulty and time

#### Step 16: Generate Learning Recommendations (If Use Case 3 or 5)
- **Action:** Create personalized learning plan
- **Recommendation Process:**
  - For each gap, retrieve learning resources from knowledge base
  - Estimate time to learn each skill
  - Create prioritized learning timeline
  - Assess impact of learning each skill on fitment

---

### PHASE 4: Response Generation

#### Step 17: Format Response Based on Use Case
- **Action:** Structure output according to use case type
- **Formatting Rules:**
  - **Use Case 1:** Job recommendations with fitment estimates, search guidance
  - **Use Case 2:** Fitment percentage, match breakdown, recommendation
  - **Use Case 3:** Skill gaps, learning plan, timeline
  - **Use Case 4:** Side-by-side comparison, ranking, recommendations
  - **Use Case 5:** Complete strategy, roadmap, timeline, action items

#### Step 18: Include Mental Health Benefits Messaging
- **Action:** Add messaging about reducing stress and search anxiety
- **Messaging Examples:**
  - "This will save you hours of searching"
  - "No more getting lost in endless job boards"
  - "One clear answer instead of constant searching"
  - "Focused results to reduce overwhelm"

#### Step 19: Provide Actionable Recommendations
- **Action:** Include clear next steps
- **Recommendation Types:**
  - Apply/Consider/Not Recommended (for job fitment)
  - Skills to learn first (for skill gaps)
  - Companies to focus on (for strategy)
  - Timeline and milestones

#### Step 20: Apply Personality and Tone
- **Action:** Ensure response is supportive, clear, and empathetic
- **Tone Guidelines:**
  - Supportive and encouraging
  - Clear and student-friendly
  - Action-oriented
  - Empathetic (acknowledges stress)

---

### PHASE 5: Output Delivery

#### Step 21: Deliver Response to User
- **Action:** Present formatted response
- **Output Format:**
  - Clear structure with sections
  - Fitment percentage prominently displayed
  - Match breakdown clearly explained
  - Recommendations highlighted
  - Next steps clearly listed

#### Step 22: Wait for User Follow-up (If Needed)
- **Action:** Monitor for additional questions or clarifications
- **Follow-up Scenarios:**
  - User asks for more details
  - User provides additional information
  - User requests different use case
  - User needs clarification

---

## Decision Points Summary

### Decision Point 1: Company Name Validation
- **Criteria:** Company exists in knowledge base
- **Branch 1:** Valid → Continue
- **Branch 2:** Invalid/Typo → Suggest corrections
- **Branch 3:** Not in KB → Acknowledge limitation

### Decision Point 2: Profile Completeness
- **Criteria:** Required components present
- **Branch 1:** Complete → Full analysis
- **Branch 2:** Incomplete → Request info or partial analysis

### Decision Point 3: Use Case Identification
- **Criteria:** Input clarity
- **Branch 1:** Clear → Route directly
- **Branch 2:** Unclear → Ask questions
- **Branch 3:** Multiple → Process sequentially

### Decision Point 4: Fitment Level
- **Criteria:** Calculated fitment percentage
- **Branch 1:** 90-100% → Strongly recommend
- **Branch 2:** 75-89% → Recommend
- **Branch 3:** 60-74% → Consider
- **Branch 4:** 45-59% → Not recommended
- **Branch 5:** <45% → Suggest alternatives

---

## Data Transformations

### Transformation 1: Input Text → Structured Data
- **Input:** Natural language text
- **Output:** Structured components (companies, skills, experience, etc.)
- **Method:** LLM parsing and extraction

### Transformation 2: Job Description → Requirements
- **Input:** Unstructured job posting text
- **Output:** Structured requirements (skills, experience, education, location)
- **Method:** Pattern matching and extraction using knowledge base framework

### Transformation 3: Profile + Requirements → Match Analysis
- **Input:** Student profile and job requirements
- **Output:** Match breakdown (matched/missing skills, experience alignment, etc.)
- **Method:** Comparison algorithm

### Transformation 4: Match Analysis → Fitment Percentage
- **Input:** Match breakdown
- **Output:** Single fitment percentage (0-100%)
- **Method:** Weighted calculation formula

### Transformation 5: Gaps → Learning Plan
- **Input:** Identified skill gaps
- **Output:** Prioritized learning plan with resources and timeline
- **Method:** Knowledge base retrieval and prioritization

---

## Optimization Notes

### Performance Optimization
1. **Efficient Knowledge Base:** Well-organized files for fast retrieval
2. **Semantic Search:** Optimized retrieval of relevant chunks
3. **Response Formatting:** Clear, concise responses
4. **Error Handling:** Quick error recovery

### User Experience Optimization
1. **Clear Instructions:** Helpful input format guidance
2. **Error Messages:** Supportive, not just error codes
3. **Response Clarity:** Easy to understand format
4. **Actionable Steps:** Clear next steps always provided

### Accuracy Optimization
1. **Comprehensive Knowledge Base:** Covers all essential topics
2. **Structured Methodology:** Consistent calculation approach
3. **Validation:** Input validation prevents errors
4. **Transparency:** Clear limitations stated

---

**Last Updated:** 2025-11-29  
**Version:** 1.0  
**Status:** Complete



