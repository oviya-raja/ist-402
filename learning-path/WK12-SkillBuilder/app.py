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
import json
import re
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
        
        # OpenAI Web Search status (required for news and conferences API)
        if st.session_state.api_manager.is_openai_web_search_available():
            st.success("✅ OpenAI Web Search: Connected")
        else:
            st.error("❌ OpenAI Web Search: Not configured - Set OPENAI_API_KEY in .env")
            st.caption("⚠️ Required for news and AI conferences functionality")
        
        if ist_concepts_df is not None:
            st.success(f"✅ IST Concepts: {len(ist_concepts_df)} loaded")
        else:
            st.warning("⚠️ IST Concepts: Not loaded")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Topic Explanation",
        "📅 Study Plan Generator",
        "🔍 Research Assistant",
        "📁 Data Processing",
        "🎯 AI Conferences"
    ])
    
    # Tab 1: Topic Explanation (with Quiz Me feature)
    with tab1:
        st.header("📚 Topic Explanation & Quiz")
        st.markdown("Learn IST concepts through detailed explanations or test your knowledge with quizzes.")
        
        # Mode selector
        mode = st.radio(
            "Select Mode",
            ["Topic Explanation", "Quiz Me"],
            horizontal=True
        )
        
        # Shared concept selection
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
            if mode == "Topic Explanation":
                include_prerequisites = st.checkbox("Include Prerequisites", value=True)
                include_examples = st.checkbox("Include Examples", value=True)
            else:  # Quiz Me mode
                num_questions = st.slider("Number of Questions", 3, 10, 5)
        
        if mode == "Topic Explanation":
            # Topic Explanation Mode
            st.subheader("📖 Topic Explanation")
            
            if st.button("Generate Explanation", type="primary"):
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
                        logger.log_error(e, "Error in topic explanation")
        
        else:  # Quiz Me mode
            st.subheader("🎯 Quiz Me")
            
            # Initialize quiz state
            if 'quiz_questions' not in st.session_state:
                st.session_state.quiz_questions = None
            if 'quiz_answers' not in st.session_state:
                st.session_state.quiz_answers = {}
            if 'quiz_submitted' not in st.session_state:
                st.session_state.quiz_submitted = False
            
            def parse_quiz_json(content):
                """Parse quiz JSON from AI response."""
                # Try to extract JSON from the response
                # Look for JSON code blocks first
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
                else:
                    # Try to find JSON object directly
                    json_match = re.search(r'\{.*"questions".*\}', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(0)
                
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract manually
                    logger.warning("Failed to parse JSON, attempting manual extraction")
                    return None
            
            if st.button("Generate Quiz", type="primary"):
                if not selected_concept or selected_concept == "Select a concept...":
                    st.warning("Please select or enter a concept name")
                else:
                    try:
                        if not st.session_state.generator:
                            initialize_generator()
                        
                        # Reset quiz state
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        
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
                                'keywords': concept_info.get('keywords', ''),
                                'num_questions': num_questions
                            }
                        else:
                            # Use basic info
                            prompt_kwargs = {
                                'concept_name': selected_concept,
                                'week': '',
                                'description': f"Quiz on the concept: {selected_concept}",
                                'learning_objectives': 'Test understanding of the concept',
                                'prerequisites': 'None',
                                'difficulty': 'intermediate',
                                'keywords': '',
                                'num_questions': num_questions
                            }
                        
                        with st.spinner(f"Generating {num_questions} quiz questions..."):
                            result = st.session_state.generator.generate_with_prompt_type(
                                prompt_type=PromptType.CONCEPT_QUIZ,
                                **prompt_kwargs
                            )
                        
                        # Parse quiz JSON
                        quiz_data = parse_quiz_json(result['content'])
                        
                        if quiz_data and 'questions' in quiz_data:
                            st.session_state.quiz_questions = quiz_data['questions']
                            st.success(f"✅ Quiz generated with {len(quiz_data['questions'])} questions!")
                        else:
                            st.error("Failed to parse quiz. Please try again.")
                            logger.error(f"Failed to parse quiz JSON: {result['content'][:200]}")
                    
                    except Exception as e:
                        st.error(f"Error generating quiz: {str(e)}")
                        logger.log_error(e, "Error in quiz generation")
            
            # Display interactive quiz
            if st.session_state.quiz_questions:
                st.divider()
                st.subheader(f"Quiz: {selected_concept}")
                
                # Display questions for user to answer
                for idx, question in enumerate(st.session_state.quiz_questions):
                    q_num = question.get('number', idx + 1)
                    q_type = question.get('type', 'multiple_choice')
                    q_text = question.get('question', '')
                    
                    st.markdown(f"**Question {q_num}:** {q_text}")
                    
                    # Get user answer based on question type
                    if q_type == 'multiple_choice':
                        options = question.get('options', {})
                        if options:
                            answer_key = f"q_{q_num}"
                            if answer_key not in st.session_state.quiz_answers:
                                st.session_state.quiz_answers[answer_key] = None
                            
                            # Format options to show both letter and text: "A) Option text"
                            formatted_options = []
                            option_mapping = {}
                            for key, value in options.items():
                                formatted_text = f"{key}) {value}"
                                formatted_options.append(formatted_text)
                                option_mapping[formatted_text] = key
                            
                            # Get current selection index
                            current_answer = st.session_state.quiz_answers.get(answer_key)
                            selected_index = None
                            if current_answer and current_answer in options:
                                for idx, formatted_text in enumerate(formatted_options):
                                    if option_mapping[formatted_text] == current_answer:
                                        selected_index = idx
                                        break
                            
                            selected = st.radio(
                                "Select your answer:",
                                options=formatted_options,
                                key=f"answer_{q_num}",
                                index=selected_index
                            )
                            # Store just the letter (A, B, C, D) as the answer
                            if selected:
                                st.session_state.quiz_answers[answer_key] = option_mapping[selected]
                    
                    elif q_type == 'true_false':
                        answer_key = f"q_{q_num}"
                        if answer_key not in st.session_state.quiz_answers:
                            st.session_state.quiz_answers[answer_key] = None
                        
                        selected = st.radio(
                            "Select your answer:",
                            options=["True", "False"],
                            key=f"answer_{q_num}",
                            index=None if st.session_state.quiz_answers.get(answer_key) is None else ["True", "False"].index(st.session_state.quiz_answers.get(answer_key)) if st.session_state.quiz_answers.get(answer_key) in ["True", "False"] else None
                        )
                        st.session_state.quiz_answers[answer_key] = selected
                    
                    elif q_type == 'short_answer':
                        answer_key = f"q_{q_num}"
                        if answer_key not in st.session_state.quiz_answers:
                            st.session_state.quiz_answers[answer_key] = ""
                        
                        user_answer = st.text_input(
                            "Your answer:",
                            key=f"answer_{q_num}",
                            value=st.session_state.quiz_answers.get(answer_key, "")
                        )
                        st.session_state.quiz_answers[answer_key] = user_answer
                    
                    st.divider()
                
                # Submit button
                if st.button("Submit Answers", type="primary"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
                
                # Show results after submission
                if st.session_state.quiz_submitted:
                    st.divider()
                    st.subheader("📊 Quiz Results")
                    
                    correct_count = 0
                    total_questions = len(st.session_state.quiz_questions)
                    
                    for idx, question in enumerate(st.session_state.quiz_questions):
                        q_num = question.get('number', idx + 1)
                        q_type = question.get('type', 'multiple_choice')
                        correct_answer = question.get('correct_answer', '')
                        explanation = question.get('explanation', '')
                        answer_key = f"q_{q_num}"
                        user_answer = st.session_state.quiz_answers.get(answer_key, '')
                        
                        # Check if answer is correct
                        is_correct = False
                        if q_type == 'short_answer':
                            # For short answer, do case-insensitive comparison
                            is_correct = user_answer.strip().lower() == correct_answer.lower()
                        else:
                            is_correct = str(user_answer).strip() == str(correct_answer).strip()
                        
                        if is_correct:
                            correct_count += 1
                        
                        # Display result
                        st.markdown(f"**Question {q_num}:** {question.get('question', '')}")
                        
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if is_correct:
                                st.success(f"✅ Correct!")
                            else:
                                st.error(f"❌ Incorrect")
                        
                        with col2:
                            # Format answer display for multiple choice
                            if q_type == 'multiple_choice':
                                options = question.get('options', {})
                                user_display = f"{user_answer}) {options.get(user_answer, '')}" if user_answer and user_answer in options else (user_answer if user_answer else '(No answer provided)')
                                correct_display = f"{correct_answer}) {options.get(correct_answer, '')}" if correct_answer in options else correct_answer
                            else:
                                user_display = user_answer if user_answer else '(No answer provided)'
                                correct_display = correct_answer
                            
                            st.markdown(f"**Your Answer:** {user_display}")
                            st.markdown(f"**Correct Answer:** {correct_display}")
                        
                        st.info(f"**Explanation:** {explanation}")
                        st.divider()
                    
                    # Show score
                    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
                    st.metric("Score", f"{correct_count}/{total_questions} ({score_percentage:.1f}%)")
                    
                    if score_percentage == 100:
                        st.success("🎉 Perfect score! Excellent work!")
                    elif score_percentage >= 70:
                        st.success("👍 Good job! You're on the right track.")
                    else:
                        st.warning("💪 Keep practicing! Review the explanations above.")
    
    # Tab 2: Study Plan Generator
    with tab2:
        st.header("📅 Study Plan Generator")
        st.markdown("Generate personalized study plans by week or topic to help you master IST402 concepts.")
        
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
                            st.info("💡 Please configure OPENAI_API_KEY in your .env file")
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
                with st.spinner("Searching for AI conferences using OpenAI web search..."):
                    conferences_data = st.session_state.api_manager.get_ai_conferences(
                        category=category,
                        limit=limit
                    )
            except Exception as e:
                st.error(f"❌ Failed to fetch conferences: {str(e)}")
                st.info("💡 Please configure OPENAI_API_KEY in your .env file")
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