# Smart Content Generator & Research Assistant

**Course:** IST402  
**Assignment:** W12 - GenAI-Driven Application Development  
**Project Type:** Full-Stack GenAI Application

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Project Objectives](#-project-objectives)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Setup Instructions](#-setup-instructions)
- [Usage Guide](#-usage-guide)
- [Use Cases](#-use-cases)
- [Integration Points](#-integration-points)
- [Error Handling & Logging](#-error-handling--logging)
- [Custom Prompt Engineering](#-custom-prompt-engineering)
- [Data Preprocessing](#-data-preprocessing)
- [Model Integration](#-model-integration)
- [API Integrations](#-api-integrations)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Contributors](#-contributors)

---

## 📋 Overview

**Project Name:** Smart Content Generator & Research Assistant

**Purpose:** A fully functional GenAI-driven web application that demonstrates advanced prompt engineering, data preprocessing, model integration, and external API integration. The system processes real-world data, applies generative AI techniques, and produces intelligent, contextual outputs for end users.

**Key Capabilities:**
- 📝 **Content Generation:** Generate contextual articles, blog posts, summaries, and reports
- 📊 **Data Analysis:** Analyze uploaded CSV/text files and generate insights
- 🔍 **Research Assistant:** Synthesize information from multiple sources with external context
- 📁 **Data Processing:** Upload, preprocess, and prepare data for GenAI consumption

**Platform:** Web Application (Streamlit)  
**Deployment:** Local/Cloud-ready

---

## 🎯 Project Objectives

This project fulfills all required objectives for the GenAI-driven application assignment:

✅ **Design, develop, and deploy a GenAI-driven application**  
✅ **Demonstrates understanding of prompt engineering**  
✅ **Implements data preprocessing for real-world data**  
✅ **Integrates GenAI models (OpenAI via LangChain)**  
✅ **Processes real-world data (CSV, text files)**  
✅ **Applies generative AI techniques**  
✅ **Produces intelligent, usable outputs**  
✅ **Fully functional web application**  
✅ **Simulates/ingests input data using GenAI models**  
✅ **Generates contextual and useful outputs**  
✅ **Automates tasks through external API integration**  
✅ **Includes custom prompt design**  
✅ **Includes at least one integration (Weather API, News API)**  
✅ **Implements error handling and logging**  
✅ **Comprehensive README with architecture and setup**

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                    │
│  (Content Generation | Data Analysis | Research | Processing) │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer (app.py)                 │
│              Routes requests to appropriate modules           │
└──────┬──────────────┬──────────────┬──────────────┬─────────┘
       │              │              │              │
       ▼              ▼              ▼              ▼
┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────────┐
│   Data   │  │    Prompt    │  │ Content  │  │     API      │
│Processor │  │  Engineer    │  │Generator │  │ Integration  │
└────┬─────┘  └──────┬───────┘  └────┬─────┘  └──────┬───────┘
     │               │                │               │
     │               │                │               │
     ▼               ▼                ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Services Layer                       │
│  • CSV/Text Loading  • Prompt Templates  • LangChain/OpenAI  │
│  • Data Validation   • Few-shot Learning • Weather API       │
│  • Text Chunking     • CoT Prompting    • News API          │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  • OpenAI API (GPT-4, GPT-4o-mini, GPT-3.5-turbo)          │
│  • OpenWeatherMap API (Weather Data)                        │
│  • NewsAPI (News Articles)                                  │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### 1. **Data Processing Module** (`core/data_processor.py`)
- **Purpose:** Handles ingestion and preprocessing of real-world data
- **Capabilities:**
  - CSV file loading and validation
  - Text file loading with multiple encoding support
  - DataFrame preprocessing and cleaning
  - Text chunking for large documents
  - Data validation and error handling

#### 2. **Prompt Engineering Module** (`core/prompt_engineer.py`)
- **Purpose:** Custom prompt design and management
- **Capabilities:**
  - Multiple prompt types (Content Generation, Data Analysis, Research Summary, etc.)
  - Few-shot learning examples
  - Chain-of-thought prompting
  - Role-based prompting
  - Dynamic prompt customization

#### 3. **Content Generator Module** (`core/content_generator.py`)
- **Purpose:** GenAI model integration using LangChain and OpenAI
- **Capabilities:**
  - OpenAI model initialization (GPT-4, GPT-4o-mini, GPT-3.5-turbo)
  - Content generation with custom prompts
  - Token usage tracking
  - Batch processing
  - Error handling and fallback

#### 4. **API Integration Module** (`core/api_integration.py`)
- **Purpose:** External API integration for contextual data
- **Capabilities:**
  - Weather API integration (OpenWeatherMap)
  - News API integration (NewsAPI)
  - Context formatting for prompts
  - Error handling with mock data fallback

#### 5. **Logging Module** (`core/logger.py`)
- **Purpose:** Centralized logging system
- **Capabilities:**
  - File and console logging
  - Daily log rotation
  - Error tracking with context
  - API call monitoring

#### 6. **Web Application** (`app.py`)
- **Purpose:** Streamlit-based user interface
- **Features:**
  - Four main tabs (Content Generation, Data Analysis, Research Assistant, Data Processing)
  - Real-time content generation
  - File upload and processing
  - External context integration
  - Model configuration

---

## ✨ Features

### 1. Content Generation
- Generate articles, blog posts, summaries, and reports
- Customizable tone, length, and audience
- Integration with external context (weather, news)
- Multiple prompt types and templates

### 2. Data Analysis
- Upload and analyze CSV files
- Upload and analyze text files
- Automatic data preprocessing
- GenAI-powered insights generation

### 3. Research Assistant
- Synthesize information from multiple sources
- Integrate external news and weather data
- Generate comprehensive research summaries
- Context-aware content generation

### 4. Data Processing
- CSV file upload and preview
- Text file upload and statistics
- Data preprocessing and cleaning
- Text chunking for large documents

### 5. External API Integration
- **Weather API:** Real-time weather data for contextual content
- **News API:** Recent news articles for research and content generation
- Graceful fallback to mock data when APIs are unavailable

### 6. Error Handling & Logging
- Comprehensive error handling throughout
- Centralized logging system
- API call monitoring
- User-friendly error messages

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+:** Primary programming language
- **Streamlit:** Web application framework
- **LangChain:** LLM orchestration framework
- **OpenAI API:** Generative AI models (GPT-4, GPT-4o-mini, GPT-3.5-turbo)

### Data Processing
- **Pandas:** Data manipulation and analysis
- **NumPy:** Numerical computing

### API Integration
- **Requests:** HTTP library for API calls
- **OpenWeatherMap API:** Weather data
- **NewsAPI:** News articles

### Utilities
- **Python-dotenv:** Environment variable management
- **PyYAML:** Configuration file parsing
- **Logging:** Built-in Python logging module

---

## 🔧 Setup Instructions

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **API Keys (Optional but recommended)**
   - OpenAI API Key: [Get from OpenAI Platform](https://platform.openai.com/api-keys)
   - OpenWeatherMap API Key: [Get from OpenWeatherMap](https://openweathermap.org/api) (Optional)
   - NewsAPI Key: [Get from NewsAPI](https://newsapi.org/) (Optional)

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd learning-path/W12
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```bash
   # Copy the example file
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here  # Optional
   NEWS_API_KEY=your_news_api_key_here  # Optional
   ```

5. **Create necessary directories:**
   ```bash
   mkdir -p logs data
   ```

6. **Run the application:**
   ```bash
   streamlit run app.py
   ```

7. **Access the application:**
   - Open your browser to `http://localhost:8501`
   - The application will open automatically

### Quick Start (Without API Keys)

The application can run in demo mode without API keys:
- Content generation will use mock responses
- Weather and news features will use mock data
- All features remain functional for demonstration

---

## 📖 Usage Guide

### Content Generation Tab

1. **Select Content Type:** Choose from Article, Blog Post, Summary, Creative Writing, or Report
2. **Enter Topic:** Type your topic or subject
3. **Configure Settings:**
   - Select tone (Professional, Casual, Academic, etc.)
   - Choose length (Short, Medium, Long)
4. **Add External Context (Optional):**
   - Enable weather data for a specific city
   - Enable news data with category selection
5. **Click "Generate Content"** to create your content

### Data Analysis Tab

1. **Upload File:** Click "Upload Data File" and select a CSV or text file
2. **Preview Data:** Review the uploaded data
3. **Click "Analyze Data"** to generate AI-powered insights
4. **View Results:** See analysis with key trends and patterns

### Research Assistant Tab

1. **Enter Research Topic:** Type your research question or topic
2. **Configure Context:**
   - Enable news integration with category selection
   - Enable weather context for location-based research
3. **Add Additional Sources:** Paste additional information or sources
4. **Click "Generate Research Summary"** to create a comprehensive summary

### Data Processing Tab

1. **Upload File:** Select CSV or text file
2. **View Statistics:** See data overview and statistics
3. **Preprocess Data:** Click "Preprocess Data" to prepare data for GenAI
4. **Chunk Text:** For text files, use chunking to split large documents

---

## 🎯 Use Cases

### Use Case 1: Content Marketing
**Scenario:** A marketing team needs to generate blog posts about their products.

**Solution:**
1. Upload product data (CSV) in Data Processing tab
2. Use Content Generation tab with product information
3. Include recent news about the industry
4. Generate multiple variations with different tones

**Automation:** Eliminates manual content writing, ensures consistency, incorporates external context automatically.

### Use Case 2: Research Synthesis
**Scenario:** A researcher needs to synthesize information from multiple sources for a literature review.

**Solution:**
1. Use Research Assistant tab
2. Enter research topic
3. Include relevant news articles
4. Add additional sources in text format
5. Generate comprehensive summary

**Automation:** Automatically fetches relevant news, synthesizes information, creates structured summaries.

### Use Case 3: Data-Driven Insights
**Scenario:** A business analyst needs to quickly understand trends in sales data.

**Solution:**
1. Upload sales CSV in Data Analysis tab
2. System automatically preprocesses data
3. Generates AI-powered insights with key trends
4. Identifies anomalies and patterns

**Automation:** Eliminates manual data analysis, provides instant insights, highlights important patterns.

### Use Case 4: Contextual Content with External Data
**Scenario:** A travel writer needs to create location-specific content with current weather and local news.

**Solution:**
1. Use Content Generation tab
2. Enter destination city
3. Enable weather integration for that city
4. Enable news for local context
5. Generate contextual, location-aware content

**Automation:** Automatically fetches real-time weather and news, integrates into content generation.

---

## 🔗 Integration Points

### 1. OpenAI API Integration

**Purpose:** Generative AI content creation

**Integration Details:**
- **API:** OpenAI GPT Models (GPT-4, GPT-4o-mini, GPT-3.5-turbo)
- **Method:** LangChain ChatOpenAI wrapper
- **Authentication:** API key via environment variable
- **Features:**
  - Model selection (configurable)
  - Temperature control
  - Token usage tracking
  - Cost monitoring
  - Error handling with fallback

**Implementation:** `core/content_generator.py`

**Error Handling:**
- API key validation
- Request timeout handling
- Rate limit management
- Fallback to mock responses

### 2. OpenWeatherMap API Integration

**Purpose:** Real-time weather data for contextual content

**Integration Details:**
- **API:** OpenWeatherMap Current Weather API
- **Endpoint:** `https://api.openweathermap.org/data/2.5/weather`
- **Authentication:** API key via environment variable
- **Data Provided:**
  - Temperature, humidity, wind speed
  - Weather conditions
  - Location information

**Implementation:** `core/api_integration.py` - `WeatherAPI` class

**Error Handling:**
- API key validation
- Network error handling
- Fallback to mock weather data
- Timeout management

### 3. NewsAPI Integration

**Purpose:** Recent news articles for research and content generation

**Integration Details:**
- **API:** NewsAPI Top Headlines
- **Endpoint:** `https://newsapi.org/v2/top-headlines`
- **Authentication:** API key via environment variable
- **Features:**
  - Category filtering (technology, business, science, etc.)
  - Country-specific news
  - Article metadata (title, description, source, URL)

**Implementation:** `core/api_integration.py` - `NewsAPI` class

**Error Handling:**
- API key validation
- Network error handling
- Fallback to mock news data
- Rate limit management

### 4. Data File Integration

**Purpose:** Process real-world data files

**Integration Details:**
- **Formats Supported:** CSV, TXT
- **Processing:**
  - CSV: Pandas DataFrame processing
  - TXT: Text extraction and chunking
- **Validation:** File existence, encoding, format validation

**Implementation:** `core/data_processor.py`

**Error Handling:**
- File not found errors
- Encoding issues (multiple encoding attempts)
- Invalid format handling
- Empty file detection

---

## 🛡️ Error Handling & Logging

### Error Handling Strategy

The application implements comprehensive error handling at multiple levels:

#### 1. **API Error Handling**
- **Network Errors:** Timeout handling, retry logic, graceful degradation
- **Authentication Errors:** Clear error messages, fallback to mock data
- **Rate Limiting:** User notifications, queue management

#### 2. **Data Processing Errors**
- **File Errors:** File not found, encoding issues, format validation
- **Data Validation:** Empty data detection, type checking
- **Processing Errors:** Exception catching with context

#### 3. **Model Generation Errors**
- **API Failures:** Fallback to mock responses
- **Token Limits:** Automatic truncation
- **Invalid Prompts:** Validation and error messages

#### 4. **User Interface Errors**
- **Input Validation:** Real-time validation with helpful messages
- **State Management:** Session state error recovery
- **Display Errors:** User-friendly error messages

### Logging System

**Implementation:** `core/logger.py`

**Features:**
- **Dual Output:** File and console logging
- **Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Daily Rotation:** Automatic log file rotation
- **Structured Logging:** Timestamp, level, function, line number, message
- **API Monitoring:** Tracks all API calls with status and details
- **Error Tracking:** Full exception traceback with context

**Log Files:**
- Location: `logs/` directory
- Format: `app_YYYYMMDD.log`
- Encoding: UTF-8

**Example Log Entry:**
```
2024-01-15 14:30:25 - ContentGenerator - INFO - generate_content:45 - Generated content: 1250 characters
2024-01-15 14:30:26 - ContentGenerator - INFO - log_api_call:78 - API Call - OpenAI: success - tokens: 1250
```

---

## 🎨 Custom Prompt Engineering

### Prompt Types

The system implements multiple specialized prompt types:

#### 1. **Content Generation Prompt**
- **Purpose:** Generate articles, blog posts, summaries
- **Features:**
  - Domain-specific customization
  - Tone and audience targeting
  - Length control
  - Context integration

#### 2. **Data Analysis Prompt**
- **Purpose:** Analyze data and generate insights
- **Features:**
  - Trend identification
  - Pattern recognition
  - Statistical analysis
  - Actionable insights

#### 3. **Research Summary Prompt**
- **Purpose:** Synthesize information from multiple sources
- **Features:**
  - Source integration
  - External context inclusion
  - Connection identification
  - Structured summaries

#### 4. **Contextual Response Prompt**
- **Purpose:** Provide context-aware responses
- **Features:**
  - Query understanding
  - Context integration
  - Information synthesis

#### 5. **Creative Writing Prompt**
- **Purpose:** Generate creative content
- **Features:**
  - Genre-specific templates
  - Style customization
  - Element inclusion

### Prompt Engineering Techniques

#### 1. **Few-Shot Learning**
- Provides examples in prompts
- Improves output quality and consistency
- Configurable example sets

#### 2. **Chain-of-Thought Prompting**
- Step-by-step reasoning instructions
- Improves complex reasoning tasks
- Optional enhancement for all prompt types

#### 3. **Role-Based Prompting**
- Defines AI role and expertise
- Contextualizes responses
- Enhances domain-specific outputs

#### 4. **Dynamic Customization**
- Task-specific instructions
- Constraint application
- Parameter-based adaptation

**Implementation:** `core/prompt_engineer.py`

---

## 📊 Data Preprocessing

### CSV Processing

**Capabilities:**
- Automatic column detection
- Data type inference
- Missing value handling
- Text extraction from multiple columns
- Metadata preservation

**Process:**
1. Load CSV file with validation
2. Detect text columns automatically
3. Remove or handle missing values
4. Extract text content
5. Preserve metadata (non-text columns)
6. Convert to structured format for GenAI

### Text Processing

**Capabilities:**
- Multiple encoding support (UTF-8, Latin-1, CP1252)
- Text chunking for large documents
- Overlap preservation for context
- Statistics generation

**Process:**
1. Load text file with encoding detection
2. Validate content
3. Generate statistics (characters, words, lines)
4. Chunk text if needed (configurable size and overlap)
5. Prepare for GenAI processing

**Implementation:** `core/data_processor.py`

---

## 🤖 Model Integration

### LangChain Integration

**Framework:** LangChain for LLM orchestration

**Benefits:**
- Standardized interface
- Token usage tracking
- Callback support
- Easy model switching

**Implementation:**
```python
from langchain_openai import ChatOpenAI
from langchain.callbacks import get_openai_callback

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
with get_openai_callback() as cb:
    response = llm.invoke(messages)
    # Track tokens and cost
```

### OpenAI Models Supported

1. **GPT-4o-mini** (Default)
   - Cost-effective
   - Fast responses
   - Good quality

2. **GPT-4**
   - Highest quality
   - Better reasoning
   - Higher cost

3. **GPT-3.5-turbo**
   - Fast and economical
   - Good for simple tasks

### Token Management

- **Tracking:** Automatic token usage tracking
- **Cost Calculation:** Real-time cost estimation
- **Limits:** Configurable max tokens
- **Optimization:** Prompt optimization for efficiency

**Implementation:** `core/content_generator.py`

---

## 🌐 API Integrations

### Weather API (OpenWeatherMap)

**Use Cases:**
- Location-specific content generation
- Travel writing with weather context
- Event planning content
- Seasonal content creation

**Data Provided:**
- Current temperature
- Weather conditions
- Humidity and wind speed
- Location information

**Integration:** Automatic context injection into prompts

### News API (NewsAPI)

**Use Cases:**
- Current events integration
- Industry-specific content
- Research with recent developments
- Trend-aware content generation

**Data Provided:**
- Top headlines by category
- Article descriptions
- Source information
- Publication dates

**Integration:** Automatic context injection into research and content generation

**Implementation:** `core/api_integration.py`

---

## 📁 Project Structure

```
W12/
├── README.md                 # This comprehensive documentation
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── config/
│   └── config.yaml          # Application configuration
├── core/
│   ├── __init__.py          # Core module exports
│   ├── logger.py            # Logging system
│   ├── data_processor.py   # Data preprocessing
│   ├── prompt_engineer.py   # Custom prompt engineering
│   ├── content_generator.py # GenAI model integration
│   └── api_integration.py   # External API integration
├── data/
│   ├── sample_data.csv      # Sample CSV data
│   └── temp_*.csv           # Temporary uploaded files
└── logs/
    └── app_YYYYMMDD.log     # Daily log files
```

---

## 🧪 Testing

### Manual Testing

1. **Content Generation:**
   - Test with different topics and tones
   - Verify external context integration
   - Check token usage and costs

2. **Data Analysis:**
   - Upload sample CSV file
   - Verify preprocessing
   - Check analysis quality

3. **Research Assistant:**
   - Test with various topics
   - Verify news integration
   - Check summary quality

4. **Error Handling:**
   - Test without API keys (mock mode)
   - Test with invalid files
   - Test with network errors

### Test Scenarios

**Scenario 1: Full Functionality**
- All API keys configured
- Upload real data files
- Generate content with external context
- Verify all features work

**Scenario 2: Limited Functionality**
- Only OpenAI API key configured
- Weather and news use mock data
- Verify graceful degradation

**Scenario 3: Demo Mode**
- No API keys configured
- All features use mock data
- Verify application still functions

---

## ⚠️ Limitations

1. **API Dependencies:**
   - Requires OpenAI API key for real content generation
   - Weather and news APIs are optional but enhance functionality

2. **File Size Limits:**
   - Large files may take time to process
   - Text chunking handles large documents but may lose some context

3. **Model Constraints:**
   - Token limits based on selected model
   - Rate limits from OpenAI API
   - Cost considerations for high-volume usage

4. **External API Limits:**
   - NewsAPI free tier has rate limits
   - OpenWeatherMap free tier has request limits

5. **Data Format Support:**
   - Currently supports CSV and TXT files
   - Other formats require preprocessing

---

## 🔮 Future Improvements

### Short-Term Enhancements

1. **Additional Data Formats:**
   - PDF file support
   - JSON file processing
   - Excel file support

2. **Enhanced Prompt Engineering:**
   - Prompt templates library
   - User-defined prompts
   - Prompt versioning

3. **Advanced Features:**
   - Content export (PDF, DOCX)
   - Batch processing interface
   - Content history and versioning

### Long-Term Enhancements

1. **Multi-Model Support:**
   - HuggingFace model integration
   - Local model support
   - Model comparison tools

2. **Database Integration:**
   - Store generated content
   - User preferences
   - Content templates

3. **Advanced Analytics:**
   - Usage analytics dashboard
   - Content quality metrics
   - Cost tracking and optimization

4. **Collaboration Features:**
   - Multi-user support
   - Content sharing
   - Team workspaces

5. **Deployment:**
   - Cloud deployment (AWS, GCP, Azure)
   - Docker containerization
   - CI/CD pipeline

---

## 👥 Contributors

### Development Team

**Oviya Raja**
- **Role:** Primary Developer & Project Lead
- **Responsibilities:**
  - System architecture and design
  - Core module development
  - Prompt engineering implementation
  - API integration
  - Web application development
  - Documentation

### Contribution Areas

- **Core Development:**
  - Data processing module
  - Prompt engineering system
  - Content generator with LangChain
  - API integration modules
  - Logging system

- **Application Development:**
  - Streamlit web interface
  - User experience design
  - Error handling
  - State management

- **Documentation:**
  - Comprehensive README
  - Code documentation
  - Usage guides
  - Architecture documentation

---

## 📄 License

This project is developed for educational purposes as part of IST402 course requirements.

---

## 🙏 Acknowledgments

- **OpenAI** for GPT models and API
- **LangChain** for LLM orchestration framework
- **Streamlit** for web application framework
- **OpenWeatherMap** and **NewsAPI** for external data sources

---

## 📞 Support

For questions or issues:
1. Check the documentation in this README
2. Review error logs in `logs/` directory
3. Verify API keys are correctly configured
4. Check that all dependencies are installed

---

**Last Updated:** January 2024  
**Version:** 1.0.0  
**Status:** Production Ready
