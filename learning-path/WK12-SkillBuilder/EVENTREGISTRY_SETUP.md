# EventRegistry API Setup Guide

This guide explains how to set up and use EventRegistry API for news and AI conferences.

## What is EventRegistry?

EventRegistry is a powerful news and event aggregation service that provides:
- **Event-based search** - Better for finding actual conferences/events (not just articles)
- **Concept-based filtering** - Uses Wikipedia URIs for semantic search
- **Structured event data** - Dates, locations, and event types are properly structured
- **Better accuracy** - Event-based search is more accurate than filtering articles

## Installation

1. **Install the EventRegistry package:**
   ```bash
   pip install eventregistry
   ```

2. **Get your API key:**
   - Go to [EventRegistry.org](https://eventregistry.org/)
   - Sign up for a free account
   - Get your API key from the dashboard

3. **Add to `.env` file:**
   ```env
   EVENTREGISTRY_API_KEY=your_eventregistry_api_key_here
   ```

   **Note:** The code also checks for `NEWS_API_KEY` for backward compatibility.

## Free Tier Limitations

- Access to last 30 days of content only
- Limited number of queries per day
- Non-commercial use only
- Check EventRegistry documentation for current limits

## How It Works in This Application

### News Articles
- Uses `QueryArticlesIter` to search for articles
- Supports category filtering (technology, science, business, etc.)
- Returns structured article data

### AI Conferences
- Uses `QueryEvents` to search for actual events
- Filters by AI/ML concepts using concept URIs
- Returns structured event data with dates and locations
- Much more accurate than filtering articles

## API Key Setup

1. **Create `.env` file** in the project root:
   ```bash
   cd learning-path/WK12-SkillBuilder
   touch .env
   ```

2. **Add your API key:**
   ```env
   # Required for real content generation
   OPENAI_API_KEY=sk-your-openai-api-key-here

   # Optional - for news and AI conferences
   EVENTREGISTRY_API_KEY=your-eventregistry-api-key-here
   ```

3. **Restart the application** if it's running

## Testing

1. **Without API key:**
   - Application will use mock data
   - All features work for demonstration
   - You'll see "Mock data" notes

2. **With API key:**
   - Real news articles from EventRegistry
   - Real AI conferences/events
   - Better accuracy for conference detection

## Troubleshooting

**Issue: "EventRegistry package not installed"**
- Solution: Run `pip install eventregistry`

**Issue: "No conferences found"**
- Solution: Check API key is correct
- Try different categories
- Check EventRegistry service status

**Issue: "API key not configured"**
- Solution: Add `EVENTREGISTRY_API_KEY` to `.env` file
- Restart the application

## Benefits Over NewsAPI

1. **Event-based search** - Finds actual events, not just articles
2. **Better structure** - Dates and locations are properly formatted
3. **Concept-based filtering** - More accurate AI/ML topic matching
4. **Structured data** - Events have proper metadata

## Documentation

- EventRegistry Python SDK: https://github.com/EventRegistry/event-registry-python/wiki
- EventRegistry API Docs: https://eventregistry.org/documentation
- Examples: See the GitHub wiki for code examples
