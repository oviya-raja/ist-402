#!/usr/bin/env python3
"""
Automated Screenshot Capture for W07 Assignment
Uses Playwright to capture required screenshots from OpenAI Assistant page.

Requirements:
- You must be logged into OpenAI Platform in your browser
- Playwright browser must have access to your authenticated session
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import time

# Assistant URL
ASSISTANT_URL = "https://platform.openai.com/assistants/asst_HhWz11KVfZgudaIxXlqXHLt2"

# Screenshot directory
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Screenshot configurations
SCREENSHOTS = [
    {
        "name": "01_agent_configuration",
        "description": "Agent Configuration - Name, Model, Description",
        "selector": None,  # Full page
        "wait_selector": None,
        "wait_time": 3
    },
    {
        "name": "02_tools_setup",
        "description": "Tools Setup - File Search Enabled",
        "selector": None,
        "wait_selector": None,
        "wait_time": 2
    },
    {
        "name": "03_instructions",
        "description": "Instructions/System Prompt",
        "selector": None,
        "wait_selector": None,
        "wait_time": 2
    },
    {
        "name": "04_knowledge_base",
        "description": "Knowledge Base/Vector Store",
        "selector": None,
        "wait_selector": None,
        "wait_time": 2
    },
    {
        "name": "05_test_chat",
        "description": "Test Chat - Conversation",
        "selector": None,
        "wait_selector": None,
        "wait_time": 2
    },
    {
        "name": "06_deployment_evidence",
        "description": "Deployment Evidence - Agent Working",
        "selector": None,
        "wait_selector": None,
        "wait_time": 2
    }
]


async def capture_screenshot(page, config, index):
    """Capture a single screenshot."""
    print(f"\n📸 Capturing: {config['description']}")
    
    # Wait for page to load
    if config.get('wait_time'):
        await asyncio.sleep(config['wait_time'])
    
    # Wait for specific element if specified
    if config.get('wait_selector'):
        try:
            await page.wait_for_selector(config['wait_selector'], timeout=10000)
        except:
            print(f"   ⚠️  Warning: Selector {config['wait_selector']} not found")
    
    # Take screenshot
    screenshot_path = SCREENSHOTS_DIR / f"{config['name']}.png"
    
    if config.get('selector'):
        # Screenshot specific element
        try:
            element = await page.query_selector(config['selector'])
            if element:
                await element.screenshot(path=str(screenshot_path))
                print(f"   ✅ Saved: {screenshot_path}")
            else:
                # Fallback to full page
                await page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"   ✅ Saved (full page): {screenshot_path}")
        except Exception as e:
            print(f"   ⚠️  Error capturing element: {e}")
            # Fallback to full page
            await page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"   ✅ Saved (full page fallback): {screenshot_path}")
    else:
        # Full page screenshot
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"   ✅ Saved: {screenshot_path}")
    
    return screenshot_path


async def main():
    """Main function to capture all screenshots."""
    print("🚀 Starting automated screenshot capture...")
    print(f"📁 Screenshots will be saved to: {SCREENSHOTS_DIR}")
    print(f"🔗 Assistant URL: {ASSISTANT_URL}")
    print("\n⚠️  IMPORTANT: You must be logged into OpenAI Platform!")
    print("   The browser will use your existing session.\n")
    
    async with async_playwright() as p:
        # Launch browser (use existing user data for authentication)
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(
            headless=False,  # Set to True for headless mode
            channel="chrome"  # Use Chrome if available
        )
        
        # Create context with persistent storage (to use existing login)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            # Uncomment to use existing browser profile:
            # storage_state="auth.json"  # If you've saved auth state
        )
        
        page = await context.new_page()
        
        try:
            # Navigate to assistant page
            print(f"\n📍 Navigating to: {ASSISTANT_URL}")
            await page.goto(ASSISTANT_URL, wait_until='networkidle', timeout=30000)
            
            # Wait for page to load
            await asyncio.sleep(5)
            
            # Check if we're logged in
            page_title = await page.title()
            if "Just a moment" in page_title or "Login" in page_title:
                print("\n❌ ERROR: Not logged in or page blocked!")
                print("   Please:")
                print("   1. Log into OpenAI Platform in your browser")
                print("   2. Or run this script manually after logging in")
                return
            
            print(f"✅ Page loaded: {page_title}")
            
            # Capture all screenshots
            captured = []
            for i, config in enumerate(SCREENSHOTS, 1):
                screenshot_path = await capture_screenshot(page, config, i)
                captured.append(screenshot_path)
                await asyncio.sleep(1)  # Small delay between screenshots
            
            print(f"\n✅ Successfully captured {len(captured)} screenshots!")
            print(f"📁 Location: {SCREENSHOTS_DIR}")
            print("\n📋 Captured screenshots:")
            for path in captured:
                print(f"   - {path.name}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\n💡 Tips:")
            print("   - Make sure you're logged into OpenAI Platform")
            print("   - Check your internet connection")
            print("   - Try running the script again")
        
        finally:
            # Keep browser open for a moment to see results
            print("\n⏳ Keeping browser open for 5 seconds...")
            await asyncio.sleep(5)
            await browser.close()


if __name__ == "__main__":
    print("=" * 60)
    print("W07 Assignment - Automated Screenshot Capture")
    print("=" * 60)
    asyncio.run(main())

