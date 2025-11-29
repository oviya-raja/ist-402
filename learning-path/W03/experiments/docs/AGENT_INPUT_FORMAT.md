# Agent Input Format Specification

## Overview

This document specifies the input format for the Job Fitment Analysis Agent. Students provide their profile information and company lists organized by priority levels.

## Student Profile Format

### JSON Format

```json
{
  "name": "Your Full Name",
  "email": "your.email@university.edu",
  "phone": "+1-555-0123",
  "location": "City, State/Country",
  
  "education": [
    {
      "degree": "Bachelor of Science",
      "field": "Computer Science",
      "institution": "University Name",
      "graduation_year": "2024",
      "gpa": "3.7"
    }
  ],
  
  "skills": [
    "Python", "Java", "JavaScript", "React", "Node.js",
    "SQL", "Git", "Docker", "AWS", "Machine Learning"
  ],
  
  "experience": [
    {
      "title": "Software Engineering Intern",
      "company": "Company Name",
      "duration": "3 months",
      "description": "Brief description of responsibilities"
    }
  ],
  
  "certifications": [
    "AWS Certified Cloud Practitioner",
    "Google Data Analytics Certificate"
  ],
  
  "projects": [
    {
      "name": "Project Name",
      "description": "Brief description",
      "technologies": "Tech1, Tech2, Tech3"
    }
  ],
  
  "preferences": {
    "location": "Preferred City or 'Remote'",
    "job_type": "Full-time",
    "salary_min": 100000,
    "willing_to_relocate": true
  }
}
```

## Company Priority List Format

### Priority Levels

| Priority | Description | Analysis Detail |
|----------|-------------|-----------------|
| **Priority 1** | Dream companies, highest interest | Detailed analysis with comprehensive recommendations |
| **Priority 2** | Strong interest companies | Standard analysis with key recommendations |
| **Priority 3** | Backup options, lower priority | Summary analysis with essential points |

### JSON Format

```json
{
  "priority_1": [
    {"name": "Google", "url": "https://careers.google.com/"},
    {"name": "Apple", "url": "https://jobs.apple.com/"},
    {"name": "Cisco", "url": "https://careers.cisco.com/"}
  ],
  
  "priority_2": [
    {"name": "Amazon", "url": "https://www.amazon.jobs/"},
    {"name": "Microsoft", "url": "https://careers.microsoft.com/"},
    {"name": "Meta", "url": "https://www.metacareers.com/"}
  ],
  
  "priority_3": [
    {"name": "Netflix", "url": "https://jobs.netflix.com/"},
    {"name": "NVIDIA", "url": "https://www.nvidia.com/careers/"},
    {"name": "Intel", "url": "https://jobs.intel.com/"}
  ]
}
```

## Job Search Keywords

Optionally, provide keywords to filter job searches:

```json
{
  "keywords": [
    "software engineer",
    "new grad",
    "entry level",
    "machine learning",
    "backend",
    "full stack"
  ],
  
  "exclude_keywords": [
    "senior",
    "principal",
    "director",
    "manager"
  ],
  
  "locations": [
    "San Francisco, CA",
    "Seattle, WA",
    "Remote"
  ]
}
```

## Complete Input Example

```json
{
  "profile": {
    "name": "Alex Johnson",
    "email": "alex.johnson@university.edu",
    "location": "San Francisco, CA",
    "education": [
      {
        "degree": "Bachelor of Science",
        "field": "Computer Science",
        "institution": "UC Berkeley",
        "graduation_year": "2024"
      }
    ],
    "skills": ["Python", "Java", "React", "AWS", "Machine Learning"],
    "experience": [
      {
        "title": "Software Engineering Intern",
        "company": "TechCorp",
        "duration": "3 months"
      }
    ],
    "certifications": ["AWS Cloud Practitioner"],
    "preferences": {
      "location": "Bay Area or Remote",
      "willing_to_relocate": true
    }
  },
  
  "companies": {
    "priority_1": [
      {"name": "Google", "url": "https://careers.google.com/"}
    ],
    "priority_2": [
      {"name": "Amazon", "url": "https://www.amazon.jobs/"}
    ],
    "priority_3": [
      {"name": "Netflix", "url": "https://jobs.netflix.com/"}
    ]
  },
  
  "search": {
    "keywords": ["software engineer", "new grad"],
    "locations": ["San Francisco", "Remote"]
  }
}
```

## Validation Rules

### Required Fields

- `profile.name` - Student's full name
- `profile.education` - At least one education entry
- `profile.skills` - At least 3 skills
- `companies.priority_1` - At least one Priority 1 company

### Skill Format

- Use standard industry terms
- Capitalize properly (e.g., "Python" not "python")
- Include both technical and soft skills
- List in order of proficiency

### Experience Duration

Use consistent formats:
- "3 months"
- "1 year"
- "6 months - ongoing"

## Output Format

The agent will return:

1. **Fitment Rankings** - Jobs ranked by fitment score and priority
2. **Skill Analysis** - Matched skills and gaps per job
3. **Recommendations** - Actionable steps for each opportunity
4. **Learning Roadmap** - Skills to develop with resources

See the generated `fitment_report.md` for complete analysis output.
