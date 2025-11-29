import re
from typing import Tuple, List
from .environment import EnvironmentConfig
from .models import StudentProfile, JobPosting, FitmentResult
from .vector_db import JobFitmentVectorDB

class JobFitmentAnalyzer:
    """
    Core analyzer for job fitment calculations.
    Computes fitment scores and identifies skill gaps.
    """
    
    WEIGHTS = {
        'skills': 0.40,
        'experience': 0.25,
        'education': 0.20,
        'location': 0.10,
        'culture': 0.05
    }
    
    def __init__(self, env: EnvironmentConfig, vector_db: JobFitmentVectorDB):
        self.env = env
        self.vector_db = vector_db
    
    def calculate_skill_match(self, profile: StudentProfile, job: JobPosting) -> Tuple[float, List[str], List[str]]:
        """Calculate skill match percentage."""
        profile_skills = set(s.lower() for s in profile.skills)
        
        # Combine required and preferred skills
        job_skills = set(s.lower() for s in job.requirements + job.preferred_skills)
        
        if not job_skills:
            return 100.0, [], []
        
        # Find matches and gaps
        matches = profile_skills & job_skills
        gaps = job_skills - profile_skills
        
        # Calculate percentage (required skills weighted more)
        required_skills = set(s.lower() for s in job.requirements)
        required_matches = matches & required_skills
        preferred_matches = matches - required_skills
        
        required_count = len(required_skills) if required_skills else 1
        preferred_count = len(set(s.lower() for s in job.preferred_skills)) if job.preferred_skills else 0
        
        # Weighted score: required skills matter more
        required_score = (len(required_matches) / required_count) * 0.7 if required_count else 0.7
        preferred_score = (len(preferred_matches) / max(preferred_count, 1)) * 0.3 if preferred_count else 0.3
        
        score = (required_score + preferred_score) * 100
        
        return min(score, 100.0), list(matches), list(gaps)
    
    def calculate_experience_match(self, profile: StudentProfile, job: JobPosting) -> float:
        """Calculate experience level match."""
        # Get total years of experience from profile
        total_years = 0
        for exp in profile.experience:
            duration = exp.get('duration', '')
            # Simple parsing: look for numbers
            numbers = re.findall(r'\d+', duration)
            if numbers:
                total_years += int(numbers[0])
        
        # Map experience level to expected years
        level_requirements = {
            "Entry": (0, 2),
            "Mid": (2, 5),
            "Senior": (5, 10),
            "Executive": (10, 20)
        }
        
        min_years, max_years = level_requirements.get(job.experience_level, (0, 2))
        
        if min_years <= total_years <= max_years:
            return 100.0
        elif total_years < min_years:
            # Under-experienced: penalty based on gap
            gap = min_years - total_years
            return max(0, 100 - (gap * 20))
        else:
            # Over-experienced: slight penalty
            return max(70, 100 - ((total_years - max_years) * 5))
    
    def calculate_education_match(self, profile: StudentProfile, job: JobPosting) -> float:
        """Calculate education match."""
        if not job.education_requirements:
            return 100.0
        
        profile_degrees = []
        profile_fields = []
        
        for edu in profile.education:
            profile_degrees.append(edu.get('degree', '').lower())
            profile_fields.append(edu.get('field', '').lower())
        
        score = 0
        for req in job.education_requirements:
            req_lower = req.lower()
            
            # Check degree match
            for degree in profile_degrees:
                if any(d in degree for d in ['bachelor', 'master', 'phd', 'bs', 'ms', 'mba']):
                    score += 30
                    break
            
            # Check field match
            for field in profile_fields:
                if any(f in field for f in ['computer', 'software', 'engineering', 'science', 'data']):
                    score += 40
                    break
        
        # Add points for certifications
        if profile.certifications:
            score += min(len(profile.certifications) * 10, 30)
        
        return min(score, 100.0)
    
    def calculate_location_match(self, profile: StudentProfile, job: JobPosting) -> float:
        """Calculate location match."""
        pref_location = profile.preferences.get('location', '').lower()
        job_location = job.location.lower()
        
        # Check for remote
        if 'remote' in job_location or 'remote' in pref_location:
            return 100.0
        
        # Check for city/region match
        if pref_location and pref_location in job_location:
            return 100.0
        
        # Check for same country
        if any(country in pref_location and country in job_location 
               for country in ['us', 'usa', 'united states', 'india', 'uk', 'germany']):
            return 70.0
        
        return 50.0  # Default for relocation possible
    
    def analyze_fitment(self, profile: StudentProfile, job: JobPosting) -> FitmentResult:
        """Perform complete fitment analysis."""
        # Calculate individual scores
        skill_score, skill_matches, skill_gaps = self.calculate_skill_match(profile, job)
        exp_score = self.calculate_experience_match(profile, job)
        edu_score = self.calculate_education_match(profile, job)
        loc_score = self.calculate_location_match(profile, job)
        
        # Calculate weighted fitment score
        fitment_score = (
            skill_score * self.WEIGHTS['skills'] +
            exp_score * self.WEIGHTS['experience'] +
            edu_score * self.WEIGHTS['education'] +
            loc_score * self.WEIGHTS['location']
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            skill_gaps, skill_score, exp_score, edu_score, job
        )
        
        # Generate detailed analysis
        detailed_analysis = self._generate_detailed_analysis(
            profile, job, skill_score, exp_score, edu_score, loc_score,
            skill_matches, skill_gaps
        )
        
        return FitmentResult(
            job=job,
            fitment_score=round(fitment_score, 1),
            skill_matches=skill_matches,
            skill_gaps=skill_gaps,
            experience_match=round(exp_score, 1),
            education_match=round(edu_score, 1),
            location_match=loc_score >= 70,
            detailed_analysis=detailed_analysis,
            recommendations=recommendations,
            priority_level=job.company_priority
        )
    
    def _generate_recommendations(
        self, 
        skill_gaps: List[str], 
        skill_score: float,
        exp_score: float,
        edu_score: float,
        job: JobPosting
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Skill-based recommendations
        if skill_gaps and skill_score < 80:
            priority_gaps = skill_gaps[:3]  # Top 3 gaps
            recommendations.append(
                f"Priority Skills to Learn: {', '.join(priority_gaps)}. "
                f"Consider online courses on Coursera, Udemy, or official documentation."
            )
        
        # Experience-based recommendations
        if exp_score < 70:
            recommendations.append(
                "Build Relevant Experience: Contribute to open-source projects, "
                "create portfolio projects, or pursue internships in related areas."
            )
        
        # Education-based recommendations
        if edu_score < 70:
            recommendations.append(
                "Enhance Credentials: Consider relevant certifications like AWS, "
                "Google Cloud, or specialized courses from recognized institutions."
            )
        
        # General recommendations
        recommendations.append(
            f"Tailor your resume to highlight skills matching {job.company}'s requirements."
        )
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _generate_detailed_analysis(
        self,
        profile: StudentProfile,
        job: JobPosting,
        skill_score: float,
        exp_score: float,
        edu_score: float,
        loc_score: float,
        skill_matches: List[str],
        skill_gaps: List[str]
    ) -> str:
        """Generate detailed analysis text."""
        analysis_parts = [
            f"## Fitment Analysis: {profile.name} → {job.title} at {job.company}",
            f"\n### Score Breakdown:",
            f"- Skills Match: {skill_score:.1f}% (Weight: 40%)",
            f"- Experience Match: {exp_score:.1f}% (Weight: 25%)",
            f"- Education Match: {edu_score:.1f}% (Weight: 20%)",
            f"- Location Match: {loc_score:.1f}% (Weight: 10%)",
            f"\n### Matched Skills ({len(skill_matches)}):",
            f"{', '.join(skill_matches) if skill_matches else 'None identified'}",
            f"\n### Skill Gaps ({len(skill_gaps)}):",
            f"{', '.join(skill_gaps) if skill_gaps else 'No critical gaps'}",
        ]
        
        # Add priority-specific details
        if job.company_priority == 1:
            analysis_parts.extend([
                f"\n### Priority 1 Company - Detailed Insights:",
                f"- {job.company} is in your highest priority list",
                f"- Recommend dedicating extra preparation time",
                f"- Consider reaching out to employees for referrals"
            ])
        
        return "\n".join(analysis_parts)

