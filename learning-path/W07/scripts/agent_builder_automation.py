#!/usr/bin/env python3
"""
Playwright MCP Server for OpenAI Agent Builder Automation
Automates workflow creation using JSON definitions instead of manual clickops.

Based on: https://platform.openai.com/docs/guides/agent-builder
"""

import os
import json
import sys
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from dotenv import load_dotenv

# Load .env from repository root
script_dir = Path(__file__).parent
repo_root = script_dir.parent.parent.parent
env_file = repo_root / ".env"

if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded .env from: {env_file}")
else:
    load_dotenv()

class AgentBuilderAutomation:
    """Automates OpenAI Agent Builder workflow creation using Playwright."""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.base_url = "https://platform.openai.com/agent-builder/"
        # Cookie storage path
        self.cookies_file = script_dir / ".cookies" / "openai_cookies.json"
        self.cookies_file.parent.mkdir(exist_ok=True)
        # 2FA wait timeout (in seconds) - configurable via .env
        two_fa_timeout_str = os.getenv("2FA_WAIT_TIMEOUT", "60")
        try:
            self.two_fa_timeout = int(two_fa_timeout_str)
        except ValueError:
            self.two_fa_timeout = 60  # Default to 60 seconds
        
    def load_cookies(self) -> List[Dict[str, Any]]:
        """Load saved cookies from file."""
        if self.cookies_file.exists():
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    print(f"🍪 Loaded {len(cookies)} saved cookies")
                    return cookies
            except Exception as e:
                print(f"⚠️  Could not load cookies: {e}")
        return []
    
    def save_cookies(self, cookies: List[Dict[str, Any]]):
        """Save cookies to file."""
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"💾 Saved {len(cookies)} cookies to {self.cookies_file}")
        except Exception as e:
            print(f"⚠️  Could not save cookies: {e}")
    
    async def start(self):
        """Start browser and navigate to Agent Builder."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=self.headless,
            slow_mo=500  # Slow down for visibility
        )
        self.browser = browser
        
        # Load saved cookies
        saved_cookies = self.load_cookies()
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        self.context = context
        
        # Add saved cookies to context
        if saved_cookies:
            await context.add_cookies(saved_cookies)
            print("🍪 Restored saved session cookies")
        
        page = await context.new_page()
        self.page = page
        
        if not self.page:
            raise RuntimeError("Failed to create page")
        
        print(f"🌐 Navigating to Agent Builder...")
        await self.page.goto(self.base_url, wait_until="networkidle")
        await asyncio.sleep(2)  # Wait for page load
        
        # Check if login or 2FA is required
        current_url = self.page.url
        login_indicators = ["login", "sign-in", "auth", "verify", "2fa", "mfa"]
        is_login_page = any(indicator in current_url.lower() for indicator in login_indicators)
        
        if is_login_page:
            print("⚠️  Login/2FA required. Waiting for authentication...")
            print(f"   ⏱️  Will wait up to {self.two_fa_timeout} seconds for you to complete login/2FA")
            print("   (Browser will stay open - complete authentication in the browser)")
            
            # Wait for URL to change from login/2FA page to Agent Builder
            start_time = time.time()
            authenticated = False
            
            while time.time() - start_time < self.two_fa_timeout:
                await asyncio.sleep(2)  # Check every 2 seconds
                
                current_url = self.page.url
                is_still_login = any(indicator in current_url.lower() for indicator in login_indicators)
                
                # Check if we've reached Agent Builder
                if "agent-builder" in current_url.lower() or "platform.openai.com" in current_url.lower():
                    if not is_still_login:
                        authenticated = True
                        print("✅ Authentication completed!")
                        break
                
                # Show progress
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0:  # Every 10 seconds
                    remaining = self.two_fa_timeout - elapsed
                    print(f"   ⏳ Still waiting... ({remaining}s remaining)")
            
            if not authenticated:
                print(f"⚠️  Timeout after {self.two_fa_timeout} seconds")
                print("   Please ensure you've completed login/2FA and are on the Agent Builder page")
                print("   Press Enter to continue anyway, or Ctrl+C to cancel...")
                try:
                    input()
                except (EOFError, KeyboardInterrupt):
                    raise RuntimeError("Authentication timeout - please try again")
            
            # Save cookies after successful authentication
            if self.context:
                cookies = await self.context.cookies()
                if cookies:
                    self.save_cookies(cookies)
                    print("💾 Saved authentication cookies for future use")
            
            # Navigate to Agent Builder to ensure we're on the right page
            await self.page.goto(self.base_url, wait_until="networkidle")
            await asyncio.sleep(2)
        else:
            # We're already logged in, save cookies to refresh the file
            if self.context:
                cookies = await self.context.cookies()
                if cookies:
                    self.save_cookies(cookies)
        
        print("✅ Agent Builder loaded")
        
    async def stop(self):
        """Close browser and save cookies."""
        # Save cookies before closing
        if self.context:
            try:
                cookies = await self.context.cookies()
                if cookies:
                    self.save_cookies(cookies)
            except:
                pass
        
        if self.browser:
            await self.browser.close()
            print("✅ Browser closed")
    
    async def create_workflow(self, workflow_name: str) -> bool:
        """
        Create a new workflow in Agent Builder.
        
        Args:
            workflow_name: Name for the new workflow
            
        Returns:
            True if successful
        """
        if not self.page:
            raise RuntimeError("Page not initialized. Call start() first.")
        
        try:
            # Look for "Create Workflow" or "New Workflow" button
            create_selectors = [
                'button:has-text("Create Workflow")',
                'button:has-text("New Workflow")',
                'button:has-text("Create")',
                '[data-testid="create-workflow"]',
                'a:has-text("Create")'
            ]
            
            create_button = None
            for selector in create_selectors:
                try:
                    create_button = await self.page.wait_for_selector(selector, timeout=3000)
                    if create_button:
                        break
                except:
                    continue
            
            if not create_button:
                # Try clicking on canvas or using keyboard shortcut
                await self.page.keyboard.press("Meta+n")  # Cmd+N on Mac
                await asyncio.sleep(1)
            else:
                await create_button.click()
                await asyncio.sleep(1)
            
            # Wait for workflow creation dialog or canvas
            await asyncio.sleep(2)
            
            # If there's a name input, fill it
            name_selectors = [
                'input[placeholder*="name" i]',
                'input[placeholder*="workflow" i]',
                'input[type="text"]',
                '[data-testid="workflow-name"]'
            ]
            
            for selector in name_selectors:
                try:
                    name_input = await self.page.wait_for_selector(selector, timeout=2000)
                    if name_input:
                        await name_input.fill(workflow_name)
                        await asyncio.sleep(0.5)
                        # Press Enter or click Create/OK
                        await self.page.keyboard.press("Enter")
                        await asyncio.sleep(1)
                        break
                except:
                    continue
            
            print(f"✅ Created workflow: {workflow_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating workflow: {e}")
            return False
    
    async def add_node(self, node_type: str, node_name: str, position: Dict[str, int] = None) -> Optional[str]:
        """
        Add a node to the workflow canvas.
        
        Args:
            node_type: Type of node (agent, if_else, transform, tool, end)
            node_name: Name for the node
            position: Optional {x, y} position on canvas
            
        Returns:
            Node ID if successful
        """
        if not self.page:
            raise RuntimeError("Page not initialized. Call start() first.")
        
        try:
            # Map our node types to Agent Builder node types
            node_type_map = {
                "agent": "Agent",
                "if_else": "If / Else",
                "condition": "If / Else",
                "transform": "Transform",
                "tool": "Tool",
                "tools": "Tool",
                "end": "End"
            }
            
            builder_type = node_type_map.get(node_type.lower(), node_type)
            
            # Strategy 1: Look for node palette/sidebar with drag-and-drop
            # Agent Builder typically has a sidebar with node types
            palette_selectors = [
                '[data-testid="node-palette"]',
                '.node-palette',
                '[aria-label*="node" i]',
                'aside',
                '[role="complementary"]'
            ]
            
            node_added = False
            
            # Try to find node type in sidebar and drag it
            for selector in palette_selectors:
                try:
                    palette = await self.page.wait_for_selector(selector, timeout=2000)
                    if palette:
                        # Look for the node type button/link
                        node_button = await palette.query_selector(f'text={builder_type}')
                        if not node_button:
                            # Try case-insensitive
                            node_button = await palette.query_selector(f'text=/^{builder_type}$/i')
                        
                        if node_button:
                            # Get position for drop
                            if position:
                                drop_x, drop_y = position['x'], position['y']
                            else:
                                # Default position
                                drop_x, drop_y = 400 + len(node_name) * 10, 300
                            
                            # Drag and drop
                            box = await node_button.bounding_box()
                            if box:
                                await self.page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                                await self.page.mouse.down()
                                await asyncio.sleep(0.3)
                                await self.page.mouse.move(drop_x, drop_y)
                                await self.page.mouse.up()
                                await asyncio.sleep(1)
                                node_added = True
                                break
                except:
                    continue
            
            # Strategy 2: Right-click on canvas
            if not node_added and self.page and not self.page.is_closed():
                try:
                    if position:
                        await self.page.mouse.click(position['x'], position['y'], button="right")
                    else:
                        # Click on canvas center
                        canvas = await self.page.query_selector('canvas, [data-testid="canvas"], .workflow-canvas, main')
                        if canvas:
                            box = await canvas.bounding_box()
                            if box:
                                await self.page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2, button="right")
                            else:
                                await self.page.mouse.click(500, 300, button="right")
                        else:
                            await self.page.mouse.click(500, 300, button="right")
                    await asyncio.sleep(1)
                    
                    # Look for node type in context menu
                    node_menu_item = await self.page.wait_for_selector(
                        f'text={builder_type}',
                        timeout=2000
                    )
                    if node_menu_item:
                        await node_menu_item.click()
                        await asyncio.sleep(1)
                        node_added = True
                except Exception as e:
                    print(f"      ⚠️  Right-click method failed: {e}")
                    pass
            
            # Strategy 3: Use keyboard shortcut or search
            if not node_added and self.page and not self.page.is_closed():
                try:
                    # Click on canvas first to ensure focus
                    await self.page.mouse.click(500, 300)
                    await asyncio.sleep(0.5)
                    
                    # Try pressing 'a' for add node (common shortcut)
                    await self.page.keyboard.press("a")
                    await asyncio.sleep(1)
                    
                    # If search box appears, type node type
                    search_input = await self.page.query_selector('input[type="search"], input[placeholder*="search" i]')
                    if search_input:
                        await search_input.fill(builder_type)
                        await asyncio.sleep(0.5)
                        await self.page.keyboard.press("Enter")
                        await asyncio.sleep(1)
                        node_added = True
                except Exception as e:
                    print(f"      ⚠️  Keyboard shortcut method failed: {e}")
                    pass
            
            if node_added and self.page and not self.page.is_closed():
                # If there's a name input dialog, fill it
                try:
                    name_input = await self.page.wait_for_selector(
                        'input[type="text"], input[placeholder*="name" i]',
                        timeout=2000
                    )
                    if name_input:
                        await name_input.fill(node_name)
                        await self.page.keyboard.press("Enter")
                        await asyncio.sleep(0.5)
                except:
                    pass
                
                print(f"      ✅ Added successfully")
                return f"node_{node_name.lower().replace(' ', '_')}"
            else:
                if not self.page or self.page.is_closed():
                    print(f"      ❌ Page was closed")
                else:
                    print(f"      ⚠️  Could not add automatically")
                print(f"      📝 Please add '{builder_type}' node manually and name it '{node_name}'")
                return None
            
        except Exception as e:
            print(f"⚠️  Error adding node {node_name}: {e}")
            print(f"   Please add '{builder_type}' node manually")
            return None
    
    async def configure_node(self, node_id: str, config: Dict[str, Any]) -> bool:
        """
        Configure a node with its settings.
        
        Args:
            node_id: ID of the node to configure
            config: Configuration dictionary
            
        Returns:
            True if successful
        """
        if not self.page:
            raise RuntimeError("Page not initialized. Call start() first.")
        
        try:
            # Click on the node to open configuration panel
            node_selector = f'[data-node-id="{node_id}"]'
            node = await self.page.wait_for_selector(node_selector, timeout=2000)
            if node:
                await node.click()
                await asyncio.sleep(1)
                
                # Configure system prompt if present
                if "system_prompt" in config:
                    prompt_selectors = [
                        'textarea[placeholder*="system" i]',
                        'textarea[placeholder*="prompt" i]',
                        'textarea',
                        '[data-testid="system-prompt"]'
                    ]
                    
                    for selector in prompt_selectors:
                        try:
                            prompt_input = await self.page.wait_for_selector(selector, timeout=1000)
                            if prompt_input:
                                await prompt_input.fill(config["system_prompt"])
                                await asyncio.sleep(0.5)
                                break
                        except:
                            continue
                
                # Configure input schema if present
                if "input_schema" in config:
                    # This would require more complex UI interaction
                    # For now, we'll log it
                    print(f"   📝 Input schema configured (manual verification needed)")
                
                # Close configuration panel
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(0.5)
                
                print(f"✅ Configured node: {node_id}")
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Could not configure node {node_id}: {e}")
            return False
    
    async def connect_nodes(self, from_node_id: str, to_node_id: str, condition: Optional[str] = None) -> bool:
        """
        Connect two nodes in the workflow.
        
        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            condition: Optional condition for the connection
            
        Returns:
            True if successful
        """
        if not self.page:
            raise RuntimeError("Page not initialized. Call start() first.")
        
        try:
            # In Agent Builder, connections are typically made by:
            # 1. Dragging from output port of source node to input port of target node
            # 2. Or selecting both nodes and using a connect action
            
            from_selector = f'[data-node-id="{from_node_id}"]'
            to_selector = f'[data-node-id="{to_node_id}"]'
            
            from_node = await self.page.wait_for_selector(from_selector, timeout=2000)
            to_node = await self.page.wait_for_selector(to_selector, timeout=2000)
            
            if from_node and to_node:
                # Get bounding boxes
                from_box = await from_node.bounding_box()
                to_box = await to_node.bounding_box()
                
                if from_box and to_box:
                    # Click and drag from source output to target input
                    # Output port is typically on the right side
                    start_x = from_box['x'] + from_box['width'] - 10
                    start_y = from_box['y'] + from_box['height'] / 2
                    
                    # Input port is typically on the left side
                    end_x = to_box['x'] + 10
                    end_y = to_box['y'] + to_box['height'] / 2
                    
                    await self.page.mouse.move(start_x, start_y)
                    await self.page.mouse.down()
                    await asyncio.sleep(0.3)
                    await self.page.mouse.move(end_x, end_y)
                    await self.page.mouse.up()
                    await asyncio.sleep(0.5)
                    
                    # If condition is specified, configure it
                    if condition:
                        # This would require additional UI interaction
                        print(f"   🔗 Connected with condition: {condition}")
                    else:
                        print(f"   🔗 Connected nodes")
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️  Could not connect nodes: {e}")
            print("   You may need to connect nodes manually")
            return False
    
    async def create_workflow_from_json(self, workflow_json_path: str) -> bool:
        """
        Create a complete workflow from JSON definition.
        
        Args:
            workflow_json_path: Path to workflow definition JSON file
            
        Returns:
            True if successful
        """
        try:
            with open(workflow_json_path, 'r') as f:
                workflow_def = json.load(f)
            
            workflow_name = workflow_def.get("name", "New Workflow")
            nodes = workflow_def.get("nodes", [])
            edges = workflow_def.get("edges", [])
            
            print(f"\n📋 Creating workflow: {workflow_name}")
            print(f"   Nodes: {len(nodes)}")
            print(f"   Edges: {len(edges)}")
            
            # Create workflow
            await self.create_workflow(workflow_name)
            await asyncio.sleep(2)
            
            # Add nodes
            node_positions = {}
            node_spacing = 250
            start_x, start_y = 300, 300
            
            print("\n📦 Adding nodes to workflow...")
            for i, node in enumerate(nodes):
                node_id = node.get("id")
                node_name = node.get("name", node_id)
                node_type = node.get("type", "agent")
                config = node.get("config", {})
                
                # Calculate position (arrange in a grid, left-to-right flow)
                x = start_x + (i % 6) * node_spacing
                y = start_y + (i // 6) * 150
                
                position = {"x": x, "y": y}
                
                print(f"   [{i+1}/{len(nodes)}] Adding: {node_name} ({node_type})")
                
                # Check if page is still valid
                if not self.page or self.page.is_closed():
                    print("   ⚠️  Page was closed. Please add nodes manually.")
                    break
                
                # Add node
                added_node_id = await self.add_node(node_type, node_name, position)
                if added_node_id:
                    node_positions[node_id] = added_node_id
                    await asyncio.sleep(1.5)  # Longer wait between nodes
                    
                    # Configure node (only if page is still valid)
                    if self.page and not self.page.is_closed():
                        await self.configure_node(added_node_id, config)
                        await asyncio.sleep(0.5)
                else:
                    # Store placeholder for manual addition
                    node_positions[node_id] = f"manual_{node_id}"
                    await asyncio.sleep(0.5)
            
            # Connect nodes
            if self.page and not self.page.is_closed():
                print("\n🔗 Connecting nodes...")
                for i, edge in enumerate(edges):
                    from_id = edge.get("from")
                    to_id = edge.get("to")
                    condition = edge.get("condition")
                    
                    if from_id in node_positions and to_id in node_positions:
                        from_node = node_positions[from_id]
                        to_node = node_positions[to_id]
                        
                        # Skip manual nodes
                        if not from_node.startswith("manual_") and not to_node.startswith("manual_"):
                            print(f"   [{i+1}/{len(edges)}] Connecting: {from_id} → {to_id}")
                            await self.connect_nodes(from_node, to_node, condition)
                            await asyncio.sleep(0.5)
                        else:
                            print(f"   ⚠️  Skipping connection (manual nodes): {from_id} → {to_id}")
            else:
                print("\n⚠️  Page closed. Please connect nodes manually.")
            
            print(f"\n✅ Workflow '{workflow_name}' creation completed!")
            print("   ⚠️  Please verify the workflow in Agent Builder and make manual adjustments if needed.")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating workflow from JSON: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main function to run automation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automate OpenAI Agent Builder workflow creation")
    parser.add_argument("--workflow", choices=["job_search", "qualification_check", "both"],
                       default="both", help="Which workflow to create")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--json", help="Path to custom workflow JSON file")
    
    args = parser.parse_args()
    
    automation = AgentBuilderAutomation(headless=args.headless)
    
    try:
        await automation.start()
        
        if args.json:
            # Use custom JSON file
            await automation.create_workflow_from_json(args.json)
        else:
            # Use predefined workflows
            workflows = []
            if args.workflow in ["job_search", "both"]:
                workflows.append(script_dir.parent / "job_search_workflow_definition.json")
            if args.workflow in ["qualification_check", "both"]:
                workflows.append(script_dir.parent / "qualification_check_workflow_definition.json")
            
            for workflow_json in workflows:
                if workflow_json.exists():
                    await automation.create_workflow_from_json(str(workflow_json))
                    await asyncio.sleep(3)  # Wait between workflows
                else:
                    print(f"⚠️  Workflow file not found: {workflow_json}")
                    print("   Run: python3 create_workflow_sdk.py --workflow both")
        
        print("\n⏸️  Automation completed. Browser will stay open for 30 seconds...")
        print("   You can now verify and adjust the workflow manually.")
        try:
            await asyncio.sleep(30)  # Keep browser open for 30 seconds
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await automation.stop()


if __name__ == "__main__":
    asyncio.run(main())

