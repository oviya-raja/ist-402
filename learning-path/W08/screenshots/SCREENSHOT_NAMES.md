# Screenshot Filenames for PDF Q&A System

## Existing Screenshots (Already Captured)
- `01_initial_interface.png` ✅
- `02_pdf_uploaded.png` ✅
- `03_index_built.png` ✅
- `04_question_entered.png` ✅ (This is for the first question)

## Required Screenshots for All Questions & Answers

### Question 1: "What is the main topic of this document?"
- `04_q1_question_entered.png` - Question entered in the input field
- `05_q1_answer_displayed.png` - Answer displayed with retrieved chunks

### Question 2: "Summarize the key findings"
- `04_q2_question_entered.png` - Question entered in the input field
- `05_q2_answer_displayed.png` - Answer displayed with retrieved chunks

### Question 3: "Explain the methodology used"
- `04_q3_question_entered.png` - Question entered in the input field
- `05_q3_answer_displayed.png` - Answer displayed with retrieved chunks

### Question 4: "What are the limitations mentioned?"
- `04_q4_question_entered.png` - Question entered in the input field
- `05_q4_answer_displayed.png` - Answer displayed with retrieved chunks

## Summary

**Total screenshots needed:**
- 4 existing screenshots (setup flow)
- 8 new screenshots (4 questions × 2 screenshots each = 8)
- **Total: 12 screenshots**

## Naming Convention
- `04_q{N}_question_entered.png` - Shows the question in the input field
- `05_q{N}_answer_displayed.png` - Shows the complete answer with retrieved chunks visible

## Instructions
1. Open the Streamlit app at: https://computing-triumph-acres-majority.trycloudflare.com
2. Ensure PDF is uploaded and index is built
3. For each question:
   - Enter the question
   - Take screenshot: `04_q{N}_question_entered.png`
   - Click "Retrieve & Answer"
   - Wait for answer to appear
   - Take screenshot: `05_q{N}_answer_displayed.png`
4. Save all screenshots in the `screenshots/` directory
