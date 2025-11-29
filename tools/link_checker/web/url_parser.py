#!/usr/bin/env python3
"""
Web URL parser - Domain-specific URL utilities
Following DRY: Don't Repeat Yourself
"""

from urllib.parse import urlparse, urljoin
from typing import Set


# Constants - following KISS
NON_WEBPAGE_EXTENSIONS = ['.pdf', '.zip', '.tar', '.gz', '.exe', '.dmg', '.deb', '.rpm']
FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg', 'ico', 'css', 'js', 'json', 'xml']
ALLOWED_DOMAINS = ['github.com', 'oviya-raja.github.io']


def is_webpage_url(url: str) -> bool:
    """
    Check if URL is a webpage (not a file download)
    
    Args:
        url: URL to check
        
    Returns:
        True if URL is a webpage
    """
    if not url:
        return False
    
    url_lower = url.lower()
    
    # Skip non-webpage extensions
    if any(url_lower.endswith(ext) for ext in NON_WEBPAGE_EXTENSIONS):
        return False
    
    # GitHub blob/tree URLs are webpages
    if 'github.com' in url and ('blob' in url or 'tree' in url):
        return True
    
    # HTML files are webpages
    if url_lower.endswith(('.html', '.htm')):
        return True
    
    # URLs without file extensions are likely webpages
    if not any(url_lower.endswith(f'.{ext}') for ext in FILE_EXTENSIONS):
        return True
    
    return False


def resolve_url(href: str, current_url: str) -> str:
    """
    Resolve relative URL to absolute URL
    
    Args:
        href: Relative or absolute URL
        current_url: Current page URL for resolution
        
    Returns:
        Absolute URL
    """
    if href.startswith('http'):
        return href
    elif href.startswith('/'):
        parsed = urlparse(current_url)
        return f"{parsed.scheme}://{parsed.netloc}{href}"
    else:
        return urljoin(current_url, href)


def should_recurse(current_url: str, link_url: str) -> bool:
    """
    Determine if we should recursively check a link
    
    Args:
        current_url: Current page URL
        link_url: Link URL to check
        
    Returns:
        True if should recurse
    """
    parsed_current = urlparse(current_url)
    parsed_link = urlparse(link_url)
    
    # Check same domain or allowed domains
    return (parsed_link.netloc == parsed_current.netloc or
            any(domain in parsed_link.netloc for domain in ALLOWED_DOMAINS))


def is_valid_link(href: str) -> bool:
    """
    Check if href is a valid link to check
    
    Args:
        href: Link href attribute
        
    Returns:
        True if link should be checked
    """
    return not href.startswith(('#', 'javascript:'))

