# ============================================================================
# OBJECTIVE 1: DESIGN SYSTEM PROMPTS FOR LLM-BASED CUSTOMER SERVICE
# ============================================================================
#
# LEARNING OBJECTIVES DEMONSTRATED:
#   1. System Prompt Engineering - Crafting prompts that shape LLM behavior
#   2. Modular Design - SOLID, KISS, DRY principles in practice
#
# THEORETICAL BACKGROUND:
#   System prompts serve as the "constitution" for LLM behavior, establishing:
#   - Role Identity: Who the model should act as
#   - Knowledge Boundaries: What the model knows and doesn't know
#   - Behavioral Constraints: Response style, escalation rules
#   - Domain Context: Business-specific information
#
# ============================================================================

import os
from typing import Optional, Tuple

# Import ObjectiveSupport for DRY (optional - graceful fallback)
try:
    from objective_support import ObjectiveSupport
    _support = ObjectiveSupport()
except ImportError:
    # Fallback if not available (for notebook extraction)
    _support = None

# ============================================================================
# InferenceEngine Class - Model Loading, Generation & Verification
# ============================================================================
class InferenceEngine:
    """
    Handles all model inference operations: loading, generation, and verification.
    Reusable across all objectives - follows Single Responsibility Principle.
    Uses env from Objective 0 - no duplicate code!
    
    Usage:
        engine = InferenceEngine(env)
        tokenizer, model = engine.load_model("mistralai/Mistral-7B-Instruct-v0.3")
        response = engine.generate_response(tokenizer, model, prompt)
    """
    
    def __init__(self, env):
        """
        Initialize with environment config from Objective 0.
        
        Args:
            env: EnvironmentConfig instance from Objective 0
        """
        self.env = env
        
        # Use libraries from env (no duplicate imports!)
        self.torch = env.torch
        self.AutoTokenizer = env.AutoTokenizer
        self.AutoModelForCausalLM = env.AutoModelForCausalLM
        
        # Model cache (keyed by model name)
        self._model_cache = {}
        self._tokenizer_cache = {}
    
    def load_model(
        self,
        model_name: str,
        force_reload: bool = False,
        use_cache: bool = True
    ) -> Tuple:
        """
        Load model with caching support.
        Uses env from Objective 0 - automatically handles GPU/CPU!
        
        Args:
            model_name: Hugging Face model identifier
            force_reload: Force reload even if cached
            use_cache: Use global cache (for sharing across objectives)
            
        Returns:
            Tuple of (tokenizer, model)
        """
        # Check instance cache first (fastest - instant return)
        if not force_reload and model_name in self._model_cache:
            print(f"⚡ Using cached model from instance cache: {model_name}")
            return self._tokenizer_cache[model_name], self._model_cache[model_name]
        
        # Check global cache (for sharing across objectives)
        if use_cache and not force_reload:
            global_key_tokenizer = f"{model_name}_tokenizer"
            global_key_model = f"{model_name}_model"
            
            if global_key_tokenizer in globals() and global_key_model in globals():
                tokenizer = globals()[global_key_tokenizer]
                model = globals()[global_key_model]
                
                # Store in instance cache for faster access next time
                self._tokenizer_cache[model_name] = tokenizer
                self._model_cache[model_name] = model
                
                print(f"⚡ Using cached model from global cache: {model_name}")
                return tokenizer, model
        
        print(f"Loading {model_name}...")
        
        try:
            # Use env libraries - works in both Colab and local!
            tokenizer = self.AutoTokenizer.from_pretrained(model_name)
            model = self.AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=self.torch.float16 if self.env.has_gpu else self.torch.float32,
                device_map="auto" if self.env.has_gpu else None,
                low_cpu_mem_usage=True
            )
            
            # Use env.device - no if statement needed!
            if not self.env.has_gpu:
                model = model.to(self.env.device)
            
            # Store in caches
            self._tokenizer_cache[model_name] = tokenizer
            self._model_cache[model_name] = model
            
            # Store in globals for sharing across objectives
            if use_cache:
                globals()[f"{model_name}_tokenizer"] = tokenizer
                globals()[f"{model_name}_model"] = model
            
            device_display = 'GPU' if self.env.has_gpu else 'CPU'
            print(f"✅ Model loaded on {device_display}")
            
            return tokenizer, model
            
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_name}: {e}")
    
    def generate_response(
        self,
        tokenizer,
        model,
        formatted_prompt: str,
        max_new_tokens: int = 200,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Generate model response.
        Uses env from Objective 0 - no if statements needed!
        
        Args:
            tokenizer: Model tokenizer
            model: Loaded model instance
            formatted_prompt: Formatted prompt string
            max_new_tokens: Max tokens to generate
            temperature: Sampling temperature (0=deterministic, 1=creative)
            top_p: Nucleus sampling threshold
            
        Returns:
            str: Generated response
            
        Raises:
            RuntimeError: If generation fails
        """
        try:
            inputs = tokenizer(formatted_prompt, return_tensors="pt")
            
            # Use env.has_gpu - no if statement needed!
            if self.env.has_gpu:
                inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            with self.torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=top_p,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decode only new tokens
            input_length = inputs['input_ids'].shape[1]
            generated_tokens = outputs[0][input_length:]
            response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            
            return response
            
        except self.torch.cuda.OutOfMemoryError:
            raise RuntimeError("GPU out of memory. Try reducing max_new_tokens or use CPU.")
        except Exception as e:
            raise RuntimeError(f"Generation failed: {e}")
    
    def verify_model(self, tokenizer, model) -> bool:
        """
        Verify model is loaded and ready for inference.
        
        Args:
            tokenizer: Model tokenizer to verify
            model: Model instance to verify
            
        Returns:
            bool: True if model is ready, False otherwise
        """
        errors = []
        
        if not tokenizer:
            errors.append("❌ Tokenizer not loaded")
        if not model:
            errors.append("❌ Model not loaded")
        
        if errors:
            print("❌ Model verification failed:", "\n".join(errors))
            return False
        
        device_display = 'GPU' if self.env.has_gpu else 'CPU'
        print(f"✅ Model verified - Loaded on {device_display}")
        return True
    
    def get_device_info(self) -> dict:
        """Get device information using env."""
        return self.env.get_device_info()
    
    def clear_cache(self, model_name: str = None):
        """
        Clear model cache.
        
        Args:
            model_name: Specific model to clear, or None to clear all
        """
        if model_name:
            self._model_cache.pop(model_name, None)
            self._tokenizer_cache.pop(model_name, None)
        else:
            self._model_cache.clear()
            self._tokenizer_cache.clear()


# ============================================================================
# SystemPromptEngineer Class - Centralized Objective 1 Logic
# ============================================================================
class SystemPromptEngineer:
    """
    System prompt engineering for Objective 1.
    Focuses ONLY on prompt creation, formatting, and file I/O.
    Uses env from Objective 0 - no duplicate code, no if statements needed!
    
    Usage:
        engineer = SystemPromptEngineer(env)
        prompt = engineer.create_system_prompt()
        formatted = engineer.format_prompt(prompt, question)
    """
    
    # Configuration constants
    MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
    MAX_NEW_TOKENS = 200
    TEMPERATURE = 0.7
    TOP_P = 0.9
    OUTPUT_DIR = "data/system_prompt_engineering"
    
    def __init__(self, env, support=None):
        """
        Initialize with environment config.
        
        Args:
            env: EnvironmentConfig instance from Objective 0
            support: Optional ObjectiveSupport instance for DRY patterns
        """
        self.env = env
        self.support = support
        self.system_prompt = None
    
    def create_system_prompt(
        self,
        business_name: str = "GreenTech Marketplace",
        business_type: str = "e-commerce",
        support_email: str = "support@greentechmarketplace.com",
        support_phone: str = "1-800-GREEN-TECH"
    ) -> str:
        """
        Create optimized customer service system prompt.
        
        Prompt Engineering Best Practices:
        1. Role Definition: Clear, specific identity
        2. Task Boundaries: Explicit scope
        3. Knowledge Base: Comprehensive domain info
        4. Behavioral Rules: Tone and style guidelines
        5. Edge Case Handling: Unknown information handling
        6. Output Format: Response structure expectations
        
        Args:
            business_name: Company name
            business_type: Type of business
            support_email: Support email
            support_phone: Support phone
            
        Returns:
            str: Formatted system prompt
        """
        prompt = f"""You are a friendly and knowledgeable customer service assistant for {business_name}, a leading {business_type} platform specializing in sustainable technology products.

## YOUR ROLE
You are the first point of contact for customers. Your expertise includes product information, orders, shipping, returns, and general inquiries. You embody the company's commitment to sustainability and excellent service.

## KNOWLEDGE BASE

**Products:**
- Solar panels, energy-efficient appliances, smart home devices, eco-friendly accessories
- Warranty: 1-3 years depending on product category

**Shipping:**
- Standard: 5-7 business days (free over $75)
- Express: 2-3 business days (additional fee)

**Returns & Refunds:**
- 30-day return policy for unopened items in original packaging
- Refunds processed within 5-7 business days after receipt

**Customer Service Hours:**
- Monday-Friday: 9 AM - 6 PM EST
- Saturday: 10 AM - 4 PM EST
- Closed Sunday

**Contact Methods:**
- Email: {support_email}
- Phone: {support_phone}
- Live chat: Available during business hours in EST 

## COMMUNICATION GUIDELINES

**Tone:** Warm, professional, solution-oriented
**Style:** Clear, concise, helpful

**Always:**
- Greet customers warmly
- Acknowledge their concerns before providing solutions
- Provide specific, actionable information
- Include relevant timeframes and next steps
- Thank them for choosing {business_name}

**Never:**
- Make promises you cannot keep
- Provide information not in your knowledge base
- Use technical jargon without explanation

## HANDLING LIMITATIONS

If you don't know the answer:
1. Acknowledge the question honestly
2. Explain that the information is not in your current knowledge base
3. Offer to connect them with a specialist or provide contact information
4. Suggest alternative resources if available

## RESPONSE FORMAT

Keep responses concise but complete. Structure longer responses with clear sections. Always end with an offer to help further."""
        
        self.system_prompt = prompt
        return prompt
    
    def format_prompt(self, system_prompt: str, user_input: str) -> str:
        """
        Format for Mistral Instruct template.
        
        Template: <s>[INST] {system} {user} [/INST]
        
        Args:
            system_prompt: System prompt
            user_input: User question
            
        Returns:
            str: Formatted prompt
        """
        return f"<s>[INST] {system_prompt} {user_input} [/INST]"
    @staticmethod
    def format_template(prompt_template: str, **kwargs) -> str:
        """
        Format prompt template using Mistral Instruct format.
        General utility for formatting any prompt template.
        
        Handles two cases:
        1. Template with placeholders: format_template(template, **kwargs)
        2. Already-formatted string: format_template(formatted_string)
        
        Args:
            prompt_template: Prompt template string (may contain {placeholders}) or already-formatted string
            **kwargs: Format arguments for template (optional)
            
        Returns:
            Formatted prompt string wrapped in Mistral Instruct format
        
        Example:
            template = "Generate {num} items about {topic}"
            formatted = SystemPromptEngineer.format_template(template, num=3, topic="shipping")
            # Returns: "<s>[INST] Generate 3 items about shipping [/INST]"
            
            # Or with already-formatted string:
            formatted = SystemPromptEngineer.format_template("Generate 3 items about shipping")
            # Returns: "<s>[INST] Generate 3 items about shipping [/INST]"
        """
        # Bulletproof implementation: Never call .format() if kwargs is empty
        # This prevents KeyError when string contains JSON braces like {"question": "..."}
        if not kwargs or len(kwargs) == 0:
            # No kwargs - string is already formatted, just wrap in Mistral format
            # Do NOT call .format() - it will try to interpret { braces } as placeholders
            return f"<s>[INST] {prompt_template} [/INST]"
        
        # kwargs provided - try to format, but catch KeyError if string already formatted
        try:
            formatted = prompt_template.format(**kwargs)
        except KeyError:
            # String already formatted or has unmatched braces, use as-is
            formatted = prompt_template
        return f"<s>[INST] {formatted} [/INST]"
    def save_system_prompt(self, filename: str = "system_prompt.txt") -> str:
        """Save system prompt to file."""
        if not self.system_prompt:
            raise ValueError("No system prompt created. Call create_system_prompt() first.")
        
        # Use ObjectiveSupport if available (DRY)
        if self.support:
            self.OUTPUT_DIR = self.support.setup_output_dir(self.OUTPUT_DIR)
        else:
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(self.system_prompt)
        print(f"✅ Saved: {filepath}")
        return filepath
    
    def save_response(self, response: str, question: str, filename: str = "test_response.txt") -> str:
        """Save generated response to file."""
        # Use ObjectiveSupport if available (DRY)
        if self.support:
            self.OUTPUT_DIR = self.support.setup_output_dir(self.OUTPUT_DIR)
        else:
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(self.OUTPUT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(f"Question: {question}\n\n")
            f.write(f"Response:\n{response}")
        print(f"✅ Saved: {filepath}")
        return filepath
    
    def verify_prompt(self) -> bool:
        """
        Verify prompt engineering components only.
        Follows SRP - only verifies SystemPromptEngineer responsibilities.
        
        Returns:
            bool: True if prompt engineering is complete
        """
        errors = []
        
        # Verify system prompt
        if not self.system_prompt:
            errors.append("❌ System prompt not created")
        elif len(self.system_prompt) < 100:
            errors.append(f"❌ System prompt too short ({len(self.system_prompt)} chars)")
        
        # Check files exist
        prompt_file = os.path.join(self.OUTPUT_DIR, "system_prompt.txt")
        response_file = os.path.join(self.OUTPUT_DIR, "test_response.txt")
        
        if not os.path.exists(prompt_file):
            errors.append("❌ system_prompt.txt not found")
        if not os.path.exists(response_file):
            errors.append("❌ test_response.txt not found")
        
        # Print results
        if errors:
            print("❌ Prompt verification failed:", "\n".join(errors))
            return False
        
        print(f"✅ Prompt verified - Length: {len(self.system_prompt)} chars")
        return True
    



# ============================================================================
# EXECUTION - Uses env from Objective 0, wrapped with timing
# ============================================================================

# Verify prerequisites using ObjectiveSupport (DRY)
if _support:
    _support.ensure_prerequisites({
        'env': 'Objective 0 (Prerequisites & Setup)'
    }, globals())
else:
    # Fallback to manual checking if ObjectiveSupport not available
    if 'env' not in globals():
        raise RuntimeError("❌ 'env' not found! Please run Objective 0 (Prerequisites & Setup) first.")

# ============================================================================
# EXECUTION - Orchestrates Objective 1 workflow
# ============================================================================
# Class provides capabilities, execution orchestrates the workflow
# This follows better separation of concerns!

with env.timer.objective(ObjectiveNames.OBJECTIVE_1):
    print("Objective 1: Creating System Prompt\n")
    
    # Reuse InferenceEngine from globals if available (performance optimization!)
    if 'inference_engine' in globals() and isinstance(globals()['inference_engine'], InferenceEngine):
        inference_engine = globals()['inference_engine']
        print("♻️  Reusing existing InferenceEngine (model cache preserved)\n")
    else:
        # Create InferenceEngine (can be shared across objectives for efficiency)
        inference_engine = InferenceEngine(env)
    
    # Create SystemPromptEngineer instance (prompt engineering only)
    # Pass _support for DRY output directory setup
    system_prompt_engineer = SystemPromptEngineer(env, support=_support)
    
    # Authenticate using env from Objective 0
    if env.hf_token:
        env.authenticate_hf()
    
    # Load model using InferenceEngine (model operation)
    tokenizer, model = inference_engine.load_model(system_prompt_engineer.MODEL_NAME)
    
    # Create system prompt (prompt engineering operation)
    system_prompt = system_prompt_engineer.create_system_prompt()
    globals()['system_prompt'] = system_prompt
    print(f"✅ System prompt created ({len(system_prompt)} chars)\n")
    
    # Test with sample question
    test_question = "What are your store hours and how can I contact customer support?"
    formatted_prompt = system_prompt_engineer.format_prompt(system_prompt, test_question)
    
    # Generate response using InferenceEngine (model operation)
    generated_response = inference_engine.generate_response(
        tokenizer, model, formatted_prompt,
        max_new_tokens=system_prompt_engineer.MAX_NEW_TOKENS,
        temperature=system_prompt_engineer.TEMPERATURE,
        top_p=system_prompt_engineer.TOP_P
    )
    
    print("Sample Response:")
    print("-" * 50)
    print(generated_response)
    print("-" * 50)
    
    # Save files (prompt engineering operation)
    system_prompt_engineer.save_system_prompt()
    system_prompt_engineer.save_response(generated_response, test_question)
    
    # Verify both components separately (SRP: each verifies its own responsibility)
    inference_engine.verify_model(tokenizer, model)
    system_prompt_engineer.verify_prompt()
    
    print(f"\n✅ Objective 1 complete - Model on {'GPU' if env.has_gpu else 'CPU'}, Prompt: {len(system_prompt)} chars")
    
    # Store in globals for other objectives
    globals()['InferenceEngine'] = InferenceEngine
    globals()['SystemPromptEngineer'] = SystemPromptEngineer
    globals()['system_prompt'] = system_prompt
    globals()['inference_engine'] = inference_engine  # Reusable across objectives!
