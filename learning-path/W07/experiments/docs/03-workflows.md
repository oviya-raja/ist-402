# Workflows to Automate

## Workflow 1: Job Search & Fitment Analysis

### Process Flow
1. **Trigger:** User provides profile (skills, experience, education) and target companies
2. **Action:** Agent validates input and loads target companies from CSV
3. **Action:** Agent searches company job sites for matching positions
4. **Decision Point:** Check if jobs were found
5. **Action:** Agent extracts job details from postings
6. **Action:** Agent analyzes each job posting against user profile
7. **Action:** Agent calculates fitment percentage and identifies skill gaps
8. **Action:** Agent ranks results by fitment score
9. **End:** Agent returns ranked list with fitment percentage and skill gaps

### Detailed Flow Breakdown

#### Trigger: User Input
- **Input Format:** JSON with profile object
- **Required Fields:** skills (array), experience (string), education (string)
- **Optional Fields:** target_companies (array), location_preference (string)
- **Validation:** Check for required fields, validate data types

#### Action: Load Companies
- **Data Source:** `target-companies.csv`
- **Filter:** Only active companies (status='active')
- **Priority:** Sort by priority_level for analysis depth
- **Output:** List of company objects with careers_url

#### Action: Search Job Sites
- **Method:** Web scraping using Playwright/BeautifulSoup
- **Input:** Company careers URLs
- **Process:** Navigate to job listings, filter by keywords from profile
- **Output:** List of job posting URLs and basic metadata

#### Decision Point: Jobs Found?
- **Condition:** Check if any jobs were returned
- **True Path:** Continue to Extract Job Details
- **False Path:** Return "No Results" message and end workflow

#### Action: Extract Job Details
- **Input:** Job posting URLs
- **Process:** Parse HTML to extract: title, description, requirements, skills, location, salary
- **Output:** Structured job objects

#### Action: Analyze Profile Match
- **Agent:** Profile Match Analysis Agent
- **Input:** Job requirements + user profile
- **Process:** Multi-criteria matching (skills, experience, education)
- **Output:** Match scores for each criteria

#### Action: Calculate Fitment
- **Formula:** `(matched_required_skills × 0.4) + (matched_preferred_skills × 0.2) + (experience_match × 0.2) + (education_match × 0.2)`
- **Output:** Fitment percentage (0-100%)

#### Action: Identify Skill Gaps
- **Process:** Compare required skills vs user skills
- **Output:** List of missing skills (required and preferred)

#### Action: Rank Results
- **Sort:** By fitment percentage (descending)
- **Weighting:** Apply company priority boost (+10% for Priority 1)
- **Limit:** Top 10 results
- **Output:** Ranked job list

### Automation Benefits
- **Time Reduction:** Reduces search time from hours to minutes
- **Objective Assessment:** Provides consistent, data-driven fitment evaluation
- **Skill Gap Identification:** Identifies specific areas needing improvement

### Interactive Workflow Diagram

📊 **[View All Workflows](workflow-diagrams/workflows.html)** - Interactive HTML diagrams with OpenAI Agent Builder implementation steps

The interactive diagrams show:
- Complete workflows with triggers, actions, and decision points
- Color-coded nodes (Green: Trigger/End, Blue: Agent, Orange: Condition, Purple: Action)
- Left-to-right flow matching OpenAI Agent Builder interface
- Step-by-step configuration instructions
- Click on any node for implementation notes
- Switch between workflows using tabs at the top

---

## Workflow 2: Job Qualification Check

### Process Flow
1. **Trigger:** User provides job posting URL and profile
2. **Decision Point:** Validate URL format and profile
3. **Action:** Agent fetches job posting content from URL
4. **Decision Point:** Verify job posting is accessible
5. **Action:** Agent extracts job requirements from posting
6. **Action:** Agent loads user profile from knowledge base
7. **Action:** Agent compares requirements with user profile
8. **Action:** Agent calculates fitment percentage
9. **Action:** Agent identifies matched skills and gaps
10. **Decision Point:** Generate recommendation based on fitment score
11. **End:** Agent returns fitment score, matched skills, missing qualifications, and recommendation

### Detailed Flow Breakdown

#### Trigger: Job URL Input
- **Input Format:** JSON with job_url (string) and profile (object)
- **Required Fields:** job_url, profile
- **Validation:** Check URL format, verify profile exists

#### Decision Point: Validate URL
- **Condition:** URL format is valid AND profile is provided
- **True Path:** Continue to Access Job Posting
- **False Path:** Return error message and end workflow

#### Action: Access Job Posting
- **Method:** Web scraping using Playwright/BeautifulSoup
- **Input:** Job posting URL
- **Process:** Fetch HTML content from URL
- **Error Handling:** Retry on failure, timeout after 30 seconds

