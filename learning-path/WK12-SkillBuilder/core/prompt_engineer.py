"""
Custom Prompt Engineering Module
Designs and manages custom prompts for different use cases.
Demonstrates advanced prompt engineering techniques.
"""

from typing import Dict, List, Optional, Any
from enum import Enum

from core.logger import get_logger

logger = get_logger()


class PromptType(Enum):
    """Enumeration of prompt types."""
    CONTENT_GENERATION = "content_generation"
    DATA_ANALYSIS = "data_analysis"
    RESEARCH_SUMMARY = "research_summary"
    CONTEXTUAL_RESPONSE = "contextual_response"
    CREATIVE_WRITING = "creative_writing"
    IST_CONCEPT_EXPLANATION = "ist_concept_explanation"
    STUDY_PLAN_GENERATION = "study_plan_generation"
    CONCEPT_QUIZ = "concept_quiz"


class PromptEngineer:
    """
    Custom prompt engineering system with templates and dynamic generation.
    Implements various prompt engineering techniques:
    - Few-shot learning
    - Chain-of-thought prompting
    - Role-based prompting
    - Context injection
    """
    
    def __init__(self):
        """Initialize prompt engineer with base templates."""
        self.logger = logger
        self.prompt_templates: Dict[str, str] = self._initialize_templates()
        self.few_shot_examples: Dict[str, List[Dict]] = self._initialize_examples()
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize base prompt templates."""
        return {
            PromptType.CONTENT_GENERATION.value: """You are an expert content creator specializing in {domain}.
Your task is to generate high-quality, engaging content based on the following information:

CONTEXT:
{context}

DATA PROVIDED:
{data}

REQUIREMENTS:
- Content should be accurate and well-researched
- Use a {tone} tone
- Target audience: {audience}
- Length: approximately {length} words
- Include relevant examples and insights

Please generate the content following these guidelines.""",
            
            PromptType.DATA_ANALYSIS.value: """You are a data analyst with expertise in interpreting and summarizing data.

Analyze the following data and provide insights:

DATA:
{data}

ANALYSIS REQUIREMENTS:
- Identify key trends and patterns
- Highlight important statistics
- Provide actionable insights
- Note any anomalies or outliers
- Format output as structured analysis

Please provide a comprehensive analysis.""",
            
            PromptType.RESEARCH_SUMMARY.value: """You are a research assistant helping to synthesize information from multiple sources.

RESEARCH TOPIC: {topic}

SOURCES:
{sources}

EXTERNAL CONTEXT:
{external_context}

TASK:
Create a comprehensive summary that:
1. Synthesizes key findings from all sources
2. Integrates relevant external context
3. Identifies connections and patterns
4. Highlights important insights
5. Provides a clear, structured summary

Please generate the research summary.""",
            
            PromptType.CONTEXTUAL_RESPONSE.value: """You are an intelligent assistant that provides contextual, helpful responses.

USER QUERY: {query}

RELEVANT CONTEXT:
{context}

ADDITIONAL INFORMATION:
{additional_info}

INSTRUCTIONS:
- Provide a clear, accurate response
- Use the context provided to enhance your answer
- If information is missing, acknowledge it
- Maintain a helpful and professional tone

