# Prompt Engineering Patterns & Techniques

## Course Context
**Concepts:** Prompt Engineering, Few-Shot Learning, Chain-of-Thought  
**Related Weeks:** W01 (Prompt Engineering)

---

## 1. What is Prompt Engineering?

Prompt engineering is the art of **designing effective inputs** to get desired outputs from LLMs. It's about communicating intent clearly and structurally.

### Why It Matters

```
Poor Prompt:     "Tell me about RAG"
Better Prompt:   "Explain RAG (Retrieval-Augmented Generation) for a 
                  student learning about AI. Include: definition, 
                  components, and a practical example."
```

---

## 2. Prompt Types (From the Project)

### Enum-Based Organization

```python
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
```

### Benefits of Enum-Based Design

| Benefit | Description |
|---------|-------------|
| **Type Safety** | IDE autocomplete, prevents typos |
| **Extensibility** | Add new types without breaking code |
| **Organization** | Clear categorization of prompts |
| **Maintainability** | Single source of truth for prompt types |

---

## 3. Prompt Template Structure

### IST Concept Explanation Template

```python
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

Please generate a detailed explanation suitable for IST402 students."""
```

### Anatomy of a Good Template

```
┌──────────────────────────────────────────┐
│  1. ROLE DEFINITION                      │
│     "You are an expert IST402 instructor"│
├──────────────────────────────────────────┤
│  2. CONTEXT INJECTION                    │
│     {concept_name}, {description}, etc.  │
├──────────────────────────────────────────┤
│  3. TASK SPECIFICATION                   │
│     Clear numbered requirements          │
├──────────────────────────────────────────┤
│  4. OUTPUT FORMAT                        │
│     How to structure the response        │
├──────────────────────────────────────────┤
│  5. AUDIENCE CONTEXT                     │
│     "suitable for IST402 students"       │
└──────────────────────────────────────────┘
```

---

## 4. Dynamic Prompt Building

### From the Project: `prompt_engineer.py`

```python
def build_prompt(self, 
                prompt_type: PromptType,
                context: Optional[str] = None,
                data: Optional[str] = None,
                **kwargs) -> str:
    """
    Build a custom prompt based on type and parameters.
    """
    # Get template
    template = self.prompt_templates.get(prompt_type.value)
    if not template:
        raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    # Default parameters with fallbacks
    params = {
        'context': context or "No specific context provided",
        'data': data or "No data provided",
        'tone': kwargs.get('tone', 'professional'),
        'audience': kwargs.get('audience', 'general audience'),
        'length': kwargs.get('length', '500'),
        # ... more defaults
    }
    
    # Override with provided kwargs
    params.update(kwargs)
    
    # Format template with parameters
    prompt = template.format(**params)
    
    # Add few-shot examples if available
    if prompt_type.value in self.few_shot_examples:
        examples = self.few_shot_examples[prompt_type.value]
        if examples:
            prompt += "\n\nEXAMPLES:\n"
            for i, example in enumerate(examples[:2], 1):
                prompt += f"\nExample {i}:\nInput: {example.get('input', '')}\nOutput: {example.get('output', '')}\n"
    
    return prompt
```

### Parameter Flow

```
User Input                  Default Values           Final Prompt
┌────────────┐             ┌────────────┐           ┌────────────┐
│concept_name│────────────►│            │           │            │
│week        │             │ tone:      │           │  Merged    │
│description │             │ professional│──merge──►│  Prompt    │
└────────────┘             │ length: 500│           │            │
                           │ ...        │           └────────────┘
                           └────────────┘
```

---

## 5. Few-Shot Learning

### What is Few-Shot Learning?

Providing examples in the prompt to guide the model's output format and style.

### From the Project: Example Structure

