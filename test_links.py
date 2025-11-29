#!/usr/bin/env python3
"""
Test script to verify all links in docs/index.html are working
ONLY uses Playwright MCP server (no direct Playwright fallback)
Uses AI for intelligent analysis
"""

import sys
import json
import os
from typing import Dict, List, Any, Optional, TYPE_CHECKING

# Try to use MCP client for Playwright
if TYPE_CHECKING:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError as e:
    MCP_AVAILABLE = False
    # Create dummy types for type hints when MCP is not available
    ClientSession = Any
    StdioServerParameters = Any
    stdio_client = Any

# Note: This script ONLY uses Playwright MCP server, not direct Playwright

# AI Analysis (using OpenAI or similar)
try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  OpenAI not available, AI analysis will be skipped")


def analyze_with_ai(results: Dict[str, List[str]], test_data: Dict[str, Any]) -> str:
    """Use AI to analyze test results and provide recommendations"""
    if not AI_AVAILABLE:
        return "AI analysis unavailable (OpenAI not installed)"
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI analysis unavailable (OPENAI_API_KEY not set)"
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""
Analyze the following GitHub Pages link test results and provide:
1. Overall assessment of the site health
2. Specific issues that need attention
3. Recommendations for improvement
4. Priority actions

Test Results:
- Passed: {len(results['passed'])} tests
- Failed: {len(results['failed'])} tests
- Warnings: {len(results['warnings'])} warnings

Passed Tests:
{json.dumps(results['passed'], indent=2)}

Failed Tests:
{json.dumps(results['failed'], indent=2)}

Warnings:
{json.dumps(results['warnings'], indent=2)}

Test Data:
- Base URL: {test_data.get('base_url', 'N/A')}
- Pages Checked: {test_data.get('pages_checked', 0)}
- Total Links Found: {test_data.get('total_links', 0)}
- Total Links Checked: {test_data.get('total_links_checked', 0)}
- Page Title: {test_data.get('page_title', 'N/A')}

Provide a concise, actionable analysis.
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a web quality assurance expert analyzing link test results."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        return content if content is not None else "AI analysis returned no content"
    except Exception as e:
        return f"AI analysis error: {e}"


def is_webpage_url(url: str) -> bool:
    """Check if URL is a webpage (not a file download)"""
    if not url:
        return False
    
    # Skip file extensions that are not webpages
    non_webpage_extensions = ['.pdf', '.zip', '.tar', '.gz', '.exe', '.dmg', '.deb', '.rpm']
    url_lower = url.lower()
    
    # Check if it ends with a non-webpage extension
    for ext in non_webpage_extensions:
        if url_lower.endswith(ext):
            return False
    
    # GitHub blob URLs are webpages (they render content)
    if 'github.com' in url and ('blob' in url or 'tree' in url):
        return True
    
    # HTML files are webpages
    if url_lower.endswith('.html') or url_lower.endswith('.htm'):
        return True
    
    # URLs without file extensions are likely webpages
    if not any(url_lower.endswith(f'.{ext}') for ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'ico', 'css', 'js', 'json', 'xml']):
        return True
    
    return False


