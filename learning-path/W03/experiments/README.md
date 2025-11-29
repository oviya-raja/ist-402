# Job Fitment Analysis Agent

An AI-powered system for analyzing job fitment and identifying skill gaps for final-year students.

## 🎯 Problem Solved

Final year students face significant challenges in efficiently identifying and evaluating job opportunities:

- **Time-Consuming Manual Search**: Hours spent checking multiple job boards
- **Fitment Assessment Difficulty**: Subjective comparison of skills vs requirements
- **Skill Gap Identification**: Struggle to identify areas needing improvement
- **Inconsistent Evaluation**: No systematic approach to assess job fit
- **Information Overload**: Too much data to analyze manually

## ✨ Solution

The Job Fitment Analysis Agent provides:

1. **Automated Job Matching**: Search company job sites and match to profile
2. **Fitment Scoring**: Precise percentage-based match analysis
3. **Skill Gap Analysis**: Identify missing skills with learning recommendations
4. **Priority-Based Analysis**: Detailed analysis for high-priority companies
5. **Actionable Recommendations**: Concrete steps to improve candidacy

## 🏗️ Architecture

The system follows a RAG (Retrieval-Augmented Generation) pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                   JOB FITMENT AGENT                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Objective 0: Environment Setup                             │
│      ↓                                                      │
│  Objective 1: System Prompt Design                          │
│      ↓                                                      │
│  Objective 2: Knowledge Base Generation                     │
│      ↓                                                      │
│  Objective 3: Vector Database (FAISS)                       │
│      ↓                                                      │
│  Objective 4: RAG Pipeline                                  │
│      ↓                                                      │
│  Objective 5: Fitment Scoring & Ranking                     │
│      ↓                                                      │
│  Objective 6: Report Generation                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Clone or download the repository
git clone <repository-url>
cd experiments

# Install dependencies
pip install -r requirements.txt

# Or run directly (auto-installs dependencies)
python main.py
```

### Basic Usage

```python
from src.job_fitment import JobFitmentAgent, create_sample_profile, create_sample_jobs

# Initialize the agent
agent = JobFitmentAgent()
agent.setup()

# Create or load your profile
profile = create_sample_profile()  # Or load your own

# Define jobs to analyze
jobs = create_sample_jobs()  # Or provide your own

# Run analysis
results = agent.analyze(profile, jobs)

# Access results
for result in results:
    print(f"{result.job.company}: {result.fitment_score}%")
```

### Custom Profile

```python
from src.job_fitment import StudentProfile

my_profile = StudentProfile(
    name="Your Name",
    email="your.email@university.edu",
    location="San Francisco, CA",
    education=[{
        "degree": "Bachelor of Science",
        "field": "Computer Science",
        "institution": "Your University",
        "graduation_year": "2024"
    }],
    skills=["Python", "Java", "React", "AWS", "Machine Learning"],
    experience=[{
        "title": "Software Engineering Intern",
        "company": "TechCorp",
        "duration": "3 months"
    }],
    certifications=["AWS Certified Cloud Practitioner"],
    preferences={
        "location": "Bay Area or Remote",
        "willing_to_relocate": True
    }
)
```

### Custom Jobs

```python
from src.job_fitment import JobPosting

custom_job = JobPosting(
    job_id="CUSTOM-001",
    title="Software Engineer",
    company="Dream Company",
    company_priority=1,  # 1 = highest priority
    location="Remote",
    requirements=["Python", "AWS", "Docker"],
    preferred_skills=["Kubernetes", "Machine Learning"],
    experience_level="Entry"
)
```

## 📊 Fitment Scoring

The agent uses weighted criteria for fitment calculation:

| Criteria | Weight | Description |
|----------|--------|-------------|
| Skills Match | 40% | Technical and soft skills alignment |
| Experience Match | 25% | Relevant work experience |
| Education Match | 20% | Degree and certifications |
| Location Match | 10% | Geographic preferences |
| Culture Fit | 5% | Company values alignment |

### Score Interpretation

| Score | Interpretation |
|-------|---------------|
| 80-100% | Excellent fit - High interview chances |
| 70-79% | Strong fit - Good alignment |
| 60-69% | Moderate fit - Some gaps to address |
| 50-59% | Weak fit - Significant skill gaps |
| <50% | Poor fit - Major gaps to address |

## 📁 Output Files

The agent generates:

```
data/job_fitment/
├── fitment_report.md      # Comprehensive analysis report
├── knowledge_base.json    # Generated Q&A pairs
├── system_prompt.txt      # AI system prompt
├── job_fitment.faiss      # Vector database
└── embeddings.npy         # Embedding vectors
```

## 🏢 Supported Companies

### Primary Target Companies

- **Cisco** - https://careers.cisco.com/
- **SAP** - https://jobs.sap.com/
- **Google** - https://careers.google.com/
- **Apple** - https://jobs.apple.com/
- **Amazon** - https://www.amazon.jobs/
- **Tesla** - https://www.tesla.com/careers

See `docs/TARGET_COMPANIES_JOB_SITES.md` for the full list of 40+ companies.

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Hugging Face token for model access
export HUGGINGFACE_HUB_TOKEN=your_token_here

# Optional: OpenAI API key for enhanced analysis
export OPENAI_API_KEY=your_key_here
```

### Priority Levels

When adding companies, assign priority levels:
- **Priority 1**: Dream companies (detailed analysis)
- **Priority 2**: Strong interest (standard analysis)
- **Priority 3**: Backup options (summary analysis)

## 🧪 Testing

```bash
# Run with sample data
python main.py

# Or in Python
from main import main
agent, results = main()
```

## 📐 Design Principles

The codebase follows:

- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution
- **KISS**: Keep It Simple, Stupid
- **DRY**: Don't Repeat Yourself
- **YAGNI**: You Aren't Gonna Need It

## 📚 Input Formats

See `docs/AGENT_INPUT_FORMAT.md` for detailed specifications on:
- Student profile JSON format
- Company priority list format
- Job search keywords

## 📁 Project Structure

The project is organized into a modular structure:

```
src/job_fitment/     # Main package with modular components
docs/                # Documentation files
examples/            # Example scripts
tests/               # Unit tests
main.py              # Entry point
```

See `PROJECT_STRUCTURE.md` for detailed structure documentation.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details.

## 🆘 Support

- Check the FAQ in the documentation
- Open an issue on GitHub
- Contact: support@example.com

## 🔜 Roadmap

- [ ] Real-time job board scraping
- [ ] LinkedIn integration
- [ ] Resume optimization suggestions
- [ ] Interview preparation module
- [ ] Salary negotiation insights
- [ ] Company culture analysis

---

**Built with ❤️ for final-year students seeking their dream jobs.**
