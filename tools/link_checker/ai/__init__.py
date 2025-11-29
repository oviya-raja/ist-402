"""
AI domain - Link quality analysis and AI prompts
"""

from .quality_analyzer import analyze_with_ai, is_ai_available
from .prompts import get_ai_prompt, AI_SYSTEM_PROMPT

__all__ = [
    'analyze_with_ai',
    'is_ai_available',
    'get_ai_prompt',
    'AI_SYSTEM_PROMPT',
]


