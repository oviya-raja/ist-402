# W7 Project: Job Fitment Analysis Agent

## 📋 Project Overview

**Project Name:** Job Fitment Analysis Agent  
**Technology:** OpenAI Agent Builder  
**Objective:** Automate job search and fitment analysis workflows for students

This project develops an AI agent using OpenAI Agent Builder to automate the job search and fitment analysis process for final year students. The agent searches company job sites, analyzes job postings against student profiles, and provides fitment percentages with skill gap identification.

---

## 🎯 Problem Statement

Final year students struggle to efficiently identify job opportunities matching their profile. Manual job search is time-consuming, requiring constant monitoring of multiple company job boards and subjective fitment assessment.

**Key Challenges:**
- Time-consuming manual search across multiple company websites
- Difficulty assessing job fitment objectively
- Hard to identify skill gaps for specific roles

**Solution:** An AI agent that automatically searches company job sites, analyzes job postings against student profiles, and provides fitment percentages with skill gap identification.

**Target Companies:** Configurable via CSV file (`docs/target-companies.csv`). Default: Cisco, SAP, Google, Apple, Amazon, Tesla

> 📄 **Detailed Problem Statement:** [docs/02-problem-statement.md](docs/02-problem-statement.md)

---

## 🔄 Workflows to Automate

### Workflow 1: Job Search & Fitment Analysis
User provides profile → Agent searches job sites → Analyzes postings → Returns ranked list with fitment scores

**Benefits:** Reduces search time from hours to minutes, provides objective assessment

### Workflow 2: Job Qualification Check
User provides job URL → Agent extracts requirements → Compares with profile → Returns fitment score and recommendations

**Benefits:** Quick assessment (2 min vs 30 min), clear application recommendations

> 📄 **Detailed Workflows:** [docs/03-workflows.md](docs/03-workflows.md) - Includes process flows, diagrams, and optimization notes

---

## 💼 Use Cases

1. **Find Matching Jobs** - Search company sites by skills/experience → Get ranked job list
2. **Check Qualification** - Analyze specific job posting → Get fitment percentage and skill gaps
3. **Compare Jobs** - Compare multiple postings → Get ranked recommendations

> 📄 **Detailed Use Cases:** [docs/04-use-cases.md](docs/04-use-cases.md) - Includes input/output examples and scenarios

---

## 🔌 Integration Points

**External Data Sources:**
- Company job posting websites (configurable via CSV)
- Knowledge base with student profiles and company information

**APIs and Services:**
- OpenAI Agent Builder for agent orchestration
- Web scraping tools (Playwright, BeautifulSoup)
- Knowledge base API for profile matching
- Analysis engine for fitment calculations

**Data Formats:** JSON input/output for profiles and job recommendations

> 📄 **Detailed Integration Points:** [docs/05-integration-points.md](docs/05-integration-points.md) - Includes CSV format, authentication methods, error handling strategies, and code examples

---

## 🤖 Agent Capabilities

**Core Capabilities:**
- Intelligent job matching (multi-criteria, fuzzy matching)
- Priority-based analysis (weighted by company priority)
- Context handling (profile persistence, session management)
- Error handling (graceful degradation, user-friendly messages)
- Multi-step execution (workflow orchestration, parallel processing)

> 📄 **Detailed Agent Capabilities:** [docs/06-agent-capabilities.md](docs/06-agent-capabilities.md) - Includes prompt engineering strategy, limitations, and testing approach

---

## 🎯 Project Scope

**Initial Implementation:**
- Focus on 2-3 companies (e.g., Cisco, Google)
- Implement Workflow 1 (Job Search & Fitment Analysis)
- Basic fitment calculation and knowledge base
- Use Cases 1 & 2

> 📄 **Detailed Project Scope:** [docs/07-project-scope.md](docs/07-project-scope.md) - Includes deliverables, success criteria, and future enhancements

---

## 📊 Assignment Alignment

