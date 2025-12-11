# LangChain Integration & Content Generation

## Course Context
**Concepts:** LLM Integration, LangChain, Token Management  
**Related Weeks:** W00 (LLM Architecture), W05 (Cost Optimization)

---

## 1. What is LangChain?

LangChain is a **framework for building applications with LLMs**. It provides:

- **Standardized interfaces** for different LLM providers
- **Chains** for composing multiple operations
- **Memory** for conversation context
- **Callbacks** for monitoring and logging
- **Agents** for autonomous decision-making

### Why Use LangChain?

| Benefit | Description |
|---------|-------------|
| **Abstraction** | Same code works with OpenAI, Anthropic, etc. |
| **Composition** | Chain multiple LLM calls together |
| **Monitoring** | Built-in token tracking and callbacks |
| **Ecosystem** | Rich set of integrations and tools |

---

## 2. LangChain Setup (From the Project)

### Imports and Dependencies

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Optional: Token tracking callback
try:
    from langchain.callbacks import get_openai_callback
    HAS_CALLBACK = True
except ImportError:
    try:
        from langchain_community.callbacks import get_openai_callback
        HAS_CALLBACK = True
    except ImportError:
        HAS_CALLBACK = False
```

### Package Structure

```
langchain-core      # Base classes, message types
langchain-openai    # OpenAI-specific implementation
langchain-community # Community integrations, callbacks
langchain           # Main package (legacy callbacks)
```

---

## 3. Content Generator Class

### From the Project: `content_generator.py`

```python
class ContentGenerator:
    """
    Main content generation engine using LangChain and OpenAI.
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.7):
        """
        Initialize content generator with OpenAI model.
        
        Args:
            model_name: OpenAI model name (gpt-4, gpt-4o-mini, gpt-3.5-turbo)
            temperature: Sampling temperature (0.0-2.0)
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                openai_api_key=self.api_key
            )
        
        self.prompt_engineer = PromptEngineer()
        self.model_name = model_name
        self.temperature = temperature
```

### Key Design Decisions

1. **Graceful Degradation**: Check for API key before initialization
2. **Composition**: Includes PromptEngineer for prompt building
3. **Configuration**: Model and temperature as parameters
4. **Logging**: Uses centralized logger

---

## 4. Message Types in LangChain

### Three Core Message Types

```python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# System: Sets behavior/context for the entire conversation
system = SystemMessage(content="You are an expert IST402 instructor...")

# Human: User input
human = HumanMessage(content="Explain RAG to me")

# AI: Model response (useful for conversation history)
ai = AIMessage(content="RAG stands for Retrieval-Augmented Generation...")
```

### Message Flow

```
┌─────────────────┐
│  SystemMessage  │  "You are an expert..."
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HumanMessage   │  "Explain RAG"
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │   LLM   │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│   AIMessage     │  "RAG is..."
└─────────────────┘
```

---

## 5. Content Generation with Callbacks

### From the Project: `content_generator.py`

```python
def generate_content(self,
                    prompt: str,
                    system_message: Optional[str] = None,
                    max_tokens: int = 1000,
                    use_callback: bool = True) -> Dict[str, Any]:
    """
    Generate content using the LLM.
    """
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
        token_usage = {}
    
    content = response.content if hasattr(response, 'content') else str(response)
    
    return {
        'content': content,
        'model': self.model_name,
        'token_usage': token_usage,
        'success': True
    }
```

### Callback Context Manager

```python
with get_openai_callback() as cb:
    # All LLM calls inside this block are tracked
    response = self.llm.invoke(messages)
    
    # After the call, cb contains:
    print(cb.total_tokens)        # Total tokens used
    print(cb.prompt_tokens)       # Input tokens
    print(cb.completion_tokens)   # Output tokens
    print(cb.total_cost)          # Cost in USD
```

---

## 6. Token Usage Tracking

### Why Track Tokens?

| Reason | Description |
|--------|-------------|
| **Cost Management** | API calls cost per token |
| **Optimization** | Identify expensive prompts |
| **Debugging** | Understand model behavior |
| **Quotas** | Stay within rate limits |

### Token Breakdown

```
Prompt (Input):
┌──────────────────────────────────────────┐
│ System Message: ~50 tokens               │
│ User Prompt: ~200 tokens                 │
│ Context/Examples: ~300 tokens            │
├──────────────────────────────────────────┤
│ Total Prompt Tokens: ~550                │
└──────────────────────────────────────────┘

Completion (Output):
┌──────────────────────────────────────────┐
│ Generated Response: ~800 tokens          │
└──────────────────────────────────────────┘

Total: ~1350 tokens
Cost: $0.002 (GPT-4o-mini pricing)
```

---

## 7. Generation with Prompt Types

### From the Project: `content_generator.py`

```python
def generate_with_prompt_type(self,
                              prompt_type: PromptType,
                              context: Optional[str] = None,
                              data: Optional[str] = None,
                              system_message: Optional[str] = None,
                              **kwargs) -> Dict[str, Any]:
    """
    Generate content using a specific prompt type.
    """
    # Build custom prompt using PromptEngineer
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
```

### Usage Example

```python
# Generate concept explanation
result = generator.generate_with_prompt_type(
    prompt_type=PromptType.IST_CONCEPT_EXPLANATION,
    concept_name="RAG",
    week="W02",
    description="Retrieval-Augmented Generation...",
    learning_objectives="Understand RAG architecture...",
    prerequisites="Embeddings",
    difficulty="intermediate",
    time_estimate="90",
    keywords="RAG, retrieval, augmented generation"
)

