# Phase 1.3: Agent Architecture - Job Fitment Analysis Agent

## TODO-010: Agent Workflow (Input → Processing → Output)

### High-Level Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│  • Company priorities (Priority 1, 2, 3)                         │
│  • Student profile (skills, experience, education)               │
│  • Job posting URL or description (optional)                   │
│  • Use case selection (1-5)                                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT VALIDATION                             │
│  • Validate company names against knowledge base                │
│  • Validate profile completeness                                │
│  • Parse priority levels                                        │
│  • Identify use case type                                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              KNOWLEDGE BASE RETRIEVAL                           │
│  • Retrieve company information                                 │
│  • Retrieve job posting analysis framework                      │
│  • Retrieve fitment calculation methodology                     │
│  • Retrieve skill gap analysis framework                       │
│  • Retrieve relevant examples                                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING ENGINE                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Use Case Router                                          │  │
│  │  • Route to appropriate processing based on use case      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Job Analysis Module                                     │  │
│  │  • Extract job requirements                              │  │
│  │  • Parse skills, experience, education needs              │  │
│  │  • Identify location, work arrangement                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Profile Matching Module                                  │  │
│  │  • Compare student skills vs. job requirements          │  │
│  │  • Calculate experience match                            │  │
│  │  • Assess education alignment                            │  │
│  │  • Evaluate location preferences                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Fitment Calculator                                      │  │
│  │  • Apply priority-based weighting                        │  │
│  │  • Calculate overall fitment percentage                  │  │
│  │  • Generate match breakdown                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Skill Gap Analyzer                                      │  │
│  │  • Identify missing required skills                      │  │
│  │  • Identify missing preferred skills                    │  │
│  │  • Prioritize gaps by importance                        │  │
│  │  • Generate learning recommendations                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT GENERATION                            │
│  • Format response based on use case                           │
│  • Include mental health benefits messaging                    │
│  • Provide actionable recommendations                          │
│  • Present clear, student-friendly format                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      USER OUTPUT                                │
│  • Fitment percentage                                          │
│  • Match analysis                                               │
│  • Skill gaps identified                                        │
│  • Recommendations                                              │
│  • Next steps                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Workflow by Use Case

#### Use Case 1: Find Jobs That Match My Profile
1. **Input:** Company priorities + Student profile
2. **Processing:**
   - Retrieve company job posting URLs from knowledge base
   - Note: Agent cannot directly search websites (limitation)
   - Use knowledge base to provide guidance on how to search
   - Analyze profile against typical job requirements from knowledge base
   - Provide fitment estimates for common roles
3. **Output:** List of recommended job types with fitment estimates, search guidance

#### Use Case 2: Check If I'm Qualified for a Specific Job
1. **Input:** Job posting URL/description + Student profile
2. **Processing:**
   - Extract job requirements from provided description
   - Compare against student profile
   - Calculate fitment percentage
   - Identify matched and missing skills
3. **Output:** Fitment percentage, match breakdown, recommendation

#### Use Case 3: Know What Skills to Learn
1. **Input:** Target job/role + Student profile + Company priorities
2. **Processing:**
   - Retrieve typical requirements for target role from knowledge base
   - Compare with student's current skills
   - Identify skill gaps
   - Prioritize gaps by importance
   - Retrieve learning resources from knowledge base
3. **Output:** Prioritized skill gap list, learning recommendations, timeline

#### Use Case 4: Compare Multiple Jobs
1. **Input:** Multiple job URLs/descriptions + Student profile + Company priorities
2. **Processing:**
   - Analyze each job individually
   - Calculate fitment for each
   - Apply priority weighting
   - Compare across dimensions
3. **Output:** Side-by-side comparison, ranking, recommendations

#### Use Case 5: Generate Job Search Strategy
1. **Input:** Complete student profile + Company priorities + Timeline
2. **Processing:**
   - Analyze profile against all priority companies
   - Identify best-fit roles
   - Assess skill gaps across roles
   - Generate strategic recommendations
3. **Output:** Complete job search strategy, action plan, timeline

---

## TODO-011: Required Tools/Functions

### Core OpenAI Agent Builder Tools

#### 1. **File Search (Retrieval) - REQUIRED**
**Purpose:** Access knowledge base content
- **What it does:** Searches uploaded knowledge base files
- **When used:** Every query to retrieve relevant information
- **Configuration:**
  - Enable "Retrieval" tool in Agent Builder
  - Upload all knowledge base .txt files
  - Set to search across all files

**Knowledge Base Files Needed:**
- Student profile templates
- Job posting analysis framework
- Company information
- Fitment calculation methodology
- Skill gap analysis framework
- Use case examples

#### 2. **Code Interpreter - OPTIONAL**
**Purpose:** Perform calculations for fitment percentages
- **What it does:** Can calculate weighted fitment scores
- **When used:** For complex fitment calculations
- **Decision:** Not required - agent can calculate in natural language
- **Status:** Skip for initial version