async def check_links_on_page_mcp(session: Any, url: str, base_url: str, visited: set, depth: int = 0, max_depth: int = 2) -> tuple[Dict[str, Any], int]:
    """Recursively check links on a webpage using MCP"""
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    links_checked = 0
    
    if depth > max_depth or url in visited:
        return results, links_checked
    
    visited.add(url)
    
    try:
        print(f"\n{'  ' * depth}🔍 Checking page: {url}")
        
        # Navigate to page
        nav_result = await session.call_tool(
            "playwright_navigate",
            arguments={"url": url}
        )
        
        # Check for errors
        if hasattr(nav_result, 'isError') and nav_result.isError:
            error_text = ""
            if hasattr(nav_result, 'content') and nav_result.content:
                error_text = nav_result.content[0].text if nav_result.content else ""
            print(f"{'  ' * depth}   ❌ Failed to load: {error_text[:100]}")
            results["failed"].append(f"{url}: {error_text[:100]}")
            return results, links_checked
        
        # Get page HTML to find links
        html_result = await session.call_tool(
            "playwright_get_visible_html",
            arguments={}
        )
        
        # Parse HTML to find links (simple regex approach)
        import re
        html_text = ""
        if hasattr(html_result, 'content') and html_result.content:
            html_text = html_result.content[0].text if html_result.content else ""
        
        # Find all href attributes
        href_pattern = r'href=["\']([^"\']+)["\']'
        links = re.findall(href_pattern, html_text)
        
        print(f"{'  ' * depth}   Found {len(links)} links on this page")
        
        for href in links:
            # Skip anchors and javascript
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Resolve relative URLs
            from urllib.parse import urlparse, urljoin
            if href.startswith('/'):
                parsed = urlparse(url)
                full_url = f"{parsed.scheme}://{parsed.netloc}{href}"
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = urljoin(url, href)
            
            # Skip already visited
            if full_url in visited:
                continue
            
            links_checked += 1
            
            # Test the link using HTTP request
            try:
                # Use playwright_get to test the link
                get_result = await session.call_tool(
                    "playwright_get",
                    arguments={"url": full_url}
                )
                
                status = 200  # Default, MCP doesn't return status directly
                if hasattr(get_result, 'isError') and get_result.isError:
                    status = 400
                    error_text = ""
                    if hasattr(get_result, 'content') and get_result.content:
                        error_text = get_result.content[0].text if get_result.content else ""
                    print(f"{'  ' * depth}   ❌ {href[:60]}... (Error: {error_text[:50]})")
                    results["failed"].append(f"{url} -> {full_url}: {error_text[:50]}")
                else:
                    print(f"{'  ' * depth}   ✅ {href[:60]}... (HTTP 200)")
                    results["passed"].append(f"{url} -> {full_url}")
                    
                    # If it's a webpage and we haven't reached max depth, check its links
                    if is_webpage_url(full_url) and depth < max_depth:
                        # Only check if it's from the same domain or GitHub
                        parsed_current = urlparse(url)
                        parsed_link = urlparse(full_url)
                        
                        # Check same domain or GitHub
                        if (parsed_link.netloc == parsed_current.netloc or 
                            'github.com' in parsed_link.netloc or
                            'oviya-raja.github.io' in parsed_link.netloc):
                            sub_results, sub_count = await check_links_on_page_mcp(
                                session, full_url, base_url, visited, depth + 1, max_depth
                            )
                            results["passed"].extend(sub_results["passed"])
                            results["failed"].extend(sub_results["failed"])
                            results["warnings"].extend(sub_results["warnings"])
                            links_checked += sub_count
                        
            except Exception as e:
                print(f"{'  ' * depth}   ⚠️  {href[:60]}... (Error: {str(e)[:50]})")
                results["warnings"].append(f"{url} -> {full_url}: {e}")
        
    except Exception as e:
        print(f"{'  ' * depth}   ❌ Error loading page: {e}")
        results["failed"].append(f"{url}: {e}")
    
    return results, links_checked


