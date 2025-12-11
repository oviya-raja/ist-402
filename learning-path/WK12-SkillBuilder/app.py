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

# Fix OpenMP library conflict on macOS (required for FAISS)
# This prevents the "libomp.dylib already initialized" error
import os
os.environ.setdefault('KMP_DUPLICATE_LIB_OK', 'TRUE')

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import json
import re
from dotenv import load_dotenv

# Check for FAISS availability
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

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
if 'ist_concepts_vector_store_ready' not in st.session_state:
    st.session_state.ist_concepts_vector_store_ready = False
if 'execution_log' not in st.session_state:
    st.session_state.execution_log = {}  # Store execution logs per tab


def log_execution(tab_name: str, step: str, status: str = "⏳", details: str = "", update_display: bool = True):
    """
    Log execution step for flow tracking with live updates.
    
    Args:
        tab_name: Name of the tab
        step: Description of the step
        status: Status icon (✅, ⏳, ❌)
        details: Additional details
        update_display: Whether to update the display immediately
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if tab_name not in st.session_state.execution_log:
        st.session_state.execution_log[tab_name] = []
    
    log_entry = f"[{timestamp}] {status} {step}"
    if details:
        log_entry += f" - {details}"
    
    st.session_state.execution_log[tab_name].append(log_entry)
    # Keep only last 20 entries
    if len(st.session_state.execution_log[tab_name]) > 20:
        st.session_state.execution_log[tab_name] = st.session_state.execution_log[tab_name][-20:]
    
    # Live update the display if requested
    if update_display and f"{tab_name}_log_display" in st.session_state:
        log_placeholder = st.session_state[f"{tab_name}_log_display"]
        with log_placeholder.container():
            # Show all log entries, most recent first
            for log_entry in reversed(st.session_state.execution_log[tab_name][-15:]):
                st.markdown(f"`{log_entry}`")


def show_flow_accordion(tab_name: str, expected_flow: list):
    """
    Display flow accordion showing expected and actual execution flow.
    
    Args:
        tab_name: Name of the tab
        expected_flow: List of expected steps
    """
    with st.expander("📋 Process Flow", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expected Flow")
            for i, step in enumerate(expected_flow, 1):
                st.markdown(f"{i}. {step}")
        
        with col2:
            st.subheader("Actual Flow (Execution Log)")
            # Create a placeholder for live updates
            log_placeholder = st.empty()
            
            # Initialize log display key if not exists
            if f"{tab_name}_log_display" not in st.session_state:
                st.session_state[f"{tab_name}_log_display"] = log_placeholder
            
            # Update log display
            if tab_name in st.session_state.execution_log and st.session_state.execution_log[tab_name]:
                with log_placeholder.container():
                    # Show all log entries, most recent first
                    for log_entry in reversed(st.session_state.execution_log[tab_name][-15:]):  # Show last 15
                        st.markdown(f"`{log_entry}`")
            else:
                with log_placeholder.container():
                    st.info("No execution log yet. Actions will be logged here.")


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
    """Load IST concepts knowledge base and build vector store for semantic search."""
    try:
        if 'ist_concepts' not in st.session_state or st.session_state.ist_concepts is None:
            # Use path relative to app.py file location
            app_dir = Path(__file__).parent
            concepts_path = app_dir / "data" / "ist_concepts.csv"
            
            if concepts_path.exists():
                ist_concepts_df = st.session_state.data_processor.load_ist_concepts(
                    str(concepts_path)
                )
                st.session_state.ist_concepts = ist_concepts_df
                logger.info(f"Loaded {len(ist_concepts_df)} IST concepts")
                
                # Build vector store from IST concepts for semantic search
                if st.session_state.data_processor.embeddings_model and FAISS_AVAILABLE:
                    try:
                        # Create text chunks from concept information
                        concept_chunks = []
                        concept_metadata = []
                        
                        for idx, row in ist_concepts_df.iterrows():
                            # Combine concept information into searchable text
                            concept_text = f"""
                            Concept: {row.get('concept_name', '')}
                            Week: {row.get('week', '')}
                            Description: {row.get('description', '')}
                            Learning Objectives: {row.get('learning_objectives', '')}
                            Prerequisites: {row.get('prerequisites', 'None')}
                            Difficulty: {row.get('difficulty', '')}
                            Keywords: {row.get('keywords', '')}
                            """.strip()
                            
                            concept_chunks.append(concept_text)
                            concept_metadata.append({
                                'concept_name': row.get('concept_name', ''),
                                'week': row.get('week', ''),
                                'difficulty': row.get('difficulty', ''),
                                'chunk_id': idx
                            })
                        
                        # Build vector store
                        if concept_chunks:
                            st.session_state.data_processor.build_vector_store(
                                chunks=concept_chunks,
                                metadata=concept_metadata,
                                model="text-embedding-3-small"
                            )
                            st.session_state.ist_concepts_vector_store_ready = True
                            logger.info(f"Built vector store for {len(concept_chunks)} IST concepts")
                        else:
                            st.session_state.ist_concepts_vector_store_ready = False
                    except Exception as e:
                        logger.warning(f"Could not build vector store for IST concepts: {str(e)}")
                        st.session_state.ist_concepts_vector_store_ready = False
                else:
                    st.session_state.ist_concepts_vector_store_ready = False
                    if not st.session_state.data_processor.embeddings_model:
                        logger.warning("OpenAI API key not configured. Vector search for IST concepts unavailable.")
                    if not FAISS_AVAILABLE:
                        logger.warning("FAISS not available. Vector search for IST concepts unavailable.")
            else:
                logger.warning(f"IST concepts file not found at: {concepts_path}")
                st.warning(f"IST concepts file not found at: {concepts_path}. Some features may not work.")
                st.session_state.ist_concepts_vector_store_ready = False
        
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
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in generation (0 = deterministic, 1 = creative)"
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
            vector_status = ""
            if st.session_state.get('ist_concepts_vector_store_ready', False):
                vector_status = " (Vector Search Enabled)"
            st.success(f"✅ IST Concepts: {len(ist_concepts_df)} loaded{vector_status}")
        else:
            st.warning("⚠️ IST Concepts: Not loaded")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Concept Explainer",
        "📅 Study Plan Generator",
        "📁 Data Processing",
        "🎯 AI Conferences"
    ])
    
    # Tab 1: Concept Explainer (with Quiz Me feature)
    with tab1:
        st.header("📚 Concept Explainer & Quiz")
        st.markdown("Learn IST concepts through detailed explanations or test your knowledge with quizzes.")
        
        # Mode selector
        mode = st.radio(
            "Select Mode",
            ["Concept Explainer", "Quiz Me"],
            horizontal=True
        )
        
        # Shared concept selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if ist_concepts_df is not None:
                concept_list = ["Select a concept..."] + ist_concepts_df['concept_name'].tolist()
                selected_concept = st.selectbox(
                    "Select Concept",
                    concept_list,
                    key="concept_selector"
                )
                
                if selected_concept != "Select a concept...":
                    # Log concept selection
                    if 'last_logged_concept' not in st.session_state or st.session_state.last_logged_concept != selected_concept:
                        log_execution("Concept Explainer", f"Concept selected: {selected_concept}", "✅")
                        st.session_state.last_logged_concept = selected_concept
                    
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
                concept_name = st.text_input("Concept Name", placeholder="e.g., RAG, Tokenization", key="concept_input")
                selected_concept = concept_name
                if selected_concept:
                    # Log concept entry
                    if 'last_logged_concept' not in st.session_state or st.session_state.last_logged_concept != selected_concept:
                        log_execution("Concept Explainer", f"Concept entered: {selected_concept}", "✅")
                        st.session_state.last_logged_concept = selected_concept
        
        with col2:
            st.subheader("Options")
            if mode == "Concept Explainer":
                include_prerequisites = st.checkbox("Include Prerequisites", value=True)
                include_examples = st.checkbox("Include Examples", value=True)
            else:  # Quiz Me mode
                num_questions = st.slider("Number of Questions", 3, 10, 5)
        
        if mode == "Concept Explainer":
            # Concept Explainer Mode
            st.subheader("📖 Concept Explainer")
            
            # Flow accordion
            expected_flow = [
                "1. User selects/enters concept name",
                "2. System initializes content generator (if needed)",
                "3. System performs semantic search on IST concepts vector store",
                "4. System identifies related concepts from vector search results",
                "5. System loads concept information from database (CSV)",
                "6. System combines concept info with related concepts context",
                "7. System generates explanation using AI (OpenAI) with enhanced context",
                "8. System displays explanation with generation metadata"
            ]
            show_flow_accordion("Concept Explainer", expected_flow)
            st.divider()
            
            if st.button("Generate Explanation", type="primary"):
                if not selected_concept or selected_concept == "Select a concept...":
                    st.warning("Please select or enter a concept name")
                    log_execution("Concept Explainer", "No concept selected - action cancelled", "❌")
                else:
                    try:
                        # Create a status container for live updates
                        with st.status("🔄 Generating explanation...", expanded=True) as status:
                            # Step 1: User action logged
                            log_execution("Concept Explainer", "Generate Explanation button clicked", "⏳")
                            
                            # Step 2: Initialize generator (if needed)
                            if not st.session_state.generator:
                                status.update(label="🔄 Step 2/8: Initializing content generator...", state="running")
                                initialize_generator()
                                log_execution("Concept Explainer", "Step 2: Content generator initialized", "✅")
                            else:
                                log_execution("Concept Explainer", "Step 2: Content generator already initialized", "✅")
                            
                            # Step 3: Perform semantic search on IST concepts vector store
                            related_concepts_context = ""
                            related_concepts_list = []
                            
                            if st.session_state.get('ist_concepts_vector_store_ready', False):
                                if st.session_state.data_processor.vector_store:
                                    status.update(label="🔍 Step 3/8: Performing semantic search on IST concepts vector store...", state="running")
                                    log_execution("Concept Explainer", "Step 3: Performing semantic search on IST concepts vector store", "⏳")
                                    try:
                                        # Search for similar concepts
                                        search_results = st.session_state.data_processor.search_vectors(
                                            query=f"{selected_concept} concept explanation learning objectives",
                                            k=5,  # Get top 5 for better context
                                            model="text-embedding-3-small"
                                        )
                                        if search_results:
                                            related_concepts = []
                                            for result in search_results:
                                                concept_name = result.get('metadata', {}).get('concept_name', '')
                                                # Exclude the current concept and add related ones
                                                if concept_name and concept_name.lower() != selected_concept.lower():
                                                    related_concepts.append(concept_name)
                                            
                                            if related_concepts:
                                                # Remove duplicates while preserving order
                                                unique_concepts = list(dict.fromkeys(related_concepts))[:3]  # Top 3 unique
                                                related_concepts_list = unique_concepts
                                                related_concepts_context = f"\n\nRelated concepts found via vector search: {', '.join(unique_concepts)}"
                                                log_execution("Concept Explainer", "Step 3: Semantic search completed", "✅", f"Found {len(unique_concepts)} related concepts: {', '.join(unique_concepts)}")
                                            else:
                                                log_execution("Concept Explainer", "Step 3: Semantic search completed", "✅", "Current concept is most relevant, no additional related concepts")
                                        else:
                                            log_execution("Concept Explainer", "Step 3: Semantic search completed", "⚠️", "No search results returned")
                                    except Exception as e:
                                        log_execution("Concept Explainer", f"Step 3: Vector search error: {str(e)}", "❌")
                                        logger.log_error(e, "Error in vector search for concept explainer")
                                else:
                                    log_execution("Concept Explainer", "Step 3: Vector search skipped", "⚠️", "Vector store object not found")
                            else:
                                log_execution("Concept Explainer", "Step 3: Vector search skipped", "⚠️", f"Vector store not ready (ist_concepts_vector_store_ready={st.session_state.get('ist_concepts_vector_store_ready', False)})")
                            
                            # Step 4: Identify related concepts from vector search results
                            if related_concepts_list:
                                status.update(label="🔗 Step 4/8: Identifying related concepts from vector search...", state="running")
                                log_execution("Concept Explainer", "Step 4: Related concepts identified", "✅", f"Related concepts: {', '.join(related_concepts_list)}")
                            else:
                                log_execution("Concept Explainer", "Step 4: No additional related concepts to identify", "✅")
                            
                            # Step 5: Load concept information from database
                            status.update(label="📚 Step 5/8: Loading concept information from database...", state="running")
                            log_execution("Concept Explainer", "Step 5: Loading concept information from database", "⏳")
                            if ist_concepts_df is not None and isinstance(selected_concept, str):
                                concept_info = st.session_state.data_processor.get_concept_info(
                                    ist_concepts_df, selected_concept
                                )
                                if concept_info:
                                    log_execution("Concept Explainer", "Step 5: Concept info loaded from database", "✅", f"Week: {concept_info.get('week', 'N/A')}, Difficulty: {concept_info.get('difficulty', 'N/A')}")
                                else:
                                    log_execution("Concept Explainer", "Step 5: Concept not found in database, using basic info", "⚠️")
                                    concept_info = None
                            else:
                                concept_info = None
                                log_execution("Concept Explainer", "Step 5: No database available, using basic info", "⚠️")
                            
                            # Step 6: Combine concept info with related concepts context
                            status.update(label="🔗 Step 6/8: Combining concept info with related concepts context...", state="running")
                            log_execution("Concept Explainer", "Step 6: Combining concept info with vector search context", "⏳")
                            
                            # Prepare prompt parameters with vector search context
                            if concept_info:
                                # Use concept info from database, add vector search context
                                description = concept_info.get('description', '')
                                if related_concepts_context:
                                    description += related_concepts_context
                                
                                prompt_kwargs = {
                                    'concept_name': concept_info.get('concept_name', selected_concept),
                                    'week': concept_info.get('week', ''),
                                    'description': description,
                                    'learning_objectives': concept_info.get('learning_objectives', ''),
                                    'prerequisites': concept_info.get('prerequisites', 'None'),
                                    'difficulty': concept_info.get('difficulty', 'intermediate'),
                                    'time_estimate': concept_info.get('time_estimate', '60'),
                                    'keywords': concept_info.get('keywords', '')
                                }
                            else:
                                # Use basic info with vector search context
                                description = f"Explain the concept: {selected_concept}"
                                if related_concepts_context:
                                    description += related_concepts_context
                                
                                prompt_kwargs = {
                                    'concept_name': selected_concept,
                                    'week': '',
                                    'description': description,
                                    'learning_objectives': 'Understand the concept thoroughly',
                                    'prerequisites': 'None',
                                    'difficulty': 'intermediate',
                                    'time_estimate': '60',
                                    'keywords': ''
                                }
                            log_execution("Concept Explainer", "Step 6: Context combined successfully", "✅", f"Enhanced with {len(related_concepts_list)} related concepts" if related_concepts_list else "Using base concept info")
                            
                            # Step 7: Generate explanation using AI (OpenAI) with enhanced context
                            status.update(label="🤖 Step 7/8: Generating explanation using AI (OpenAI) with enhanced context...", state="running")
                            log_execution("Concept Explainer", "Step 7: Generating explanation using AI (OpenAI) with enhanced context", "⏳")
                            result = st.session_state.generator.generate_with_prompt_type(
                                prompt_type=PromptType.IST_CONCEPT_EXPLANATION,
                                **prompt_kwargs
                            )
                            tokens = result.get('token_usage', {}).get('total_tokens', 'N/A')
                            model = result.get('model', 'N/A')
                            log_execution("Concept Explainer", "Step 7: AI explanation generated successfully", "✅", f"Model: {model}, Tokens: {tokens}")
                            
                            # Step 8: Display explanation with metadata
                            status.update(label="📊 Step 8/8: Displaying explanation with metadata...", state="running")
                            log_execution("Concept Explainer", "Step 8: Displaying explanation with metadata", "⏳")
                            log_execution("Concept Explainer", "Step 8: Explanation displayed successfully", "✅", f"Content length: {len(result.get('content', ''))} chars")
                            status.update(label="✅ Generation complete", state="complete")
                        
                        # Display results outside status container for permanent view
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
                        log_execution("Concept Explainer", f"Error occurred: {str(e)}", "❌")
                        logger.log_error(e, "Error in concept explainer")
        
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
        
        # Flow accordion
        expected_flow = [
            "User selects week(s) or topic filter",
            "System filters IST concepts based on selection",
            "System generates personalized study plan using AI (OpenAI)",
            "System displays study plan with schedule and recommendations"
        ]
        show_flow_accordion("Study Plan Generator", expected_flow)
        st.divider()
        
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
                log_execution("Study Plan Generator", f"Generating study plan for: {weeks}", "⏳")
                
                if not st.session_state.generator:
                    initialize_generator()
                    log_execution("Study Plan Generator", "Generator initialized", "✅")
                
                if ist_concepts_df is None:
                    st.error("IST concepts not loaded. Please ensure data/ist_concepts.csv exists.")
                    log_execution("Study Plan Generator", "IST concepts not loaded", "❌")
                else:
                    # Filter concepts by week
                    if week_selection == "Single Week":
                        filtered_concepts = st.session_state.data_processor.get_concepts_by_week(
                            ist_concepts_df, weeks
                        )
                        log_execution("Study Plan Generator", f"Filtered concepts for week {weeks}", "✅", f"Found {len(filtered_concepts)} concepts")
                    else:
                        # Get range of weeks
                        start_idx = int(week_start.replace('W', ''))
                        end_idx = int(week_end.replace('W', ''))
                        filtered_concepts = ist_concepts_df[
                            ist_concepts_df['week'].str.replace('W', '').astype(int).between(start_idx, end_idx)
                        ]
                        log_execution("Study Plan Generator", f"Filtered concepts for weeks {weeks}", "✅", f"Found {len(filtered_concepts)} concepts")
                    
                    # Filter by topic if specified
                    if topic_filter:
                        filtered_concepts = filtered_concepts[
                            filtered_concepts['concept_name'].str.contains(topic_filter, case=False, na=False) |
                            filtered_concepts['keywords'].str.contains(topic_filter, case=False, na=False)
                        ]
                        log_execution("Study Plan Generator", f"Applied topic filter: {topic_filter}", "✅")
                    
                    # Prepare concepts data for prompt
                    concepts_data = filtered_concepts.to_string(index=False) if not filtered_concepts.empty else "No concepts found"
                    
                    log_execution("Study Plan Generator", "Calling OpenAI API to generate study plan", "⏳")
                    with st.spinner("Generating personalized study plan..."):
                        result = st.session_state.generator.generate_with_prompt_type(
                            prompt_type=PromptType.STUDY_PLAN_GENERATION,
                            weeks=weeks,
                            topics=topic_filter or "All topics",
                            pace=pace.lower(),
                            difficulty=difficulty.lower(),
                            concepts_data=concepts_data
                        )
                        tokens = result.get('token_usage', {}).get('total_tokens', 'N/A')
                        model = result.get('model', 'N/A')
                        log_execution("Study Plan Generator", "Study plan generated", "✅", f"Model: {model}, Tokens: {tokens}")
                    
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
    
    # Tab 3: Data Processing (with Vector Search)
    with tab3:
        st.header("📁 Data Processing & Vector Search")
        st.markdown("Upload and preprocess data files, then create embeddings and perform semantic search using FAISS vector database.")
        
        # Flow accordion
        expected_flow = [
            "User uploads file (CSV or TXT)",
            "System processes and chunks the file",
            "System creates embeddings using OpenAI",
            "System builds FAISS vector store",
            "Vector store ready for semantic search",
            "User can search uploaded documents"
        ]
        show_flow_accordion("Data Processing", expected_flow)
        st.divider()
        
        # Initialize session state for vector store
        if 'vector_store_ready' not in st.session_state:
            st.session_state.vector_store_ready = False
        if 'uploaded_chunks' not in st.session_state:
            st.session_state.uploaded_chunks = []
        if 'current_uploaded_file' not in st.session_state:
            st.session_state.current_uploaded_file = None
        
        # Vector Store Status Card
        if st.session_state.vector_store_ready and st.session_state.data_processor.vector_store:
            st.success("✅ **Vector Store Active**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("File", st.session_state.current_uploaded_file or "Unknown")
            with col2:
                st.metric("Vectors", st.session_state.data_processor.vector_store.ntotal if st.session_state.data_processor.vector_store else 0)
            with col3:
                st.metric("Chunks", len(st.session_state.uploaded_chunks))
            with col4:
                st.metric("Status", "Ready")
            
            st.info("""
            **📌 This Vector Store is Used For:**
            - 🔍 Semantic search in this tab (search uploaded documents)
            - 💾 Can be saved and loaded for reuse
            - 🔗 Can be integrated with other features (future enhancement)
            """)
            st.divider()
        
        uploaded_file = st.file_uploader(
            "Upload File",
            type=['csv', 'txt'],
            key="data_processing_uploader"
        )
        
        if uploaded_file:
            try:
                log_execution("Data Processing", f"File uploaded: {uploaded_file.name}", "✅")
                st.session_state.current_uploaded_file = uploaded_file.name
                file_path = f"data/temp_{uploaded_file.name}"
                Path("data").mkdir(exist_ok=True)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                log_execution("Data Processing", "File saved to disk", "✅")
                
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
                    
                    # For CSV, convert to text for vector search
                    st.info("💡 Tip: For vector search, convert CSV columns to text or upload a text file.")
                    if st.button("Convert to Text for Vector Search"):
                        # Combine all text columns
                        text_columns = df.select_dtypes(include=['object']).columns
                        if len(text_columns) > 0:
                            combined_text = "\n\n".join([f"{col}: {df[col].astype(str).str.cat(sep=' ')}" for col in text_columns])
                            st.session_state.uploaded_chunks = st.session_state.data_processor.chunk_text(combined_text, 1000)
                            st.success(f"Created {len(st.session_state.uploaded_chunks)} text chunks from CSV")
                        else:
                            st.warning("No text columns found in CSV for vector search.")
                
                elif uploaded_file.name.endswith('.txt'):
                    log_execution("Data Processing", "Loading text file", "⏳")
                    text = st.session_state.data_processor.load_text_file(file_path)
                    log_execution("Data Processing", f"Text loaded: {len(text)} characters", "✅")
                    
                    st.subheader("Text Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Characters", len(text))
                    with col2:
                        st.metric("Words", len(text.split()))
                    with col3:
                        st.metric("Lines", len(text.split('\n')))
                    
                    st.divider()
                    st.subheader("📝 Text Chunking")
                    chunk_size = st.slider("Chunk Size", 500, 2000, 1000, 100)
                    if st.button("Chunk Text"):
                        log_execution("Data Processing", f"Chunking text with size {chunk_size}", "⏳")
                        chunks = st.session_state.data_processor.chunk_text(text, chunk_size)
                        st.session_state.uploaded_chunks = chunks
                        log_execution("Data Processing", f"Created {len(chunks)} chunks", "✅")
                        st.success(f"Created {len(chunks)} chunks")
                        for i, chunk in enumerate(chunks[:3], 1):
                            with st.expander(f"Chunk {i} (Preview)"):
                                st.text(chunk[:500])
                    
                    # Vector Store Creation
                    if st.session_state.uploaded_chunks:
                        st.divider()
                        st.subheader("🔍 Vector Search Setup")
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            embedding_model = st.selectbox(
                                "Embedding Model",
                                ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"],
                                help="OpenAI embedding model to use"
                            )
                        with col2:
                            st.metric("Chunks Ready", len(st.session_state.uploaded_chunks))
                        
                        if st.button("🔨 Build Vector Store", type="primary"):
                            try:
                                if not st.session_state.data_processor.embeddings_model:
                                    st.error("❌ OpenAI API key not configured. Please set OPENAI_API_KEY in .env file.")
                                    log_execution("Data Processing", "OpenAI API key not configured", "❌")
                                else:
                                    log_execution("Data Processing", f"Creating embeddings for {len(st.session_state.uploaded_chunks)} chunks using {embedding_model}", "⏳")
                                    with st.spinner(f"Creating embeddings for {len(st.session_state.uploaded_chunks)} chunks..."):
                                        # Create metadata for chunks
                                        metadata = [{"chunk_id": i, "file": uploaded_file.name} for i in range(len(st.session_state.uploaded_chunks))]
                                        
                                        st.session_state.data_processor.build_vector_store(
                                            chunks=st.session_state.uploaded_chunks,
                                            metadata=metadata,
                                            model=embedding_model
                                        )
                                        st.session_state.vector_store_ready = True
                                        num_vectors = st.session_state.data_processor.vector_store.ntotal if st.session_state.data_processor.vector_store else 0
                                        log_execution("Data Processing", f"Vector store built successfully", "✅", f"{num_vectors} vectors created")
                                        st.success(f"✅ Vector store created with {num_vectors} vectors!")
                                        st.balloons()  # Celebration!
                            except Exception as e:
                                st.error(f"Error building vector store: {str(e)}")
                                log_execution("Data Processing", f"Error building vector store: {str(e)}", "❌")
                                logger.log_error(e, "Error building vector store")
                        
                        # Vector Search
                        if st.session_state.vector_store_ready:
                            st.divider()
                            st.subheader("🔎 Semantic Search")
                            
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                search_query = st.text_input(
                                    "Search Query",
                                    placeholder="Enter your search query...",
                                    key="vector_search_query"
                                )
                            with col2:
                                num_results = st.number_input("Results", min_value=1, max_value=20, value=5, step=1)
                            
                            if st.button("🔍 Search", type="primary") and search_query:
                                try:
                                    log_execution("Data Processing", f"Searching for: '{search_query}'", "⏳")
                                    with st.spinner("Searching vector store..."):
                                        results = st.session_state.data_processor.search_vectors(
                                            query=search_query,
                                            k=num_results,
                                            model=embedding_model
                                        )
                                        log_execution("Data Processing", f"Search completed", "✅", f"Found {len(results)} results")
                                    
                                    st.subheader(f"📊 Search Results ({len(results)} found)")
                                    
                                    for result in results:
                                        with st.expander(f"Result #{result['rank']} (Similarity: {result['similarity']:.2%})"):
                                            st.markdown(f"**Similarity Score:** {result['similarity']:.2%}")
                                            st.markdown(f"**Distance:** {result['score']:.4f}")
                                            st.markdown("**Content:**")
                                            st.text(result['chunk'])
                                            if result['metadata']:
                                                st.markdown("**Metadata:**")
                                                st.json(result['metadata'])
                                    
                                    # Show summary
                                    st.info(f"Found {len(results)} most similar chunks for: '{search_query}'")
                                    
                                except Exception as e:
                                    st.error(f"Error searching: {str(e)}")
                                    logger.log_error(e, "Error in vector search")
                            
                            # Save/Load Vector Store
                            st.divider()
                            st.subheader("💾 Vector Store Management")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("💾 Save Vector Store"):
                                    try:
                                        save_path = f"data/vector_store_{uploaded_file.name.replace('.txt', '')}.pkl"
                                        st.session_state.data_processor.save_vector_store(save_path)
                                        st.success(f"Vector store saved to {save_path}")
                                    except Exception as e:
                                        st.error(f"Error saving: {str(e)}")
                            
                            with col2:
                                load_file = st.file_uploader(
                                    "Load Vector Store",
                                    type=['pkl'],
                                    key="load_vector_store"
                                )
                                if load_file and st.button("📂 Load Vector Store"):
                                    try:
                                        load_path = f"data/temp_{load_file.name}"
                                        with open(load_path, "wb") as f:
                                            f.write(load_file.getbuffer())
                                        st.session_state.data_processor.load_vector_store(load_path)
                                        st.session_state.vector_store_ready = True
                                        st.success("Vector store loaded successfully!")
                                    except Exception as e:
                                        st.error(f"Error loading: {str(e)}")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                logger.log_error(e, "Error in data processing tab")
    
    # Tab 4: AI Conferences
    with tab4:
        st.header("🎯 AI Conferences")
        st.markdown("Discover AI-related conferences and events happening around the world.")
        
        # Flow accordion
        expected_flow = [
            "User requests AI conferences",
            "System searches web using OpenAI web search",
            "System parses conference information (title, date, location, URL)",
            "System displays AI-related conferences with details"
        ]
        show_flow_accordion("AI Conferences", expected_flow)
        st.divider()
        
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
                log_execution("AI Conferences", f"Searching for AI conferences (limit: {limit})", "⏳")
                with st.spinner("Searching for AI conferences using OpenAI web search..."):
                    conferences_data = st.session_state.api_manager.get_ai_conferences(
                        category=category,
                        limit=limit
                    )
                    num_conferences = conferences_data.get('total_results', 0)
                    log_execution("AI Conferences", f"Conferences retrieved", "✅", f"Found {num_conferences} conferences")
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