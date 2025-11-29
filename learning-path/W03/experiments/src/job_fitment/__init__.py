"""
Job Fitment Analysis Agent

A comprehensive RAG-based system for analyzing job fitment and identifying skill gaps.
"""

__version__ = "1.0.0"

# Core Classes
from .agent import JobFitmentAgent
from .environment import EnvironmentConfig
from .prompts import JobFitmentPromptEngineer
from .knowledge_base import KnowledgeBaseGenerator
from .vector_db import JobFitmentVectorDB
from .analyzer import JobFitmentAnalyzer
from .pipeline import JobFitmentRAGPipeline
from .scorer import FitmentScorer

# Data Models
from .models import (
    StudentProfile,
    JobPosting,
    FitmentResult,
    CompanyConfig
)

# Configuration
from .config import TARGET_COMPANIES, OUTPUT_DIR

# Sample Data
from .samples import create_sample_profile, create_sample_jobs

__all__ = [
    # Core Classes
    'JobFitmentAgent',
    'EnvironmentConfig',
    'JobFitmentPromptEngineer',
    'KnowledgeBaseGenerator',
    'JobFitmentVectorDB',
    'JobFitmentAnalyzer',
    'JobFitmentRAGPipeline',
    'FitmentScorer',
    
    # Data Models
    'StudentProfile',
    'JobPosting',
    'FitmentResult',
    'CompanyConfig',
    
    # Sample Data
    'create_sample_profile',
    'create_sample_jobs',
    
    # Configuration
    'TARGET_COMPANIES',
    'OUTPUT_DIR',
    
    # Version
    '__version__',
]

