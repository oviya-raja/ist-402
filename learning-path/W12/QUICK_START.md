# Quick Start Guide

Get up and running with the Smart Content Generator in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional but recommended)

## Installation

### Option 1: Automated Setup (Recommended)

```bash
cd learning-path/W12
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p logs data

# Create .env file (copy from .env.example or create manually)
# Add your OPENAI_API_KEY
```

## Running the Application

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

## First Steps

1. **Initialize Generator:**
   - Go to sidebar
   - Click "Initialize Generator"
   - Select model (gpt-4o-mini recommended for cost-effectiveness)

2. **Try Content Generation:**
   - Go to "Content Generation" tab
   - Enter a topic (e.g., "Artificial Intelligence in Healthcare")
   - Select tone and length
   - Click "Generate Content"

3. **Try Data Analysis:**
   - Go to "Data Analysis" tab
   - Upload `data/sample_data.csv`
   - Click "Analyze Data"
   - View AI-generated insights

4. **Try Research Assistant:**
   - Go to "Research Assistant" tab
   - Enter a research topic
   - Enable news integration (optional)
   - Click "Generate Research Summary"

## API Keys

### Quick Setup

1. **Edit the `.env` file** in the project root:
   ```bash
   # Open .env file
   nano .env  # or use your preferred editor
   ```

2. **Add your API keys:**
   ```env
   OPENAI_API_KEY=sk-your-key-here
   OPENWEATHER_API_KEY=your-key-here
   NEWS_API_KEY=your-key-here
   ```

3. **Save and restart** the application

### Required (for real content generation)
- **OpenAI API Key:** Get from [OpenAI Platform](https://platform.openai.com/api-keys)
  - Required for actual content generation
  - Free credits available for new accounts

### Optional (for enhanced features)
- **OpenWeatherMap API Key:** Get from [OpenWeatherMap](https://openweathermap.org/api)
  - Free tier: 1M calls/month
  - Provides real-time weather data
  
- **NewsAPI Key:** Get from [NewsAPI](https://newsapi.org/)
  - Free tier: 100 requests/day
  - Provides recent news articles

### Demo Mode

The application works without API keys in demo mode:
- Content generation uses mock responses
- Weather and news use mock data
- All features remain functional for demonstration

**📖 For detailed API setup instructions, see [API_SETUP.md](API_SETUP.md)**

## Troubleshooting

**Issue: Module not found**
- Solution: Make sure virtual environment is activated and dependencies are installed

**Issue: API errors**
- Solution: Check that API keys are correctly set in `.env` file

**Issue: Port already in use**
- Solution: Use `streamlit run app.py --server.port 8502` to use a different port

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all features in the web interface
- Try uploading your own data files
- Experiment with different prompt types and settings

## Support

For detailed documentation, see [README.md](README.md)
