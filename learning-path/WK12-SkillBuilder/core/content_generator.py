"""
GenAI Model Integration Module
Integrates with OpenAI and LangChain for content generation.
"""

import os
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Try to import callback for token tracking (optional)
try:
    from langchain.callbacks import get_openai_callback
    HAS_CALLBACK = True
except ImportError:
    try:
        from langchain_community.callbacks import get_openai_callback
        HAS_CALLBACK = True
    except ImportError:
        HAS_CALLBACK = False
        # Create a dummy callback context manager
        class DummyCallback:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            @property
            def total_tokens(self):
                return None
            @property
            def prompt_tokens(self):
                return None
            @property
            def completion_tokens(self):
                return None
            @property
            def total_cost(self):
                return None
        get_openai_callback = lambda: DummyCallback()

from core.logger import get_logger
from core.prompt_engineer import PromptEngineer, PromptType

logger = get_logger()


class ContentGenerator:
    """
    Main content generation engine using LangChain and OpenAI.
    Handles model initialization, prompt execution, and response generation.
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.7):
        """
        Initialize content generator with OpenAI model.
        
        Args:
            model_name: OpenAI model name (gpt-4, gpt-4o-mini, gpt-3.5-turbo)
            temperature: Sampling temperature (0.0-2.0)
        """
        self.logger = logger
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            self.logger.error("OPENAI_API_KEY not configured. Content generation will fail.")
            self.llm = None
        else:
            try:
                self.llm = ChatOpenAI(
                    model_name=model_name,
                    temperature=temperature,
                    openai_api_key=self.api_key
                )
                self.logger.info(f"Initialized OpenAI model: {model_name}")
            except Exception as e:
                self.logger.log_error(e, f"Error initializing OpenAI model: {model_name}")
                self.llm = None
        
        self.prompt_engineer = PromptEngineer()
        self.model_name = model_name
        self.temperature = temperature
    
    def generate_content(self,
                        prompt: str,
                        system_message: Optional[str] = None,
                        max_tokens: int = 1000,
                        use_callback: bool = True) -> Dict[str, Any]:
        """
        Generate content using the LLM.
        
        Args:
            prompt: User prompt
            system_message: Optional system message for context
            max_tokens: Maximum tokens in response
            use_callback: Whether to track token usage
            
        Returns:
            Dictionary with generated content and metadata
        """
        try:
            if not self.llm:
                error_msg = "OpenAI API not configured. Please set OPENAI_API_KEY environment variable."
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Build messages
            messages = []
            if system_message:
                messages.append(SystemMessage(content=system_message))
            messages.append(HumanMessage(content=prompt))
            
            # Generate with callback for token tracking
            if use_callback:
                with get_openai_callback() as cb:
                    response = self.llm.invoke(messages)
                    token_usage = {
                        'total_tokens': cb.total_tokens,
                        'prompt_tokens': cb.prompt_tokens,
                        'completion_tokens': cb.completion_tokens,
                        'total_cost': cb.total_cost
                    }
            else:
                response = self.llm.invoke(messages)
                token_usage = {
                    'total_tokens': None,
                    'prompt_tokens': None,
                    'completion_tokens': None,
                    'total_cost': None
                }
            
            content = response.content if hasattr(response, 'content') else str(response)
            
            self.logger.info(f"Generated content: {len(content)} characters")
            if token_usage['total_tokens']:
                self.logger.info(f"Token usage: {token_usage['total_tokens']} tokens")
            
            return {
                'content': content,
                'model': self.model_name,
                'token_usage': token_usage,
                'success': True
            }
            
        except Exception as e:
            self.logger.log_error(e, "Error generating content")
            return {
                'content': f"Error generating content: {str(e)}",
                'model': self.model_name,
                'token_usage': {},
                'success': False,
                'error': str(e)
            }
    
    def generate_with_prompt_type(self,
                                  prompt_type: PromptType,
                                  context: Optional[str] = None,
                                  data: Optional[str] = None,
                                  system_message: Optional[str] = None,
                                  **kwargs) -> Dict[str, Any]:
        """
        Generate content using a specific prompt type.
        
        Args:
            prompt_type: Type of prompt to use
            context: Contextual information
            data: Data to include
            system_message: Optional system message
            **kwargs: Additional prompt parameters
            
        Returns:
            Dictionary with generated content
        """
        try:
            # Build custom prompt
            prompt = self.prompt_engineer.build_prompt(
                prompt_type=prompt_type,
                context=context,
                data=data,
                **kwargs
            )
            
            # Generate content
            result = self.generate_content(
                prompt=prompt,
                system_message=system_message
            )
            
            # Add prompt metadata
            result['prompt_type'] = prompt_type.value
            result['prompt_stats'] = self.prompt_engineer.get_prompt_stats(prompt)
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, f"Error generating content with prompt type: {prompt_type}")
            return {
                'content': f"Error: {str(e)}",
                'success': False,
                'error': str(e)
            }
    
    def generate_with_external_context(self,
                                      prompt: str,
                                      external_context: Dict[str, Any],
                                      system_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate content with external context (news, etc.).
        
        Args:
            prompt: Base prompt
            external_context: External context data
            system_message: Optional system message
            
        Returns:
            Dictionary with generated content
        """
        try:
            from core.api_integration import APIIntegrationManager
            
            api_manager = APIIntegrationManager()
            context_text = api_manager.format_context_for_prompt(external_context)
            
            # Enhance prompt with external context
            enhanced_prompt = f"{prompt}\n\n{context_text}"
            
            return self.generate_content(
                prompt=enhanced_prompt,
                system_message=system_message
            )
            
        except Exception as e:
            self.logger.log_error(e, "Error generating content with external context")
            return {
                'content': f"Error: {str(e)}",
                'success': False,
                'error': str(e)
            }
    
    def batch_generate(self,
                      prompts: List[str],
                      system_message: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate content for multiple prompts.
        
        Args:
            prompts: List of prompts
            system_message: Optional system message for all prompts
            
        Returns:
            List of generation results
        """
        results = []
        for i, prompt in enumerate(prompts, 1):
            self.logger.info(f"Processing prompt {i}/{len(prompts)}")
            result = self.generate_content(
                prompt=prompt,
                system_message=system_message
            )
            results.append(result)
        return results
    
    
    def is_available(self) -> bool:
        """
        Check if the generator is properly configured.
        
        Returns:
            True if API key is set and model is initialized
        """
        return self.llm is not None and self.api_key is not None