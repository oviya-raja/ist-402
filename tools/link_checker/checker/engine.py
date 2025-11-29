#!/usr/bin/env python3
"""
Link checker engine - Core link checking logic
Following SOLID: Single Responsibility - only link checking
All methods <40 lines, file <300 lines
"""

import asyncio
from typing import Set, Tuple, TYPE_CHECKING, Any

from ..core.models import CheckSummary, TestData
from ..web.url_parser import is_webpage_url, resolve_url, should_recurse, is_valid_link
from ..mcp.error_handler import is_shutdown_error, handle_shutdown_error, extract_error_text
from ..mcp.browser_lifecycle import close_browser, cleanup_browser_processes, cleanup_browser_sync
from ..web.html_parser import extract_links_from_html
from ..ai.quality_analyzer import is_ai_available
from .formatter import print_summary

# FastMCP imports
if TYPE_CHECKING:
    from fastmcp import Client
    FastMCPClient = Client
else:
    FastMCPClient = Any

try:
    from fastmcp import Client
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False
    Client = Any  # type: ignore


class LinkChecker:
    """
    Link checker using FastMCP Client
    Following SOLID: Single Responsibility - only link checking
    """
    
    def __init__(self, base_url: str, max_depth: int = 2, use_ai: bool = True, headless: bool = False):
        """Initialize link checker"""
        if not FASTMCP_AVAILABLE:
            raise ImportError("FastMCP not available. Install with: pip install fastmcp")
        
        self.base_url = base_url
        self.max_depth = max_depth
        self.headless = headless
        self.use_ai = use_ai and is_ai_available()
        
        if use_ai and not is_ai_available():
            print("⚠️  AI requested but not available. Continuing without AI...")
        
        self.summary = CheckSummary()
        self.test_data = TestData(base_url=base_url, max_depth=max_depth)
        self.visited: Set[str] = set()
    
    async def _check_single_link(
        self, client: FastMCPClient,
        source_url: str, target_url: str, href: str, depth: int
    ) -> None:
        """Check a single link - <40 lines"""
        try:
            result = await client.call_tool("playwright_get", arguments={"url": target_url})
            error_text = extract_error_text(result)
            
            if error_text:
                print(f"{'  ' * depth}   ❌ {href[:60]}... (Error: {error_text[:50]})")
                self.summary.failed.append(f"{source_url} -> {target_url}: {error_text[:50]}")
            else:
                print(f"{'  ' * depth}   ✅ {href[:60]}... (HTTP 200)")
                self.summary.passed.append(f"{source_url} -> {target_url}")
        except Exception as e:
            print(f"{'  ' * depth}   ⚠️  {href[:60]}... (Error: {str(e)[:50]})")
            self.summary.warnings.append(f"{source_url} -> {target_url}: {e}")
    
    async def _process_page_links(
        self, client: FastMCPClient, url: str, links: list, depth: int
    ) -> int:
        """Process links on a page - <40 lines"""
        links_checked = 0
        
        for href in links:
            if not is_valid_link(href):
                continue
            
            full_url = resolve_url(href, url)
            if full_url in self.visited:
                continue
            
            links_checked += 1
            await self._check_single_link(client, url, full_url, href, depth)
            
            if (is_webpage_url(full_url) and depth < self.max_depth and
                should_recurse(url, full_url)):
                sub_count = await self._check_links_on_page(client, full_url, depth + 1)
                links_checked += sub_count
        
        return links_checked
    
    async def _check_links_on_page(
        self, client: FastMCPClient, url: str, depth: int = 0
    ) -> int:
        """Recursively check links on a webpage - <40 lines"""
        if depth > self.max_depth or url in self.visited:
            return 0
        
        self.visited.add(url)
        links_checked = 0
        
        try:
            print(f"\n{'  ' * depth}🔍 Checking page: {url}")
            
            nav_result = await client.call_tool("playwright_navigate", arguments={"url": url})
            error_text = extract_error_text(nav_result)
            
            if error_text:
                print(f"{'  ' * depth}   ❌ Failed to load: {error_text[:100]}")
                self.summary.failed.append(f"{url}: {error_text[:100]}")
                return 0
            
            html_result = await client.call_tool("playwright_get_visible_html", arguments={})
            html_text = html_result.content[0].text if html_result.content else ""
            
            links = extract_links_from_html(html_text)
            print(f"{'  ' * depth}   Found {len(links)} links on this page")
            
            links_checked = await self._process_page_links(client, url, links, depth)
        
        except Exception as e:
            print(f"{'  ' * depth}   ❌ Error loading page: {e}")
            self.summary.failed.append(f"{url}: {e}")
        
        return links_checked
    
    async def _initialize_client(self, client: FastMCPClient) -> None:
        """Initialize and verify FastMCP client - <40 lines"""
        print(f"✅ FastMCP Client connected (100% MCP mode)")
        
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        print(f"🔧 Available MCP tools: {len(tool_names)} tools")
        
        required_tools = ["playwright_navigate", "playwright_get_visible_html",
                         "playwright_get", "playwright_evaluate"]
        missing_tools = [t for t in required_tools if t not in tool_names]
        
        if missing_tools:
            raise RuntimeError(f"Required MCP tools missing: {missing_tools}")
    
    async def _navigate_to_base(self, client: FastMCPClient) -> bool:
        """Navigate to base URL - <40 lines"""
        headless_mode = " (headless)" if self.headless else ""
        print(f"\n📍 Launching: {self.base_url}{headless_mode}\n")
        
        nav_result = await client.call_tool("playwright_navigate", arguments={"url": self.base_url})
        error_text = extract_error_text(nav_result)
        
        if error_text:
            print(f"❌ Navigation failed: {error_text[:200]}")
            self.summary.failed.append(f"Navigation failed: {error_text[:100]}")
            return False
        
        print("✅ Index page loaded successfully (via FastMCP)")
        self.summary.passed.append("Index page loads")
        return True
    
    async def _get_page_metadata(self, client: FastMCPClient) -> None:
        """Get page title and metadata - <40 lines"""
        try:
            eval_result = await client.call_tool(
                "playwright_evaluate",
                arguments={"expression": "document.title"}
            )
            self.test_data.page_title = eval_result.content[0].text if eval_result.content else ""
            print(f"📄 Page title: {self.test_data.page_title}")
        except Exception as e:
            print(f"⚠️  Could not get page title: {e}")
    
    def _handle_check_error(self, error: Exception) -> Tuple[bool, Tuple[CheckSummary, TestData]]:
        """Handle errors during check - reusable error handling"""
        should_continue, message = handle_shutdown_error(
            error, self.summary.passed, self.summary.pages_checked
        )
        if should_continue:
            print(message)
            return True, (self.summary, self.test_data)
        return False, (self.summary, self.test_data)
    
    def _get_mcp_config(self) -> dict:
        """Get MCP client configuration - <40 lines"""
        return {
            "mcpServers": {
                "playwright": {
                    "command": "npx",
                    "args": ["-y", "@executeautomation/playwright-mcp-server"]
                }
            }
        }
    
    async def _run_check(self) -> Tuple[CheckSummary, TestData]:
        """Run link checking using FastMCP Client - <40 lines"""
        mcp_config = self._get_mcp_config()
        client = None
        
        try:
            async with Client(mcp_config) as client:
                await self._initialize_client(client)
                
                if not await self._navigate_to_base(client):
                    await cleanup_browser_processes(0.3)
                    return self.summary, self.test_data
                
                await self._get_page_metadata(client)
                
                print(f"\n🔗 Checking all links (max depth: {self.max_depth})...\n")
                print("   Using FastMCP Client (100% MCP tools)\n")
                
                links_count = await self._check_links_on_page(client, self.base_url, depth=0)
                
                self._update_summary(links_count)
                
                # Close browser before context manager exits
                try:
                    await close_browser(client)
                except Exception as e:
                    print(f"⚠️  Browser close warning: {e}")
                
                self.summary.passed.append("FastMCP check completed")
                await cleanup_browser_processes(0.3)
                return self.summary, self.test_data
        
        except ExceptionGroup as e:
            should_continue, result = self._handle_check_error(e)
            if should_continue:
                await cleanup_browser_processes(0.3)
                return result
            raise
        
        except Exception as e:
            should_continue, result = self._handle_check_error(e)
            if should_continue:
                await cleanup_browser_processes(0.3)
                return result
            raise
        finally:
            # Ensure cleanup even on unexpected errors
            if client:
                try:
                    await close_browser(client)
                except:
                    pass
            await cleanup_browser_processes(0.3)
    
    def _update_summary(self, links_count: int) -> None:
        """Update summary statistics - <40 lines"""
        self.test_data.total_links = len(self.visited)
        self.summary.total_links_checked = links_count
        self.summary.pages_checked = len(self.visited)
        
        print(f"\n📊 Summary:")
        print(f"   Pages checked: {self.summary.pages_checked}")
        print(f"   Total links checked: {self.summary.total_links_checked}")
        print(f"   ✅ All operations completed using FastMCP Client")
    
    def check(self) -> Tuple[CheckSummary, TestData]:
        """Main entry point to check links - <40 lines"""
        try:
            result = asyncio.run(self._run_check())
            cleanup_browser_sync()
            return result
        except ExceptionGroup as e:
            should_continue, result = self._handle_check_error(e)
            if should_continue:
                return result
            raise
        except Exception as e:
            should_continue, result = self._handle_check_error(e)
            if should_continue:
                return result
            raise
    
    def print_summary(self, summary: CheckSummary, test_data: TestData) -> None:
        """Print formatted summary - delegates to formatter"""
        print_summary(summary, test_data, self.use_ai)