#### Decision Point: Posting Accessible?
- **Condition:** Check if job posting content was successfully retrieved
- **True Path:** Continue to Extract Requirements
- **False Path:** Return "Access Error" message and end workflow

#### Action: Extract Requirements
- **Input:** Job posting HTML content
- **Process:** Parse to extract: required skills, preferred skills, experience level, education requirements, location
- **Output:** Structured requirements object

#### Action: Load User Profile
- **Data Source:** Knowledge base or input parameter
- **Process:** Retrieve user profile (skills, experience, education)
- **Output:** User profile object

#### Action: Compare Requirements
- **Agent:** Profile Comparison Agent
- **Input:** Job requirements + user profile
- **Process:** Match skills, compare experience levels, check education
- **Output:** Match results for each requirement category

#### Action: Calculate Fitment
- **Formula:** `(matched_required × 0.4) + (matched_preferred × 0.2) + (experience × 0.2) + (education × 0.2)`
- **Output:** Fitment percentage (0-100%)

#### Action: Identify Matches
- **Process:** List all matched skills and experience
- **Output:** Array of matched items with details

#### Action: Identify Gaps
- **Process:** List missing skills and qualifications
- **Output:** Array of gaps with priority (required vs preferred)

#### Decision Point: Generate Recommendation
- **Condition:** Fitment percentage thresholds
- **Branch 1 (≥80%):** "Recommend: Apply" - Strong match
- **Branch 2 (60-79%):** "Consider Applying" - Good match with some gaps
- **Branch 3 (<60%):** "Improve Skills First" - Significant gaps
- **Output:** Recommendation message with reasoning

### Automation Benefits
- **Quick Assessment:** 2 minutes vs 30 minutes manual analysis
- **Clear Recommendation:** Explicit guidance on whether to apply
- **Interview Preparation:** Identifies areas to improve before interview

### Interactive Workflow Diagram

📊 **[View All Workflows](workflow-diagrams/workflows.html)** - Switch to "Workflow 2" tab in the interactive diagram

See Workflow 1 description above for details on the interactive features.

---

## Data Flow

### Input Data
- **User Profile:** Skills, experience, education, preferences
- **Target Companies:** From CSV configuration file
- **Job URLs:** User-provided or agent-discovered

### Processing Data
- **Job Postings:** Extracted from company websites
- **Match Results:** Skills, experience, education comparisons
- **Fitment Scores:** Calculated percentages

### Output Data
- **Ranked Job List:** Sorted by fitment score
- **Fitment Analysis:** Percentages, matches, gaps
- **Recommendations:** Application guidance

## Decision Points

### Workflow 1 Decision Points
1. **Validate Input:** Check if profile has required fields
   - True: Continue to Load Companies
   - False: Return error and end
2. **Jobs Found?:** Check if any jobs were discovered
   - True: Continue to Extract Job Details
   - False: Return "No Results" and end

### Workflow 2 Decision Points
1. **Validate URL:** Check URL format and profile existence
   - True: Continue to Access Job Posting
   - False: Return error and end
2. **Posting Accessible?:** Verify job posting can be retrieved
   - True: Continue to Extract Requirements
   - False: Return "Access Error" and end
3. **Generate Recommendation:** Based on fitment percentage
   - ≥80%: "Recommend: Apply"
   - 60-79%: "Consider Applying"
   - <60%: "Improve Skills First"

## Error Handling Strategies

### Website Access Failures
- **Retry Logic:** 3 attempts with exponential backoff (1s, 2s, 4s)
- **Timeout:** 30 seconds per request
- **Fallback:** Return cached data if available
- **User Notification:** Clear error message with retry suggestion

### Invalid Input Handling
- **Validation:** Check required fields before processing
- **Error Messages:** Specific, actionable messages
- **Format Examples:** Provide input format examples in error

### Missing Data Scenarios
- **Partial Data:** Continue with available information
- **User Prompt:** Request missing critical information
- **Default Values:** Use sensible defaults where appropriate

### Rate Limiting
- **Respect Limits:** Implement delays between requests
- **Queue Management:** Process requests in batches
- **User Feedback:** Inform user of rate limit delays

## Workflow Optimization Notes

- **Caching:** Cache job postings to reduce API calls (24-hour TTL)
- **Batch Processing:** Process multiple jobs in parallel (max 5 concurrent)
- **Rate Limiting:** Respect website rate limits (1 request per 2 seconds)
- **Error Recovery:** Retry logic for failed website access (3 attempts)
- **Result Caching:** Store recent results for quick re-queries
- **Priority Processing:** Process Priority 1 companies first

---

**Status:** ✅ Complete  
**Last Updated:** 2025-11-29

