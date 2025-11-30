"""
Web domain - URL parsing and HTML link extraction
"""

from .url_parser import is_webpage_url, resolve_url, should_recurse, is_valid_link
from .html_parser import extract_links_from_html

__all__ = [
    'is_webpage_url',
    'resolve_url',
    'should_recurse',
    'is_valid_link',
    'extract_links_from_html',
]




