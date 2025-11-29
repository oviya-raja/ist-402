"""
Sample data generators for testing.
"""

from typing import List
from .models import StudentProfile, JobPosting


def create_sample_profile() -> StudentProfile:
    """Create a sample student profile for testing."""
    return StudentProfile(
        name="Alex Johnson",
        email="alex.johnson@university.edu",
        phone="+1-555-0123",
        location="San Francisco, CA",
        education=[{
            "degree": "Bachelor of Science",
            "field": "Computer Science",
            "institution": "University of California, Berkeley",
            "graduation_year": "2024",
            "gpa": "3.7"
        }],
        skills=[
            "Python", "Java", "JavaScript", "React", "Node.js",
            "SQL", "Git", "Docker", "AWS", "Machine Learning",
            "Data Structures", "Algorithms", "REST APIs"
        ],
        experience=[
            {
                "title": "Software Engineering Intern",
                "company": "TechStartup Inc.",
                "duration": "3 months",
                "description": "Developed REST APIs using Python and Flask"
            },
            {
                "title": "Research Assistant",
                "company": "UC Berkeley AI Lab",
                "duration": "6 months",
                "description": "Worked on NLP projects using PyTorch"
            }
        ],
        certifications=[
            "AWS Certified Cloud Practitioner",
            "Google Data Analytics Certificate"
        ],
        projects=[
            {
                "name": "E-commerce Platform",
                "description": "Full-stack web app with React and Node.js",
                "technologies": "React, Node.js, MongoDB, AWS"
            },
            {
                "name": "ML Sentiment Analyzer",
                "description": "NLP model for social media sentiment",
                "technologies": "Python, PyTorch, BERT"
            }
        ],
        preferences={
            "location": "San Francisco, CA or Remote",
            "job_type": "Full-time",
            "salary_min": 100000,
            "willing_to_relocate": True
        }
    )


def create_sample_jobs() -> List[JobPosting]:
    """Create sample job postings for testing."""
    return [
        JobPosting(
            job_id="GOOG-001",
            title="Software Engineer, New Grad",
            company="Google",
            company_priority=1,
            location="Mountain View, CA",
            job_type="Full-time",
            description="Join Google as a new grad software engineer.",
            requirements=["Python", "Java", "Data Structures", "Algorithms", "SQL"],
            preferred_skills=["Machine Learning", "Distributed Systems", "Kubernetes"],
            experience_level="Entry",
            education_requirements=["BS in Computer Science or related field"],
            url="https://careers.google.com/"
        ),
        JobPosting(
            job_id="AMZN-001",
            title="Software Development Engineer I",
            company="Amazon",
            company_priority=2,
            location="Seattle, WA",
            job_type="Full-time",
            description="Build and operate massively scalable systems.",
            requirements=["Java", "Python", "AWS", "Data Structures", "Algorithms"],
            preferred_skills=["Docker", "Kubernetes", "CI/CD"],
            experience_level="Entry",
            education_requirements=["BS/MS in Computer Science"],
            url="https://www.amazon.jobs/"
        ),
        JobPosting(
            job_id="MSFT-001",
            title="Software Engineer",
            company="Microsoft",
            company_priority=2,
            location="Redmond, WA or Remote",
            job_type="Full-time",
            description="Build next-generation cloud solutions.",
            requirements=["C#", "Python", "Azure", "SQL", "Git"],
            preferred_skills=["Machine Learning", "TypeScript", "React"],
            experience_level="Entry",
            education_requirements=["BS in Computer Science or equivalent"],
            url="https://careers.microsoft.com/"
        ),
        JobPosting(
            job_id="AAPL-001",
            title="Software Engineer - Machine Learning",
            company="Apple",
            company_priority=1,
            location="Cupertino, CA",
            job_type="Full-time",
            description="Work on cutting-edge ML applications.",
            requirements=["Python", "Machine Learning", "Deep Learning", "TensorFlow"],
            preferred_skills=["PyTorch", "Computer Vision", "NLP", "Swift"],
            experience_level="Entry",
            education_requirements=["BS/MS in CS, ML, or related field"],
            url="https://jobs.apple.com/"
        ),
        JobPosting(
            job_id="CSCO-001",
            title="Software Engineer - Cloud",
            company="Cisco",
            company_priority=1,
            location="San Jose, CA",
            job_type="Full-time",
            description="Develop cloud-native networking solutions.",
            requirements=["Python", "Go", "Kubernetes", "Docker", "REST APIs"],
            preferred_skills=["Networking", "Security", "CI/CD"],
            experience_level="Entry",
            education_requirements=["BS in Computer Science"],
            url="https://careers.cisco.com/"
        ),
        JobPosting(
            job_id="TSLA-001",
            title="Software Engineer - Autopilot",
            company="Tesla",
            company_priority=2,
            location="Palo Alto, CA",
            job_type="Full-time",
            description="Work on Tesla's Autopilot software.",
            requirements=["C++", "Python", "Computer Vision", "Deep Learning"],
            preferred_skills=["CUDA", "TensorRT", "Embedded Systems"],
            experience_level="Mid",
            education_requirements=["MS in CS, Robotics, or related field"],
            url="https://www.tesla.com/careers"
        ),
        JobPosting(
            job_id="NFLX-001",
            title="Software Engineer - Streaming",
            company="Netflix",
            company_priority=3,
            location="Los Gatos, CA or Remote",
            job_type="Full-time",
            description="Build the world's best streaming platform.",
            requirements=["Java", "Python", "AWS", "Microservices"],
            preferred_skills=["Kafka", "Cassandra", "Spring Boot"],
            experience_level="Mid",
            education_requirements=["BS in Computer Science"],
            url="https://jobs.netflix.com/"
        ),
    ]

