"""
External API Integration Module
Integrates with external APIs (weather, news, etc.) to enrich content generation.
"""

import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import json

from core.logger import get_logger

logger = get_logger()


class APIError(Exception):
    """Custom exception for API errors."""
    pass


class WeatherAPI:
    """
    Integration with OpenWeatherMap API for weather data.
    Provides real-time weather information to enhance content generation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weather API client.
        
        Args:
            api_key: OpenWeatherMap API key (or from environment)
        """
        self.logger = logger
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            self.logger.info("OpenWeatherMap API key not configured. Using mock data for weather features.")
    
    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get current weather for a city.
        
        Args:
            city: City name
            units: Temperature units (metric, imperial, kelvin)
            
        Returns:
            Dictionary with weather data
            
        Raises:
            APIError: If API call fails
        """
        try:
            if not self.api_key:
                # Return mock data if API key not available
                self.logger.info(f"Using mock weather data for {city}")
                return self._get_mock_weather(city)
            
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units
            }
            
            self.logger.log_api_call("OpenWeatherMap", "requesting", f"city={city}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.logger.log_api_call("OpenWeatherMap", "success", f"city={city}")
            
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, f"Weather API error for city: {city}")
            self.logger.log_api_call("OpenWeatherMap", "failed", str(e))
            # Return mock data on error
            return self._get_mock_weather(city)
        except Exception as e:
            self.logger.log_error(e, f"Unexpected error getting weather for {city}")
            return self._get_mock_weather(city)
    
    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """Return mock weather data for testing/demo purposes."""
        return {
            'city': city,
            'country': 'US',
            'temperature': 22.5,
            'feels_like': 21.0,
            'description': 'clear sky',
            'humidity': 65,
            'wind_speed': 3.5,
            'timestamp': datetime.now().isoformat(),
            'note': 'Mock data - API key not configured'
        }


class NewsAPI:
    """
    Integration with NewsAPI for current news and articles.
    Provides real-time news data to enhance content generation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize News API client.
        
        Args:
            api_key: NewsAPI key (or from environment)
        """
        self.logger = logger
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        
        if not self.api_key:
            self.logger.info("NewsAPI key not configured. Using mock data for news features.")
    
    def get_top_headlines(self, 
                         country: str = "us",
                         category: Optional[str] = None,
                         page_size: int = 5) -> Dict[str, Any]:
        """
        Get top news headlines.
        
        Args:
            country: Country code (us, gb, etc.)
            category: News category (business, technology, etc.)
            page_size: Number of articles to retrieve
            
        Returns:
            Dictionary with news articles
            
        Raises:
            APIError: If API call fails
        """
        try:
            if not self.api_key:
                # Return mock data if API key not available
                self.logger.info("Using mock news data")
                return self._get_mock_news()
            
            url = f"{self.base_url}/top-headlines"
            params = {
                'country': country,
                'pageSize': page_size,
                'apiKey': self.api_key
            }
            
            if category:
                params['category'] = category
            
            self.logger.log_api_call("NewsAPI", "requesting", f"country={country}, category={category}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.logger.log_api_call("NewsAPI", "success", f"retrieved {len(data.get('articles', []))} articles")
            
            return {
                'status': data.get('status'),
                'total_results': data.get('totalResults', 0),
                'articles': [
                    {
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'published_at': article.get('publishedAt', ''),
                        'url': article.get('url', '')
                    }
                    for article in data.get('articles', [])[:page_size]
                ]
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, "News API error")
            self.logger.log_api_call("NewsAPI", "failed", str(e))
            # Return mock data on error
            return self._get_mock_news()
        except Exception as e:
            self.logger.log_error(e, "Unexpected error getting news")
            return self._get_mock_news()
    
    def _get_mock_news(self) -> Dict[str, Any]:
        """Return mock news data for testing/demo purposes."""
        return {
            'status': 'ok',
            'total_results': 3,
            'articles': [
                {
                    'title': 'AI Technology Advances in 2024',
                    'description': 'Recent developments in artificial intelligence show promising results.',
                    'source': 'Tech News',
                    'published_at': datetime.now().isoformat(),
                    'url': 'https://example.com/news1'
                },
                {
                    'title': 'Climate Change Summit Results',
                    'description': 'Global leaders reach new agreements on climate action.',
                    'source': 'World News',
                    'published_at': datetime.now().isoformat(),
                    'url': 'https://example.com/news2'
                },
                {
                    'title': 'Economic Growth Trends',
                    'description': 'Analysis of current economic indicators and future projections.',
                    'source': 'Business Daily',
                    'published_at': datetime.now().isoformat(),
                    'url': 'https://example.com/news3'
                }
            ],
            'note': 'Mock data - API key not configured'
        }


class APIIntegrationManager:
    """
    Manages all external API integrations.
    Provides unified interface for accessing external data sources.
    """
    
    def __init__(self):
        """Initialize API integration manager."""
        self.logger = logger
        self.weather_api = WeatherAPI()
        self.news_api = NewsAPI()
    
    def get_contextual_data(self, 
                           city: Optional[str] = None,
                           news_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Get contextual data from multiple APIs.
        
        Args:
            city: City for weather data
            news_topic: Topic for news search
            
        Returns:
            Dictionary with combined contextual data
        """
        try:
            context = {
                'timestamp': datetime.now().isoformat(),
                'weather': None,
                'news': None
            }
            
            if city:
                context['weather'] = self.weather_api.get_weather(city)
                self.logger.info(f"Retrieved weather data for {city}")
            
            if news_topic:
                # Get news related to topic
                news_data = self.news_api.get_top_headlines(category=news_topic)
                context['news'] = news_data
                self.logger.info(f"Retrieved news data for topic: {news_topic}")
            else:
                # Get general top headlines
                news_data = self.news_api.get_top_headlines()
                context['news'] = news_data
                self.logger.info("Retrieved general news data")
            
            return context
            
        except Exception as e:
            self.logger.log_error(e, "Error getting contextual data")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format contextual data for inclusion in prompts.
        
        Args:
            context: Contextual data dictionary
            
        Returns:
            Formatted string for prompt inclusion
        """
        formatted = "EXTERNAL CONTEXT:\n\n"
        
        if context.get('weather'):
            weather = context['weather']
            formatted += f"Weather Information:\n"
            formatted += f"- Location: {weather.get('city', 'N/A')}, {weather.get('country', 'N/A')}\n"
            formatted += f"- Temperature: {weather.get('temperature', 'N/A')}°C\n"
            formatted += f"- Conditions: {weather.get('description', 'N/A')}\n"
            formatted += f"- Humidity: {weather.get('humidity', 'N/A')}%\n\n"
        
        if context.get('news'):
            news = context['news']
            formatted += f"Recent News ({news.get('total_results', 0)} articles):\n"
            for article in news.get('articles', [])[:3]:
                formatted += f"- {article.get('title', 'N/A')}\n"
                formatted += f"  {article.get('description', 'N/A')}\n"
            formatted += "\n"
        
        return formatted
