#!/usr/bin/env python3
"""
Main entry point for the Job Fitment Analysis Agent.
"""

from src.job_fitment import (
    JobFitmentAgent,
    create_sample_profile,
    create_sample_jobs,
    OUTPUT_DIR
)


def main():
    """Main entry point for the Job Fitment Agent."""
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                    JOB FITMENT ANALYSIS AGENT                              ║
    ║                                                                           ║
    ║  Helping final-year students find and evaluate job opportunities          ║
    ║  through AI-powered matching and skill gap analysis.                      ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize agent
    agent = JobFitmentAgent()
    
    try:
        # Setup
        agent.setup(skip_packages=False)
        
        # Create sample data
        profile = create_sample_profile()
        jobs = create_sample_jobs()
        
        print(f"\n👤 Student Profile: {profile.name}")
        print(f"   Skills: {', '.join(profile.skills[:5])}...")
        print(f"   Education: {profile.education[0]['degree']} in {profile.education[0]['field']}")
        
        print(f"\n📋 Jobs to analyze: {len(jobs)}")
        for job in jobs:
            print(f"   - {job.title} at {job.company} (P{job.company_priority})")
        
        # Run analysis
        results = agent.analyze(profile, jobs, generate_report=True, verbose=True)
        
        # Display top match
        if results:
            top = results[0]
            print("\n" + "=" * 80)
            print("🏆 TOP MATCH")
            print("=" * 80)
            print(f"\n   Position: {top.job.title}")
            print(f"   Company: {top.job.company}")
            print(f"   Fitment Score: {top.fitment_score}%")
            print(f"\n   Matched Skills: {', '.join(top.skill_matches[:5])}")
            print(f"   Skill Gaps: {', '.join(top.skill_gaps[:5])}")
            print(f"\n   Top Recommendation: {top.recommendations[0] if top.recommendations else 'N/A'}")
        
        # Save artifacts
        agent.save_all()
        
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE!")
        print("=" * 80)
        print(f"\nReport saved to: {OUTPUT_DIR}/fitment_report.md")
        print("Open the report to see detailed analysis and recommendations.")
        
        return agent, results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    agent, results = main()

