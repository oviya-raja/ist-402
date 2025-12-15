#!/usr/bin/env python3
"""
Script to capture screenshots of all example questions and answers
"""
from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('screenshots', exist_ok=True)
pdf_path = os.path.abspath('data/knowledge_card.pdf')
url = 'https://computing-triumph-acres-majority.trycloudflare.com'

# All example questions
questions = [
    "What is the main topic of this document?",
    "Summarize the key findings",
    "Explain the methodology used",
    "What are the limitations mentioned?"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    print('🌐 Navigating to Streamlit app...')
    page.goto(url, wait_until='networkidle', timeout=60000)
    time.sleep(6)
    
    # Screenshot 1: Initial interface
    page.screenshot(path='screenshots/01_initial_interface.png', full_page=True)
    print('✅ Screenshot 1: Initial interface')
    
    # Upload PDF - Streamlit file uploader
    print('\n📤 Uploading PDF file...')
    # Streamlit uses a hidden file input that gets triggered
    file_input = page.locator('input[type="file"]')
    
    if file_input.count() > 0:
        # Set the file
        file_input.first.set_input_files(pdf_path)
        print('   File selected, waiting for upload...')
        time.sleep(5)
        
        page.screenshot(path='screenshots/02_pdf_uploaded.png', full_page=True)
        print('✅ Screenshot 2: PDF uploaded')
        
        # Build index
        print('\n🔧 Building FAISS index...')
        # Find build button - try multiple selectors
        build_clicked = False
        for attempt in range(3):
            try:
                # Try different button finding strategies
                buttons = page.locator('button').all()
                for btn in buttons:
                    try:
                        btn_text = btn.inner_text().strip()
                        if 'Build' in btn_text and 'Index' in btn_text:
                            if btn.is_visible() and btn.is_enabled():
                                btn.click()
                                build_clicked = True
                                print(f'   ✅ Clicked Build Index button (attempt {attempt + 1})')
                                break
                    except:
                        continue
                if build_clicked:
                    break
            except Exception as e:
                print(f'   Attempt {attempt + 1} failed: {e}')
                time.sleep(2)
        
        if build_clicked:
            print('   ⏳ Waiting for index to build (25 seconds)...')
            time.sleep(25)
            page.screenshot(path='screenshots/03_index_built.png', full_page=True)
            print('✅ Screenshot 3: Index built')
            
            # Process each question
            print('\n' + '=' * 70)
            print('📝 Processing All Example Questions')
            print('=' * 70)
            
            for q_num, question in enumerate(questions, 1):
                print(f'\n📌 Question {q_num}/{len(questions)}: {question}')
                print('-' * 70)
                
                # Scroll to bottom to see question section
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2)
                
                # Find the question text input
                # Streamlit text inputs are usually the last visible text input
                text_inputs = page.locator('input[type="text"]').all()
                question_input = None
                
                # Try to find the question input (usually the last one)
                for inp in reversed(text_inputs):
                    try:
                        if inp.is_visible():
                            # Check if it's in the question section by scrolling to it
                            inp.scroll_into_view_if_needed()
                            time.sleep(0.5)
                            question_input = inp
                            break
                    except:
                        continue
                
                if question_input:
                    # Clear and enter question
                    question_input.click()
                    time.sleep(0.5)
                    question_input.fill('')  # Clear
                    time.sleep(0.3)
                    question_input.type(question, delay=50)  # Type slowly
                    time.sleep(2)
                    
                    # Screenshot: Question entered
                    page.screenshot(path=f'screenshots/04_q{q_num}_question_entered.png', full_page=True)
                    print(f'   ✅ Question entered')
                    
                    # Find and click retrieve button
                    print('   🔍 Finding retrieve button...')
                    retrieve_clicked = False
                    
                    # Get all buttons
                    all_buttons = page.locator('button').all()
                    
                    for btn in all_buttons:
                        try:
                            if not btn.is_visible():
                                continue
                            
                            btn_text = btn.inner_text().strip()
                            
                            # Look for retrieve/answer button
                            if ('Retrieve' in btn_text or 
                                ('Answer' in btn_text and len(btn_text) > 8 and 'Clear' not in btn_text)):
                                # Check if enabled
                                is_enabled = btn.is_enabled()
                                if is_enabled:
                                    print(f'   ✅ Found enabled button: "{btn_text}"')
                                    btn.scroll_into_view_if_needed()
                                    time.sleep(0.5)
                                    btn.click()
                                    retrieve_clicked = True
                                    break
                        except Exception as e:
                            continue
                    
                    if retrieve_clicked:
                        print(f'   ⏳ Waiting for answer generation (35 seconds)...')
                        time.sleep(35)  # Wait for retrieval + generation
                        
                        # Screenshot: Answer displayed
                        page.screenshot(path=f'screenshots/05_q{q_num}_answer_displayed.png', full_page=True)
                        print(f'   ✅ Answer captured!')
                        
                        # Brief pause before next question
                        time.sleep(2)
                    else:
                        print(f'   ⚠️ Could not find enabled retrieve button')
                        # Take screenshot anyway
                        page.screenshot(path=f'screenshots/04_q{q_num}_question_only.png', full_page=True)
                else:
                    print(f'   ⚠️ Could not find question input field')
        else:
            print('⚠️ Could not click Build Index button')
    else:
        print('⚠️ Could not find file upload input')
    
    browser.close()
    
    # Summary
    print('\n' + '=' * 70)
    print('✅ Screenshot Capture Complete!')
    print('=' * 70)
    
    screenshot_files = sorted([f for f in os.listdir('screenshots') if f.endswith('.png')])
    print(f'\n📸 Total screenshots: {len(screenshot_files)}')
    for f in screenshot_files:
        size = os.path.getsize(f'screenshots/{f}') / 1024
        print(f'   - {f} ({size:.1f} KB)')
    print(f'\n📁 Location: {os.path.abspath("screenshots")}')
