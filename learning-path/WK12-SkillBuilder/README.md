# Skill Builder for IST Students

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

**Project Name:** Skill Builder for IST Students

**Purpose:** A fully functional GenAI-driven web application designed specifically for IST402 students. The system helps students understand course concepts, create personalized study plans, analyze data, conduct research, and discover AI-related conferences. The application demonstrates advanced prompt engineering, data preprocessing, model integration, and external API integration.

**Key Capabilities:**
- 📚 **IST Concept Explanations:** Get detailed explanations of IST402 course concepts with learning objectives
- 📅 **Study Plan Generation:** Create personalized study plans by week or topic
- 📊 **Data Analysis:** Analyze uploaded CSV/text files and generate insights
- 🔍 **Research Assistant:** Synthesize information from multiple sources with external context
- 📁 **Data Processing:** Upload, preprocess, and prepare data for GenAI consumption
- 🎯 **AI Conferences:** Discover AI-related conferences and events using OpenAI web search

**Platform:** Web Application (Streamlit)  
**Deployment:** Local/Cloud-ready

---

## 🎯 Project Objectives

This project fulfills all required objectives for the GenAI-driven application assignment:

✅ **Design, develop, and deploy a GenAI-driven application**  
✅ **Demonstrates understanding of prompt engineering**  
✅ **Implements data preprocessing for real-world data**  
✅ **Integrates GenAI models (OpenAI via LangChain)**  
✅ **Processes real-world data (CSV, text files, IST concepts database)**  
✅ **Applies generative AI techniques**  
✅ **Produces intelligent, usable outputs**  
✅ **Fully functional web application**  
✅ **Simulates/ingests input data using GenAI models**  
✅ **Generates contextual and useful outputs**  
✅ **Automates tasks through external API integration**  
✅ **Includes custom prompt design**  
✅ **Includes at least one integration (OpenAI Web Search)**  
✅ **Implements error handling and logging**  
✅ **Comprehensive README with architecture and setup**

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Streamlit Web Interface                          │
│  (Content Gen | Data Analysis | Research | Processing |     │
│   Conferences)                                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Layer (app.py)                      │
│         Routes requests to appropriate modules               │
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
│  • CSV/Text Loading  • Prompt Templates  • LangChain/OpenAI│
│  • IST Concepts DB   • Few-shot Learning • News API        │
│  • Text Chunking     • CoT Prompting    • AI Conferences   │
│  • Data Validation   • IST Prompts      • News Integration │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  • OpenAI API (GPT-4, GPT-4o-mini, GPT-3.5-turbo)          │
│  • OpenAI Web Search (News Articles & AI Conferences)      │
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
  - IST concepts database loading and querying
  - Data validation and error handling

#### 2. **Prompt Engineering Module** (`core/prompt_engineer.py`)
- **Purpose:** Custom prompt design and management
- **Capabilities:**
  - Multiple prompt types (Content Generation, Data Analysis, Research Summary, IST Concept Explanation, Study Plan Generation)
  - Few-shot learning examples
  - Chain-of-thought prompting
  - Role-based prompting
  - Dynamic prompt customization
  - IST-specific prompt templates

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
  - OpenAI Web Search API integration for news and events
  - AI Conferences detection using event-based search (NEW)
  - Context formatting for prompts
  - Error handling with clear error messages (no mock data)

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
  - Five main tabs (Content Generation, Data Analysis, Research Assistant, Data Processing, AI Conferences)
  - IST Concept Explanation mode
  - Study Plan Generator mode
  - Real-time content generation
  - File upload and processing
  - External context integration
  - Model configuration

---

## ✨ Features

### 1. Content Generation (Enhanced)
- **General Content Mode:** Generate articles, blog posts, summaries, and reports
- **IST Concept Explanation Mode (NEW):**
  - Select from IST concepts database
  - Get detailed explanations with learning objectives
  - View prerequisites and difficulty levels
  - See time estimates
- Customizable tone, length, and audience
- Integration with external context (news)
- Multiple prompt types and templates

### 2. Data Analysis (Enhanced)
- **Data Analysis Mode:** Upload and analyze CSV/text files
- **Study Plan Generator Mode (NEW):**
  - Generate personalized study plans by week or week range
  - Filter by topic
  - Set learning pace and difficulty preferences
  - Get organized study schedules with prerequisites
  - Time estimates and learning tips
- Automatic data preprocessing
- GenAI-powered insights generation

