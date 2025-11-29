"""
Data models for Job Fitment Agent.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class StudentProfile:
    """Student profile for job fitment analysis."""
    name: str
    email: str = ""
    phone: str = ""
    location: str = ""
    education: List[Dict[str, str]] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    experience: List[Dict[str, Any]] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    projects: List[Dict[str, str]] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    
    def to_text(self) -> str:
        """Convert profile to searchable text."""
        parts = [f"Name: {self.name}"]
        
        if self.education:
            edu_text = "; ".join([
                f"{e.get('degree', '')} in {e.get('field', '')} from {e.get('institution', '')}"
                for e in self.education
            ])
            parts.append(f"Education: {edu_text}")
        
        if self.skills:
            parts.append(f"Skills: {', '.join(self.skills)}")
        
        if self.experience:
            exp_text = "; ".join([
                f"{e.get('title', '')} at {e.get('company', '')} ({e.get('duration', '')})"
                for e in self.experience
            ])
            parts.append(f"Experience: {exp_text}")
        
        if self.certifications:
            parts.append(f"Certifications: {', '.join(self.certifications)}")
        
        return " | ".join(parts)


@dataclass
class JobPosting:
    """Job posting data model."""
    job_id: str
    title: str
    company: str
    company_priority: int  # 1, 2, or 3
    location: str = ""
    job_type: str = "Full-time"
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    experience_level: str = "Entry"  # Entry, Mid, Senior
    education_requirements: List[str] = field(default_factory=list)
    salary_range: str = ""
    benefits: List[str] = field(default_factory=list)
    posted_date: str = ""
    url: str = ""
    
    def to_text(self) -> str:
        """Convert job posting to searchable text."""
        parts = [
            f"Title: {self.title}",
            f"Company: {self.company}",
            f"Location: {self.location}",
            f"Type: {self.job_type}",
            f"Level: {self.experience_level}",
        ]
        
        if self.requirements:
            parts.append(f"Requirements: {', '.join(self.requirements)}")
        
        if self.preferred_skills:
            parts.append(f"Preferred Skills: {', '.join(self.preferred_skills)}")
        
        if self.description:
            parts.append(f"Description: {self.description[:500]}")
        
        return " | ".join(parts)


@dataclass
class FitmentResult:
    """Job fitment analysis result."""
    job: JobPosting
    fitment_score: float  # 0-100
    skill_matches: List[str]
    skill_gaps: List[str]
    experience_match: float  # 0-100
    education_match: float  # 0-100
    location_match: bool
    detailed_analysis: str
    recommendations: List[str]
    priority_level: int


@dataclass
class CompanyConfig:
    """Company configuration for job searching."""
    name: str
    job_site_url: str
    priority: int  # 1 = highest, 2 = medium, 3 = lower
    keywords: List[str] = field(default_factory=list)