✅ **Workflow identification and justification** - 2 workflows defined  
✅ **Integration points documentation** - APIs, data sources, authentication  
✅ **Agent capabilities** - 5 core capabilities with prompt engineering  
✅ **Project overview** - Clear problem statement and solution  
✅ **Use cases** - 3 practical use cases  
✅ **Project scope** - Realistic implementation plan

---

## 📚 Documentation Structure

For detailed information, see:

1. **[Project Overview](docs/01-project-overview.md)** - Project description
2. **[Problem Statement](docs/02-problem-statement.md)** - Problem, challenges, solution
3. **[Workflows](docs/03-workflows.md)** - Detailed workflow processes and optimization
4. **[Use Cases](docs/04-use-cases.md)** - Complete use case scenarios with examples
5. **[Integration Points](docs/05-integration-points.md)** - Technical details, CSV format, error handling
6. **[Agent Capabilities](docs/06-agent-capabilities.md)** - Capabilities, prompt engineering, testing
7. **[Project Scope](docs/07-project-scope.md)** - Implementation plan and enhancements

---

## 🚀 Setup Instructions

### Prerequisites
- OpenAI API account with access to Agent Builder
- OpenAI API key
- Access to company job posting websites (public access)
- CSV file editor for configuring target companies

### Step 1: Configure Target Companies
1. Open `docs/target-companies.csv`
2. Edit company list, priority levels, and status as needed
3. Save the CSV file

### Step 2: Set Up OpenAI Agent Builder
1. Go to [OpenAI Agent Builder](https://platform.openai.com/agent-builder/)
2. Create a new agent
3. Configure agent name: "Job Fitment Analysis Agent"
4. Set up API key in environment settings

### Step 3: Configure Agent Tools/Functions
1. Add web scraping tool (for job site access)
2. Add CSV reader tool (for company configuration)
3. Add knowledge base tool (for profile matching)
4. Configure analysis engine function

### Step 4: Set Up Knowledge Base
1. Create knowledge base with student profile templates
2. Add company information and job site structures
3. Configure profile matching rules

### Step 5: Test Agent
1. Test with sample profile input
2. Verify job search functionality
3. Verify fitment calculation
4. Check error handling

> 📄 **Detailed Setup Guide:** See workflow diagrams in `docs/workflow-diagrams/` for step-by-step OpenAI Agent Builder setup

### Alternative: Automated Workflow Creation

Instead of manual clickops, you can use the automation script:

```bash
# 1. Generate workflow definitions
python3 scripts/create_workflow_sdk.py --workflow both

# 2. Run automation (opens browser and creates workflows)
python3 scripts/agent_builder_automation.py --workflow both
```

**Note:** The automation script uses Playwright to automate Agent Builder UI. Some steps may require manual intervention. See `scripts/AUTOMATION_README.md` for details.

---

## 👥 Team Members

**Team Name:** [Your Team Name]

| Name | Role | Responsibilities |
|------|------|------------------|
| [Member 1 Name] | [Role, e.g., Lead Developer] | [Responsibilities, e.g., Agent development, workflow implementation] |
| [Member 2 Name] | [Role, e.g., Integration Specialist] | [Responsibilities, e.g., API integration, testing] |
| [Member 3 Name] | [Role, e.g., Documentation Lead] | [Responsibilities, e.g., Documentation, report preparation] |

**Team Roles:**
- **Agent Development:** [Who handles agent configuration and deployment]
- **Integration:** [Who handles API and tool integration]
- **Testing:** [Who handles testing and validation]
- **Documentation:** [Who handles documentation and reporting]

---

## 📄 PDF Generation

To combine all documents into a single PDF:

```bash
pandoc README.md docs/*.md -o PROJECT_DEFINITION.pdf
```

Or use markdown-to-PDF tools to combine README.md and docs/*.md files in order.

---

**Status:** ✅ Documentation Complete  
**Date:** 2025-11-29  
**Next Steps:** Implementation and testing
