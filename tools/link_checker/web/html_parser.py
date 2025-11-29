#!/usr/bin/env python3
"""
HTML link parser - Domain-specific link extraction from HTML
Following Single Responsibility Principle
"""

import re
from typing import List


HREF_PATTERN = r'href=["\']([^"\']+)["\']'


def extract_links_from_html(html_text: str) -> List[str]:
    """
    Extract all href links from HTML text
    
    Args:
        html_text: HTML content as string
        
    Returns:
        List of href URLs
    """
    if not html_text:
        return []
    
    return re.findall(HREF_PATTERN, html_text)

