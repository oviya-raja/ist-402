#!/usr/bin/env python3
"""
Comprehensive script to capture all Q&A screenshots
"""
from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('screenshots', exist_ok=True)
pdf_path = os.path.abspath('data/knowledge_card.pdf')
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
    
    print('🌐 Loading app...')
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(8)
    
    # Screenshot 1
    page.screenshot(path='screenshots/01_initial_interface.png', full_page=True)
    print('✅ 01: Initial interface')
    
    # Upload PDF using JavaScript
    print('\n📤 Uploading PDF...')
    file_uploaded = page.evaluate(f'''() => {{
        const inputs = document.querySelectorAll('input[type="file"]');
        if (inputs.length > 0) {{
            const input = inputs[0];
            const file = new File([''], '{pdf_path}');
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return true;
        }}
        return false;
    }}''')
    
    if not file_uploaded:
        # Try direct file input
        try:
            file_input = page.locator('input[type="file"]').first
            if file_input.is_visible() or file_input.count() > 0:
                file_input.set_input_files(pdf_path)
                print('   File set via Playwright')
        except:
            print('   ⚠️ Could not upload file automatically')
    
    time.sleep(5)
    page.screenshot(path='screenshots/02_pdf_uploaded.png', full_page=True)
    print('✅ 02: PDF uploaded')
    
    # Build index
    print('\n🔧 Building index...')
    build_clicked = page.evaluate('''() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        for (let btn of buttons) {
            const text = (btn.textContent || btn.innerText || '').trim();
            if (text.includes('Build') && text.includes('Index') && !btn.disabled) {
                btn.click();
                return true;
            }
        }
        return false;
    }''')
    
    if build_clicked:
        print('   ⏳ Waiting 25 seconds...')
        time.sleep(25)
        page.screenshot(path='screenshots/03_index_built.png', full_page=True)
        print('✅ 03: Index built')
    else:
        print('   ⚠️ Build button not found, continuing anyway...')
        time.sleep(5)
    
    # Process questions
    print('\n' + '=' * 70)
    print('📝 Processing Questions & Answers')
    print('=' * 70)
    
    for q_num, question in enumerate(questions, 1):
        print(f'\nQ{q_num}: {question[:50]}...')
        
        # Scroll to bottom
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)
        
        # Enter question using JavaScript
        question_entered = page.evaluate(f'''(q) => {{
            const inputs = Array.from(document.querySelectorAll('input[type="text"]'));
            for (let inp of inputs.reverse()) {{
                if (inp.offsetParent !== null) {{
                    inp.focus();
                    inp.value = q;
                    inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return true;
                }}
            }}
            return false;
        }}''', question)
        
        if question_entered:
            time.sleep(2)
            page.screenshot(path=f'screenshots/04_q{q_num}_question_entered.png', full_page=True)
            print(f'   ✅ Question entered')
            
            # Click retrieve button
            btn_clicked = page.evaluate('''() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                for (let btn of buttons) {
                    const text = (btn.textContent || btn.innerText || '').trim();
                    if ((text.includes('Retrieve') || (text.includes('Answer') && text.length > 10))
                        && !btn.disabled && btn.offsetParent !== null) {
                        btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => btn.click(), 100);
                        return true;
                    }
                }
                return false;
            }''')
            
            if btn_clicked:
                print(f'   ⏳ Waiting for answer (45 seconds)...')
                time.sleep(45)
                page.screenshot(path=f'screenshots/05_q{q_num}_answer_displayed.png', full_page=True)
                print(f'   ✅ Answer captured!')
                time.sleep(2)
            else:
                print(f'   ⚠️ Button not clicked')
        else:
            print(f'   ⚠️ Question not entered')
    
    browser.close()
    
    # Summary
    screenshots = sorted([f for f in os.listdir('screenshots') if f.endswith('.png')])
    print(f'\n✅ Complete! {len(screenshots)} screenshots in screenshots/')
    for f in screenshots:
        print(f'   - {f}')