### 3. Research Assistant
- Synthesize information from multiple sources
- Integrate external news data
- Generate comprehensive research summaries
- Context-aware content generation

### 4. Data Processing
- CSV file upload and preview
- Text file upload and statistics
- Data preprocessing and cleaning
- Text chunking for large documents

### 5. AI Conferences (NEW)
- Fetch AI-related conferences from OpenAI web search
- Event-based search (not just articles) for better accuracy
- Filter by category (technology, science, business, general)
- View conference details (date, location, description)
- Conference type detection (summit, workshop, conference, etc.)
- Direct links to conference information

### 6. External API Integration
- **News API:** Recent news articles for research and content generation
- **AI Conferences:** Automatic detection and parsing of AI-related events
- Clear error messages when APIs are unavailable (no mock data fallback)

### 7. Error Handling & Logging
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
- **OpenAI Web Search:** News articles and event/conference detection using web_search_preview tool

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
   - OpenAI API Key: Already required for content generation (used for web search too)

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd learning-path/WK12-SkillBuilder
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
   # Copy the example file (if available) or create manually
   ```
   
   Edit `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   # OpenAI API key is used for both content generation and web search
   ```

5. **Create necessary directories:**
   ```bash
   mkdir -p logs data
   ```

6. **Verify IST concepts database exists:**
   ```bash
   ls data/ist_concepts.csv
   ```
   The file should already be included in the project.

7. **Run the application:**
   ```bash
   streamlit run app.py
   ```

8. **Access the application:**
   - Open your browser to `http://localhost:8501`
   - The application will open automatically

### Quick Start (Without API Keys)

The application can run in demo mode without API keys:
- Content generation will fail with clear error if OPENAI_API_KEY is not configured
- News features will fail with clear error if OPENAI_API_KEY is not configured
- AI Conferences will fail with clear error if OPENAI_API_KEY is not configured
- All features remain functional for demonstration

**Note:** OpenAI API key is used for both content generation and web search functionality

---

## 📖 Usage Guide

### Content Generation Tab

#### IST Concept Explanation Mode
1. **Select Mode:** Choose "IST Concept Explanation"
2. **Select Concept:** Choose from dropdown or enter concept name
3. **View Concept Info:** See week, difficulty, time estimate, prerequisites
4. **Configure Options:** Include prerequisites and examples
5. **Click "Generate Concept Explanation"** to get detailed explanation

#### General Content Mode
1. **Select Mode:** Choose "General Content"
2. **Enter Topic:** Type your topic or subject
3. **Configure Settings:**
   - Select tone (Professional, Casual, Academic, etc.)
   - Choose length (Short, Medium, Long)
4. **Add External Context (Optional):**
   - Enable news data with category selection
5. **Click "Generate Content"** to create your content

### Data Analysis Tab

#### Study Plan Generator Mode
1. **Select Mode:** Choose "Study Plan Generator"
2. **Select Week(s):** Choose single week or week range
3. **Set Preferences:**
   - Learning pace (Slow, Moderate, Fast)
   - Difficulty preference (Beginner, Intermediate, Advanced, All Levels)
4. **Add Topic Filter (Optional):** Filter by specific topics
5. **Click "Generate Study Plan"** to create personalized plan

#### Data Analysis Mode
1. **Select Mode:** Choose "Data Analysis"
2. **Upload File:** Click "Upload Data File" and select a CSV or text file
3. **Preview Data:** Review the uploaded data
4. **Click "Analyze Data"** to generate AI-powered insights
5. **View Results:** See analysis with key trends and patterns

### Research Assistant Tab

1. **Enter Research Topic:** Type your research question or topic
2. **Configure Context:**
   - Enable news integration with category selection
3. **Add Additional Sources:** Paste additional information or sources
4. **Click "Generate Research Summary"** to create a comprehensive summary

### Data Processing Tab

1. **Upload File:** Select CSV or text file
2. **View Statistics:** See data overview and statistics
3. **Preprocess Data:** Click "Preprocess Data" to prepare data for GenAI
4. **Chunk Text:** For text files, use chunking to split large documents

### AI Conferences Tab (NEW)

1. **Select Category:** Choose category (technology, science, business, general)
2. **Set Max Results:** Choose how many conferences to display (5-20)
3. **Click "Fetch AI Conferences"** to get latest conferences
4. **View Details:** Expand each conference to see details
5. **Access Links:** Click "Read More" to visit conference website

---

## 🎯 Use Cases

