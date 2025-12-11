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

Please create the requested creative content."""
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
                'elements': kwargs.get('elements', 'standard narrative elements')
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
