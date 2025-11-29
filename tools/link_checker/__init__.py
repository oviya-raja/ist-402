"""
Link Checker Module - Domain-Based Structure
Following KISS, YAGNI, SOLID, DRY principles

All modules are <300 lines, methods <40 lines
"""

from .checker import LinkChecker, main
from .core import CheckSummary, TestData, LinkCheckResult
from .web import is_webpage_url, resolve_url, should_recurse, is_valid_link, extract_links_from_html
from .mcp import is_shutdown_error, handle_shutdown_error, close_browser, cleanup_browser_processes, verify_tools, navigate_to_url, get_page_html
from .ai import analyze_with_ai, is_ai_available

__all__ = [
    'LinkChecker',
    'main',
    'CheckSummary',
    'TestData',
    'LinkCheckResult',
    'is_webpage_url',
    'resolve_url',
    'should_recurse',
    'is_valid_link',
    'is_shutdown_error',
    'handle_shutdown_error',
    'close_browser',
    'cleanup_browser_processes',
    'extract_links_from_html',
    'verify_tools',
    'navigate_to_url',
    'get_page_html',
    'analyze_with_ai',
    'is_ai_available',
]