```python
def _initialize_examples(self) -> Dict[str, List[Dict]]:
    """Initialize few-shot learning examples."""
    return {
        PromptType.CONTENT_GENERATION.value: [
            {
                "input": "Product: Smartphone, Features: 5G, AI camera",
                "output": "The latest smartphone revolutionizes mobile technology 
                          with cutting-edge 5G connectivity and an advanced 
                          AI-powered camera system..."
            }
        ],
        PromptType.IST_CONCEPT_EXPLANATION.value: [
            {
                "input": "Concept: Tokenization, Week: W00",
                "output": "Tokenization is the process of breaking down text 
                          into smaller units called tokens..."
            }
        ],
        # ... more examples
    }
```

### Few-Shot Pattern

```
PROMPT:
Here are examples of how to respond:

Example 1:
Input: [sample input]
Output: [desired output format]

Example 2:
Input: [sample input]
Output: [desired output format]

Now, given this input: [actual input]
Generate the output:
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **Format Guidance** | Model learns expected structure |
| **Tone Matching** | Consistent voice across outputs |
| **Quality Bar** | Sets expectation for response quality |
| **Reduced Ambiguity** | Concrete examples > abstract instructions |

---

## 6. Chain-of-Thought (CoT) Prompting

### From the Project: `prompt_engineer.py`

```python
def add_chain_of_thought(self, prompt: str) -> str:
    """
    Add chain-of-thought reasoning to prompt.
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
```

### Why CoT Works

```
Without CoT:
Q: What is 17 * 24?
A: 408  (might be wrong)

With CoT:
Q: What is 17 * 24? Think step by step.
A: Let me break this down:
   17 * 24 = 17 * (20 + 4)
           = 17 * 20 + 17 * 4
           = 340 + 68
           = 408  ✓ (reasoning visible, verifiable)
```

### When to Use CoT

| Use Case | CoT Helpful? |
|----------|--------------|
| Simple factual questions | ❌ No |
| Complex reasoning | ✅ Yes |
| Multi-step problems | ✅ Yes |
| Analysis tasks | ✅ Yes |
| Creative writing | ⚠️ Sometimes |

---

## 7. Role-Based Prompting

### From the Project: `prompt_engineer.py`

```python
def add_role_definition(self, prompt: str, role: str, expertise: List[str]) -> str:
    """
    Add role-based context to prompt.
    """
    role_definition = f"""

ROLE DEFINITION:
You are {role} with expertise in:
{chr(10).join(f'- {exp}' for exp in expertise)}

Apply this expertise to provide the best possible response."""
    
    return prompt + role_definition
```

### Role Definition Pattern

```python
# Example usage:
prompt = prompt_engineer.add_role_definition(
    base_prompt,
    role="a senior data scientist",
    expertise=[
        "Machine Learning algorithms",
        "Statistical analysis",
        "Python and R programming",
        "Data visualization"
    ]
)
```

### Effective Roles

| Role | Best For |
|------|----------|
| "Expert instructor" | Educational content |
| "Technical writer" | Documentation |
| "Data analyst" | Analysis tasks |
| "Creative writer" | Storytelling |
| "Code reviewer" | Code analysis |

---

## 8. Structured Output: JSON Generation

### Quiz Generation Template (From Project)

```python
PromptType.CONCEPT_QUIZ.value: """...

CRITICAL: You MUST return ONLY valid JSON. No markdown, no code blocks, no additional text.
The JSON format must be EXACTLY as shown below:

{{
  "questions": [
    {{
      "number": 1,
      "type": "multiple_choice",
      "question": "What is the primary purpose of tokenization...",
      "options": {{
        "A": "To translate text into different languages",
        "B": "To split text into smaller units called tokens",
        "C": "To enhance visual formatting",
        "D": "To store text efficiently"
      }},
      "correct_answer": "B",
      "explanation": "Tokenization is the process of dividing text..."
    }}
  ]
}}

