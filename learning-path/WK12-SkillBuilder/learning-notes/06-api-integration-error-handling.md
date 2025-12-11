# API Integration & Error Handling Patterns

## Course Context
**Concepts:** External API Integration, Error Handling, Production Patterns  
**Related Weeks:** W06 (Safety and Guardrails)

---

## 1. API Integration Architecture

### From the Project: Multi-API Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    API INTEGRATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                APIIntegrationManager                       │ │
│  │  (Unified interface for all external APIs)                 │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                           │                                      │
│           ┌───────────────┼───────────────┐                     │
│           │               │               │                     │
│           ▼               ▼               ▼                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │   NewsAPI    │ │  OpenAI      │ │   OpenAI     │            │
│  │  (Optional)  │ │  Embeddings  │ │  Web Search  │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Custom Exception Class

### From the Project: `api_integration.py`

```python
class APIError(Exception):
    """Custom exception for API errors."""
    pass
```

### Why Custom Exceptions?

| Benefit | Description |
|---------|-------------|
| **Specificity** | Distinguish API errors from other exceptions |
| **Handling** | Catch API errors separately |
| **Context** | Include API-specific error information |
| **Clarity** | Clear error hierarchy |

### Usage Pattern

```python
try:
    result = api.fetch_data()
except APIError as e:
    # Handle API-specific errors
    logger.error(f"API failed: {e}")
    return fallback_response()
except Exception as e:
    # Handle unexpected errors
    logger.critical(f"Unexpected error: {e}")
    raise
```

---

## 3. API Client Initialization

### From the Project: `api_integration.py`

```python
class OpenAIWebSearchAPI:
    """Integration with OpenAI Responses API using web_search_preview tool."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logger
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        # Check package availability
        if not OPENAI_AVAILABLE:
            self.logger.error("OpenAI package not available. Install with: pip install openai")
            self.client = None
        elif not self.api_key:
            self.logger.error("OpenAI API key not configured...")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.logger.info("OpenAI Web Search API initialized successfully")
            except Exception as e:
                self.logger.log_error(e, "Error initializing OpenAI client")
                self.client = None
```

### Initialization Checklist

```
┌─────────────────────────────────────────┐
│        API Initialization Flow          │
├─────────────────────────────────────────┤
│                                         │
│  1. Check package availability          │
│     └─► OPENAI_AVAILABLE check         │
│                                         │
│  2. Check API key                       │
│     └─► Environment variable           │
│     └─► Constructor parameter          │
│                                         │
│  3. Initialize client                   │
│     └─► Try/catch for errors           │
│     └─► Log success/failure            │
│                                         │
│  4. Set client to None on failure       │
│     └─► Allows graceful checks later   │
│                                         │
└─────────────────────────────────────────┘
```

---

## 4. Availability Checking Pattern

### From the Project: `api_integration.py`

```python
def is_available(self) -> bool:
    """
    Check if OpenAI Web Search API is available.
    
    Returns:
        True if API key is configured and package is available
    """
    return self.client is not None
```

### Usage in UI

```python
# From app.py: Show API status to user
if st.session_state.api_manager.is_openai_web_search_available():
    st.success("✅ OpenAI Web Search: Connected")
else:
    st.error("❌ OpenAI Web Search: Not configured")
    st.caption("⚠️ Required for news and AI conferences functionality")
```

### Why This Pattern?

1. **User Feedback**: Clear status in UI
2. **Graceful Degradation**: Don't break if API unavailable
3. **Feature Toggling**: Enable/disable features based on availability
4. **Debugging**: Easy to identify configuration issues

---

## 5. API Call with Error Handling

### From the Project: `api_integration.py`

```python
def get_top_headlines(self, 
                     country: str = "us",
                     category: Optional[str] = None,
                     page_size: int = 5) -> Dict[str, Any]:
    """Get top news headlines."""
    
    # Pre-condition check
    if not self.api_key:
        error_msg = "NewsAPI key not configured..."
        self.logger.error(error_msg)
        raise APIError(error_msg)
    
    try:
        # Prepare request
        url = f"{self.base_url}/top-headlines"
        params = {
            'country': country,
            'pageSize': page_size,
            'apiKey': self.api_key
        }
        
        if category:
            params['category'] = category
        
        # Log API call start
        self.logger.log_api_call("NewsAPI", "requesting", f"country={country}")
        
        # Make request with timeout
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise for HTTP errors
        
        data = response.json()
        
        # Log success
        self.logger.log_api_call("NewsAPI", "success", 
                                 f"retrieved {len(data.get('articles', []))} articles")
        
        # Transform response
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
```

### Error Handling Layers