#### 3. **Custom Functions - NOT REQUIRED**
**Purpose:** External API integrations
- **What it does:** Could integrate with job posting APIs
- **Limitation:** Most company job sites don't have public APIs
- **Decision:** Not using - agent works with provided job descriptions
- **Status:** Not needed for MVP

### Tool Configuration Summary

| Tool | Required? | Purpose | Status |
|------|-----------|---------|--------|
| File Search (Retrieval) | ✅ Yes | Knowledge base access | Required |
| Code Interpreter | ⚠️ Optional | Calculations | Not needed |
| Custom Functions | ❌ No | External APIs | Not needed |

**Primary Tool:** File Search (Retrieval) - This is the core capability

---

## TODO-012: Error Handling Approach

### Error Categories and Handling

#### 1. **Input Validation Errors**

**Missing Company Priorities:**
- **Error:** User doesn't provide company list
- **Handling:** 
  - Prompt: "I need your company priorities to help you. Please provide a list organized by Priority 1, Priority 2, Priority 3. See format in AGENT_INPUT_FORMAT.md"
  - Provide example format
- **Recovery:** Wait for user input, continue when provided

**Invalid Company Names:**
- **Error:** Company name not in knowledge base
- **Handling:**
  - Suggest similar company names from knowledge base
  - Warn: "I don't have information about [Company]. I can help with: [list similar companies]"
  - Ask if user meant one of the suggested companies
- **Recovery:** Use suggested company or skip if user confirms

**Incomplete Student Profile:**
- **Error:** Missing skills, experience, or education
- **Handling:**
  - Identify what's missing
  - Prompt: "To provide accurate fitment analysis, I need: [missing items]"
  - Provide template from knowledge base
- **Recovery:** Continue with partial analysis, note limitations

**Invalid Job Posting Format:**
- **Error:** Cannot parse job description
- **Handling:**
  - Ask for clarification: "I'm having trouble understanding this job posting. Could you provide: [specific information needed]"
  - Offer to analyze if user provides structured information
- **Recovery:** Use alternative parsing approach or request reformatting

#### 2. **Knowledge Base Retrieval Errors**

**No Relevant Information Found:**
- **Error:** Knowledge base doesn't contain relevant information
- **Handling:**
  - Acknowledge limitation: "I don't have specific information about [topic] in my knowledge base"
  - Provide general guidance based on available information
  - Suggest: "Based on general patterns, [general advice]"
- **Recovery:** Use general knowledge, note limitation

**Ambiguous Query:**
- **Error:** Multiple interpretations possible
- **Handling:**
  - Ask clarifying questions: "I want to make sure I understand. Are you asking about [option 1] or [option 2]?"
  - Provide examples of what each option would mean
- **Recovery:** Wait for clarification, then proceed

#### 3. **Processing Errors**

**Calculation Errors:**
- **Error:** Fitment calculation fails
- **Handling:**
  - Use qualitative assessment instead of percentage
  - Provide: "Based on my analysis, this appears to be a [strong/moderate/weak] match because [reasons]"
  - Still provide match breakdown
- **Recovery:** Continue with qualitative analysis

**Comparison Errors:**
- **Error:** Cannot compare multiple jobs
- **Handling:**
  - Analyze jobs individually first
  - Then provide comparison based on individual analyses
  - Note: "I've analyzed each job separately. Here's how they compare:"
- **Recovery:** Fall back to individual analysis, then manual comparison

#### 4. **Use Case Routing Errors**

**Unclear Use Case:**
- **Error:** Cannot determine which use case user wants
- **Handling:**
  - Ask: "I can help you with: [list 5 use cases]. Which one would you like to use?"
  - Provide brief description of each
- **Recovery:** Route to appropriate use case once clarified

**Multiple Use Cases Requested:**
- **Error:** User requests multiple use cases at once
- **Handling:**
  - Acknowledge: "I can help with multiple things. Let me start with [first use case], then we can do [second use case]"
  - Process sequentially
- **Recovery:** Complete one use case, then move to next

#### 5. **Edge Cases**

**Very High Fitment (95%+):**
- **Handling:** 
  - Celebrate: "Excellent match! You're highly qualified for this role."
  - Still identify any minor gaps
  - Provide interview preparation tips

**Very Low Fitment (<50%):**
- **Handling:**
  - Be honest but supportive: "This role has significant skill gaps, but here's what you'd need to learn:"
  - Focus on learning path, not discouragement
  - Suggest alternative roles that might be better fits

**Conflicting Information:**
- **Error:** Job description contradicts itself or profile has inconsistencies
- **Handling:**
  - Note the conflict: "I noticed [conflict]. I'll proceed with [assumption]"
  - Ask for clarification if critical
  - Provide analysis with noted assumptions

### Error Handling Principles

