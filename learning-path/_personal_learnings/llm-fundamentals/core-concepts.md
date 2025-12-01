# Core AI Concepts - LLM Fundamentals

## 🧠 The 6 Core Components

### 1️⃣ Tokens
Text split into small units (tokens).

### 2️⃣ Embeddings
Tokens → vectors (numerical representation).

### 3️⃣ Vector Relationships (Attention)
The model computes how each token/vector relates to every other.

### 4️⃣ Layers (stacked attention + feedforward blocks)
Multiple transformer layers apply attention + transformations repeatedly.

### 5️⃣ Tensors
Data and weights are stored and computed in tensors (multi-dim arrays).

### 6️⃣ Parameters (Weights)
Learned numerical values inside those tensors, updated during training.

---

## ✅ Clean Final Version

**LLM = Tokens → Embeddings → Vector Relationships (Attention) → Layers → Tensors → Parameters (Weights)**

---

## 💻 Code Example: Loading and Using Mistral

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 1. Choose a Mistral model from Hugging Face
model_name = "mistralai/Mistral-7B-v0.1"  # example

# 2. Load tokenizer (Tokens)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. Load model (Embeddings + Attention + Layers + Weights)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"  # put it on GPU(s) if available
)

# 4. Go from Text → Tokens
prompt = "Explain what a Large Language Model is in one sentence."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# 5. Run the model (forward pass: embeddings → attention → layers → tensors)
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        top_p=0.9,
        temperature=0.7,
    )

# 6. Decode back to text
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

---

## 🔍 Retrieving Model Configuration

We can retrieve:
- hidden size
- number of layers
- number of attention heads
- tensor shapes
- embedding size
- vocabulary size
- activation functions
- positional embedding type
- attention variants

```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
print(model.config)
```


