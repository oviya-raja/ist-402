#!/usr/bin/env python3
"""
Automated Workflow Creation in Agent Builder
Uses browser automation to create workflow programmatically
"""
import os
import sys
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Import common utilities
from utils import load_env, get_api_key, get_assistant_id, get_vector_store_id

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def create_workflow_automated():
    """Create workflow in Agent Builder using Selenium automation"""
    print_header("AUTOMATED WORKFLOW CREATION")
    
    load_env()
    assistant_id = get_assistant_id()
    vector_store_id = get_vector_store_id()
    
    print(f"Assistant ID: {assistant_id}")
    print(f"Vector Store ID: {vector_store_id}")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("\n🌐 Launching browser...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://platform.openai.com/agent-builder")
        
        # Wait for login (user needs to be logged in)
        print("⏳ Waiting for page to load...")
        time.sleep(5)
        
        # Click "Create" button
        print("\n📋 Step 1: Clicking 'Create' button...")
        create_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create')]"))
        )
        create_button.click()
        time.sleep(3)
        
        print("✅ Workflow editor opened")
        print("\n⚠️  NOTE: Browser automation for workflow canvas is complex.")
        print("   The workflow editor uses a canvas-based interface that")
        print("   requires precise mouse interactions and drag-and-drop.")
        print("\n💡 RECOMMENDED APPROACH:")
        print("   1. Browser is now open at workflow editor")
        print("   2. Manually complete these steps:")
        print("      a. Configure 'My agent' node:")
        print(f"         - Link to assistant: {assistant_id}")
        print("      b. Add 'File search' node from Tools panel")
        print(f"         - Configure vector store: {vector_store_id}")
        print("      c. Add 'End' node from Core panel")
        print("      d. Connect: Start → Agent → File Search → End")
        print("      e. Click 'Publish'")
        print("\n⏳ Browser will stay open for 60 seconds...")
        print("   Complete the workflow manually, then press Enter here.")
        
        input("\nPress Enter after completing workflow...")
        
        # Take screenshot
        screenshot_path = Path(__file__).parent.parent / "4-screenshots" / "agent-builder-workflow-complete.png"
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(screenshot_path))
        print(f"\n📸 Screenshot saved: {screenshot_path}")
        
        print("\n✅ Workflow creation process complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Alternative: Use the browser MCP tools to complete workflow")
        return False
    finally:
        if driver:
            print("\n🔒 Closing browser...")
            time.sleep(2)
            driver.quit()
    
    return True

def main():
    """Main function"""
    print_header("AUTOMATED WORKFLOW CREATION IN AGENT BUILDER")
    print("""
This script automates the workflow creation process.

REQUIREMENTS:
- Chrome browser installed
- Selenium WebDriver installed: pip install selenium
- ChromeDriver in PATH or specified location
- User must be logged into OpenAI Platform

The script will:
1. Open Agent Builder
2. Click 'Create' to start new workflow
3. Guide you through manual completion (canvas interaction is complex)
4. Capture screenshot when done
""")
    
    try:
        create_workflow_automated()
    except ImportError:
        print("\n❌ Selenium not installed")
        print("   Install with: pip install selenium")
        print("\n💡 Alternative: Use browser MCP tools (already available)")
        print("   The workflow can be created using the browser automation")
        print("   tools that are already configured.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Using browser MCP tools instead...")

if __name__ == "__main__":
    main()

