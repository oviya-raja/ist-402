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

## 2. Prompt Types Organization

### Enum-Based Design

The project uses an enumeration to organize different prompt types:

- `IST_CONCEPT_EXPLANATION` - Detailed concept explanations
- `STUDY_PLAN_GENERATION` - Personalized study plans
- `CONCEPT_QUIZ` - Structured quiz generation
- `RESEARCH_SUMMARY` - Research synthesis

### Benefits of Enum-Based Design

| Benefit | Description |
|---------|-------------|
| **Type Safety** | IDE autocomplete, prevents typos |
| **Extensibility** | Add new types without breaking code |
| **Organization** | Clear categorization of prompts |
| **Maintainability** | Single source of truth for prompt types |

---

## 3. Prompt Template Structure

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

### IST Concept Explanation Template Structure

**Role**: Expert IST402 instructor

**Context Provided**:
- Concept Name
- Week
- Description
- Learning Objectives
- Prerequisites
- Difficulty Level
- Estimated Time
- Keywords

**Task Requirements**:
1. Explain in simple, understandable terms
2. Cover all learning objectives
3. Include relevant examples
4. Connect to prerequisites
5. Relate to other IST402 concepts
6. Use appropriate technical terminology
7. Provide practical insights

**Output Format**:
- Clear introduction
- Detailed explanation
- Examples and use cases
- Connections to related concepts
- Key takeaways

---

## 4. Dynamic Prompt Building

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

### Building Process Steps

1. **Get Template**: Select template based on prompt type
2. **Set Defaults**: Use sensible default values
3. **Override with User Input**: Replace defaults with provided values
4. **Format Template**: Fill in all placeholders
5. **Add Enhancements**: Include few-shot examples if available

---

## 5. Few-Shot Learning

### What is Few-Shot Learning?

Providing examples in the prompt to guide the model's output format and style.

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

### What is Chain-of-Thought?

Asking the model to show its reasoning process step-by-step.

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

### CoT Reasoning Process

1. First, analyze the provided information
2. Identify key points and relationships
3. Consider the context and requirements
4. Generate your response based on this analysis
5. Review and refine your output

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

### Role Definition Pattern

```
ROLE DEFINITION:
You are {role} with expertise in:
- {expertise area 1}
- {expertise area 2}
- {expertise area 3}

Apply this expertise to provide the best possible response.
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

### Key Techniques for JSON Output

1. **Explicit Format Requirement**: "MUST return ONLY valid JSON"
2. **Template Example**: Show exact expected structure
3. **Validation Rules**: Numbered list of constraints
4. **No Markdown**: Explicitly forbid code blocks

### JSON Output Requirements

- Return ONLY the JSON object, nothing else
- All multiple choice questions must have exactly 4 options labeled A, B, C, D
- Option text should be clear, distinct, and educational
- Include correct answer and explanation for each question

### Parsing Strategy

1. **Extract JSON**: Try to find JSON in markdown code blocks
2. **Fallback**: Search for JSON object directly in text
3. **Parse**: Use JSON parser to validate and extract data
4. **Handle Errors**: Gracefully handle parsing failures

---

## 9. Prompt Statistics & Monitoring

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

### Constraint Examples

- Response must be under 500 words
- Use only technical terminology appropriate for beginners
- Include at least 2 practical examples
- Avoid jargon without explanation
- Format output as markdown

### Customization Flow

```
Base Prompt
    │
    ▼
┌─────────────────┐
│ Add Task-Specific│
│ Instructions     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Add Constraints │
│ (if any)         │
└────────┬────────┘
         │
         ▼
    Final Prompt
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
