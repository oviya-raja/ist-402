# Setup Guide - Skill Builder for IST Students

This guide will help you set up the Skill Builder application on your local machine.

## Prerequisites

- **Python 3.8+** (Python 3.10 or higher recommended)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

## Quick Setup

```bash
# Navigate to the project directory
cd learning-path/WK12-SkillBuilder

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Environment Configuration

1. **Create a `.env` file** in the `WK12-SkillBuilder` directory:

```bash
cd learning-path/WK12-SkillBuilder
touch .env
```

2. **Add your API keys** to the `.env` file:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: NewsAPI Key (for news features)
NEWS_API_KEY=your_news_api_key_here
```

### Getting API Keys

- **OpenAI API Key**: 
  - Visit https://platform.openai.com/api-keys
  - Sign up or log in
  - Create a new API key
  - Copy and paste into `.env` file

- **NewsAPI Key** (Optional):
  - Visit https://newsapi.org/
  - Sign up for a free account
  - Get your API key from the dashboard
  - Copy and paste into `.env` file

## Running the Application

### Method 1: Using Streamlit directly

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the application
streamlit run app.py
```

### Method 2: Using the run script (with OpenMP fix)

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run using the provided script (handles OpenMP library conflict on macOS)
./run.sh
```

The application will start and be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

## Verifying Installation

After installation, verify that all dependencies are installed correctly:

```bash
# Activate virtual environment
source .venv/bin/activate

# Check Python version
python --version

# Check installed packages
pip list

# Verify key packages
python -c "import streamlit; import langchain; import faiss; import openai; print('All packages installed successfully!')"
```

## Troubleshooting

### Common Issues

1. **OpenMP Library Conflict (macOS)**
   - Error: `OMP: Error #15: Initializing libomp.dylib, but found libomp.dylib already initialized`
   - Solution: Use `./run.sh` script which sets `KMP_DUPLICATE_LIB_OK=TRUE` automatically
   - Or manually: `export KMP_DUPLICATE_LIB_OK=TRUE` before running

2. **FAISS Installation Issues**
   - If `faiss-cpu` fails to install, try:
     ```bash
     pip install faiss-cpu --no-cache-dir
     ```

3. **LangChain Import Errors**
   - Ensure all LangChain packages are installed:
     ```bash
     pip install langchain langchain-openai langchain-community
     ```

4. **Port Already in Use**
   - If port 8501 is already in use, Streamlit will automatically use the next available port
   - Or specify a custom port: `streamlit run app.py --server.port 8502`

5. **API Key Not Found**
   - Ensure `.env` file is in the `WK12-SkillBuilder` directory
   - Check that API keys are correctly formatted (no quotes, no spaces)
   - Restart the application after adding/changing API keys

## Project Structure

After setup, your directory structure should look like:

```
WK12-SkillBuilder/
├── .env                    # Your API keys (create this)
├── .venv/                  # Virtual environment (created)
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── run.sh                  # Run script with OpenMP fix
├── SETUP.md               # This file
├── README.md              # Project documentation
├── config/
│   └── config.yaml        # Application configuration
├── core/
│   ├── __init__.py
│   ├── api_integration.py
│   ├── content_generator.py
│   ├── data_processor.py
│   ├── logger.py
│   └── prompt_engineer.py
├── data/
│   └── ist_concepts.csv   # IST concepts database
└── learning-notes/         # Learning notes documentation
```

## Next Steps

1. **Start the application**: `streamlit run app.py` or `./run.sh`
2. **Upload learning notes**: Go to "Data Processing" tab and upload your notes (TXT, CSV, or MD)
3. **Explore features**: Try Concept Explainer, Study Plan Generator, and Quiz Me
4. **Read the README**: Check `README.md` for detailed feature documentation

## Support

For issues or questions:
- Check the `README.md` for detailed documentation
- Review error messages in the application logs
- Ensure all prerequisites are met
- Verify API keys are correctly configured

---

**Note**: Make sure to keep your `.env` file secure and never commit it to version control. The `.gitignore` file should already exclude it.
