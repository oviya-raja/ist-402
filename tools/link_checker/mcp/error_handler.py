#!/usr/bin/env python3
"""
MCP error handler - Domain-specific error handling for MCP operations
Following DRY: Centralized error handling logic
"""

from typing import Union, Tuple, Any
import sys


def is_shutdown_error(error: Union[Exception, ExceptionGroup, str]) -> bool:
    """
    Check if error is a non-critical MCP shutdown error
    
    Args:
        error: Exception or error string to check
        
    Returns:
        True if error is a shutdown error (non-critical)
    """
    if isinstance(error, ExceptionGroup):
        return any(
            _is_shutdown_error_str(str(exc)) or _is_shutdown_error_str(repr(exc))
            for exc in error.exceptions
        )
    
    error_str = str(error) if isinstance(error, Exception) else error
    return _is_shutdown_error_str(error_str)


def _is_shutdown_error_str(error_str: str) -> bool:
    """Internal helper to check shutdown error patterns"""
    shutdown_patterns = [
        "Shutdown signal received",
        "JSON" in error_str and "Shutdown" in error_str,
        "ValidationError" in error_str and "JSON" in error_str,
        "BrokenResourceError" in error_str,
        "TaskGroup" in error_str and "ValidationError" in error_str,
    ]
    return any(shutdown_patterns)


def handle_shutdown_error(
    error: Union[Exception, ExceptionGroup],
    summary_passed: list,
    pages_checked: int
) -> Tuple[bool, str]:
    """
    Handle MCP server shutdown errors gracefully
    
    Args:
        error: Exception to handle
        summary_passed: List of passed items
        pages_checked: Number of pages checked
        
    Returns:
        Tuple of (should_continue, message)
    """
    if not is_shutdown_error(error):
        return False, ""
    
    # Only suppress if we have results
    if summary_passed or pages_checked > 0:
        return True, "\n✅ MCP server shutdown handled gracefully (non-critical)"
    
    return False, ""


def extract_error_text(result: Any) -> str:
    """
    Extract error text from MCP result
    
    Args:
        result: MCP tool result
        
    Returns:
        Error text or empty string
    """
    if not hasattr(result, 'isError') or not result.isError:
        return ""
    
    if hasattr(result, 'content') and result.content:
        return result.content[0].text if result.content else ""
    
    return ""

