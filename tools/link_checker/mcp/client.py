#!/usr/bin/env python3
"""
MCP client wrapper - reusable MCP operations
Following DRY and Single Responsibility
"""

from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from mcp import ClientSession
    MCPClientSession = ClientSession
else:
    MCPClientSession = Any

REQUIRED_TOOLS = [
    "playwright_navigate",
    "playwright_get_visible_html",
    "playwright_get",
    "playwright_evaluate"
]


async def verify_tools(session: MCPClientSession) -> List[str]:
    """
    Verify required MCP tools are available
    
    Args:
        session: MCP client session
        
    Returns:
        List of missing tool names (empty if all present)
    """
    tools_result = await session.list_tools()
    tool_names = [tool.name for tool in tools_result.tools]
    
    return [t for t in REQUIRED_TOOLS if t not in tool_names]


async def navigate_to_url(
    session: MCPClientSession,
    url: str,
    headless: bool = False
) -> Any:
    """
    Navigate to URL using MCP tool
    
    Args:
        session: MCP client session
        url: URL to navigate to
        headless: Run in headless mode
        
    Returns:
        Navigation result
    """
    nav_args = {"url": url}
    if headless:
        nav_args["headless"] = True
    
    return await session.call_tool("playwright_navigate", arguments=nav_args)


async def get_page_html(session: MCPClientSession) -> str:
    """
    Get visible HTML from current page
    
    Args:
        session: MCP client session
        
    Returns:
        HTML content as string
    """
    html_result = await session.call_tool(
        "playwright_get_visible_html",
        arguments={}
    )
    
    if hasattr(html_result, 'content') and html_result.content:
        return html_result.content[0].text if html_result.content else ""
    
    return ""


async def get_page_title(session: MCPClientSession) -> str:
    """
    Get page title using MCP tool
    
    Args:
        session: MCP client session
        
    Returns:
        Page title or empty string
    """
    try:
        eval_result = await session.call_tool(
            "playwright_evaluate",
            arguments={"expression": "document.title"}
        )
        if hasattr(eval_result, 'content') and eval_result.content:
            return eval_result.content[0].text if eval_result.content else ""
    except Exception:
        pass
    
    return ""


async def check_link(session: MCPClientSession, url: str) -> Any:
    """
    Check if link is accessible using MCP tool
    
    Args:
        session: MCP client session
        url: URL to check
        
    Returns:
        Check result
    """
    return await session.call_tool("playwright_get", arguments={"url": url})

