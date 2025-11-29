# Job Fitment Analysis Agent - W7 Assignment

**Course:** IST402 - AI Agents, Retrieval-Augmented Generation (RAG), and Modern LLM Applications  
**Assignment:** Week 7 - OpenAI Agents Development  
**Project:** Job Fitment Analysis Agent using Knowledge Base  
**Status:** 🟢 Functional Agent Complete | 🟡 Documentation In Progress

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Prerequisites](#-prerequisites)
4. [Installation & Setup](#-installation--setup)
5. [Usage Examples](#-usage-examples)
6. [API Documentation](#-api-documentation)
7. [Project Structure](#-project-structure)
8. [Team Member Details](#-team-member-details)
9. [Contributing](#-contributing)
10. [License](#-license)
11. [Acknowledgments](#-acknowledgments)

---

## 🎯 Project Overview

The **Job Fitment Analysis Agent** is an AI-powered assistant built using OpenAI's Agent Builder that helps students analyze their fitment for job postings, identify skill gaps, and receive personalized job search guidance. The agent uses a knowledge base of 10 structured documents covering student profiles, job analysis, company information, fitment calculations, skill gaps, and use case examples.

### Problem Statement

Students struggle to:
- Understand how well they match job requirements
- Identify specific skills they need to develop
- Compare multiple job opportunities effectively
- Create personalized job search strategies

### Solution

An intelligent AI agent that:
- Analyzes job postings against student profiles
- Calculates fitment scores with detailed breakdowns
- Identifies skill gaps and provides learning recommendations
- Compares multiple jobs side-by-side
- Generates personalized 6-month job search strategies

---

## ✨ Features

### Core Capabilities

1. **Multi-Criteria Job Search** (Use Case 1)
   - Search and filter jobs by skills, experience, location, and target companies
   - Provides guidance for finding relevant roles
   - Estimates fitment for common positions

2. **Job Fitment Analysis** (Use Case 2)
   - Analyzes job postings against student profiles
   - Calculates fitment percentage (0-100%)
   - Provides detailed match breakdown
   - Identifies areas for improvement

3. **Skill Gap Identification** (Use Case 3)
   - Identifies missing critical and preferred skills
   - Prioritizes gaps by importance
   - Provides specific learning resources
   - Creates personalized learning timelines

4. **Job Comparison** (Use Case 4)
   - Compares multiple job postings side-by-side
   - Calculates fitment for each position
   - Applies priority-based weighting
   - Ranks jobs by recommendation

5. **Job Search Strategy** (Use Case 5)
   - Generates comprehensive 6-month strategies
   - Identifies best-fit roles across companies
   - Provides application timelines
   - Includes backup options

### Intelligent Features

- **Context-Aware Responses**: Understands student profiles, job requirements, and company priorities
- **Mental Health Support**: Encouraging and supportive tone throughout interactions
- **Actionable Recommendations**: Specific, measurable next steps for students
- **Knowledge Base Integration**: Uses 10 structured documents for accurate analysis

---

## 📋 Prerequisites

### Required

- **OpenAI Account**: Active account with API access
  - Paid account recommended (for GPT-4o access)
  - API key with sufficient credits
- **Python 3.8+**: For running test scripts (optional)
- **Web Browser**: For accessing OpenAI Platform

### Optional

- **Python Environment**: For local testing
  - `openai` Python package
  - Environment variables configured (`.env` file)

---

## 🚀 Installation & Setup

### Step 1: OpenAI Platform Setup

1. **Create OpenAI Account**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Sign up or log in
   - Navigate to API Keys section

2. **Create API Key**
   - Click "Create new secret key"
   - Name it (e.g., "W7 Assignment")
   - Copy and save the key securely

3. **Access Agent Builder**
   - Navigate to "Assistants" section
   - Click "Create" to start building your agent

### Step 2: Agent Configuration

1. **Set Agent Name**: "Job Fitment Analysis Agent"

2. **Configure Model**: Select GPT-4o

3. **Add System Prompt**:
   - Copy content from `deliverables/1-functional-agent/system-prompt.txt`
   - Paste into system instructions field

4. **Enable File Search Tool**:
   - Go to Tools section
   - Enable "File Search" / "Retrieval"

5. **Upload Knowledge Base Files**:
   - Navigate to Files section
   - Upload all 10 files from `knowledge-base/` directory:
     - `01-student-profiles/profile-template.txt`
     - `01-student-profiles/skills-taxonomy.txt`
     - `01-student-profiles/experience-levels.txt`
     - `02-job-analysis/job-posting-structure.txt`
     - `03-company-info/target-companies.txt`
     - `04-fitment-analysis/calculation-methodology.txt`
     - `04-fitment-analysis/interpretation-guide.txt`
     - `05-skill-gaps/gap-identification.txt`
     - `05-skill-gaps/learning-resources.txt`
     - `06-use-case-examples/use-case-1-example.txt`

6. **Save Agent**:
   - Click "Save" or "Create"
   - Note the Assistant ID for future reference

### Step 3: Local Testing (Optional)

1. **Clone Repository**:
   ```bash
   git clone https://github.com/oviya-raja/ist-402.git
   cd ist-402/learning-path/W07
   ```

2. **Set Up Environment**:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "OPENAI_ASSISTANT_ID=your_assistant_id_here" >> .env
   ```

3. **Install Dependencies**:
   ```bash
   pip install openai python-dotenv
   ```

4. **Run Tests**:
   ```bash
   cd deliverables/1-functional-agent/scripts
   python test_all_use_cases.py
   ```

### Detailed Setup Instructions

For complete step-by-step instructions, see:
- **Quick Start**: `BUILD_AGENT_NOW.md`
- **Detailed Guide**: `COMPLETE_BUILD_INSTRUCTIONS.md`
- **Printable Checklist**: `PRINTABLE_CHECKLIST.md`

---

## 💡 Usage Examples

### Example 1: Job Fitment Analysis

**Input:**
```
I found this job posting:

Title: Software Engineer II - Machine Learning Platform
Company: Google
Requirements:
- 3+ years experience in Python, Java, or C++
- Experience with ML frameworks (TensorFlow, PyTorch)
- Strong algorithms and data structures
- BS/MS in Computer Science

My profile:
- 2 years internship experience
- Skills: Python, TensorFlow, basic ML
- Education: BS Computer Science (graduating soon)

Can you analyze my fitment score and tell me what I need to improve?
```

**Expected Output:**
- Fitment score calculation (e.g., 72%)
- Detailed breakdown of matched skills
- Missing skills identification
- Specific improvement recommendations
- Learning resources and timeline

### Example 2: Skill Gap Analysis

**Input:**
```
I want to apply for a "Senior Data Scientist" position at Amazon.

My current skills:
- Python (intermediate)
- SQL (basic)
- Statistics (college level)
- Machine Learning (took one course)

What skills am I missing? What should I learn to be competitive?
```

**Expected Output:**
- Critical skill gaps identified
- Preferred skill gaps listed
- Prioritized learning recommendations
- Estimated time to learn each skill
- Impact on fitment score

### Example 3: Job Comparison

**Input:**
```
I'm considering two positions:

Job 1: Software Engineer at Google
- Focus: Backend systems, distributed systems
- Tech: Java, Python, Go
- Experience: 2+ years

Job 2: Software Engineer at Apple
- Focus: iOS development
- Tech: Swift, Objective-C
- Experience: 1+ years

My profile: 1 year experience, Python, JavaScript, some mobile dev

Can you compare these and tell me which is a better fit?
```

**Expected Output:**
- Fitment score for each job
- Side-by-side comparison
- Recommendation with justification
- Priority-based ranking

### More Examples

See `deliverables/1-functional-agent/test-cases.txt` for 10 comprehensive test cases.

---

## 🔌 API Documentation

### OpenAI Assistants API

The agent uses OpenAI's Assistants API for interaction.

#### Authentication

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

#### Create Thread

```python
thread = client.beta.threads.create()
```

#### Send Message

```python
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Your query here"
)
```

#### Run Assistant

```python
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=ASSISTANT_ID
)
```

#### Retrieve Response

```python
messages = client.beta.threads.messages.list(thread_id=thread.id)
assistant_messages = [m for m in messages.data if m.role == "assistant"]
response = assistant_messages[0].content[0].text.value
```

### Integration Points

1. **OpenAI Platform**
   - Endpoint: `https://api.openai.com/v1/assistants`
   - Authentication: API Key (Bearer token)
   - Request Format: JSON
   - Response Format: JSON

2. **Knowledge Base (File Search)**
   - Format: Text files (.txt)
   - Storage: OpenAI Vector Store
   - Retrieval: Automatic via File Search tool
   - Processing: Automatic embedding and indexing

3. **Model Configuration**
   - Model: GPT-4o
   - Context Window: 128k tokens
   - Temperature: Default (0.7)
   - Max Tokens: Default

### Rate Limits

- **API Requests**: Varies by tier
- **File Uploads**: 512MB per file, 100 files per assistant
- **Vector Store**: 1GB total storage

### Error Handling

The agent handles:
- Invalid queries gracefully
- Missing information with helpful guidance
- Ambiguous requests with clarification questions
- Off-topic questions with redirection

---

## 📁 Project Structure

```
W07/
├── ASSIGNMENT_README.md          # This file
├── W7_Assignment_Analysis_Prompt.md
├── W7_Assignment_TODO_Tracker.md
│
├── deliverables/
│   ├── 1-functional-agent/
│   │   ├── AGENT_CAPABILITIES.md
│   │   ├── AGENT_SETUP_GUIDE.md
│   │   ├── BUILD_CHECKLIST.md
│   │   ├── system-prompt.txt
│   │   ├── test-cases.txt
│   │   ├── VERIFICATION_CHECKLIST.md
│   │   └── scripts/
│   │       ├── test_all_use_cases.py
│   │       ├── test_agent_e2e.py
│   │       └── utils.py
│   │
│   ├── 2-workflow-documentation/
│   │   ├── workflow-overview.md
│   │   ├── step-by-step-process.md
│   │   ├── integration-points.md
│   │   ├── technical-specifications.md
│   │   └── workflow-diagrams/
│   │       ├── main-workflow.mmd
│   │       ├── decision-flow.mmd
│   │       └── error-handling-flow.mmd
│   │
│   ├── 3-github-repository/       # This repository
│   │
│   ├── 4-screenshots/
│   │   ├── agent-configuration/  # 9+ screenshots
│   │   ├── memory-settings/
│   │   └── tools-functions/
│   │
│   └── 5-final-report/
│       └── REPORT_TEMPLATE.md
│
└── knowledge-base/
    ├── 01-student-profiles/      # 3 files
    ├── 02-job-analysis/          # 1 file
    ├── 03-company-info/          # 1 file
    ├── 04-fitment-analysis/      # 2 files
    ├── 05-skill-gaps/            # 2 files
    └── 06-use-case-examples/     # 1 file
```

---

## 👤 Team Member Details

**Project Type:** Solo Assignment  
**Student Name:** [Your Name]  
**Student ID:** [Your ID]  
**Email:** [Your Email]  
**Role:** Full-Stack Developer & AI Engineer

### Responsibilities

- **Agent Design & Development**: Designed system prompt, configured agent, integrated knowledge base
- **Knowledge Base Creation**: Created 10 structured documents covering all domains
- **Testing & Validation**: Developed test scripts, validated all 5 use cases
- **Documentation**: Created workflow diagrams, technical specifications, setup guides
- **Report Writing**: Compiled final report with all deliverables

---

## 🤝 Contributing

This is a course assignment project. However, if you'd like to contribute improvements:

### Guidelines

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/improvement`
3. **Make Changes**: Follow existing code style and documentation standards
4. **Test Thoroughly**: Ensure all use cases still pass
5. **Update Documentation**: Update relevant docs if needed
6. **Submit Pull Request**: Describe changes clearly

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Reporting Issues

If you find issues or have suggestions:
1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Environment details

---

## 📄 License

This project is part of a course assignment for IST402. 

**License:** MIT License (or as specified by course requirements)

**Copyright:** © 2025 [Your Name]

---

## 🙏 Acknowledgments

### Resources Used

- **OpenAI**: For Agent Builder platform and GPT-4o model
- **IST402 Course**: For assignment framework and requirements
- **Penn State University**: For course materials and guidance

### Documentation References

- [OpenAI Assistants API Documentation](https://platform.openai.com/docs/assistants)
- [OpenAI Platform Guide](https://platform.openai.com/docs)
- [Agent Builder Documentation](https://platform.openai.com/docs/assistants/tools)

### Tools & Libraries

- **OpenAI Python SDK**: For API integration
- **Python-dotenv**: For environment variable management
- **Mermaid**: For workflow diagram creation

---

## 📊 Project Status

**Overall Completion:** 79% (79/100 points)

| Deliverable | Status | Completion |
|-------------|--------|------------|
| 1. Functional Agent | ✅ Complete | 100% |
| 2. Workflow Documentation | 🟡 In Progress | 90% |
| 3. GitHub Repository | 🟡 In Progress | 75% |
| 4. Screenshots | ✅ Complete | 100% |
| 5. Final PDF Report | 🟡 In Progress | 30% |

### Phase Completion

- ✅ Phase 1: Project Setup & Planning (100%)
- ✅ Phase 2: Build OpenAI Agent (100%)
- ✅ Phase 3: Testing & Refinement (100%)
- ✅ Phase 4: Workflow Documentation (100%)
- 🟡 Phase 5: GitHub Repository (36%)
- 🟡 Phase 6: Final PDF Report (4%)
- 🔴 Phase 7: Final Submission (0%)

---

## 📞 Contact

For questions about this project:
- **Email:** [Your Email]
- **GitHub:** [Your GitHub Profile]

---

**Last Updated:** 2025-11-29  
**Version:** 1.0.0

---

*This project is part of IST402 - AI Agents, RAG, and Modern LLM Applications course assignment.*