print(result['content'])  # The explanation
print(result['token_usage'])  # Token metrics
print(result['prompt_stats'])  # Prompt analysis
```

---

## 8. External Context Integration

### From the Project: `content_generator.py`

```python
def generate_with_external_context(self,
                                  prompt: str,
                                  external_context: Dict[str, Any],
                                  system_message: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate content with external context (news, etc.).
    """
    from core.api_integration import APIIntegrationManager
    
    api_manager = APIIntegrationManager()
    context_text = api_manager.format_context_for_prompt(external_context)
    
    # Enhance prompt with external context
    enhanced_prompt = f"{prompt}\n\n{context_text}"
    
    return self.generate_content(
        prompt=enhanced_prompt,
        system_message=system_message
    )
```

### Context Enrichment Flow

```
Base Prompt                External Data              Enhanced Prompt
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│ "Explain     │          │ News API     │          │ "Explain     │
│  trends in   │    +     │ results:     │    =     │  trends in   │
│  AI..."      │          │ - Article 1  │          │  AI...       │
└──────────────┘          │ - Article 2  │          │              │
                          └──────────────┘          │ CONTEXT:     │
                                                    │ - Article 1  │
                                                    │ - Article 2  │
                                                    └──────────────┘
```

---

## 9. Batch Processing

### From the Project: `content_generator.py`

```python
def batch_generate(self,
                  prompts: List[str],
                  system_message: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Generate content for multiple prompts.
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
```

### Batch Processing Pattern

```python
# Example: Generate explanations for multiple concepts
concepts = ["RAG", "Tokenization", "Embeddings"]
prompts = [f"Explain {c} briefly" for c in concepts]

results = generator.batch_generate(prompts)

for concept, result in zip(concepts, results):
    print(f"\n{concept}:")
    print(result['content'][:200] + "...")
```

---

## 10. Model Configuration

### Available Models

| Model | Characteristics | Use Case |
|-------|-----------------|----------|
| `gpt-4o-mini` | Fast, cost-effective | Default, general tasks |
| `gpt-4` | Highest capability | Complex reasoning |
| `gpt-4o` | Multimodal, fast | Vision + text |
| `gpt-3.5-turbo` | Fast, cheapest | Simple tasks |

### Temperature Settings

```python
temperature = 0.0  # Deterministic, consistent
temperature = 0.3  # Low creativity, factual
temperature = 0.7  # Balanced (default)
temperature = 1.0  # Creative, varied
temperature = 2.0  # Maximum randomness
```

### Temperature Guidelines

| Task | Recommended Temperature |
|------|-------------------------|
| Code generation | 0.0 - 0.3 |
| Factual explanations | 0.3 - 0.5 |
| General content | 0.5 - 0.7 |
| Creative writing | 0.7 - 1.0 |
| Brainstorming | 1.0 - 1.5 |

---

## 11. Error Handling Pattern

### From the Project: `content_generator.py`

```python
def generate_content(self, prompt: str, ...) -> Dict[str, Any]:
    try:
        if not self.llm:
            raise ValueError("OpenAI API not configured...")
        
        # ... generation logic ...
        
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
```

### Error Handling Best Practices

1. **Check Prerequisites**: Verify API key, model availability
2. **Catch Specific Exceptions**: Handle different error types
3. **Return Structured Errors**: Include `success` flag and `error` message
4. **Log Errors**: Use centralized logging with context
5. **Graceful Degradation**: Return useful error messages

---

## 12. Availability Check

### From the Project: `content_generator.py`

```python
def is_available(self) -> bool:
    """
    Check if the generator is properly configured.
    """
    return self.llm is not None and self.api_key is not None
```

### Usage in UI

```python
# From app.py
if st.session_state.generator:
    if st.session_state.generator.is_available():
        st.success("✅ OpenAI API: Connected")
    else:
        st.warning("⚠️ OpenAI API: Not configured")
else:
    st.info("ℹ️ Generator not initialized")
```

---

## 13. Session State Management

### From the Project: `app.py`

```python
# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = None

# Initialize on demand
def initialize_generator():
    if st.session_state.generator is None:
        st.session_state.generator = ContentGenerator(
            model_name="gpt-4o-mini",
            temperature=0.7
        )
```

### Why Session State?

| Reason | Description |
|--------|-------------|
| **Persistence** | Survives Streamlit reruns |
| **Efficiency** | Don't recreate objects repeatedly |
| **State Sharing** | Access across tabs/components |
| **User Experience** | Maintain context throughout session |

---

## 14. Complete Generation Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────┐
│  1. Check generator availability    │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  2. Build prompt (PromptEngineer)   │
│     - Select template               │
│     - Inject parameters             │
│     - Add few-shot examples         │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  3. Build messages                  │
│     - SystemMessage (optional)      │
│     - HumanMessage (prompt)         │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  4. Invoke LLM with callback        │
│     - ChatOpenAI.invoke()           │
│     - Track token usage             │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  5. Process response                │
│     - Extract content               │
│     - Add metadata                  │
│     - Handle errors                 │
└─────────────────┬───────────────────┘
                  │
                  ▼
          Return Result
```

---

## 15. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **LangChain** | Standardizes LLM interactions across providers |
| **Message Types** | System, Human, AI messages structure conversations |
| **Callbacks** | Enable token tracking and cost monitoring |
| **Temperature** | Controls randomness vs. consistency |
| **Session State** | Maintains objects across Streamlit reruns |
| **Error Handling** | Return structured results with success flags |

---

## Related Concepts

- [Prompt Engineering](./03-prompt-engineering.md) - Building effective prompts
- [RAG Pipeline](./05-rag-pipeline.md) - Using generation with retrieval
- [Embeddings](./02-embeddings-vector-search.md) - Vector representations
