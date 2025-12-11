"""
External API Integration Module
Integrates with EventRegistry API and NewsAPI for news and events.
"""

import os
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from core.logger import get_logger

logger = get_logger()

# Try to import EventRegistry
try:
    from eventregistry import (
        EventRegistry, QueryArticlesIter, QueryEvents, RequestEventsInfo, 
        QueryItems, ReturnInfo, EventInfoFlags
    )
    EVENTREGISTRY_AVAILABLE = True
except ImportError:
    EVENTREGISTRY_AVAILABLE = False
    logger.warning("EventRegistry package not installed. Install with: pip install eventregistry")


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


class EventRegistryAPI:
    """
    Integration with EventRegistry API for news articles and events.
    Provides real-time news data and event information for content generation.
    Includes AI conferences detection functionality.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize EventRegistry API client.
        
        Args:
            api_key: EventRegistry API key (or from environment)
        """
        self.logger = logger
        # Try to get API key from parameter, then environment variables
        self.api_key = api_key or os.getenv('EVENTREGISTRY_API_KEY') or os.getenv('NEWS_API_KEY')
        
        # Debug logging
        if self.api_key:
            self.logger.info(f"EventRegistry API key found (length: {len(self.api_key)})")
        else:
            self.logger.warning("EventRegistry API key not found in environment variables")
            # Log all env vars that start with EVENT or NEWS for debugging
            env_vars = {k: v for k, v in os.environ.items() if 'EVENT' in k.upper() or 'NEWS' in k.upper()}
            if env_vars:
                self.logger.info(f"Found related env vars: {list(env_vars.keys())}")
        
        if not EVENTREGISTRY_AVAILABLE:
            self.logger.error("EventRegistry package not available. Install with: pip install eventregistry")
            self.er = None
        elif not self.api_key:
            self.logger.error("EventRegistry API key not configured. Please set EVENTREGISTRY_API_KEY environment variable.")
            self.er = None
        else:
            try:
                self.er = EventRegistry(apiKey=self.api_key, allowUseOfArchive=False)
                self.logger.info("EventRegistry initialized successfully")
            except Exception as e:
                self.logger.log_error(e, "Error initializing EventRegistry")
                self.er = None
    
    def get_top_headlines(self, 
                         category: Optional[str] = None,
                         page_size: int = 5,
                         keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get top news headlines using EventRegistry.
        
        Args:
            category: News category (business, technology, science, etc.)
            page_size: Number of articles to retrieve
            keywords: Optional keywords to filter articles
            
        Returns:
            Dictionary with news articles
        """
        if not self.er:
            error_msg = "EventRegistry API not available. Please configure EVENTREGISTRY_API_KEY and install eventregistry package."
            self.logger.error(error_msg)
            raise APIError(error_msg)
        
        try:
            # Map category to EventRegistry category URI
            category_uri = None
            if category:
                try:
                    category_uri = self.er.getCategoryUri(f"news/{category.capitalize()}")
                except:
                    # If category mapping fails, use keywords instead
                    pass
            
            # Build query
            q = QueryArticlesIter(
                dataType=["news", "blog"],
                sortBy="date",
                maxItems=page_size
            )
            
            if category_uri:
                q.setCategoryUri(category_uri)
            
            if keywords:
                q.setKeywords(QueryItems.OR(keywords))
            
            self.logger.log_api_call("EventRegistry", "requesting", f"category={category}, page_size={page_size}")
            
            articles = []
            for art in q.execQuery(self.er):
                articles.append({
                    'title': art.get('title', ''),
                    'description': art.get('body', '')[:200] if art.get('body') else art.get('title', ''),
                    'source': art.get('source', {}).get('title', 'Unknown') if isinstance(art.get('source'), dict) else str(art.get('source', 'Unknown')),
                    'published_at': art.get('date', ''),
                    'url': art.get('url', '')
                })
                if len(articles) >= page_size:
                    break
            
            self.logger.log_api_call("EventRegistry", "success", f"retrieved {len(articles)} articles")
            
            return {
                'status': 'ok',
                'total_results': len(articles),
                'articles': articles
            }
            
        except Exception as e:
            self.logger.log_error(e, "EventRegistry API error")
            self.logger.log_api_call("EventRegistry", "failed", str(e))
            raise APIError(f"EventRegistry request failed: {str(e)}")
    
    def get_ai_conferences(self, 
                          category: str = "technology",
                          keywords: Optional[List[str]] = None,
                          limit: int = 10) -> Dict[str, Any]:
        """
        Get AI-related conferences/events from EventRegistry.
        Uses EventRegistry's event search which is better for finding conferences.
        
        Args:
            category: News category (technology, science, etc.)
            keywords: Additional keywords to filter (default: AI/ML keywords)
            limit: Maximum number of conferences to return
            
        Returns:
            Dictionary with conference information
        """
        if not self.er:
            error_msg = "EventRegistry API not available. Please configure EVENTREGISTRY_API_KEY and install eventregistry package."
            self.logger.error(error_msg)
            raise APIError(error_msg)
        
        try:
            # Default keywords for AI/ML conferences - include specific conference names
            if keywords is None:
                keywords = [
                    "AI Summit", "The AI Summit", "AI Summit New York", "artificial intelligence summit",
                    "artificial intelligence", "machine learning", "AI conference", "ML conference",
                    "deep learning", "neural networks", "data science", "AI event", "machine learning event"
                ]
            
            # Try to get concept URI for better results, but don't fail if it doesn't work
            ai_concept_uri = None
            try:
                # Try to get concept URI for "Artificial Intelligence"
                ai_concept_uri = self.er.getConceptUri("Artificial Intelligence")
                self.logger.info("Successfully obtained concept URI for 'Artificial Intelligence'")
            except Exception as e:
                self.logger.warning(f"Could not get concept URI for 'Artificial Intelligence': {str(e)}")
                # If that fails, try "Machine Learning"
                try:
                    ai_concept_uri = self.er.getConceptUri("Machine Learning")
                    self.logger.info("Successfully obtained concept URI for 'Machine Learning'")
                except Exception as e2:
                    self.logger.warning(f"Could not get concept URI for 'Machine Learning': {str(e2)}")
            
            # Build event query - use QueryItems.OR() as recommended by EventRegistry
            query_params = {}
            
            # Always add keywords - use QueryItems.OR() as recommended by the API
            if keywords:
                # Use QueryItems.OR() to explicitly specify OR operator between keywords
                # This is what EventRegistry recommends to avoid warnings
                query_params['keywords'] = QueryItems.OR(keywords[:10])  # Use up to 10 keywords
                self.logger.info(f"Using {len(keywords[:10])} keywords with OR operator: {', '.join(keywords[:5])}...")
            
            # Add concept URI if available (enhances search but not required)
            if ai_concept_uri:
                query_params['conceptUri'] = ai_concept_uri
                self.logger.info("Added concept URI to query")
            
            # NO DATE FILTERING - Get all events to see what's available
            self.logger.info("NO DATE FILTERING - Getting all available events")
            
            # Create QueryEvents with parameters (matching working example from docs)
            query = None
            result = None
            
            # Try different query approaches if one fails
            query_attempts = [
                ("Full query with keywords and conceptUri", query_params),
                ("Query with keywords only", {k: v for k, v in query_params.items() if k != 'conceptUri'}),
                ("Query with conceptUri only", {k: v for k, v in query_params.items() if k == 'conceptUri'}),
                ("Simple query with first keyword only", {'keywords': [keywords[0]] if keywords else []}),
            ]
            
            for attempt_name, params in query_attempts:
                if not params or (not params.get('keywords') and not params.get('conceptUri')):
                    continue
                    
                try:
                    self.logger.info(f"Attempting: {attempt_name}")
                    self.logger.info(f"Query params: {list(params.keys())}")
                    
                    query = QueryEvents(**params)
                    self.logger.info(f"QueryEvents created successfully")
                    
                    # Request event information
                    query.setRequestedResult(
                        RequestEventsInfo(
                            sortBy="date",
                            count=limit
                        )
                    )
                    
                    self.logger.log_api_call("EventRegistry", "requesting", f"AI conferences, limit={limit}")
                    
                    # Execute query
                    result = self.er.execQuery(query)
                    
                    # Check if we got results (not an error)
                    if isinstance(result, dict) and 'error' not in result:
                        self.logger.info(f"✓ Success with {attempt_name}")
                        break
                    elif isinstance(result, dict) and 'error' in result:
                        self.logger.warning(f"✗ {attempt_name} returned error: {result.get('error')}")
                        continue
                    else:
                        self.logger.info(f"✓ Success with {attempt_name}")
                        break
                        
                except Exception as e:
                    self.logger.warning(f"✗ {attempt_name} failed: {str(e)}")
                    continue
            
            if result is None:
                raise APIError("All query attempts failed")
            
            # Log the raw result structure for debugging
            print("\n" + "=" * 100)
            print("RAW EVENTREGISTRY API RESPONSE")
            print("=" * 100)
            print(f"Result type: {type(result)}")
            if isinstance(result, dict):
                print(f"Result keys: {list(result.keys())}")
                # Print the full result to see what's in it
                import json
                print(f"\nFull result (formatted):")
                print(json.dumps(result, indent=2, default=str))
                
                # Check for error
                if 'error' in result:
                    print(f"\n❌ ERROR FROM API: {result.get('error')}")
                    self.logger.error(f"EventRegistry API error: {result.get('error')}")
            else:
                print(f"Result: {result}")
            print("=" * 100 + "\n")
            
            self.logger.info(f"EventRegistry query result type: {type(result)}")
            if isinstance(result, dict):
                self.logger.info(f"EventRegistry result keys: {list(result.keys())}")
                if 'error' in result:
                    self.logger.error(f"EventRegistry API returned error: {result.get('error')}")
            
            conferences = []
            # EventRegistry returns events in structure: {"events": {"results": [...]}}
            events_list = []
            if result and isinstance(result, dict):
                events_data = result.get('events', {})
                if isinstance(events_data, dict):
                    events_list = events_data.get('results', [])
                    self.logger.info(f"Extracted {len(events_list)} events from events.results")
                elif isinstance(events_data, list):
                    events_list = events_data
                    self.logger.info(f"Extracted {len(events_list)} events from events list")
                else:
                    self.logger.warning(f"Unexpected events data structure: {type(events_data)}")
            elif result:
                self.logger.warning(f"Unexpected result structure: {type(result)}, keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
            
            self.logger.info(f"Total events found: {len(events_list)}")
            
            # PRINT ALL RESULTS TO CONSOLE - NO FILTERING
            print("\n" + "=" * 100)
            print("ALL EVENTREGISTRY RESULTS (NO FILTERING)")
            print("=" * 100)
            print(f"Total events returned from API: {len(events_list)}")
            print("=" * 100 + "\n")
            
            # Print all events to console
            for idx, event in enumerate(events_list, 1):
                if not isinstance(event, dict):
                    continue
                
                # Extract event date
                event_date_str = event.get('eventDate', '') or event.get('dateStart', '') or event.get('date', '')
                
                # Extract title
                title_dict = event.get('title', {})
                if isinstance(title_dict, dict):
                    event_title = title_dict.get('eng', '') or title_dict.get('en', '') or list(title_dict.values())[0] if title_dict else 'Untitled'
                else:
                    event_title = str(title_dict) if title_dict else 'Untitled'
                
                # Extract summary
                summary_dict = event.get('summary', {})
                if isinstance(summary_dict, dict):
                    event_summary = summary_dict.get('eng', '') or summary_dict.get('en', '') or list(summary_dict.values())[0] if summary_dict else ''
                else:
                    event_summary = str(summary_dict) if summary_dict else ''
                
                # Extract URI
                uri = event.get('uri', '') or event.get('url', '')
                
                # Print to console
                print(f"\n{'─' * 100}")
                print(f"EVENT #{idx}")
                print(f"{'─' * 100}")
                print(f"Title: {event_title}")
                print(f"Date: {event_date_str}")
                print(f"URI: {uri}")
                print(f"Summary: {event_summary[:200]}..." if len(event_summary) > 200 else f"Summary: {event_summary}")
                print(f"All Keys: {list(event.keys())}")
                
                # Also log to logger
                self.logger.info(f"\nEvent #{idx}: {event_title}")
                self.logger.info(f"  Date: {event_date_str}")
                self.logger.info(f"  URI: {uri}")
                self.logger.info(f"  Keys: {list(event.keys())}")
            
            print("\n" + "=" * 100)
            print("END OF ALL RESULTS")
            print("=" * 100 + "\n")
            
            # NO FILTERING - Use all events as-is
            # Just limit to requested count
            events_list = events_list[:limit]
            
            for event in events_list:
                if not isinstance(event, dict):
                    continue
                
                # EventRegistry event structure: title and summary are dicts with language keys
                # e.g., {'title': {'eng': 'Event Title'}, 'summary': {'eng': 'Summary text'}}
                title_dict = event.get('title', {})
                if isinstance(title_dict, dict):
                    title = title_dict.get('eng', '') or title_dict.get('en', '') or list(title_dict.values())[0] if title_dict else 'Untitled Event'
                else:
                    title = str(title_dict) if title_dict else 'Untitled Event'
                
                summary_dict = event.get('summary', {})
                if isinstance(summary_dict, dict):
                    summary = summary_dict.get('eng', '') or summary_dict.get('en', '') or list(summary_dict.values())[0] if summary_dict else ''
                else:
                    summary = str(summary_dict) if summary_dict else ''
                
                # Event date field
                date_start = event.get('eventDate', '') or event.get('dateStart', '') or event.get('date', '')
                
                # Event URI
                uri = event.get('uri', '') or event.get('url', '')
                
                # Use event dict directly for helper methods
                event_info = event
                
                conferences.append({
                    'title': title,
                    'description': summary[:300] if summary else '',
                    'source': 'EventRegistry',
                    'published_at': date_start,
                    'url': uri,
                    'extracted_date': date_start,
                    'extracted_location': self._extract_location_from_event(event_info),
                    'type': self._get_event_type(event_info)
                })
            
            self.logger.log_api_call("EventRegistry", "success", f"retrieved {len(conferences)} conferences")
            
            return {
                'status': 'ok',
                'total_results': len(conferences),
                'conferences': conferences[:limit],
                'category': category
            }
            
        except Exception as e:
            self.logger.log_error(e, "Error getting AI conferences from EventRegistry")
            raise APIError(f"EventRegistry conferences request failed: {str(e)}")
    
    def _extract_location_from_event(self, event_info: Dict) -> Optional[str]:
        """
        Extract location from event information.
        
        Args:
            event_info: Event information dictionary
            
        Returns:
            Location string or None
        """
        # EventRegistry may have location information
        location = event_info.get('location', {})
        if location:
            if isinstance(location, dict):
                return location.get('label', '') or location.get('name', '')
            return str(location)
        return None
    
    def _get_event_type(self, event_info: Dict) -> str:
        """
        Determine event type from event information.
        
        Args:
            event_info: Event information dictionary
            
        Returns:
            Event type string
        """
        # Handle title - can be dict or string
        title = event_info.get('title', '')
        if isinstance(title, dict):
            title = title.get('eng', '') or title.get('en', '') or list(title.values())[0] if title else ''
        title = str(title).lower() if title else ''
        
        # Handle summary - can be dict or string
        summary = event_info.get('summary', '')
        if isinstance(summary, dict):
            summary = summary.get('eng', '') or summary.get('en', '') or list(summary.values())[0] if summary else ''
        summary = str(summary).lower() if summary else ''
        
        text = f"{title} {summary}"
        
        if 'summit' in text:
            return 'summit'
        elif 'workshop' in text:
            return 'workshop'
        elif 'symposium' in text:
            return 'symposium'
        elif 'expo' in text or 'exhibition' in text:
            return 'expo'
        elif 'forum' in text:
            return 'forum'
        elif 'conference' in text:
            return 'conference'
        else:
            return 'event'
    
    def is_available(self) -> bool:
        """
        Check if EventRegistry API is available (has API key and package installed).
        
        Returns:
            True if API key is configured and package is available, False otherwise
        """
        return self.er is not None


class APIIntegrationManager:
    """
    Manages all external API integrations.
    Provides unified interface for accessing external data sources.
    
    Note: News fetching uses EventRegistry API only. NewsAPI is available
    but not currently used for news retrieval.
    """
    
    def __init__(self):
        """Initialize API integration manager."""
        self.logger = logger
        self.news_api = NewsAPI()  # Available but not used for news (EventRegistry is used instead)
        self.event_registry = EventRegistryAPI()  # Used for all news and conference data
    
    def get_contextual_data(self, 
                           news_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Get contextual data from APIs.
        
        Uses EventRegistry API for news articles (NewsAPI is not used).
        
        Args:
            news_topic: Topic for news search (category or keywords)
            
        Returns:
            Dictionary with combined contextual data
            
        Raises:
            APIError: If EventRegistry API is not configured
        """
        try:
            context = {
                'timestamp': datetime.now().isoformat(),
                'news': None
            }
            
            # Get news articles using EventRegistry (NewsAPI is not used)
            if news_topic:
                # Try as category first, then as keywords
                news_data = self.event_registry.get_top_headlines(
                    category=news_topic,
                    page_size=5
                )
            else:
                news_data = self.event_registry.get_top_headlines(page_size=5)
            
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
        Get AI-related conferences using EventRegistry.
        
        Args:
            category: News category to search
            keywords: Additional keywords for filtering
            limit: Maximum number of conferences to return
            
        Returns:
            Dictionary with conference information
        """
        return self.event_registry.get_ai_conferences(
            category=category,
            keywords=keywords,
            limit=limit
        )
    
    def is_newsapi_available(self) -> bool:
        """Check if NewsAPI is available."""
        return self.news_api.is_available()
    
    def is_eventregistry_available(self) -> bool:
        """Check if EventRegistry is available."""
        return self.event_registry.is_available()