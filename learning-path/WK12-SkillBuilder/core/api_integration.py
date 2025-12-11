"""
External API Integration Module
Integrates with OpenAI web search and NewsAPI for news and events.
"""

import os
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import re

from core.logger import get_logger

logger = get_logger()

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not installed. Install with: pip install openai")


class APIError(Exception):
    """Custom exception for API errors."""
    pass


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
            self.logger.warning("NewsAPI key not configured. API calls will fail.")
    
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
        if not self.api_key:
            error_msg = "NewsAPI key not configured. Please set NEWS_API_KEY environment variable."
            self.logger.error(error_msg)
            raise APIError(error_msg)
        
        try:
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
            raise APIError(f"NewsAPI request failed: {str(e)}")
        except Exception as e:
            self.logger.log_error(e, "Unexpected error getting news")
            raise APIError(f"Unexpected error in NewsAPI: {str(e)}")
    
    def is_available(self) -> bool:
        """
        Check if NewsAPI is available (has API key).
        
        Returns:
            True if API key is configured, False otherwise
        """
        return self.api_key is not None


class OpenAIWebSearchAPI:
    """
    Integration with OpenAI Responses API using web_search_preview tool.
    Provides real-time web search for AI conferences and events.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI Web Search API client.
        
        Args:
            api_key: OpenAI API key (or from environment)
        """
        self.logger = logger
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not OPENAI_AVAILABLE:
            self.logger.error("OpenAI package not available. Install with: pip install openai")
            self.client = None
        elif not self.api_key:
            self.logger.error("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.logger.info("OpenAI Web Search API initialized successfully")
            except Exception as e:
                self.logger.log_error(e, "Error initializing OpenAI client")
                self.client = None
    
    def get_ai_conferences(self, 
                          category: str = "technology",
                          keywords: Optional[List[str]] = None,
                          limit: int = 10) -> Dict[str, Any]:
        """
        Get AI-related conferences/events using OpenAI web search.
        
        Args:
            category: News category (not used, kept for compatibility)
            keywords: Additional keywords to filter (default: AI/ML keywords)
            limit: Maximum number of conferences to return
            
        Returns:
            Dictionary with conference information
        """
        if not self.client:
            error_msg = "OpenAI API not available. Please configure OPENAI_API_KEY and install openai package."
            self.logger.error(error_msg)
            raise APIError(error_msg)
        
        try:
            # Build search query for AI conferences
            if keywords is None:
                search_query = "Find upcoming artificial intelligence conferences, AI summits, and machine learning events happening in 2025 and 2026. Include event names, dates, locations, and URLs."
            else:
                keyword_str = ", ".join(keywords[:5])
                search_query = f"Find upcoming artificial intelligence conferences and AI events related to: {keyword_str}. Include event names, dates, locations, and URLs for events in 2025 and 2026."
            
            self.logger.log_api_call("OpenAI Web Search", "requesting", f"AI conferences, limit={limit}")
            
            # Use OpenAI Responses API with web_search_preview tool
            response = self.client.responses.create(
                model="gpt-4o",
                tools=[{"type": "web_search_preview"}],
                input=search_query
            )
            
            self.logger.log_api_call("OpenAI Web Search", "success", "retrieved web search results")
            
            # Parse the response to extract conference information
            # Handle different response structures
            output_text = ""
            if hasattr(response, 'output_text') and response.output_text:
                output_text = response.output_text
            elif hasattr(response, 'output'):
                # output might be a list of objects with text
                if isinstance(response.output, list):
                    output_text = " ".join([item.get('text', '') if isinstance(item, dict) else str(item) for item in response.output])
                else:
                    output_text = str(response.output)
            elif hasattr(response, 'text'):
                output_text = response.text
            elif hasattr(response, 'content'):
                output_text = response.content
            elif isinstance(response, str):
                output_text = response
            else:
                # Fallback: convert to string and try to extract text
                output_text = str(response)
                # Try to find text in JSON-like structure
                import json
                try:
                    if isinstance(response, dict):
                        output_text = json.dumps(response, indent=2)
                except:
                    pass
            
            # Print full response for debugging
            print("\n" + "=" * 100)
            print("OPENAI WEB SEARCH RESPONSE")
            print("=" * 100)
            print(f"Response type: {type(response)}")
            print(f"Output text length: {len(output_text)}")
            print(f"\nOutput text:\n{output_text}")
            print("=" * 100 + "\n")
            
            # Parse conferences from the response
            conferences = self._parse_conferences_from_text(output_text, limit)
            
            return {
                'status': 'ok',
                'total_results': len(conferences),
                'conferences': conferences,
                'category': category,
                'source': 'OpenAI Web Search'
            }
            
        except Exception as e:
            self.logger.log_error(e, "Error getting AI conferences from OpenAI web search")
            raise APIError(f"OpenAI web search request failed: {str(e)}")
    
    def _parse_conferences_from_text(self, text: str, limit: int) -> List[Dict[str, Any]]:
        """
        Parse conference information from OpenAI web search response text.
        Uses regex and pattern matching to extract structured data.
        
        Args:
            text: Response text from OpenAI
            limit: Maximum number of conferences to return
            
        Returns:
            List of conference dictionaries
        """
        conferences = []
        
        # Print raw text for debugging
        print(f"\nParsing {len(text)} characters of response text...")
        
        # Try to find conference entries - look for patterns
        # Split by numbered lists, bullet points, or double newlines
        sections = re.split(r'\n\s*\n|\d+\.\s+|\-\s+|\•\s+', text)
        
        for section in sections:
            section = section.strip()
            if len(section) < 30:  # Skip very short sections
                continue
            
            conf = {
                'title': '',
                'description': '',
                'source': 'OpenAI Web Search',
                'published_at': '',
                'url': '',
                'extracted_date': '',
                'extracted_location': '',
                'type': 'conference'
            }
            
            # Extract URL
            url_pattern = r'https?://[^\s\)]+'
            urls = re.findall(url_pattern, section)
            if urls:
                conf['url'] = urls[0]
            
            # Extract dates (multiple formats)
            date_patterns = [
                (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),  # YYYY-MM-DD
                (r'([A-Z][a-z]+ \d{1,2}, \d{4})', None),  # Month Day, Year
                (r'(\d{1,2} [A-Z][a-z]+ \d{4})', None),  # Day Month Year
                (r'(December \d{1,2},? \d{4}|January \d{1,2},? \d{4}|February \d{1,2},? \d{4})', None),
            ]
            
            for pattern, _ in date_patterns:
                dates = re.findall(pattern, section)
                if dates:
                    conf['extracted_date'] = dates[0]
                    conf['published_at'] = dates[0]
                    break
            
            # Extract location
            location_patterns = [
                r'in ([A-Z][a-zA-Z\s]+(?:, [A-Z][a-zA-Z\s]+)?)',
                r'at ([A-Z][a-zA-Z\s]+(?:, [A-Z][a-zA-Z\s]+)?)',
                r'Location:?\s*([A-Z][a-zA-Z\s]+)',
                r'Venue:?\s*([A-Z][a-zA-Z\s]+)',
            ]
            
            for pattern in location_patterns:
                matches = re.findall(pattern, section)
                if matches:
                    location = matches[0].strip()
                    # Filter out common false positives
                    if location and len(location) < 50 and location not in ['The', 'A', 'An']:
                        conf['extracted_location'] = location
                        break
            
            # Extract title (first substantial line or line with "Conference", "Summit", "Event")
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if not line or len(line) < 10:
                    continue
                
                # Look for conference-related keywords
                if any(kw in line.lower() for kw in ['conference', 'summit', 'event', 'symposium', 'workshop', 'forum']):
                    # Clean up the line
                    title = re.sub(r'^[\d\-•\s]+', '', line).strip()
                    title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                    if title and len(title) > 10 and len(title) < 200:
                        conf['title'] = title
                        break
            
            # If no title found, use first substantial line
            if not conf['title']:
                for line in lines:
                    line = line.strip()
                    if len(line) > 20 and line[0].isupper():
                        title = re.sub(r'^[\d\-•\s]+', '', line).strip()
                        if title:
                            conf['title'] = title[:200]
                            break
            
            # Description is the rest of the section
            if conf['title']:
                # Remove title from description
                desc = section.replace(conf['title'], '').strip()
                # Remove URLs and dates from description for cleaner text
                desc = re.sub(url_pattern, '', desc)
                desc = re.sub(r'\d{4}-\d{2}-\d{2}', '', desc)
                desc = re.sub(r'\s+', ' ', desc).strip()
                conf['description'] = desc[:500] if desc else conf['title']
            else:
                conf['description'] = section[:500]
                conf['title'] = section.split('\n')[0][:200] if '\n' in section else section[:200]
            
            # Only add if we have a meaningful title
            if conf['title'] and len(conf['title']) > 5:
                conferences.append(conf)
            
            if len(conferences) >= limit:
                break
        
        # If parsing didn't work well, try simpler approach
        if len(conferences) < 2:
            # Split by paragraphs and create entries
            paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
            for para in paragraphs[:limit]:
                urls = re.findall(url_pattern, para)
                lines = para.split('\n')
                title = lines[0][:200] if lines else para[:200]
                
                conferences.append({
                    'title': title,
                    'description': para[:500],
                    'source': 'OpenAI Web Search',
                    'published_at': '',
                    'url': urls[0] if urls else '',
                    'extracted_date': '',
                    'extracted_location': '',
                    'type': 'conference'
                })
        
        # Ensure all conferences have required fields
        for conf in conferences:
            if not conf.get('title'):
                conf['title'] = 'AI Conference'
            if not conf.get('description'):
                conf['description'] = conf.get('title', '')
            if not conf.get('source'):
                conf['source'] = 'OpenAI Web Search'
        
        print(f"Parsed {len(conferences)} conferences from response")
        return conferences[:limit]
    
    def get_top_headlines(self, 
                         category: Optional[str] = None,
                         page_size: int = 5,
                         keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get top news headlines using OpenAI web search.
        
        Args:
            category: News category (business, technology, science, etc.)
            page_size: Number of articles to retrieve
            keywords: Optional keywords to filter articles
            
        Returns:
            Dictionary with news articles
        """
        if not self.client:
            error_msg = "OpenAI API not available. Please configure OPENAI_API_KEY and install openai package."
            self.logger.error(error_msg)
            raise APIError(error_msg)
        
        try:
            # Build search query
            if keywords:
                query = f"Latest news about: {', '.join(keywords[:3])}"
            elif category:
                query = f"Latest {category} news today"
            else:
                query = "Latest technology and AI news today"
            
            self.logger.log_api_call("OpenAI Web Search", "requesting", f"news, category={category}")
            
            # Use OpenAI Responses API with web_search_preview tool
            response = self.client.responses.create(
                model="gpt-4o",
                tools=[{"type": "web_search_preview"}],
                input=query
            )
            
            # Handle different response structures
            output_text = ""
            if hasattr(response, 'output_text') and response.output_text:
                output_text = response.output_text
            elif hasattr(response, 'output'):
                if isinstance(response.output, list):
                    output_text = " ".join([item.get('text', '') if isinstance(item, dict) else str(item) for item in response.output])
                else:
                    output_text = str(response.output)
            elif hasattr(response, 'text'):
                output_text = response.text
            else:
                output_text = str(response)
            
            # Parse articles from response
            articles = self._parse_articles_from_text(output_text, page_size)
            
            self.logger.log_api_call("OpenAI Web Search", "success", f"retrieved {len(articles)} articles")
            
            return {
                'status': 'ok',
                'total_results': len(articles),
                'articles': articles
            }
            
        except Exception as e:
            self.logger.log_error(e, "OpenAI web search API error")
            self.logger.log_api_call("OpenAI Web Search", "failed", str(e))
            raise APIError(f"OpenAI web search request failed: {str(e)}")
    
    def _parse_articles_from_text(self, text: str, limit: int) -> List[Dict[str, Any]]:
        """Parse news articles from OpenAI web search response."""
        articles = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 20:
                continue
            
            # Look for URLs
            url_pattern = r'https?://[^\s\)]+'
            urls = re.findall(url_pattern, line)
            
            # Extract title (first substantial line)
            if line[0].isupper() or line[0].isdigit():
                title = re.sub(r'^[\d\-•\s]+', '', line).strip()
                if title and len(title) > 10:
                    articles.append({
                        'title': title[:200],
                        'description': line[:300],
                        'source': 'Web Search',
                        'published_at': datetime.now().isoformat(),
                        'url': urls[0] if urls else ''
                    })
            
            if len(articles) >= limit:
                break
        
        # If parsing failed, create basic structure
        if not articles:
            chunks = text.split('\n\n')
            for chunk in chunks[:limit]:
                if len(chunk.strip()) > 20:
                    urls = re.findall(r'https?://[^\s\)]+', chunk)
                    articles.append({
                        'title': chunk.split('\n')[0][:200] if '\n' in chunk else chunk[:200],
                        'description': chunk[:300],
                        'source': 'Web Search',
                        'published_at': datetime.now().isoformat(),
                        'url': urls[0] if urls else ''
                    })
        
        return articles[:limit]
    
    def is_available(self) -> bool:
        """
        Check if OpenAI Web Search API is available.
        
        Returns:
            True if API key is configured and package is available, False otherwise
        """
        return self.client is not None


class APIIntegrationManager:
    """
    Manages all external API integrations.
    Provides unified interface for accessing external data sources.
    
    Note: News and conference fetching uses OpenAI Web Search API.
    NewsAPI is available but not currently used for news retrieval.
    """
    
    def __init__(self):
        """Initialize API integration manager."""
        self.logger = logger
        self.news_api = NewsAPI()  # Available but not used for news (OpenAI Web Search is used instead)
        self.openai_web_search = OpenAIWebSearchAPI()  # Used for all news and conference data
    
    def get_contextual_data(self, 
                           news_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Get contextual data from APIs.
        
        Uses OpenAI Web Search API for news articles (NewsAPI is not used).
        
        Args:
            news_topic: Topic for news search (category or keywords)
            
        Returns:
            Dictionary with combined contextual data
            
        Raises:
            APIError: If OpenAI API is not configured
        """
        try:
            context = {
                'timestamp': datetime.now().isoformat(),
                'news': None
            }
            
            # Get news articles using OpenAI Web Search (NewsAPI is not used)
            if news_topic:
                # Use as keywords
                news_data = self.openai_web_search.get_top_headlines(
                    keywords=[news_topic],
                    page_size=5
                )
            else:
                news_data = self.openai_web_search.get_top_headlines(page_size=5)
            
            context['news'] = news_data
            self.logger.info(f"Retrieved news data: {news_data.get('total_results', 0)} articles")
            
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
        
        if context.get('news'):
            news = context['news']
            formatted += f"Recent News ({news.get('total_results', 0)} articles):\n"
            for article in news.get('articles', [])[:3]:
                formatted += f"- {article.get('title', 'N/A')}\n"
                formatted += f"  {article.get('description', 'N/A')}\n"
            formatted += "\n"
        
        return formatted
    
    def get_ai_conferences(self, 
                          category: str = "technology",
                          keywords: Optional[List[str]] = None,
                          limit: int = 10) -> Dict[str, Any]:
        """
        Get AI-related conferences using OpenAI Web Search.
        
        Args:
            category: News category to search (not used, kept for compatibility)
            keywords: Additional keywords for filtering
            limit: Maximum number of conferences to return
            
        Returns:
            Dictionary with conference information
        """
        return self.openai_web_search.get_ai_conferences(
            category=category,
            keywords=keywords,
            limit=limit
        )
    
    def is_newsapi_available(self) -> bool:
        """Check if NewsAPI is available."""
        return self.news_api.is_available()
    
    def is_openai_web_search_available(self) -> bool:
        """Check if OpenAI Web Search is available."""
        return self.openai_web_search.is_available()
