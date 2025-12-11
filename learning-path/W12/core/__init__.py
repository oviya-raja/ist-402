"""
Core modules for Smart Content Generator & Research Assistant.
"""

from core.logger import get_logger
from core.data_processor import DataProcessor
from core.prompt_engineer import PromptEngineer, PromptType
from core.api_integration import APIIntegrationManager, WeatherAPI, NewsAPI
from core.content_generator import ContentGenerator

__all__ = [
    'get_logger',
    'DataProcessor',
    'PromptEngineer',
    'PromptType',
    'APIIntegrationManager',
    'WeatherAPI',
    'NewsAPI',
    'ContentGenerator'
]