```
┌─────────────────────────────────────────────────────────────┐
│                  ERROR HANDLING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Pre-condition Check                               │
│  └─► Check API key before making request                    │
│                                                              │
│  Layer 2: Request Timeout                                   │
│  └─► timeout=10 prevents hanging                            │
│                                                              │
│  Layer 3: HTTP Status Check                                 │
│  └─► response.raise_for_status()                            │
│                                                              │
│  Layer 4: Specific Exception Handling                       │
│  └─► requests.exceptions.RequestException                   │
│                                                              │
│  Layer 5: Catch-all Exception                               │
│  └─► Exception for unexpected errors                        │
│                                                              │
│  Layer 6: Custom Exception Wrapping                         │
│  └─► Wrap in APIError with context                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. API Call Logging

### From the Project: `logger.py`

```python
def log_api_call(self, api_name: str, status: str, details: Optional[str] = None):
    """
    Log API calls for monitoring and debugging.
    
    Args:
        api_name: Name of the API being called
        status: Success or failure status
        details: Additional details about the call
    """
    log_msg = f"API Call - {api_name}: {status}"
    if details:
        log_msg += f" - {details}"
    self.logger.info(log_msg)
```

### Logging Strategy

| When | What to Log |
|------|-------------|
| **Before Call** | API name, parameters |
| **After Success** | Status, result count/size |
| **After Failure** | Error type, error message |
| **Always** | Timestamp (automatic) |

### Example Log Output

```
2024-01-15 10:23:45 - API Call - NewsAPI: requesting - country=us, category=technology
2024-01-15 10:23:46 - API Call - NewsAPI: success - retrieved 5 articles
2024-01-15 10:25:12 - API Call - OpenAI Web Search: requesting - AI conferences, limit=10
2024-01-15 10:25:18 - API Call - OpenAI Web Search: success - retrieved web search results
```

---

## 7. Response Parsing with Fallbacks

### From the Project: `api_integration.py`

```python
def _parse_conferences_from_text(self, text: str, limit: int) -> List[Dict[str, Any]]:
    """Parse conference information from OpenAI web search response text."""
    conferences = []
    
    # Split by multiple possible delimiters
    sections = re.split(r'\n\s*\n|\d+\.\s+|\-\s+|\•\s+', text)
    
    for section in sections:
        section = section.strip()
        if len(section) < 30:  # Skip very short sections
            continue
        
        conf = {
            'title': '',
            'description': '',
            'source': 'OpenAI Web Search',
            'url': '',
            'extracted_date': '',
            'extracted_location': '',
            'type': 'conference'
        }
        
        # Extract URL with regex
        url_pattern = r'https?://[^\s\)]+'
        urls = re.findall(url_pattern, section)
        if urls:
            conf['url'] = urls[0]
        
        # Extract dates with multiple format patterns
        date_patterns = [
            (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),
            (r'([A-Z][a-z]+ \d{1,2}, \d{4})', None),
            (r'(\d{1,2} [A-Z][a-z]+ \d{4})', None),
        ]
        
        for pattern, _ in date_patterns:
            dates = re.findall(pattern, section)
            if dates:
                conf['extracted_date'] = dates[0]
                break
        
        # ... more extraction logic ...
        
        if conf['title'] and len(conf['title']) > 5:
            conferences.append(conf)
        
        if len(conferences) >= limit:
            break
    
    # Fallback: Simple paragraph splitting if parsing didn't work
    if len(conferences) < 2:
        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
        for para in paragraphs[:limit]:
            conferences.append({
                'title': para.split('\n')[0][:200],
                'description': para[:500],
                'source': 'OpenAI Web Search',
                # ... default values ...
            })
    
    return conferences[:limit]
```

### Parsing Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                   PARSING STRATEGY                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Primary Parsing                                         │
│     • Split by logical delimiters                           │
│     • Extract structured fields (URL, date, location)       │
│     • Use regex patterns for each field                     │
│                                                              │
│  2. Validation                                              │
│     • Check minimum content length                          │
│     • Verify required fields exist                          │
│     • Skip invalid entries                                  │
│                                                              │
│  3. Fallback Parsing                                        │
│     • If primary fails, use simpler approach                │
│     • Split by paragraphs                                   │
│     • Use first line as title                               │
│                                                              │
│  4. Defaults                                                │
│     • Ensure all required fields have values                │
│     • Use sensible defaults for missing data                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Manager Pattern

### From the Project: `api_integration.py`

```python
class APIIntegrationManager:
    """
    Manages all external API integrations.
    Provides unified interface for accessing external data sources.
    """
    
    def __init__(self):
        self.logger = logger
        self.news_api = NewsAPI()
        self.openai_web_search = OpenAIWebSearchAPI()
    
    def get_contextual_data(self, 
                           news_topic: Optional[str] = None) -> Dict[str, Any]:
        """Get contextual data from APIs."""
        try:
            context = {
                'timestamp': datetime.now().isoformat(),
                'news': None
            }
            
            # Get news using OpenAI Web Search
            if news_topic:
                news_data = self.openai_web_search.get_top_headlines(
                    keywords=[news_topic],
                    page_size=5
                )
            else:
                news_data = self.openai_web_search.get_top_headlines(page_size=5)
            
            context['news'] = news_data
            return context
            
        except Exception as e:
            self.logger.log_error(e, "Error getting contextual data")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """Format contextual data for inclusion in prompts."""
        formatted = "EXTERNAL CONTEXT:\n\n"
        
        if context.get('news'):
            news = context['news']
            formatted += f"Recent News ({news.get('total_results', 0)} articles):\n"
            for article in news.get('articles', [])[:3]:
                formatted += f"- {article.get('title', 'N/A')}\n"
                formatted += f"  {article.get('description', 'N/A')}\n"
        
        return formatted
