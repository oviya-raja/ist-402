#!/usr/bin/env python3
"""
End-to-end test for Job Fitment Analysis Agent.
Tests the complete pipeline from setup to report generation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.job_fitment import (
    JobFitmentAgent,
    create_sample_profile,
    create_sample_jobs,
    OUTPUT_DIR
)


def test_end_to_end():
    """Run complete end-to-end test."""
    print("=" * 80)
    print("🧪 END-TO-END TEST: Job Fitment Analysis Agent")
    print("=" * 80)
    
    # Initialize agent
    print("\n📋 Step 1: Initializing Agent...")
    agent = JobFitmentAgent()
    
    try:
        # Setup
        print("📋 Step 2: Setting up agent (this may take a few minutes)...")
        agent.setup(skip_packages=True)  # Skip package installation in tests
        print("✅ Agent setup complete")
        
        # Create sample data
        print("\n📋 Step 3: Creating sample data...")
        profile = create_sample_profile()
        jobs = create_sample_jobs()
        print(f"✅ Profile created: {profile.name}")
        print(f"✅ Jobs created: {len(jobs)}")
        
        # Run analysis
        print("\n📋 Step 4: Running job fitment analysis...")
        results = agent.analyze(profile, jobs, generate_report=True, verbose=False)
        print(f"✅ Analysis complete: {len(results)} results")
        
        # Verify results
        print("\n📋 Step 5: Verifying results...")
        assert len(results) > 0, "No results generated"
        assert all(hasattr(r, 'fitment_score') for r in results), "Results missing fitment_score"
        assert all(hasattr(r, 'job') for r in results), "Results missing job"
        print("✅ Results structure verified")
        
        # Verify output files
        print("\n📋 Step 6: Verifying output files...")
        required_files = [
            "fitment_report.md",
            "system_prompt.txt",
            "knowledge_base.json",
            "job_fitment.faiss",
            "embeddings.npy"
        ]
        
        for filename in required_files:
            filepath = OUTPUT_DIR / filename
            assert filepath.exists(), f"Missing output file: {filename}"
            assert filepath.stat().st_size > 0, f"Empty output file: {filename}"
            print(f"   ✅ {filename} exists and is not empty")
        
        # Save artifacts
        print("\n📋 Step 7: Saving artifacts...")
        agent.save_all()
        print("✅ All artifacts saved")
        
        # Display summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Agent initialized successfully")
        print(f"✅ Setup completed")
        print(f"✅ Profile processed: {profile.name}")
        print(f"✅ Jobs analyzed: {len(jobs)}")
        print(f"✅ Results generated: {len(results)}")
        print(f"✅ Top match: {results[0].job.company} - {results[0].fitment_score}%")
        print(f"✅ All output files created")
        print("\n" + "=" * 80)
        print("✅ END-TO-END TEST PASSED!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quick_analyze():
    """Test quick analysis for a single job."""
    print("\n" + "=" * 80)
    print("🧪 QUICK ANALYZE TEST")
    print("=" * 80)
    
    agent = JobFitmentAgent()
    agent.setup(skip_packages=True)
    
    profile = create_sample_profile()
    jobs = create_sample_jobs()
    
    if jobs:
        result = agent.quick_analyze(profile, jobs[0])
        assert result is not None, "Quick analyze returned None"
        assert hasattr(result, 'fitment_score'), "Result missing fitment_score"
        print(f"✅ Quick analyze successful: {result.fitment_score}%")
        return True
    
    return False


if __name__ == "__main__":
    print("\n🚀 Running Job Fitment Analysis Agent Tests\n")
    
    # Run end-to-end test
    e2e_passed = test_end_to_end()
    
    # Run quick analyze test
    quick_passed = test_quick_analyze()
    
    # Final summary
    print("\n" + "=" * 80)
    print("📋 FINAL TEST RESULTS")
    print("=" * 80)
    print(f"End-to-End Test: {'✅ PASSED' if e2e_passed else '❌ FAILED'}")
    print(f"Quick Analyze Test: {'✅ PASSED' if quick_passed else '❌ FAILED'}")
    
    if e2e_passed and quick_passed:
        print("\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)