Please respond to the user's query.""",
            
            PromptType.CREATIVE_WRITING.value: """You are a creative writer with expertise in {genre}.

WRITING PROMPT: {prompt}

CONTEXT:
{context}

STYLE REQUIREMENTS:
- Genre: {genre}
- Tone: {tone}
- Target audience: {audience}
- Length: {length} words
- Include: {elements}

Please create the requested creative content.""",
            
            PromptType.IST_CONCEPT_EXPLANATION.value: """You are an expert IST402 instructor helping students understand course concepts.

CONCEPT INFORMATION:
- Concept Name: {concept_name}
- Week: {week}
- Description: {description}
- Learning Objectives: {learning_objectives}
- Prerequisites: {prerequisites}
- Difficulty Level: {difficulty}
- Estimated Time: {time_estimate} minutes
- Keywords: {keywords}

TASK:
Provide a clear, comprehensive explanation of {concept_name} that:
1. Explains the concept in simple, understandable terms
2. Covers all learning objectives listed
3. Includes relevant examples and use cases
4. Connects to prerequisite concepts (if any)
5. Relates to other IST402 concepts
6. Uses appropriate technical terminology
7. Provides practical insights for students

Format your explanation with:
- Clear introduction to the concept
- Detailed explanation covering learning objectives
- Examples and use cases
- Connections to related concepts
- Key takeaways

Please generate a detailed explanation suitable for IST402 students.""",
            
            PromptType.STUDY_PLAN_GENERATION.value: """You are an expert IST402 learning advisor creating personalized study plans.

STUDY PLAN REQUEST:
- Week(s): {weeks}
- Topic(s): {topics}
- Learning Pace: {pace}
- Difficulty Preference: {difficulty}

IST CONCEPTS DATA:
{concepts_data}

TASK:
Create a personalized study plan that:
1. Lists all concepts for the specified week(s) or topic(s)
2. Organizes concepts in logical learning order (respecting prerequisites)
3. Shows prerequisites for each concept
4. Includes time estimates for each concept
5. Indicates difficulty levels
6. Suggests review and practice activities
7. Provides a weekly/daily schedule breakdown
8. Includes tips for effective learning

Format the output as a structured study plan with:
- Overview section
- Concept list organized by learning order
- Detailed schedule with time allocations
- Prerequisites clearly marked
- Review and practice suggestions
- Learning tips

Please generate a comprehensive, personalized study plan.""",
            
            PromptType.CONCEPT_QUIZ.value: """You are an expert IST402 instructor creating interactive quiz questions to test student understanding.

CONCEPT INFORMATION:
- Concept Name: {concept_name}
- Week: {week}
- Description: {description}
- Learning Objectives: {learning_objectives}
- Prerequisites: {prerequisites}
- Difficulty Level: {difficulty}
- Keywords: {keywords}

TASK:
Create a comprehensive, interactive quiz about {concept_name} that:
1. Tests deep understanding of the core concept, not just memorization
2. Covers all learning objectives listed
3. Includes a mix of question types (multiple choice, true/false, short answer)
4. Has questions appropriate for {difficulty} difficulty level
5. Tests practical application and conceptual understanding
6. Includes clear, detailed explanations for all answers

QUIZ REQUIREMENTS:
- Number of questions: {num_questions}
- Question types: Mix of multiple choice (at least 50%), true/false, and short answer
- Difficulty: Match the concept difficulty ({difficulty})
- Multiple choice questions must have exactly 4 options (A, B, C, D)
- All questions must have clear, educational explanations

CRITICAL: You MUST return ONLY valid JSON. No markdown, no code blocks, no additional text.
The JSON format must be EXACTLY as shown below:

{{
  "questions": [
    {{
      "number": 1,
      "type": "multiple_choice",
      "question": "What is the primary purpose of tokenization in natural language processing?",
      "options": {{
        "A": "To translate text into different languages",
        "B": "To split text into smaller units called tokens for analysis",
        "C": "To enhance visual formatting of text documents",
        "D": "To store text efficiently in databases"
      }},
      "correct_answer": "B",
      "explanation": "Tokenization is the process of dividing text into smaller units, known as tokens, which can be words, subwords, or characters. This is foundational for natural language processing tasks, allowing for better analysis and understanding of the text."
    }},
    {{
      "number": 2,
      "type": "true_false",
      "question": "Byte Pair Encoding (BPE) is a method of tokenization that focuses exclusively on character-level tokenization.",
      "options": {{
        "True": true,
        "False": false
      }},
      "correct_answer": "False",
      "explanation": "Byte Pair Encoding (BPE) is a subword tokenization method that combines characters into larger units based on frequency. It is not limited to character-level tokenization; instead, it creates subword tokens that can better capture the nuances of language."
    }},
    {{
      "number": 3,
      "type": "short_answer",
      "question": "What does BPE stand for in the context of tokenization?",
      "correct_answer": "Byte Pair Encoding",
      "explanation": "BPE stands for Byte Pair Encoding, a subword tokenization technique that merges the most frequent pairs of bytes or characters to create a vocabulary of subword units."
    }}
  ]
}}

IMPORTANT RULES:
1. Return ONLY the JSON object, nothing else
2. All multiple choice questions must have exactly 4 options labeled A, B, C, D
3. Option text should be clear, distinct, and educational
4. Correct answers must match exactly (case-sensitive for short answers)
5. Explanations should be detailed and help students learn
6. Generate exactly {num_questions} questions
7. Mix question types appropriately

Now generate the quiz for {concept_name}."""
        }
    
    def _initialize_examples(self) -> Dict[str, List[Dict]]:
        """Initialize few-shot learning examples."""
        return {
            PromptType.CONTENT_GENERATION.value: [
                {
                    "input": "Product: Smartphone, Features: 5G, AI camera",
                    "output": "The latest smartphone revolutionizes mobile technology with cutting-edge 5G connectivity and an advanced AI-powered camera system..."
                }
            ],
            PromptType.DATA_ANALYSIS.value: [
                {
                    "input": "Sales data showing 20% increase",
                    "output": "Analysis reveals a significant 20% growth in sales, indicating strong market performance..."
                }
            ],
            PromptType.IST_CONCEPT_EXPLANATION.value: [
                {
                    "input": "Concept: Tokenization, Week: W00",
                    "output": "Tokenization is the process of breaking down text into smaller units called tokens..."
                }
            ],
            PromptType.STUDY_PLAN_GENERATION.value: [
                {
                    "input": "Week: W00, Pace: Moderate",
                    "output": "Study Plan for Week 0 (Core AI Concepts):\n1. Day 1-2: Tokenization (45 min)..."
                }
            ]
        }
    
    def build_prompt(self, 
                    prompt_type: PromptType,
                    context: Optional[str] = None,
                    data: Optional[str] = None,
                    **kwargs) -> str:
        """
        Build a custom prompt based on type and parameters.
        
        Args:
            prompt_type: Type of prompt to build
            context: Contextual information
            data: Data to include in prompt
            **kwargs: Additional parameters for prompt customization
            
        Returns:
            Formatted prompt string
        """
        try:
            template = self.prompt_templates.get(prompt_type.value)
            if not template:
                raise ValueError(f"Unknown prompt type: {prompt_type}")
            
            # Default parameters
            params = {
                'context': context or "No specific context provided",
                'data': data or "No data provided",
                'tone': kwargs.get('tone', 'professional'),
                'audience': kwargs.get('audience', 'general audience'),
                'length': kwargs.get('length', '500'),
                'domain': kwargs.get('domain', 'general topics'),
                'topic': kwargs.get('topic', 'general research'),
                'sources': kwargs.get('sources', 'No sources provided'),
                'external_context': kwargs.get('external_context', 'No external context'),
                'query': kwargs.get('query', ''),
                'additional_info': kwargs.get('additional_info', 'None'),
                'prompt': kwargs.get('prompt', ''),
                'genre': kwargs.get('genre', 'general'),
                'elements': kwargs.get('elements', 'standard narrative elements'),
                # IST-specific parameters
                'concept_name': kwargs.get('concept_name', ''),
                'week': kwargs.get('week', ''),
                'description': kwargs.get('description', ''),
                'learning_objectives': kwargs.get('learning_objectives', ''),
                'prerequisites': kwargs.get('prerequisites', 'None'),
                'difficulty': kwargs.get('difficulty', 'intermediate'),
                'time_estimate': kwargs.get('time_estimate', '60'),
                'keywords': kwargs.get('keywords', ''),
                'weeks': kwargs.get('weeks', ''),
                'topics': kwargs.get('topics', ''),
                'pace': kwargs.get('pace', 'moderate'),
                'concepts_data': kwargs.get('concepts_data', '')
            }
            
            # Update with provided kwargs
            params.update(kwargs)
            
            # Format template
            prompt = template.format(**params)
            
            # Add few-shot examples if available
            if prompt_type.value in self.few_shot_examples:
                examples = self.few_shot_examples[prompt_type.value]
                if examples:
                    prompt += "\n\nEXAMPLES:\n"
                    for i, example in enumerate(examples[:2], 1):  # Limit to 2 examples
                        prompt += f"\nExample {i}:\nInput: {example.get('input', '')}\nOutput: {example.get('output', '')}\n"
            
            self.logger.info(f"Built prompt of type: {prompt_type.value}, length: {len(prompt)} chars")
            return prompt
            
        except Exception as e:
            self.logger.log_error(e, f"Error building prompt of type: {prompt_type}")
            raise
    
    def add_chain_of_thought(self, prompt: str) -> str:
        """
        Add chain-of-thought reasoning to prompt.
        
        Args:
            prompt: Base prompt
            
        Returns:
            Enhanced prompt with CoT instructions
        """
        cot_instruction = """

REASONING PROCESS:
Please think through this step by step:
1. First, analyze the provided information
2. Identify key points and relationships
3. Consider the context and requirements
4. Generate your response based on this analysis
5. Review and refine your output

Let's work through this systematically."""
        
        return prompt + cot_instruction
    
    def add_role_definition(self, prompt: str, role: str, expertise: List[str]) -> str:
        """
        Add role-based context to prompt.
        
        Args:
            prompt: Base prompt
            role: Role description
            expertise: List of expertise areas
            
        Returns:
            Enhanced prompt with role definition
        """
        role_definition = f"""

ROLE DEFINITION:
You are {role} with expertise in:
{chr(10).join(f'- {exp}' for exp in expertise)}

Apply this expertise to provide the best possible response."""
        
        return prompt + role_definition
    
    def customize_for_task(self, 
                          base_prompt: str,
                          task_specific_instructions: str,
                          constraints: Optional[List[str]] = None) -> str:
        """
        Customize prompt for specific task requirements.
        
        Args:
            base_prompt: Base prompt template
            task_specific_instructions: Task-specific instructions
            constraints: List of constraints to apply
            
        Returns:
            Customized prompt
        """
        customized = base_prompt + f"\n\nTASK-SPECIFIC INSTRUCTIONS:\n{task_specific_instructions}"
        
        if constraints:
            customized += "\n\nCONSTRAINTS:\n"
            for constraint in constraints:
                customized += f"- {constraint}\n"
        
        return customized
    
    def get_prompt_stats(self, prompt: str) -> Dict[str, Any]:
        """
        Get statistics about a prompt.
        
        Args:
            prompt: Prompt string
            
        Returns:
            Dictionary with prompt statistics
        """
        return {
            'length': len(prompt),
            'word_count': len(prompt.split()),
            'has_context': 'context' in prompt.lower(),
            'has_instructions': 'instruction' in prompt.lower() or 'requirement' in prompt.lower(),
            'has_examples': 'example' in prompt.lower()
        }