```

### Manager Pattern Benefits

| Benefit | Description |
|---------|-------------|
| **Single Entry Point** | One class to access all APIs |
| **Abstraction** | Hide individual API complexity |
| **Coordination** | Combine data from multiple sources |
| **Configuration** | Centralized API setup |

---

## 9. Environment Variable Management

### From the Project: `app.py`

```python
from dotenv import load_dotenv

# Load environment variables from .env file
app_dir = Path(__file__).parent.absolute()
env_path = app_dir / ".env"

# Try loading .env file with override
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    # Fallback: try current directory
    load_dotenv(override=True)
```

### Environment Variable Best Practices

```
┌─────────────────────────────────────────────────────────────┐
│              ENVIRONMENT VARIABLE BEST PRACTICES             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. .env File                                               │
│     OPENAI_API_KEY=sk-...                                   │
│     NEWS_API_KEY=...                                        │
│                                                              │
│  2. .gitignore                                              │
│     .env  # Never commit API keys!                          │
│                                                              │
│  3. Example File                                            │
│     .env.example with dummy values                          │
│                                                              │
│  4. Load Priority                                           │
│     a) Constructor parameter                                │
│     b) Environment variable                                 │
│     c) Default value (if appropriate)                       │
│                                                              │
│  5. Validation                                              │
│     Check at startup, not at call time                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Error Display in UI

### From the Project: `app.py`

```python
if st.button("🔍 Fetch AI Conferences", type="primary"):
    try:
        with st.spinner("Searching for AI conferences..."):
            conferences_data = st.session_state.api_manager.get_ai_conferences(
                category=category,
                limit=limit
            )
    except Exception as e:
        st.error(f"❌ Failed to fetch conferences: {str(e)}")
        st.info("💡 Please configure OPENAI_API_KEY in your .env file")
        st.stop()  # Stop execution gracefully
```

### User-Friendly Error Handling

| Principle | Implementation |
|-----------|----------------|
| **Clear Message** | What went wrong |
| **Actionable** | How to fix it |
| **Non-Technical** | Avoid stack traces in UI |
| **Graceful Stop** | `st.stop()` prevents partial rendering |

---

## 11. Timeout Handling

### Request Timeout Pattern

```python
# From the project
response = requests.get(url, params=params, timeout=10)
```

### Why Timeouts Matter

```
Without Timeout:
┌─────────────────────────────────────────────────────────────┐
│  User clicks button                                          │
│       │                                                      │
│       ▼                                                      │
│  API call starts... (server is slow/down)                   │
│       │                                                      │
│       │ ← User waits... and waits... and waits...           │
│       │                                                      │
│       ▼                                                      │
│  Eventually: Connection reset / Browser timeout              │
└─────────────────────────────────────────────────────────────┘

With Timeout (10 seconds):
┌─────────────────────────────────────────────────────────────┐
│  User clicks button                                          │
│       │                                                      │
│       ▼                                                      │
│  API call starts... (server is slow/down)                   │
│       │                                                      │
│       │ ← 10 seconds max                                    │
│       │                                                      │
│       ▼                                                      │
│  Timeout exception → Show error → User can retry            │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **Custom Exceptions** | APIError for specific error handling |
| **Initialization Checks** | Validate API keys at startup |
| **Availability Pattern** | `is_available()` method for UI feedback |
| **Logging** | Log API calls for debugging |
| **Timeouts** | Prevent hanging requests |
| **Fallback Parsing** | Multiple strategies for unreliable data |
| **Manager Pattern** | Unified interface for multiple APIs |
| **User-Friendly Errors** | Clear messages with actionable advice |

---

## Error Handling Checklist

```
□ Custom exception class defined
□ Pre-condition checks before API calls
□ Timeout set on all HTTP requests
□ Specific exception handling (not just catch-all)
□ Logging at each stage (start, success, failure)
□ User-friendly error messages in UI
□ Availability checking pattern implemented
□ Fallback strategies for unreliable data
□ Environment variables properly loaded
□ API keys validated at initialization
```

---

## Related Concepts

- [LangChain Integration](./04-langchain-integration.md) - OpenAI API usage
- [RAG Pipeline](./05-rag-pipeline.md) - Using external context
- [Project Overview](./01-project-overview.md) - Architecture context
