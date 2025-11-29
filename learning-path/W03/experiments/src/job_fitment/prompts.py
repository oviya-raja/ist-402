"""
System prompt engineering for job fitment analysis.
"""

from typing import List
from .environment import EnvironmentConfig
from .models import StudentProfile, JobPosting
from .config import OUTPUT_DIR


class JobFitmentPromptEngineer:
    """
    System prompt engineering for job fitment analysis.
    Creates prompts that shape LLM behavior for job matching.
    """
    
    def __init__(self, env: EnvironmentConfig):
        self.env = env
        self.system_prompt = None
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for job fitment analysis."""
        self.system_prompt = """You are an AI-powered Job Fitment Analysis Agent designed to help final-year students find and evaluate job opportunities.

ROLE:
- Expert career advisor and job analyst
- Technical skills evaluator
- Personalized recommendation engine

CAPABILITIES:
1. JOB ANALYSIS: Analyze job postings to extract key requirements, skills, and qualifications
2. PROFILE MATCHING: Compare student profiles against job requirements
3. FITMENT SCORING: Calculate precise fitment percentages based on multiple criteria
4. SKILL GAP IDENTIFICATION: Identify specific skills students need to develop
5. RECOMMENDATIONS: Provide actionable advice for improving job candidacy

MATCHING CRITERIA (weighted):
- Skills Match (40%): Technical and soft skills alignment
- Experience Match (25%): Relevant work experience and projects
- Education Match (20%): Degree, certifications, and coursework
- Location Match (10%): Geographic preferences and remote options
- Culture Fit (5%): Company values and work style alignment

RESPONSE GUIDELINES:
- Be specific and actionable in recommendations
- Prioritize based on company priority level (P1 > P2 > P3)
- Include concrete steps for skill development
- Highlight both strengths and areas for improvement
- Provide realistic timelines for skill acquisition

OUTPUT FORMAT:
For each job analysis, provide:
1. Fitment Score (0-100%)
2. Matched Skills (list)
3. Skill Gaps (list with learning resources)
4. Experience Assessment
5. Top 3 Recommendations

PRIORITY HANDLING:
- Priority 1: Detailed analysis with comprehensive recommendations
- Priority 2: Standard analysis with key recommendations
- Priority 3: Summary analysis with essential points

Remember: Your goal is to help students make informed career decisions and improve their job prospects."""
        
        return self.system_prompt
    
    def format_analysis_prompt(self, profile: StudentProfile, job: JobPosting) -> str:
        """Format prompt for job fitment analysis."""
        return f"""<s>[INST] {self.system_prompt}

STUDENT PROFILE:
{profile.to_text()}

JOB POSTING (Priority {job.company_priority}):
{job.to_text()}

TASK: Analyze the fitment between this student profile and the job posting.
Provide a comprehensive analysis including:
1. Overall fitment score (0-100%)
2. Matched skills
3. Skill gaps with specific learning recommendations
4. Experience assessment
5. Top 3 actionable recommendations

Format your response as a structured analysis. [/INST]"""
    
    def format_skill_gap_prompt(self, profile: StudentProfile, gaps: List[str]) -> str:
        """Format prompt for skill gap recommendations."""
        return f"""<s>[INST] {self.system_prompt}

STUDENT PROFILE:
{profile.to_text()}

IDENTIFIED SKILL GAPS:
{', '.join(gaps)}

TASK: For each skill gap, provide:
1. Importance level (Critical/Important/Nice-to-have)
2. Estimated learning time
3. Recommended learning resources (courses, projects, certifications)
4. Practice project ideas

Format as a learning roadmap. [/INST]"""
    
    def save_system_prompt(self, filename: str = "system_prompt.txt") -> str:
        """Save system prompt to file."""
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w') as f:
            f.write(self.system_prompt)
        print(f"✅ Saved: {filepath}")
        return str(filepath)