### Use Case 1: Learning IST Concepts
**Scenario:** A student needs to understand the RAG concept for Week 2.

**Solution:**
1. Open Content Generation tab
2. Select "IST Concept Explanation" mode
3. Choose "RAG" from concept dropdown
4. View concept information (week, prerequisites, difficulty)
5. Generate detailed explanation with learning objectives

**Automation:** Provides instant, comprehensive concept explanations with all relevant context.

### Use Case 2: Creating Study Plans
**Scenario:** A student wants a study plan for Weeks 1-3.

**Solution:**
1. Open Data Analysis tab
2. Select "Study Plan Generator" mode
3. Choose "Week Range" and select W01 to W03
4. Set learning pace and difficulty preferences
5. Generate personalized study plan with schedule

**Automation:** Automatically organizes concepts by prerequisites, provides time estimates, and creates structured learning schedule.

### Use Case 3: Discovering AI Conferences
**Scenario:** A student wants to find AI conferences to attend.

**Solution:**
1. Open AI Conferences tab
2. Select "technology" category
3. Click "Fetch AI Conferences"
4. Browse conference list with details
5. Click links to visit conference websites

**Automation:** Automatically fetches AI-related conferences using OpenAI web search with web_search_preview tool for real-time results.

### Use Case 4: Data-Driven Insights
**Scenario:** A student needs to analyze course data.

**Solution:**
1. Open Data Analysis tab
2. Select "Data Analysis" mode
3. Upload CSV file with course data
4. System automatically preprocesses data
5. Generates AI-powered insights with key trends

**Automation:** Eliminates manual data analysis, provides instant insights, highlights important patterns.

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
- Clear error messages (no mock data)

### 2. OpenAI Web Search Integration

**Purpose:** Recent news articles and AI conferences/events

**Integration Details:**
- **API:** OpenAI Responses API with web_search_preview tool
- **Package:** `openai` Python package (already included)
- **Authentication:** API key via environment variable
- **Features:**
  - Article search with category filtering
  - Event-based search for conferences (not just articles)
  - Concept-based filtering (using Wikipedia URIs)
  - Article metadata (title, description, source, URL)
  - **AI Conferences Detection (NEW):**
    - Event-based search for actual conferences
    - Structured event data (dates, locations)
    - Conference type detection
    - Better accuracy than article filtering

**Implementation:** `core/api_integration.py` - `OpenAIWebSearchAPI` class

**Error Handling:**
- API key validation
- Network error handling
- Clear error messages for missing API keys (no mock data)
- Package availability checking

### 4. IST Concepts Database Integration

**Purpose:** Access IST402 course concepts

**Integration Details:**
- **Format:** CSV file (`data/ist_concepts.csv`)
- **Structure:**
  - concept_name, week, description, learning_objectives
  - prerequisites, difficulty, time_estimate, keywords
- **Processing:**
  - CSV loading via Pandas
  - Concept filtering by week
  - Concept lookup by name
  - Data validation

**Implementation:** `core/data_processor.py`

**Error Handling:**
- File existence validation
- Data format validation
- Missing data handling

---

## 🛡️ Error Handling & Logging

### Error Handling Strategy

The application implements comprehensive error handling at multiple levels:

#### 1. **API Error Handling**
- **Network Errors:** Timeout handling, retry logic, graceful degradation
- **Authentication Errors:** Clear error messages (API keys required)
- **Rate Limiting:** User notifications, queue management

#### 2. **Data Processing Errors**
- **File Errors:** File not found, encoding issues, format validation
- **Data Validation:** Empty data detection, type checking
- **Processing Errors:** Exception catching with context

#### 3. **Model Generation Errors**
- **API Failures:** Clear error messages (no mock data fallback)
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

#### 4. **IST Concept Explanation Prompt (NEW)**
- **Purpose:** Explain IST402 course concepts
- **Features:**
  - Learning objectives coverage
  - Prerequisites connection
  - Examples and use cases
  - Related concepts linking
  - Technical terminology

#### 5. **Study Plan Generation Prompt (NEW)**
- **Purpose:** Create personalized study plans
- **Features:**
  - Concept organization by prerequisites
  - Time estimates
  - Difficulty levels
  - Learning schedule
  - Review suggestions

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

### IST Concepts Processing

**Capabilities:**
- CSV loading and validation
- Concept filtering by week
- Concept lookup by name
- Data structure preservation

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

### News API (OpenAI Web Search)

