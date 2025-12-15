#!/usr/bin/env python3
"""
Script to capture answer screenshots for all example questions
Assumes PDF is already uploaded and index is built
"""
from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('screenshots', exist_ok=True)
url = 'https://computing-triumph-acres-majority.trycloudflare.com'

questions = [
    "What is the main topic of this document?",
    "Summarize the key findings",
    "Explain the methodology used",
    "What are the limitations mentioned?"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    
    print('🌐 Loading Streamlit app...')
    page.goto(url, wait_until='networkidle', timeout=60000)
    time.sleep(6)
    
    print('\n📝 Processing questions (assuming index is already built)...')
    print('=' * 70)
    
    for q_num, question in enumerate(questions, 1):
        print(f'\n📌 Question {q_num}: {question[:60]}...')
        
        # Scroll to question section
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)
        
        # Find text input - get all and use the last visible one
        inputs = page.query_selector_all('input[type="text"]')
        question_input = None
        
        for inp in reversed(inputs):
            try:
                if page.evaluate('(el) => el.offsetParent !== null', inp):
                    question_input = inp
                    break
            except:
                continue
        
        if question_input:
            # Clear and enter question
            question_input.click()
            time.sleep(0.5)
            question_input.evaluate('el => el.value = ""')
            time.sleep(0.3)
            question_input.type(question, delay=30)
            time.sleep(2)
            
            # Screenshot: Question
            page.screenshot(path=f'screenshots/04_q{q_num}_question_entered.png', full_page=True)
            print(f'   ✅ Question entered')
            
            # Find retrieve button using JavaScript
            retrieve_btn = page.evaluate('''() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                for (let btn of buttons) {
                    const text = btn.textContent || btn.innerText || '';
                    if ((text.includes('Retrieve') || (text.includes('Answer') && text.length > 8)) 
                        && !btn.disabled && btn.offsetParent !== null) {
                        return true;
                    }
                }
                return false;
            }''')
            
            if retrieve_btn:
                # Click using JavaScript
                page.evaluate('''() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    for (let btn of buttons) {
                        const text = btn.textContent || btn.innerText || '';
                        if ((text.includes('Retrieve') || (text.includes('Answer') && text.length > 8)) 
                            && !btn.disabled && btn.offsetParent !== null) {
                            btn.click();
                            return true;
                        }
                    }
                    return false;
                }''')
                
                print(f'   ⏳ Waiting for answer (40 seconds)...')
                time.sleep(40)
                
                # Screenshot: Answer
                page.screenshot(path=f'screenshots/05_q{q_num}_answer_displayed.png', full_page=True)
                print(f'   ✅ Answer captured!')
                time.sleep(2)
            else:
                print(f'   ⚠️ Button not found')
        else:
            print(f'   ⚠️ Input not found')
    
    browser.close()
    
    # List all screenshots
    screenshots = sorted([f for f in os.listdir('screenshots') if f.endswith('.png')])
    print(f'\n📸 Total screenshots: {len(screenshots)}')
    for f in screenshots:
        print(f'   - {f}')
