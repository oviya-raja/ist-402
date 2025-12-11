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

## 2. LangChain Setup

### Package Structure

```
langchain-core      # Base classes, message types
langchain-openai    # OpenAI-specific implementation
langchain-community # Community integrations, callbacks
langchain           # Main package (legacy callbacks)
```

### Key Design Decisions

1. **Graceful Degradation**: Check for API key before initialization
2. **Composition**: Includes PromptEngineer for prompt building
3. **Configuration**: Model and temperature as parameters
4. **Logging**: Uses centralized logger

---

## 3. Message Types in LangChain

### Three Core Message Types

**SystemMessage**: Sets behavior/context for the entire conversation
- Example: "You are an expert IST402 instructor..."

**HumanMessage**: User input
- Example: "Explain RAG to me"

**AIMessage**: Model response (useful for conversation history)
- Example: "RAG stands for Retrieval-Augmented Generation..."

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

## 4. Content Generation with Callbacks

### Token Tracking Process

1. **Wrap LLM Call**: Use callback context manager
2. **Track Usage**: Monitor tokens during generation
3. **Extract Metrics**: Get total, prompt, completion tokens
4. **Calculate Cost**: Determine API cost based on usage

### Callback Context Manager Flow

```
Start Generation
    │
    ▼
┌─────────────────┐
│  Enter Callback │
│  Context        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Invoke LLM     │
│  (tracked)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract Metrics│
│  • Total tokens │
│  • Prompt tokens│
│  • Completion   │
│  • Cost         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Exit Callback  │
│  Context        │
└─────────────────┘
```

---

## 5. Token Usage Tracking

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

## 6. Generation with Prompt Types

### Generation Flow

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

## 7. External Context Integration

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

## 8. Model Configuration

### Available Models

| Model | Characteristics | Use Case |
|-------|-----------------|----------|
| `gpt-4o-mini` | Fast, cost-effective | Default, general tasks |
| `gpt-4` | Highest capability | Complex reasoning |
| `gpt-4o` | Multimodal, fast | Vision + text |
| `gpt-3.5-turbo` | Fast, cheapest | Simple tasks |

### Temperature Settings

```
temperature = 0.0  # Deterministic, consistent
temperature = 0.3  # Low creativity, factual
temperature = 0.7  # Balanced (default)
temperature = 1.0  # Creative, varied
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

## 9. Error Handling Pattern

### Error Handling Best Practices

1. **Check Prerequisites**: Verify API key, model availability
2. **Catch Specific Exceptions**: Handle different error types
3. **Return Structured Errors**: Include `success` flag and `error` message
4. **Log Errors**: Use centralized logging with context
5. **Graceful Degradation**: Return useful error messages

### Error Handling Flow

```
Generation Request
    │
    ▼
┌─────────────────┐
│ Check Prereqs   │
│ • API key?      │
│ • Model ready?  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Generate│ │ Return Error │
│         │ │ with message │
└────┬────┘ └──────────────┘
     │
     │
     ▼
┌─────────────────┐
│ Handle Result   │
│ • Success       │
│ • Error         │
└─────────────────┘
```

---

## 10. Availability Checking Pattern

### Availability Check Flow

```
Check Generator
    │
    ▼
┌─────────────────┐
│ Is LLM Ready?   │
│ • client exists?│
│ • API key set?  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│Available│ │ Not Available│
│         │ │ Show warning │
└─────────┘ └──────────────┘
```

---

## 11. Session State Management

### Why Session State?

| Reason | Description |
|--------|-------------|
| **Persistence** | Survives Streamlit reruns |
| **Efficiency** | Don't recreate objects repeatedly |
| **State Sharing** | Access across tabs/components |
| **User Experience** | Maintain context throughout session |

### Session State Flow

```
App Start
    │
    ▼
┌─────────────────┐
│ Initialize      │
│ generator = None│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Action     │
│ (button click)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check State     │
│ generator?      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
  None      Exists
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Create │ │ Reuse  │
│ New    │ │ Existing│
└────────┘ └────────┘
```

---

## 12. Key Takeaways

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
