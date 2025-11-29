#!/usr/bin/env python3
"""
Link quality analyzer - Domain-specific AI analysis for link checking
Following Single Responsibility Principle
"""

import os
from typing import Optional

from ..core.models import CheckSummary, TestData
from .prompts import get_ai_prompt, AI_SYSTEM_PROMPT

# Check if AI is available
try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


def is_ai_available() -> bool:
    """Check if AI (OpenAI) is available"""
    return AI_AVAILABLE


def analyze_with_ai(summary: CheckSummary, test_data: TestData) -> str:
    """
    Analyze results using AI (OpenAI GPT-4o-mini)
    
    Args:
        summary: Check summary
        test_data: Test metadata
        
    Returns:
        AI analysis text
    """
    if not AI_AVAILABLE:
        return "AI analysis unavailable (OpenAI not installed). Install with: pip install openai"
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI analysis unavailable (OPENAI_API_KEY not set). Set environment variable to enable AI."
    
    try:
        client = openai.OpenAI(api_key=api_key)
        prompt = get_ai_prompt(summary, test_data)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": AI_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        return content if content else "AI analysis returned no content"
    except Exception as e:
        return f"AI analysis error: {e}"

