# API Keys Setup Guide

This guide explains how to add API keys to enable full functionality of the Smart Content Generator.

## Quick Setup

### Step 1: Locate the `.env` file

The `.env` file is in the project root directory:
```
W12/
└── .env
```

### Step 2: Edit the `.env` file

Open the `.env` file in a text editor and add your API keys:

```env
# OpenAI API Key (Required for real content generation)
OPENAI_API_KEY=sk-your-openai-api-key-here

# OpenWeatherMap API Key (Optional - for weather features)
OPENWEATHER_API_KEY=your-openweather-api-key-here

# NewsAPI Key (Optional - for news features)
NEWS_API_KEY=your-newsapi-key-here

# Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
```

### Step 3: Save and Restart

1. Save the `.env` file
2. Restart the Streamlit application if it's running
3. The application will automatically load the new API keys

## Getting API Keys

### 1. OpenAI API Key (Required)

**Purpose:** Enables real content generation using GPT models

**Steps:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste it in `.env` as `OPENAI_API_KEY=sk-...`

**Note:** You'll need to add a payment method to use the API (pay-as-you-go pricing)

**Free Tier:** No free tier, but new accounts get $5 free credits

### 2. OpenWeatherMap API Key (Optional)

**Purpose:** Provides real-time weather data for contextual content

**Steps:**
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" (free account available)
3. Verify your email
4. Go to "API keys" section
5. Copy your API key
6. Paste it in `.env` as `OPENWEATHER_API_KEY=...`

**Free Tier:** 
- 60 calls/minute
- 1,000,000 calls/month
- Current weather data

### 3. NewsAPI Key (Optional)

**Purpose:** Provides recent news articles for research and content generation

**Steps:**
1. Go to [NewsAPI](https://newsapi.org/)
2. Click "Get API Key"
3. Sign up for a free account
4. Verify your email
5. Copy your API key from the dashboard
6. Paste it in `.env` as `NEWS_API_KEY=...`

**Free Tier:**
- 100 requests/day
- Development use only
- Top headlines endpoint

## How It Works

The application reads API keys from the `.env` file using the `python-dotenv` package. Here's how each module loads the keys:

### Content Generator (`core/content_generator.py`)
```python
self.api_key = os.getenv('OPENAI_API_KEY')
```

### Weather API (`core/api_integration.py`)
```python
self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
```

### News API (`core/api_integration.py`)
```python
self.api_key = api_key or os.getenv('NEWS_API_KEY')
```

## Verification

After adding API keys, verify they're loaded correctly:

### Method 1: Check Application Logs

When you start the application, you should see:
- ✅ `INFO - Initialized OpenAI model: gpt-4o-mini` (if OpenAI key is set)
- ✅ No "mock data" messages when using features

### Method 2: Test in Application

1. **Test OpenAI:**
   - Go to "Content Generation" tab
   - Enter a topic and click "Generate Content"
   - If you see real generated content (not mock), the key works!

2. **Test Weather API:**
   - Go to "Content Generation" tab
   - Enable "Include Weather"
   - Enter a city name
   - Generate content
   - Check if real weather data appears

3. **Test News API:**
   - Go to "Research Assistant" tab
   - Enable "Include Recent News"
   - Generate research summary
   - Check if real news articles appear

## Security Best Practices

1. **Never commit `.env` to Git**
   - The `.gitignore` file already excludes `.env`
   - Double-check before committing

2. **Keep API Keys Secret**
   - Don't share your `.env` file
   - Don't paste API keys in code or documentation
   - Rotate keys if accidentally exposed

3. **Use Environment Variables in Production**
   - For production deployments, use environment variables directly
   - Don't rely on `.env` files in production

4. **Monitor API Usage**
   - Check usage in each API provider's dashboard
   - Set up usage alerts if available
   - Monitor costs for OpenAI API

## Troubleshooting

### Issue: API key not working

**Symptoms:**
- Still seeing mock data
- Error messages about authentication

**Solutions:**
1. Verify the key is correct (no extra spaces, complete key)
2. Check if the key is active in the provider's dashboard
3. Verify the `.env` file is in the correct location (project root)
4. Restart the application after adding keys
5. Check application logs for specific error messages

### Issue: Rate limit errors

**Symptoms:**
- "Rate limit exceeded" errors
- API calls failing

**Solutions:**
1. Check your API tier/plan limits
2. Wait for rate limit to reset
3. Reduce request frequency
4. Upgrade to a higher tier if needed

### Issue: Invalid API key format

**Symptoms:**
- "Invalid API key" errors
- Authentication failures

**Solutions:**
1. Verify key format:
   - OpenAI: Should start with `sk-`
   - OpenWeatherMap: Alphanumeric string
   - NewsAPI: Alphanumeric string
2. Check for extra spaces or newlines
3. Regenerate the key if needed

## Example `.env` File

Here's a complete example `.env` file:

```env
# ============================================
# Smart Content Generator - API Configuration
# ============================================

# OpenAI API Key (Required)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# OpenWeatherMap API Key (Optional)
# Get from: https://openweathermap.org/api
OPENWEATHER_API_KEY=1234567890abcdef1234567890abcdef

# NewsAPI Key (Optional)
# Get from: https://newsapi.org/
NEWS_API_KEY=1234567890abcdef1234567890abcdef

# Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
```

## Demo Mode

The application works perfectly in **demo mode** without any API keys:
- ✅ All features are functional
- ✅ Uses mock data for weather and news
- ✅ Uses mock responses for content generation
- ✅ Great for testing and demonstration

You only need API keys for:
- Real content generation (OpenAI)
- Real weather data (OpenWeatherMap)
- Real news articles (NewsAPI)

## Next Steps

1. Add your API keys to `.env`
2. Restart the application
3. Test each feature to verify keys work
4. Monitor usage in API provider dashboards

For more information, see the main [README.md](README.md).
