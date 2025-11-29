#!/usr/bin/env python3
"""
MCP browser lifecycle manager - Domain-specific browser management for MCP
Following Single Responsibility Principle
"""

from typing import Any, List
import asyncio


async def close_browser(session: Any) -> bool:
    """
    Close browser using available MCP tools
    
    Args:
        session: FastMCP client session
        
    Returns:
        True if browser was closed successfully
    """
    try:
        # FastMCP client has list_tools() that returns a list directly
        try:
            tools = await session.list_tools()
            # Handle both list and object with .tools attribute
            if hasattr(tools, 'tools'):
                tool_names = [tool.name for tool in tools.tools]
            else:
                tool_names = [tool.name for tool in tools]
        except:
            # If list_tools fails, try methods directly
            tool_names = []
        
        # Try different close methods
        close_methods = ["playwright_close", "playwright_close_browser"]
        for method in close_methods:
            if not tool_names or method in tool_names:
                try:
                    await session.call_tool(method, arguments={})
                    await asyncio.sleep(0.2)  # Brief delay for cleanup
                    return True
                except:
                    continue
        
        # Fallback: try window.close() via evaluate
        try:
            await session.call_tool("playwright_evaluate", arguments={
                "expression": "window.close()"
            })
            await asyncio.sleep(0.2)
            return True
        except:
            pass
        
        return False
    except Exception:
        return False


async def cleanup_browser_processes(delay: float = 0.5) -> None:
    """
    Wait for browser processes to clean up
    
    Args:
        delay: Delay in seconds
    """
    await asyncio.sleep(delay)


def cleanup_browser_sync(delay: float = 0.5) -> None:
    """
    Synchronous cleanup for browser processes
    
    Args:
        delay: Delay in seconds
    """
    import time
    time.sleep(delay)