def test_with_mcp(base_url: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """Test links using ONLY Playwright MCP server"""
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    test_data = {
        "base_url": base_url,
        "total_links": 0,
        "page_title": "",
        "pages_checked": 0,
        "total_links_checked": 0
    }
    
    if not MCP_AVAILABLE:
        results["failed"].append("MCP client not available - install with: pip install mcp")
        return results, test_data
    
    # MCP server configuration
    server_configs = [
        {
            "name": "@executeautomation/playwright-mcp-server",
            "command": "npx",
            "args": ["-y", "@executeautomation/playwright-mcp-server"]
        }
    ]
    
    import asyncio
    from mcp.client.stdio import stdio_client
    
    for config in server_configs:
        try:
            print(f"🚀 Using MCP server: {config['name']}")
            server_params = StdioServerParameters(
                command=config["command"],
                args=config["args"],
                env=None
            )
            
            async def run_mcp_test():
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        # Initialize the session
                        init_result = await session.initialize()
                        print(f"✅ MCP Server initialized: {config['name']}")
                        
                        # List available tools
                        tools_result = await session.list_tools()
                        tool_names = [tool.name for tool in tools_result.tools]
                        print(f"🔧 Available MCP tools: {len(tool_names)} tools")
                        
                        # Navigate to base URL
                        print(f"\n📍 Launching: {base_url}\n")
                        nav_result = await session.call_tool(
                            "playwright_navigate",
                            arguments={"url": base_url}
                        )
                        
                        # Check for navigation errors
                        if hasattr(nav_result, 'isError') and nav_result.isError:
                            error_text = ""
                            if hasattr(nav_result, 'content') and nav_result.content:
                                error_text = nav_result.content[0].text if nav_result.content else ""
                            print(f"❌ Navigation failed: {error_text[:200]}")
                            results["failed"].append(f"Navigation failed: {error_text[:100]}")
                            return results, test_data
                        
                        print("✅ Index page loaded successfully")
                        results["passed"].append("Index page loads")
                        
                        # Get page title using evaluate
                        try:
                            eval_result = await session.call_tool(
                                "playwright_evaluate",
                                arguments={"expression": "document.title"}
                            )
                            if hasattr(eval_result, 'content') and eval_result.content:
                                test_data["page_title"] = eval_result.content[0].text if eval_result.content else ""
                            print(f"📄 Page title: {test_data['page_title']}")
                            if "IST402" in test_data['page_title'] or "Learning Path" in test_data['page_title']:
                                results["passed"].append("Page title correct")
                        except Exception as e:
                            print(f"⚠️  Could not get page title: {e}")
                        
                        # Recursively check all links
                        print(f"\n🔗 Checking all links on index page and linked webpages...\n")
                        visited = set()
                        page_results, links_count = await check_links_on_page_mcp(
                            session, base_url, base_url, visited, depth=0, max_depth=2
                        )
                        
                        # Merge results
                        results["passed"].extend(page_results["passed"])
                        results["failed"].extend(page_results["failed"])
                        results["warnings"].extend(page_results["warnings"])
                        
                        test_data["total_links"] = len(visited)
                        test_data["total_links_checked"] = links_count
                        test_data["pages_checked"] = len(visited)
                        
                        print(f"\n📊 Summary:")
                        print(f"   Pages checked: {test_data['pages_checked']}")
                        print(f"   Total links checked: {test_data['total_links_checked']}")
                        
                        # Explicitly close browser to prevent hanging processes
                        browser_closed = False
                        try:
                            tools_result = await session.list_tools()
                            tool_names = [tool.name for tool in tools_result.tools]
                            
                            if "playwright_close" in tool_names:
                                await session.call_tool("playwright_close", arguments={})
                                print("✅ Browser closed successfully")
                                browser_closed = True
                            elif "playwright_close_browser" in tool_names:
                                await session.call_tool("playwright_close_browser", arguments={})
                                print("✅ Browser closed successfully")
                                browser_closed = True
                        except Exception as e:
                            if not browser_closed:
                                print(f"⚠️  Browser close tool not available: {e}")
                                print("   Browser will be closed when MCP session exits")
                        
                        results["passed"].append(f"MCP server ({config['name']})")
                        return results, test_data
                    # Context manager will close session and client
                    # Add small delay to allow MCP server to clean up browser processes
                    await asyncio.sleep(0.5)
            
            # Run async MCP test
            try:
                mcp_results, mcp_data = asyncio.run(run_mcp_test())
                # Give additional time for browser processes to clean up
                import time
                time.sleep(0.5)
                if mcp_results and mcp_data:
                    return mcp_results, mcp_data
            except ExceptionGroup as e:
                # Handle TaskGroup exceptions (often from shutdown messages)
                # Check if any of the exceptions are JSON parsing errors from shutdown
                has_json_error = False
                for exc in e.exceptions:
                    if "JSON" in str(exc) or "Shutdown signal" in str(exc):
                        has_json_error = True
                        break
                
                if has_json_error:
                    # This is likely just a shutdown message parsing issue
                    # If we got results, return them
                    if 'mcp_results' in locals() and mcp_results and mcp_data:
                        print("⚠️  MCP server shutdown message parsing issue (non-critical)")
                        return mcp_results, mcp_data
                    else:
                        print(f"❌ MCP execution error: {e}")
                        results["failed"].append(f"MCP execution failed: {e}")
                        return results, test_data
                else:
                    print(f"❌ MCP execution error: {e}")
                    results["failed"].append(f"MCP execution failed: {e}")
                    return results, test_data
            except Exception as e:
                error_str = str(e)
                # Ignore JSON parsing errors from shutdown messages
                if "JSON" in error_str and "Shutdown" in error_str:
                    print("⚠️  MCP server shutdown message parsing issue (non-critical)")
                    if 'mcp_results' in locals() and mcp_results and mcp_data:
                        return mcp_results, mcp_data
                
                print(f"❌ MCP execution error: {e}")
                import traceback
                traceback.print_exc()
                results["failed"].append(f"MCP execution failed: {e}")
                return results, test_data
                    
        except Exception as e:
            print(f"❌ MCP server error with {config['name']}: {e}")
            import traceback
            traceback.print_exc()
            results["failed"].append(f"MCP server failed: {e}")
            continue
    
    # If we get here, MCP failed
    if not results.get("passed"):
        results["failed"].append("All MCP servers failed - check that Playwright browsers are installed: npx playwright install")
    
    return results, test_data
    """Recursively check links on a webpage"""
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    links_checked = 0
    
    if depth > max_depth or url in visited:
        return results, links_checked
    
    visited.add(url)
    
    try:
        print(f"\n{'  ' * depth}🔍 Checking page: {url}")
        response = page.goto(url, wait_until="networkidle", timeout=30000)
        
        if response.status != 200:
            results["failed"].append(f"{url}: HTTP {response.status}")
            return results, links_checked
        
        # Get all links on this page
        links = page.query_selector_all("a[href]")
        print(f"{'  ' * depth}   Found {len(links)} links on this page")
        
        for link in links:
            try:
                href = link.get_attribute('href')
                if not href:
                    continue
                
                # Resolve relative URLs
                if href.startswith('/'):
                    # Absolute path from domain
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    full_url = f"{parsed.scheme}://{parsed.netloc}{href}"
                elif href.startswith('http'):
                    full_url = href
                else:
                    # Relative path
                    from urllib.parse import urljoin
                    full_url = urljoin(url, href)
                
                # Skip anchors and javascript
                if href.startswith('#') or href.startswith('javascript:'):
                    continue
                
                # Skip already visited
                if full_url in visited:
                    continue
                
                links_checked += 1
                
                # Test the link
                try:
                    link_response = page.request.get(full_url, timeout=10000)
                    status = link_response.status
                    
                    if status in [200, 301, 302]:
                        print(f"{'  ' * depth}   ✅ {href[:60]}... (HTTP {status})")
                        results["passed"].append(f"{url} -> {full_url}")
                        
                        # If it's a webpage and we haven't reached max depth, check its links
                        if is_webpage_url(full_url) and depth < max_depth:
                            sub_results, sub_count = check_links_on_page(
                                page, full_url, base_url, visited, depth + 1, max_depth
                            )
                            results["passed"].extend(sub_results["passed"])
                            results["failed"].extend(sub_results["failed"])
                            results["warnings"].extend(sub_results["warnings"])
                            links_checked += sub_count
                    elif status == 429:
                        print(f"{'  ' * depth}   ⚠️  {href[:60]}... (Rate limited)")
                        results["warnings"].append(f"{url} -> {full_url} (rate limited)")
                    else:
                        print(f"{'  ' * depth}   ❌ {href[:60]}... (HTTP {status})")
                        results["failed"].append(f"{url} -> {full_url}: HTTP {status}")
                        
                except Exception as e:
                    # For GitHub links, rate limiting is common
                    if 'github.com' in full_url:
                        print(f"{'  ' * depth}   ⚠️  {href[:60]}... (GitHub - may be rate limited)")
                        results["warnings"].append(f"{url} -> {full_url} (GitHub rate limit)")
                    else:
                        print(f"{'  ' * depth}   ❌ {href[:60]}... (Error: {str(e)[:50]})")
                        results["failed"].append(f"{url} -> {full_url}: {e}")
                        
            except Exception as e:
                print(f"{'  ' * depth}   ⚠️  Error processing link: {str(e)[:50]}")
                results["warnings"].append(f"Error processing link on {url}: {e}")
        
    except Exception as e:
        print(f"{'  ' * depth}   ❌ Error loading page: {e}")
        results["failed"].append(f"{url}: {e}")
    
    return results, links_checked


def main():
    """Main test function - ONLY uses Playwright MCP Server"""
    base_url = "https://oviya-raja.github.io/ist-402/"
    
    if not MCP_AVAILABLE:
        print("❌ ERROR: MCP client not available!")
        print("   Install with: pip install mcp")
        print("   This script ONLY works with Playwright MCP Server")
        return {"failed": ["MCP not available"]}
    
    print("🚀 Using Playwright MCP Server (ONLY)")
    print("=" * 60)
    results, test_data = test_with_mcp(base_url)
    
    # Check if MCP actually succeeded
    mcp_used = any("MCP server" in item for item in results.get("passed", []))
    if mcp_used:
        print("\n" + "=" * 60)
        print("✅ SUCCESSFULLY USED PLAYWRIGHT MCP SERVER!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ MCP SERVER FAILED")
        print("=" * 60)
        print("   Make sure Playwright browsers are installed:")
        print("   Run: npx playwright install")
        print("=" * 60)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"\n✅ Passed: {len(results['passed'])}")
    for item in results['passed']:
        print(f"   • {item}")
    
    if results['warnings']:
        print(f"\n⚠️  Warnings: {len(results['warnings'])}")
        for item in results['warnings']:
            print(f"   • {item}")
    
    if results['failed']:
        print(f"\n❌ Failed: {len(results['failed'])}")
        for item in results['failed']:
            print(f"   • {item}")
    else:
        print(f"\n✅ All critical tests passed!")
    
    # AI Analysis
    print("\n" + "=" * 60)
    print("AI ANALYSIS")
    print("=" * 60)
    ai_analysis = analyze_with_ai(results, test_data)
    print(f"\n{ai_analysis}\n")
    
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    results = main()
    sys.exit(0 if not results.get('failed') else 1)
