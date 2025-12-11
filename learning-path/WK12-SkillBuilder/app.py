"""
Skill Builder for IST Students
Main Streamlit Web Application

A GenAI-driven application that helps IST402 students with:
- IST concept explanations
- Personalized study plan generation
- Data analysis
- Research assistance
- AI conferences information
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
# Use absolute path relative to app.py location
app_dir = Path(__file__).parent.absolute()
env_path = app_dir / ".env"

# Try loading .env file with override to ensure latest values are used
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    # Fallback: try current directory (Streamlit might run from different dir)
    load_dotenv(override=True)

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
    page_title="Skill Builder for IST Students",
    page_icon="🎓",
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
if 'ist_concepts' not in st.session_state:
    st.session_state.ist_concepts = None


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


def load_ist_concepts():
    """Load IST concepts knowledge base."""
    try:
        if st.session_state.ist_concepts is None:
            # Use path relative to app.py file location
            app_dir = Path(__file__).parent
            concepts_path = app_dir / "data" / "ist_concepts.csv"
            
            if concepts_path.exists():
                st.session_state.ist_concepts = st.session_state.data_processor.load_ist_concepts(
                    str(concepts_path)
                )
                logger.info(f"Loaded {len(st.session_state.ist_concepts)} IST concepts")
            else:
                logger.warning(f"IST concepts file not found at: {concepts_path}")
                st.warning(f"IST concepts file not found at: {concepts_path}. Some features may not work.")
        return st.session_state.ist_concepts
    except Exception as e:
        logger.log_error(e, "Error loading IST concepts")
        st.error(f"Error loading IST concepts: {str(e)}")
        return None


def main():
    """Main application function."""
    st.title("🎓 Skill Builder for IST Students")
    st.markdown("""
    A GenAI-driven application designed to help IST402 students learn course concepts, 
    create personalized study plans, analyze data, and stay updated with AI conferences.
    """)
    
    # Load IST concepts
    ist_concepts_df = load_ist_concepts()
    
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
        
        # EventRegistry status (required for news API)
        if st.session_state.api_manager.is_eventregistry_available():
            st.success("✅ EventRegistry: Connected")
        else:
            st.error("❌ EventRegistry: Not configured - Set EVENTREGISTRY_API_KEY in .env")
            st.caption("⚠️ Required for news API functionality")
        
        if ist_concepts_df is not None:
            st.success(f"✅ IST Concepts: {len(ist_concepts_df)} loaded")
        else:
            st.warning("⚠️ IST Concepts: Not loaded")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Content Generation",
        "📊 Data Analysis",
        "🔍 Research Assistant",
        "📁 Data Processing",
        "🎯 AI Conferences"
    ])
    
    # Tab 1: Content Generation (Enhanced with IST Concept Explanation)
    with tab1:
        st.header("Content Generation")
        st.markdown("Generate content or get IST concept explanations using AI.")
        
        # Mode selector
        mode = st.radio(
            "Select Mode",
            ["General Content", "IST Concept Explanation"],
            horizontal=True
        )
        
        if mode == "IST Concept Explanation":
            # IST Concept Explanation Mode
            st.subheader("IST Concept Explanation")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if ist_concepts_df is not None:
                    concept_list = ["Select a concept..."] + ist_concepts_df['concept_name'].tolist()
                    selected_concept = st.selectbox(
                        "Select Concept",
                        concept_list
                    )
                    
                    if selected_concept != "Select a concept...":
                        concept_info = st.session_state.data_processor.get_concept_info(
                            ist_concepts_df, selected_concept
                        )
                        
                        if concept_info:
                            st.info(f"""
                            **Week:** {concept_info.get('week', 'N/A')}  
                            **Difficulty:** {concept_info.get('difficulty', 'N/A')}  
                            **Time Estimate:** {concept_info.get('time_estimate', 'N/A')} minutes  
                            **Prerequisites:** {concept_info.get('prerequisites', 'None')}
                            """)
                else:
                    concept_name = st.text_input("Concept Name", placeholder="e.g., RAG, Tokenization")
                    selected_concept = concept_name
            
            with col2:
                st.subheader("Options")
                include_prerequisites = st.checkbox("Include Prerequisites", value=True)
                include_examples = st.checkbox("Include Examples", value=True)
            
            if st.button("Generate Concept Explanation", type="primary"):
                if not selected_concept or selected_concept == "Select a concept...":
                    st.warning("Please select or enter a concept name")
                else:
                    try:
                        if not st.session_state.generator:
                            initialize_generator()
                        
                        # Get concept information
                        if ist_concepts_df is not None and isinstance(selected_concept, str):
                            concept_info = st.session_state.data_processor.get_concept_info(
                                ist_concepts_df, selected_concept
                            )
                        else:
                            concept_info = None
                        
                        if concept_info:
                            # Use concept info from database
                            prompt_kwargs = {
                                'concept_name': concept_info.get('concept_name', selected_concept),
                                'week': concept_info.get('week', ''),
                                'description': concept_info.get('description', ''),
                                'learning_objectives': concept_info.get('learning_objectives', ''),
                                'prerequisites': concept_info.get('prerequisites', 'None'),
                                'difficulty': concept_info.get('difficulty', 'intermediate'),
                                'time_estimate': concept_info.get('time_estimate', '60'),
                                'keywords': concept_info.get('keywords', '')
                            }
                        else:
                            # Use basic info
                            prompt_kwargs = {
                                'concept_name': selected_concept,
                                'week': '',
                                'description': f"Explain the concept: {selected_concept}",
                                'learning_objectives': 'Understand the concept thoroughly',
                                'prerequisites': 'None',
                                'difficulty': 'intermediate',
                                'time_estimate': '60',
                                'keywords': ''
                            }
                        
                        with st.spinner("Generating concept explanation..."):
                            result = st.session_state.generator.generate_with_prompt_type(
                                prompt_type=PromptType.IST_CONCEPT_EXPLANATION,
                                **prompt_kwargs
                            )
                        
                        st.subheader("Concept Explanation")
                        st.markdown(result['content'])
                        
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
                        st.error(f"Error generating explanation: {str(e)}")
                        logger.log_error(e, "Error in IST concept explanation")
        
        else:
            # General Content Generation Mode
            st.subheader("General Content Generation")
            
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
                        if not st.session_state.generator:
                            initialize_generator()
                        
                        # Get external context if requested
                        external_context = {}
                        if use_news:
                            try:
                                external_context = st.session_state.api_manager.get_contextual_data(
                                    news_topic=news_category
                                )
                            except Exception as e:
                                st.error(f"❌ Failed to fetch news: {str(e)}")
                                st.info("💡 Please configure EVENTREGISTRY_API_KEY in your .env file")
                                external_context = {}
                        
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
    
    # Tab 2: Data Analysis (Enhanced with Study Plan Generator)
    with tab2:
        st.header("Data Analysis")
        st.markdown("Analyze data or generate personalized study plans.")
        
        # Mode selector
        mode = st.radio(
            "Select Mode",
            ["Data Analysis", "Study Plan Generator"],
            horizontal=True
        )
        
        if mode == "Study Plan Generator":
            # Study Plan Generator Mode
            st.subheader("Study Plan Generator")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                week_selection = st.selectbox(
                    "Select Week(s)",
                    ["Single Week", "Week Range"],
                    help="Choose to generate plan for one week or a range"
                )
                
                if week_selection == "Single Week":
                    weeks = st.selectbox(
                        "Week",
                        ["W00", "W01", "W02", "W03", "W04", "W05", "W06", "W07", "W08", "W09", "W10", "W11"]
                    )
                else:
                    col_start, col_end = st.columns(2)
                    with col_start:
                        week_start = st.selectbox("Start Week", ["W00", "W01", "W02", "W03", "W04", "W05", "W06", "W07", "W08", "W09", "W10", "W11"])
                    with col_end:
                        week_end = st.selectbox("End Week", ["W00", "W01", "W02", "W03", "W04", "W05", "W06", "W07", "W08", "W09", "W10", "W11"])
                    weeks = f"{week_start} to {week_end}"
            
            with col2:
                pace = st.selectbox(
                    "Learning Pace",
                    ["Slow", "Moderate", "Fast"],
                    index=1,
                    help="Your preferred learning pace"
                )
                
                difficulty = st.selectbox(
                    "Difficulty Preference",
                    ["Beginner", "Intermediate", "Advanced", "All Levels"],
                    help="Focus on concepts of this difficulty level"
                )
            
            topic_filter = st.text_input(
                "Topic Filter (Optional)",
                placeholder="e.g., RAG, Fine-tuning (leave empty for all topics)"
            )
            
            if st.button("Generate Study Plan", type="primary"):
                try:
                    if not st.session_state.generator:
                        initialize_generator()
                    
                    if ist_concepts_df is None:
                        st.error("IST concepts not loaded. Please ensure data/ist_concepts.csv exists.")
                    else:
                        # Filter concepts by week
                        if week_selection == "Single Week":
                            filtered_concepts = st.session_state.data_processor.get_concepts_by_week(
                                ist_concepts_df, weeks
                            )
                        else:
                            # Get range of weeks
                            start_idx = int(week_start.replace('W', ''))
                            end_idx = int(week_end.replace('W', ''))
                            filtered_concepts = ist_concepts_df[
                                ist_concepts_df['week'].str.replace('W', '').astype(int).between(start_idx, end_idx)
                            ]
                        
                        # Filter by topic if specified
                        if topic_filter:
                            filtered_concepts = filtered_concepts[
                                filtered_concepts['concept_name'].str.contains(topic_filter, case=False, na=False) |
                                filtered_concepts['keywords'].str.contains(topic_filter, case=False, na=False)
                            ]
                        
                        # Prepare concepts data for prompt
                        concepts_data = filtered_concepts.to_string(index=False) if not filtered_concepts.empty else "No concepts found"
                        
                        with st.spinner("Generating personalized study plan..."):
                            result = st.session_state.generator.generate_with_prompt_type(
                                prompt_type=PromptType.STUDY_PLAN_GENERATION,
                                weeks=weeks,
                                topics=topic_filter or "All topics",
                                pace=pace.lower(),
                                difficulty=difficulty.lower(),
                                concepts_data=concepts_data
                            )
                        
                        st.subheader("Your Personalized Study Plan")
                        st.markdown(result['content'])
                        
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
                    st.error(f"Error generating study plan: {str(e)}")
                    logger.log_error(e, "Error in study plan generation")
        
        else:
            # Data Analysis Mode
            st.subheader("Data Analysis")
            
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
                        st.text_area("Content", text_content[:500] + "...", height=200, disabled=True)
                        
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
    
    # Tab 3: Research Assistant (Retained)
    with tab3:
        st.header("Research Assistant")
        st.markdown("Synthesize information from multiple sources with external context.")
        
        research_topic = st.text_input("Research Topic", placeholder="Enter research topic...")
        
        include_news = st.checkbox("Include Recent News")
        news_cat = st.selectbox(
            "News Category",
            ["technology", "science", "business", "general"],
            disabled=not include_news
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
                    external_context = {}
                    if include_news:
                        try:
                            external_context = st.session_state.api_manager.get_contextual_data(
                                news_topic=news_cat
                            )
                        except Exception as e:
                            st.error(f"❌ Failed to fetch news: {str(e)}")
                            st.info("💡 Please configure EVENTREGISTRY_API_KEY in your .env file")
                            external_context = {}
                    
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
    
    # Tab 4: Data Processing (Retained)
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
    
    # Tab 5: AI Conferences (NEW)
    with tab5:
        st.header("🎯 AI Conferences")
        st.markdown("Discover AI-related conferences and events happening around the world.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            category = st.selectbox(
                "Category",
                ["technology", "science", "business", "general"],
                index=0,
                help="News category to search for conferences"
            )
        
        with col2:
            limit = st.number_input(
                "Max Results",
                min_value=5,
                max_value=20,
                value=10,
                step=1
            )
        
        if st.button("🔍 Fetch AI Conferences", type="primary"):
            try:
                with st.spinner("Fetching AI conferences from EventRegistry..."):
                    conferences_data = st.session_state.api_manager.get_ai_conferences(
                        category=category,
                        limit=limit
                    )
            except Exception as e:
                st.error(f"❌ Failed to fetch conferences: {str(e)}")
                st.info("💡 Please configure EVENTREGISTRY_API_KEY in your .env file and ensure the eventregistry package is installed")
                st.stop()
            
            if conferences_data.get('conferences'):
                st.success(f"Found {conferences_data.get('total_results', 0)} AI-related conferences")
                
                st.subheader("Conferences")
                
                for i, conf in enumerate(conferences_data['conferences'], 1):
                    with st.expander(f"📅 {conf.get('title', 'Untitled Conference')}", expanded=(i == 1)):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Description:** {conf.get('description', 'No description available')}")
                            
                            if conf.get('extracted_date'):
                                st.markdown(f"**📆 Date:** {conf['extracted_date']}")
                            
                            if conf.get('extracted_location'):
                                st.markdown(f"**📍 Location:** {conf['extracted_location']}")
                            
                            if conf.get('type'):
                                st.markdown(f"**Type:** {conf['type'].title()}")
                            
                            if conf.get('source'):
                                st.markdown(f"**Source:** {conf['source']}")
                        
                        with col2:
                            if conf.get('url'):
                                st.markdown(f"[🔗 Read More]({conf['url']})")
                            
                            if conf.get('published_at'):
                                st.caption(f"Published: {conf['published_at'][:10]}")
                
                # Summary statistics
                with st.expander("📊 Conference Statistics"):
                    conf_types = {}
                    for conf in conferences_data['conferences']:
                        conf_type = conf.get('type', 'unknown')
                        conf_types[conf_type] = conf_types.get(conf_type, 0) + 1
                    
                    st.write("**Conference Types:**")
                    for conf_type, count in conf_types.items():
                        st.write(f"- {conf_type.title()}: {count}")
            else:
                st.info("No AI-related conferences found. Try a different category or check back later.")


if __name__ == "__main__":
    main()