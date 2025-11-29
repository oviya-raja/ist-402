#!/usr/bin/env python3
"""
Automated Workflow Creation using Playwright
Uses Playwright for advanced browser automation including canvas interactions
"""
import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id, get_vector_store_id

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

async def create_workflow_with_playwright():
    """Create workflow in Agent Builder using Playwright automation"""
    print_header("AUTOMATED WORKFLOW CREATION WITH PLAYWRIGHT")
    
    load_env()
    assistant_id = get_assistant_id()
    vector_store_id = get_vector_store_id()
    
    print(f"Assistant ID: {assistant_id}")
    print(f"Vector Store ID: {vector_store_id}")
    
    async with async_playwright() as p:
        # Launch browser
        print("\n🌐 Launching browser...")
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500  # Slow down for visibility
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        try:
            # Navigate to Agent Builder
            print("\n📋 Step 1: Navigating to Agent Builder...")
            await page.goto("https://platform.openai.com/agent-builder", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # Check if we're on login page
            current_url = page.url
            if "auth.openai.com" in current_url or "log-in" in current_url:
                print("\n⚠️  Redirected to login page")
                print("   ⏳ Waiting for manual login...")
                print("   Please log in, then the script will continue")
                # Wait for navigation away from login page
                await page.wait_for_url("https://platform.openai.com/**", timeout=300000)  # 5 minutes
                await asyncio.sleep(2)
            
            # Navigate to Agent Builder again if needed
            if "agent-builder" not in page.url:
                await page.goto("https://platform.openai.com/agent-builder", wait_until="networkidle")
                await asyncio.sleep(2)
            
            # Click Create button
            print("\n📋 Step 2: Clicking 'Create' button...")
            try:
                create_button = page.locator("button:has-text('Create')").first
                await create_button.wait_for(state="visible", timeout=10000)
                await create_button.click()
                await asyncio.sleep(3)
            except Exception as e:
                print(f"   ⚠️  Could not find Create button: {e}")
                print("   💡 Trying alternative selector...")
                # Try alternative selectors
                create_alt = page.locator("button").filter(has_text="Create").first
                if await create_alt.count() > 0:
                    await create_alt.click()
                    await asyncio.sleep(3)
                else:
                    raise
            
            # Wait for workflow editor to load
            print("\n📋 Step 3: Waiting for workflow editor...")
            await page.wait_for_selector('[role="application"]', timeout=10000)
            await asyncio.sleep(2)
            
            # Take initial screenshot
            screenshot_dir = Path(__file__).parent.parent.parent / "4-screenshots" / "agent-builder-workflow"
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(screenshot_dir / "01-workflow-editor-initial.png"), full_page=True)
            print(f"📸 Screenshot saved: 01-workflow-editor-initial.png")
            
            # Step 4: Configure "My agent" node
            print("\n📋 Step 4: Configuring 'My agent' node...")
            # Click on the agent node (try to find it on canvas)
            # The canvas might use different selectors, so we'll try multiple approaches
            try:
                # Try clicking on canvas where agent node might be
                canvas = page.locator('[role="application"]')
                # Get canvas dimensions and click approximately where agent node is
                canvas_box = await canvas.bounding_box()
                if canvas_box:
                    # Click approximately where "My agent" node is (right side of start node)
                    agent_x = canvas_box['x'] + canvas_box['width'] * 0.4
                    agent_y = canvas_box['y'] + canvas_box['height'] * 0.5
                    await page.mouse.click(agent_x, agent_y)
                    await asyncio.sleep(1)
                    
                    # Look for configuration panel
                    # Try to find assistant selector
                    assistant_input = page.locator('input[placeholder*="assistant"], input[placeholder*="Assistant"], select').first
                    if await assistant_input.count() > 0:
                        await assistant_input.fill(assistant_id)
                        print(f"   ✅ Configured assistant: {assistant_id}")
            except Exception as e:
                print(f"   ⚠️  Could not configure via click: {e}")
                print("   💡 Will need manual configuration")
            
            # Step 5: Add File Search node
            print("\n📋 Step 5: Adding 'File search' node...")
            try:
                # Find "File search" in the components panel (left sidebar)
                file_search_button = page.locator('text=File search').first
                if await file_search_button.count() > 0:
                    # Get position of file search button
                    box = await file_search_button.bounding_box()
                    if box:
                        # Click to add node
                        await file_search_button.click()
                        await asyncio.sleep(1)
                        print("   ✅ File search node added")
                        
                        # Try to configure it
                        # Click on the newly added node
                        canvas_box = await canvas.bounding_box()
                        if canvas_box:
                            # Click where file search node might be (further right)
                            file_search_x = canvas_box['x'] + canvas_box['width'] * 0.6
                            file_search_y = canvas_box['y'] + canvas_box['height'] * 0.5
                            await page.mouse.click(file_search_x, file_search_y)
                            await asyncio.sleep(1)
                            
                            # Try to configure vector store
                            vs_input = page.locator('input[placeholder*="vector"], input[placeholder*="Vector"]').first
                            if await vs_input.count() > 0:
                                await vs_input.fill(vector_store_id)
                                print(f"   ✅ Configured vector store: {vector_store_id}")
            except Exception as e:
                print(f"   ⚠️  Could not add file search node: {e}")
                print("   💡 Will need manual addition")
            
            # Step 6: Add End node
            print("\n📋 Step 6: Adding 'End' node...")
            try:
                end_button = page.locator('text=End').first
                if await end_button.count() > 0:
                    await end_button.click()
                    await asyncio.sleep(1)
                    print("   ✅ End node added")
            except Exception as e:
                print(f"   ⚠️  Could not add End node: {e}")
                print("   💡 Will need manual addition")
            
            # Step 7: Connect nodes (drag and drop)
            print("\n📋 Step 7: Connecting nodes...")
            print("   ⚠️  Node connections require precise drag-and-drop")
            print("   💡 Will need manual connection or advanced canvas API")
            
            # Step 8: Rename workflow
            print("\n📋 Step 8: Renaming workflow...")
            try:
                workflow_title = page.locator('text=New workflow, text="Draft"').first
                if await workflow_title.count() > 0:
                    await workflow_title.click()
                    await asyncio.sleep(0.5)
                    await page.keyboard.type("Job Fitment Analysis Workflow")
                    await page.keyboard.press("Enter")
                    print("   ✅ Workflow renamed")
            except Exception as e:
                print(f"   ⚠️  Could not rename: {e}")
            
            # Take final screenshot
            await page.screenshot(path=str(screenshot_dir / "02-workflow-editor-complete.png"), full_page=True)
            print(f"📸 Screenshot saved: 02-workflow-editor-complete.png")
            
            print("\n✅ Automation steps completed!")
            print("\n📋 Next Steps:")
            print("   1. Review workflow in browser")
            print("   2. Complete any manual steps if needed:")
            print("      - Connect nodes (drag from output to input ports)")
            print("      - Verify configurations")
            print("   3. Click 'Publish' button")
            print("   4. Capture final screenshots")
            
            # Keep browser open for review
            print("\n⏳ Browser will stay open for 60 seconds for review...")
            await asyncio.sleep(60)
            
        except PlaywrightTimeout as e:
            print(f"\n⏱️  Timeout: {e}")
            print("   Page may be loading slowly")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\n🔒 Closing browser...")
            await browser.close()

def main():
    """Main function"""
    print_header("PLAYWRIGHT WORKFLOW AUTOMATION")
    print("""
This script uses Playwright for advanced browser automation.

REQUIREMENTS:
- Playwright installed: pip install playwright
- Playwright browsers installed: playwright install chromium

The script will:
1. Open Agent Builder
2. Create new workflow
3. Configure nodes
4. Add File Search and End nodes
5. Guide through completion
""")
    
    try:
        asyncio.run(create_workflow_with_playwright())
    except ImportError:
        print("\n❌ Playwright not installed")
        print("   Install with: pip install playwright")
        print("   Then install browsers: playwright install chromium")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

