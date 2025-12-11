"""
Smart Content Generator & Research Assistant
Main Streamlit Web Application

A GenAI-driven application that demonstrates:
- Prompt engineering
- Data preprocessing
- Model integration (OpenAI via LangChain)
- External API integration
- Error handling and logging
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core import (
    get_logger,
    DataProcessor,
    PromptEngineer,
    PromptType,
    APIIntegrationManager,
    ContentGenerator
)

# Initialize logger
logger = get_logger()

# Page configuration
st.set_page_config(
    page_title="Smart Content Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'api_manager' not in st.session_state:
    st.session_state.api_manager = APIIntegrationManager()
if 'prompt_engineer' not in st.session_state:
    st.session_state.prompt_engineer = PromptEngineer()


def initialize_generator():
    """Initialize content generator if not already done."""
    if st.session_state.generator is None:
        try:
            st.session_state.generator = ContentGenerator(
                model_name="gpt-4o-mini",
                temperature=0.7
            )
            logger.info("Content generator initialized")
        except Exception as e:
            logger.log_error(e, "Error initializing content generator")
            st.error(f"Error initializing generator: {str(e)}")


def main():
    """Main application function."""
    st.title("🤖 Smart Content Generator & Research Assistant")
    st.markdown("""
    A GenAI-driven application that processes real-world data and generates intelligent, 
    contextual content using advanced prompt engineering and external API integrations.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_name = st.selectbox(
            "Model",
            ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
            index=0
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in generation"
        )
        
        # Initialize generator with selected settings
        if st.button("Initialize Generator"):
            try:
                st.session_state.generator = ContentGenerator(
                    model_name=model_name,
                    temperature=temperature
                )
                st.success("Generator initialized!")
                logger.info(f"Generator initialized with model: {model_name}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.log_error(e, "Error initializing generator")
        
        st.divider()
        
        # API status
        st.header("📡 API Status")
        if st.session_state.generator:
            if st.session_state.generator.is_available():
                st.success("✅ OpenAI API: Connected")
            else:
                st.warning("⚠️ OpenAI API: Not configured")
        else:
            st.info("ℹ️ Generator not initialized")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Content Generation",
        "📊 Data Analysis",
        "🔍 Research Assistant",
        "📁 Data Processing"
    ])
    
    # Tab 1: Content Generation
    with tab1:
        st.header("Content Generation")
        st.markdown("Generate contextual content using custom prompts and external data.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            content_type = st.selectbox(
                "Content Type",
                ["Article", "Blog Post", "Summary", "Creative Writing", "Report"]
            )
            
            topic = st.text_input("Topic", placeholder="Enter your topic...")
            
            tone = st.selectbox(
                "Tone",
                ["Professional", "Casual", "Academic", "Creative", "Technical"]
            )
            
            length = st.selectbox(
                "Length",
                ["Short (200-300 words)", "Medium (500-700 words)", "Long (1000+ words)"]
            )
        
        with col2:
            st.subheader("External Context")
            use_weather = st.checkbox("Include Weather", help="Add weather context")
            weather_city = st.text_input("City", disabled=not use_weather, placeholder="e.g., New York")
            
            use_news = st.checkbox("Include News", help="Add recent news context")
            news_category = st.selectbox(
                "News Category",
                ["general", "technology", "business", "science"],
                disabled=not use_news
            )
        
        if st.button("Generate Content", type="primary"):
            if not topic:
                st.warning("Please enter a topic")
            else:
                try:
                    # Initialize generator if needed
                    if not st.session_state.generator:
                        initialize_generator()
                    
                    # Get external context if requested
                    external_context = {}
                    if use_weather and weather_city:
                        external_context = st.session_state.api_manager.get_contextual_data(
                            city=weather_city
                        )
                    
                    if use_news:
                        if not external_context:
                            external_context = st.session_state.api_manager.get_contextual_data()
                        else:
                            news_data = st.session_state.api_manager.news_api.get_top_headlines(
                                category=news_category
                            )
                            external_context['news'] = news_data
                    
                    # Build prompt
                    prompt_type = PromptType.CONTENT_GENERATION
                    length_words = {
                        "Short (200-300 words)": "250",
                        "Medium (500-700 words)": "600",
                        "Long (1000+ words)": "1200"
                    }[length]
                    
                    # Generate content
                    with st.spinner("Generating content..."):
                        result = st.session_state.generator.generate_with_prompt_type(
                            prompt_type=prompt_type,
                            context=f"Topic: {topic}",
                            data="",
                            domain="general",
                            tone=tone.lower(),
                            audience="general audience",
                            length=length_words,
                            **{"prompt": topic}
                        )
                        
                        # Add external context if available
                        if external_context:
                            result = st.session_state.generator.generate_with_external_context(
                                prompt=result['content'],
                                external_context=external_context
                            )
                    
                    # Display results
                    st.subheader("Generated Content")
                    st.write(result['content'])
                    
                    # Show metadata
                    with st.expander("Generation Metadata"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Model", result.get('model', 'N/A'))
                        with col2:
                            if result.get('token_usage', {}).get('total_tokens'):
                                st.metric("Tokens", result['token_usage']['total_tokens'])
                        with col3:
                            if result.get('token_usage', {}).get('total_cost'):
                                st.metric("Cost", f"${result['token_usage']['total_cost']:.4f}")
                    
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
                    logger.log_error(e, "Error in content generation")
    
    # Tab 2: Data Analysis
    with tab2:
        st.header("Data Analysis")
        st.markdown("Analyze uploaded data and generate insights using GenAI.")
        
        uploaded_file = st.file_uploader(
            "Upload Data File",
            type=['csv', 'txt'],
            help="Upload CSV or text file for analysis"
        )
        
        if uploaded_file:
            try:
                # Process file
                file_path = f"data/temp_{uploaded_file.name}"
                Path("data").mkdir(exist_ok=True)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load and process data
                if uploaded_file.name.endswith('.csv'):
                    df = st.session_state.data_processor.load_csv(file_path)
                    processed_data = st.session_state.data_processor.preprocess_dataframe(df)
                    
                    st.subheader("Data Preview")
                    st.dataframe(df.head(10))
                    
                    if st.button("Analyze Data", type="primary"):
                        # Initialize generator if needed
                        if not st.session_state.generator:
                            initialize_generator()
                        
                        # Prepare data summary
                        data_summary = f"""
                        Dataset Shape: {df.shape}
                        Columns: {', '.join(df.columns.tolist())}
                        Sample Data:
                        {df.head(5).to_string()}
                        """
                        
                        with st.spinner("Analyzing data..."):
                            result = st.session_state.generator.generate_with_prompt_type(
                                prompt_type=PromptType.DATA_ANALYSIS,
                                data=data_summary
                            )
                        
                        st.subheader("Analysis Results")
                        st.write(result['content'])
                
                elif uploaded_file.name.endswith('.txt'):
                    text_content = st.session_state.data_processor.load_text_file(file_path)
                    
                    st.subheader("Text Preview")
                    st.text_area("Content", text_content[:500] + "...", height=200)
                    
                    if st.button("Analyze Text", type="primary"):
                        if not st.session_state.generator:
                            initialize_generator()
                        
                        with st.spinner("Analyzing text..."):
                            result = st.session_state.generator.generate_with_prompt_type(
                                prompt_type=PromptType.DATA_ANALYSIS,
                                data=text_content[:5000]  # Limit for demo
                            )
                        
                        st.subheader("Analysis Results")
                        st.write(result['content'])
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                logger.log_error(e, "Error processing uploaded file")
    
    # Tab 3: Research Assistant
    with tab3:
        st.header("Research Assistant")
        st.markdown("Synthesize information from multiple sources with external context.")
        
        research_topic = st.text_input("Research Topic", placeholder="Enter research topic...")
        
        col1, col2 = st.columns(2)
        with col1:
            include_news = st.checkbox("Include Recent News")
            news_cat = st.selectbox(
                "News Category",
                ["technology", "science", "business", "general"],
                disabled=not include_news
            )
        
        with col2:
            include_weather = st.checkbox("Include Weather Context")
            weather_city = st.text_input(
                "City for Weather",
                disabled=not include_weather,
                placeholder="e.g., San Francisco"
            )
        
        additional_sources = st.text_area(
            "Additional Sources/Context",
            placeholder="Paste additional information or sources here...",
            height=150
        )
        
        if st.button("Generate Research Summary", type="primary"):
            if not research_topic:
                st.warning("Please enter a research topic")
            else:
                try:
                    if not st.session_state.generator:
                        initialize_generator()
                    
                    # Get external context
                    external_context = st.session_state.api_manager.get_contextual_data(
                        city=weather_city if include_weather else None,
                        news_topic=news_cat if include_news else None
                    )
                    
                    # Generate research summary
                    with st.spinner("Generating research summary..."):
                        result = st.session_state.generator.generate_with_prompt_type(
                            prompt_type=PromptType.RESEARCH_SUMMARY,
                            topic=research_topic,
                            sources=additional_sources or "No additional sources provided",
                            external_context=st.session_state.api_manager.format_context_for_prompt(external_context)
                        )
                    
                    st.subheader("Research Summary")
                    st.write(result['content'])
                    
                except Exception as e:
                    st.error(f"Error generating research summary: {str(e)}")
                    logger.log_error(e, "Error in research assistant")
    
    # Tab 4: Data Processing
    with tab4:
        st.header("Data Processing")
        st.markdown("Upload and preprocess data files for GenAI consumption.")
        
        uploaded_file = st.file_uploader(
            "Upload File",
            type=['csv', 'txt'],
            key="data_processing_uploader"
        )
        
        if uploaded_file:
            try:
                file_path = f"data/temp_{uploaded_file.name}"
                Path("data").mkdir(exist_ok=True)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                if uploaded_file.name.endswith('.csv'):
                    df = st.session_state.data_processor.load_csv(file_path)
                    
                    st.subheader("Data Overview")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Rows", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                    with col3:
                        st.metric("Missing Values", df.isna().sum().sum())
                    with col4:
                        st.metric("Data Types", len(df.dtypes.unique()))
                    
                    st.subheader("Data Preview")
                    st.dataframe(df)
                    
                    st.subheader("Column Information")
                    st.json(df.dtypes.to_dict())
                    
                    if st.button("Preprocess Data"):
                        processed = st.session_state.data_processor.preprocess_dataframe(df)
                        st.success(f"Processed {len(processed)} records")
                        st.json(processed[:3])  # Show first 3 records
                
                elif uploaded_file.name.endswith('.txt'):
                    text = st.session_state.data_processor.load_text_file(file_path)
                    
                    st.subheader("Text Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Characters", len(text))
                    with col2:
                        st.metric("Words", len(text.split()))
                    with col3:
                        st.metric("Lines", len(text.split('\n')))
                    
                    chunk_size = st.slider("Chunk Size", 500, 2000, 1000, 100)
                    if st.button("Chunk Text"):
                        chunks = st.session_state.data_processor.chunk_text(text, chunk_size)
                        st.success(f"Created {len(chunks)} chunks")
                        for i, chunk in enumerate(chunks[:3], 1):
                            with st.expander(f"Chunk {i}"):
                                st.text(chunk[:500])
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                logger.log_error(e, "Error in data processing tab")


if __name__ == "__main__":
    main()
