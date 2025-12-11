#!/usr/bin/env python3
"""
Link checker formatter - Output formatting
Following Single Responsibility Principle
"""

from ..core.models import CheckSummary, TestData
from ..ai.quality_analyzer import analyze_with_ai


def print_summary(summary: CheckSummary, test_data: TestData, use_ai: bool = False) -> None:
    """
    Print formatted summary - <40 lines
    
    Args:
        summary: Check summary
        test_data: Test metadata
        use_ai: Whether to include AI analysis
    """
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"\n✅ Passed: {len(summary.passed)}")
    for item in summary.passed[:10]:
        print(f"   • {item}")
    if len(summary.passed) > 10:
        print(f"   ... and {len(summary.passed) - 10} more")
    
    if summary.warnings:
        print(f"\n⚠️  Warnings: {len(summary.warnings)}")
        for item in summary.warnings[:5]:
            print(f"   • {item}")
        if len(summary.warnings) > 5:
            print(f"   ... and {len(summary.warnings) - 5} more")
    
    if summary.failed:
        print(f"\n❌ Failed: {len(summary.failed)}")
        for item in summary.failed:
            print(f"   • {item}")
    else:
        print(f"\n✅ All critical tests passed!")
    
    if use_ai:
        print("\n" + "=" * 60)
        print("AI ANALYSIS (OpenAI GPT-4o-mini)")
        print("=" * 60)
        ai_analysis = analyze_with_ai(summary, test_data)
        print(f"\n{ai_analysis}\n")
    
    print("=" * 60)