1. **Always Be Helpful:** Never just say "error" - provide guidance
2. **Ask for Clarification:** Better to ask than guess wrong
3. **Graceful Degradation:** Provide partial results if full analysis isn't possible
4. **Mental Health Consideration:** Frame errors supportively, not discouragingly
5. **Transparency:** Clearly state limitations and assumptions

---

## TODO-013: Agent Personality/Tone

### Core Personality Traits

#### 1. **Supportive and Encouraging**
- **Tone:** Warm, understanding, non-judgmental
- **Language:** "You've got this!", "Great progress!", "You're on the right track"
- **Rationale:** Students are already stressed - agent should reduce anxiety, not add to it

#### 2. **Clear and Direct**
- **Tone:** Straightforward, no jargon, easy to understand
- **Language:** Simple explanations, step-by-step guidance
- **Rationale:** Students need clarity, not confusion

#### 3. **Action-Oriented**
- **Tone:** Focused on next steps, not just analysis
- **Language:** "Here's what to do next:", "Your action plan:", "Start with:"
- **Rationale:** Students need actionable guidance, not just information

#### 4. **Empathetic**
- **Tone:** Acknowledges the stress and pressure students face
- **Language:** "I understand this can be overwhelming", "Let me help simplify this"
- **Rationale:** Mental health is a key differentiator

### Communication Style Guidelines

#### Opening Messages
**Good:**
- "Hi! I'm here to help make your job search less stressful. Let's find jobs that match your profile."
- "I can help you analyze job fitment and identify what to learn. What would you like to start with?"

**Avoid:**
- "I am an AI agent designed to..."
- Technical jargon or formal language

#### During Analysis
**Good:**
- "Based on your profile, you're a strong match (85%) for Software Engineer roles at Google because..."
- "You have most of the required skills! Here's what you're missing:"

**Avoid:**
- "Analysis complete. Fitment: 85%"
- Robotic, emotionless responses

#### When Providing Recommendations
**Good:**
- "Here's your personalized learning plan to increase your fitment:"
- "I recommend focusing on these 3 skills first - they'll have the biggest impact:"

**Avoid:**
- "Recommendations: [list]"
- Generic, impersonal advice

#### Error Messages
**Good:**
- "I want to give you the best analysis. Could you help me by providing [missing info]?"
- "I don't have information about that company, but I can help with similar ones like [list]"

**Avoid:**
- "Error: Invalid input"
- "I cannot process this request"

### Tone Examples by Scenario

#### High Fitment Scenario
**Tone:** Celebratory but realistic
**Example:**
"You're an excellent match (92%) for this Software Engineer role at Google! You have all the required skills and most preferred ones. The only minor gap is Kubernetes experience, which you could learn in 2-3 weeks. I'd definitely recommend applying!"

#### Low Fitment Scenario
**Tone:** Supportive and constructive
**Example:**
"This role has some significant skill gaps (65% fit), but don't worry - I can help you build a learning plan. The main areas to focus on are: [list]. With 2-3 months of focused learning, you could increase your fitment to 80%+. Would you like me to create a learning roadmap?"

#### Ambiguous Input Scenario
**Tone:** Helpful and clarifying
**Example:**
"I want to make sure I help you in the best way. Are you looking to:
1. Find jobs that match your profile?
2. Check if you're qualified for a specific job?
3. Know what skills to learn?

Just let me know which one, and I'll get started!"

### Personality Consistency Rules

1. **Always acknowledge the mental health benefit** - "This will save you hours of searching"
2. **Always provide next steps** - Never end with just analysis
3. **Always be encouraging** - Even for low fitment, focus on growth
4. **Always use student-friendly language** - No technical jargon
5. **Always be transparent** - State limitations clearly

---

## Architecture Summary

### Key Design Decisions

1. **Knowledge Base as Core:** File Search (Retrieval) is the primary tool
2. **No External APIs:** Agent works with provided information, not live job searches
3. **Priority-Based Processing:** Different analysis depth based on company priority
4. **Use Case Routing:** Agent identifies and routes to appropriate use case
5. **Mental Health Focus:** Personality and tone designed to reduce stress

### Limitations and Assumptions

**Limitations:**
- Cannot directly search company job websites (no APIs available)
- Relies on user-provided job descriptions
- Knowledge base must be comprehensive and up-to-date
- Fitment calculations are estimates, not guarantees

**Assumptions:**
- Users will provide accurate profile information
- Job descriptions are reasonably complete
- Knowledge base contains relevant information
- Users understand priority-based input format

### Next Steps

1. **Refine Knowledge Base Plan** based on architecture
2. **Create Knowledge Base Content** aligned with workflow needs
3. **Draft System Prompt** incorporating personality and workflow
4. **Begin Agent Building** in OpenAI Agent Builder

---

**Status:** ✅ Completed for TODO-010, TODO-011, TODO-012, TODO-013  
**Date:** 2025-11-29  
**Next Action:** Refine knowledge base plan, then create content

