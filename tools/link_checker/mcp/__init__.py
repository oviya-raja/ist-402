"""
MCP domain - MCP operations, error handling, browser lifecycle
"""

from .client import (
    verify_tools, navigate_to_url, get_page_html,
    get_page_title, check_link, MCPClientSession
)
from .error_handler import is_shutdown_error, handle_shutdown_error, extract_error_text
from .browser_lifecycle import close_browser, cleanup_browser_processes, cleanup_browser_sync

__all__ = [
    'verify_tools',
    'navigate_to_url',
    'get_page_html',
    'get_page_title',
    'check_link',
    'MCPClientSession',
    'is_shutdown_error',
    'handle_shutdown_error',
    'extract_error_text',
    'close_browser',
    'cleanup_browser_processes',
    'cleanup_browser_sync',
]



