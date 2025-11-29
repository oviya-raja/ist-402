#!/usr/bin/env python3
"""
Link checker data models - Domain-specific data structures
Following SOLID: Single Responsibility - only data structures
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class LinkCheckResult:
    """Results from checking a single link"""
    url: str
    status: str  # 'passed', 'failed', 'warning'
    message: str
    depth: int = 0


@dataclass
class CheckSummary:
    """Summary of link checking results"""
    passed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    pages_checked: int = 0
    total_links_checked: int = 0


@dataclass
class TestData:
    """Test execution metadata"""
    base_url: str
    max_depth: int
    page_title: str = ""
    total_links: int = 0

