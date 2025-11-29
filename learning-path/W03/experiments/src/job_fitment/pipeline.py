from datetime import datetime
from typing import List, Dict, Any
from .environment import EnvironmentConfig
from .models import StudentProfile, JobPosting, FitmentResult
from .prompts import JobFitmentPromptEngineer
from .vector_db import JobFitmentVectorDB
from .analyzer import JobFitmentAnalyzer
from .config import OUTPUT_DIR

class JobFitmentRAGPipeline:
    """
    Complete RAG pipeline for job fitment analysis.
    Combines retrieval, augmentation, and generation.
    """
    
    def __init__(
        self,
        env: EnvironmentConfig,
        prompt_engineer: JobFitmentPromptEngineer,
        vector_db: JobFitmentVectorDB,
        analyzer: JobFitmentAnalyzer
    ):
        self.env = env
        self.prompt_engineer = prompt_engineer
        self.vector_db = vector_db
        self.analyzer = analyzer
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant context from knowledge base."""
        return self.vector_db.search(query, top_k)
    
    def format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents as context string."""
        if not retrieved_docs:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            q = doc.get('question', 'N/A')
            a = doc.get('answer', 'N/A')
            score = doc.get('similarity_score', 0)
            context_parts.append(f"[{i}] (Score: {score:.2f})\nQ: {q}\nA: {a}")
        
        return "\n\n".join(context_parts)
    
    def analyze_job(
        self, 
        profile: StudentProfile, 
        job: JobPosting,
        verbose: bool = False
    ) -> FitmentResult:
        """Run complete job fitment analysis."""
        if verbose:
            print(f"\n📊 Analyzing: {job.title} at {job.company}")
        
        # Get fitment result from analyzer
        result = self.analyzer.analyze_fitment(profile, job)
        
        # Retrieve relevant context for skill gaps
        if result.skill_gaps:
            context_docs = self.retrieve_context(
                f"How to learn {' '.join(result.skill_gaps[:3])}"
            )
            if context_docs:
                result.recommendations.extend([
                    doc.get('answer', '')[:200] for doc in context_docs[:2]
                ])
        
        if verbose:
            print(f"   ✅ Fitment Score: {result.fitment_score}%")
            print(f"   📈 Matches: {len(result.skill_matches)} skills")
            print(f"   📉 Gaps: {len(result.skill_gaps)} skills")
        
        return result
    
    def batch_analyze(
        self,
        profile: StudentProfile,
        jobs: List[JobPosting],
        verbose: bool = True
    ) -> List[FitmentResult]:
        """Analyze multiple jobs and rank by fitment."""
        results = []
        
        print(f"\n🔍 Analyzing {len(jobs)} job postings...")
        
        for job in jobs:
            result = self.analyze_job(profile, job, verbose=verbose)
            results.append(result)
        
        # Sort by fitment score (descending) and priority (ascending)
        results.sort(key=lambda r: (-r.fitment_score, r.priority_level))
        
        return results
    
    def generate_report(
        self,
        profile: StudentProfile,
        results: List[FitmentResult],
        filename: str = "fitment_report.md"
    ) -> str:
        """Generate comprehensive fitment report."""
        report_parts = [
            "# Job Fitment Analysis Report",
            f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Candidate:** {profile.name}",
            f"**Jobs Analyzed:** {len(results)}",
            "\n---\n",
            "## Executive Summary",
            f"\nTop match: **{results[0].job.title}** at **{results[0].job.company}** "
            f"with **{results[0].fitment_score}%** fitment" if results else "No jobs analyzed",
            "\n---\n",
            "## Rankings by Fitment Score\n"
        ]
        
        # Add rankings table
        report_parts.append("| Rank | Company | Position | Fitment | Priority |")
        report_parts.append("|------|---------|----------|---------|----------|")
        
        for i, result in enumerate(results, 1):
            report_parts.append(
                f"| {i} | {result.job.company} | {result.job.title} | "
                f"{result.fitment_score}% | P{result.priority_level} |"
            )
        
        # Add detailed analysis for top jobs
        report_parts.extend(["\n---\n", "## Detailed Analysis\n"])
        
        for result in results[:5]:  # Top 5
            report_parts.append(result.detailed_analysis)
            report_parts.append("\n---\n")
        
        # Add skill gap summary
        all_gaps = set()
        for result in results:
            all_gaps.update(result.skill_gaps)
        
        report_parts.extend([
            "## Common Skill Gaps\n",
            f"The following skills appear frequently in job requirements but are missing from your profile:\n"
        ])
        
        for gap in list(all_gaps)[:10]:
            report_parts.append(f"- {gap}")
        
        # Add recommendations
        report_parts.extend([
            "\n---\n",
            "## Top Recommendations\n"
        ])
        
        all_recommendations = []
        for result in results[:3]:
            all_recommendations.extend(result.recommendations)
        
        unique_recommendations = list(dict.fromkeys(all_recommendations))[:10]
        for rec in unique_recommendations:
            report_parts.append(f"1. {rec}")
        
        # Write report
        report_content = "\n".join(report_parts)
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w') as f:
            f.write(report_content)
        
        print(f"✅ Report saved: {filepath}")
        return report_content