**Use Cases:**
- Current events integration
- Industry-specific content
- Research with recent developments
- Trend-aware content generation

**Data Provided:**
- Articles by category or keywords
- Article descriptions
- Source information
- Publication dates

**Integration:** Automatic context injection into research and content generation

### AI Conferences (OpenAI Web Search - NEW)

**Use Cases:**
- Discover AI-related conferences
- Find learning opportunities
- Stay updated with industry events
- Plan conference attendance

**Data Provided:**
- Conference names and descriptions
- Structured event dates
- Event locations
- Conference types (summit, workshop, etc.)
- Event URIs and URLs

**Integration:** Dedicated tab with filtering and display
**Advantage:** Event-based search provides more accurate conference detection than article filtering

**Implementation:** `core/api_integration.py`

---

## 📁 Project Structure

```
WK12-SkillBuilder/
├── README.md                 # This comprehensive documentation
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
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
│   ├── ist_concepts.csv     # IST course concepts database
│   └── sample_data.csv      # Sample CSV data
└── logs/
    └── app_YYYYMMDD.log     # Daily log files
```

---

## 🧪 Testing

### Manual Testing

1. **IST Concept Explanation:**
   - Test with different concepts
   - Verify learning objectives are included
   - Check prerequisites display
   - Verify explanation quality

2. **Study Plan Generation:**
   - Test with single week
   - Test with week range
   - Test with topic filters
   - Verify schedule organization

3. **AI Conferences:**
   - Test conference fetching
   - Verify filtering works
   - Check date/location extraction
   - Test with different categories

4. **Data Analysis:**
   - Upload sample CSV file
   - Verify preprocessing
   - Check analysis quality

5. **Error Handling:**
   - All API keys are required (no mock mode)
   - Test with invalid files
   - Test with network errors

### Test Scenarios

**Scenario 1: Full Functionality**
- All API keys configured
- IST concepts loaded
- Generate concept explanation
- Generate study plan
- Fetch AI conferences
- Verify all features work

**Scenario 2: Limited Functionality**
- Only OpenAI API key configured
- News requires OPENAI_API_KEY (no mock data)
- Verify graceful degradation

**Scenario 3: Demo Mode**
- No API keys configured
- All features require valid API keys (no mock data)
- Verify application still functions

---

## ⚠️ Limitations

1. **API Dependencies:**
   - Requires OpenAI API key for real content generation
   - News API is optional but enhances functionality

2. **File Size Limits:**
   - Large files may take time to process
   - Text chunking handles large documents but may lose some context

3. **Model Constraints:**
   - Token limits based on selected model
   - Rate limits from OpenAI API
   - Cost considerations for high-volume usage

4. **External API Limits:**
   - OpenAI API has usage limits based on your subscription tier
   - Free tier allows access to last 30 days of content only

5. **Data Format Support:**
   - Currently supports CSV and TXT files
   - Other formats require preprocessing

6. **Conference Detection:**
   - Uses OpenAI web search with web_search_preview tool (real-time web search results)
   - Structured event data provides better date/location information
   - Concept-based filtering improves relevance

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
   - Study plan saving and sharing

4. **Conference Features:**
   - Conference calendar view
   - Conference reminders
   - Conference filtering by date range
   - Integration with conference registration

### Long-Term Enhancements

1. **Multi-Model Support:**
   - HuggingFace model integration
   - Local model support
   - Model comparison tools

2. **Database Integration:**
   - Store generated content
   - User preferences
   - Content templates
   - Study plan history

3. **Advanced Analytics:**
   - Usage analytics dashboard
   - Content quality metrics
   - Cost tracking and optimization
   - Learning progress tracking

4. **Collaboration Features:**
   - Multi-user support
   - Content sharing
   - Team workspaces
   - Study group features

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
  - IST-specific features

- **Application Development:**
  - Streamlit web interface
  - User experience design
  - Error handling
  - State management
  - IST concept integration
  - Study plan generator
  - AI conferences feature

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
- **OpenAI Web Search** for news and event data sources
- **IST402 Course** for providing the learning context

---

## 📞 Support

For questions or issues:
1. Check the documentation in this README
2. Review error logs in `logs/` directory
3. Verify API keys are correctly configured
4. Check that all dependencies are installed
5. Ensure IST concepts database exists at `data/ist_concepts.csv`

---

**Last Updated:** January 2024  
**Version:** 2.0.0  
**Status:** Production Ready