IMPORTANT RULES:
1. Return ONLY the JSON object, nothing else
2. All multiple choice questions must have exactly 4 options labeled A, B, C, D
3. Option text should be clear, distinct, and educational
..."""
```

### Key Techniques for JSON Output

1. **Explicit Format Requirement**: "MUST return ONLY valid JSON"
2. **Template Example**: Show exact expected structure
3. **Escape Braces**: Use `{{` and `}}` in f-strings
4. **Validation Rules**: Numbered list of constraints
5. **No Markdown**: Explicitly forbid code blocks

### Parsing Strategy

```python
def parse_quiz_json(content):
    """Parse quiz JSON from AI response."""
    # Try to extract JSON from response
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    else:
        # Try to find JSON object directly
        json_match = re.search(r'\{.*"questions".*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
    
    return json.loads(content)
```

---

## 9. Prompt Statistics & Monitoring

### From the Project: `prompt_engineer.py`

```python
def get_prompt_stats(self, prompt: str) -> Dict[str, Any]:
    """
    Get statistics about a prompt.
    """
    return {
        'length': len(prompt),
        'word_count': len(prompt.split()),
        'has_context': 'context' in prompt.lower(),
        'has_instructions': 'instruction' in prompt.lower() or 'requirement' in prompt.lower(),
        'has_examples': 'example' in prompt.lower()
    }
```

### Why Track Prompt Stats?

| Metric | Purpose |
|--------|---------|
| **Length** | Token cost estimation |
| **Word Count** | Complexity indicator |
| **Has Context** | Verify context injection |
| **Has Instructions** | Task clarity check |
| **Has Examples** | Few-shot verification |

---

## 10. Task Customization

### From the Project: `prompt_engineer.py`

```python
def customize_for_task(self, 
                      base_prompt: str,
                      task_specific_instructions: str,
                      constraints: Optional[List[str]] = None) -> str:
    """
    Customize prompt for specific task requirements.
    """
    customized = base_prompt + f"\n\nTASK-SPECIFIC INSTRUCTIONS:\n{task_specific_instructions}"
    
    if constraints:
        customized += "\n\nCONSTRAINTS:\n"
        for constraint in constraints:
            customized += f"- {constraint}\n"
    
    return customized
```

### Constraint Examples

```python
constraints = [
    "Response must be under 500 words",
    "Use only technical terminology appropriate for beginners",
    "Include at least 2 practical examples",
    "Avoid jargon without explanation",
    "Format output as markdown"
]
```

---

## 11. Prompt Engineering Best Practices

### ✅ Do's

1. **Be Specific**: Clear, detailed instructions
2. **Use Structure**: Sections, numbered lists
3. **Provide Context**: Background information
4. **Set Constraints**: Length, format, audience
5. **Give Examples**: Few-shot when helpful
6. **Define Role**: Who the AI should be
7. **Specify Output Format**: JSON, markdown, etc.

### ❌ Don'ts

1. Don't be vague or ambiguous
2. Don't overload with too many instructions
3. Don't assume the model knows context
4. Don't forget edge cases
5. Don't skip output format specification

---

## 12. Prompt Templates Comparison

### Simple vs. Production Prompts

| Aspect | Simple | Production |
|--------|--------|------------|
| **Length** | 1-2 sentences | Multiple paragraphs |
| **Structure** | Free-form | Sections with headers |
| **Context** | Minimal | Comprehensive |
| **Examples** | None | 1-3 few-shot |
| **Constraints** | Implicit | Explicit list |
| **Output Format** | Assumed | Specified |

---

## 13. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **Template Design** | Structure enables consistency and reuse |
| **Few-Shot Learning** | Examples guide format and quality |
| **Chain-of-Thought** | Step-by-step reasoning improves accuracy |
| **Role Definition** | Context shapes response style |
| **JSON Output** | Explicit format + validation = reliable parsing |
| **Dynamic Building** | Parameters + defaults = flexible prompts |

---

## Related Concepts

- [LangChain Integration](./04-langchain-integration.md) - Using prompts with LangChain
- [RAG Pipeline](./05-rag-pipeline.md) - Context-aware prompting
- [Content Generation](./04-langchain-integration.md) - Executing prompts
