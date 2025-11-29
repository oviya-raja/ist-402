#!/usr/bin/env python3
"""
Link checker runner - Entry point and configuration
Following Single Responsibility Principle
"""

from typing import Optional
from .engine import LinkChecker
from ..core.models import CheckSummary
from ..ai.quality_analyzer import is_ai_available


def main(base_url: Optional[str] = None, max_depth: int = 2, use_ai: bool = True, headless: bool = False) -> CheckSummary:
    """
    Main entry point - <40 lines
    
    Args:
        base_url: URL to check
        max_depth: Maximum recursion depth
        use_ai: Enable AI analysis
        headless: Run browser in headless mode
        
    Returns:
        Check summary
    """
    if base_url is None:
        base_url = "https://oviya-raja.github.io/ist-402/"
    
    print("🚀 Link Checker - FastMCP Client + AI")
    print("=" * 60)
    print(f"📍 Target URL: {base_url}")
    print(f"🔍 Max Depth: {max_depth}")
    print(f"🤖 AI Analysis: {'Enabled' if (use_ai and is_ai_available()) else 'Disabled'}")
    print(f"🖥️  Headless Mode: {'Enabled' if headless else 'Disabled'}")
    print(f"   FastMCP: Required")
    print(f"   AI: {'Available' if is_ai_available() else 'Not available'}")
    print("=" * 60)
    
    checker = LinkChecker(base_url=base_url, max_depth=max_depth, use_ai=use_ai, headless=headless)
    summary, test_data = checker.check()
    checker.print_summary(summary, test_data)
    
    return summary

