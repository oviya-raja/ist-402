# Bloom's Taxonomy Implementation Guide

Complete guide to building your own Bloom's Taxonomy Educational LLM.

## 🎯 Implementation Approaches

### A) Bloom's Taxonomy Answering Prompt
- Works with ANY LLM (Phi-3, Gemma-2B, TinyLlama, GPT-2 fine-tuned, your own model)
- Use as system prompt OR prepend to every query
- See `rag-prompt.md` for the master prompt

### B) Dataset Generator
- Automatically builds training dataset from your notes
- Each concept expanded in Bloom levels
- See `projects/bloom-tutor/bloom_dataset_generator.py`

### C) Custom Model Architecture
- Mini-Bloom LLM: 12M-25M parameters
- Perfect for M-series chips
- See `projects/bloom-tutor/bloom_mini_gpt.py`

### D) Training Pipeline
- Optimized for Apple Metal (MPS)
- Mixed precision training
- Gradient checkpointing
- See `projects/bloom-tutor/README.md` for details

### E) Fine-tuning Approach
- Use existing small models (Qwen2-0.5B, TinyLlama-1.1B, Gemma-2-2B, Phi-2)
- Fine-tune with Bloom dataset
- Add RAG for notes retrieval
- Deploy locally or via Ollama

## 📊 Model Architecture Specs

### Mini-Bloom LLM Architecture (Recommended)

| Component | Value |
|-----------|-------|
| Layers | 6 |
| Attention Heads | 8 |
| Embedding Size | 256 |
| Context Length | 256 tokens |
| Vocabulary Size | 8k – 16k (BPE tokenizer) |
| Parameters | 12M – 25M |
| Training Compute | Perfect for M-series chips |

**Why this is ideal:**
- Big enough to learn complex text
- Small enough to train from scratch
- Perfect for Bloom-level reasoning
- Memory footprint tiny (~100MB)
- Inference extremely fast

This architecture is 10× more powerful than a "toy GPT", but still small.

## 🚀 Full Implementation Roadmap

Here's everything in clean order:

1. **A) Use Bloom prompt** → immediate results
2. **B) Generate Bloom training dataset** from your notes
3. **C) Build a mini-LLM architecture** (20M params) or pick a small existing LLM
4. **D) Train or fine-tune** on Apple M4
5. **E) Deploy** a custom Bloom Tutor model

You can go full from scratch, or combine pretrained + RAG.

## 📁 Project Structure

```
projects/bloom-tutor/
├── bloom_mini_gpt.py              # From-scratch model
├── bloom_dataset_generator.py      # Dataset generation
├── train_tokenizer.py              # BPE tokenizer training
├── bloom_rag.py                     # RAG system
├── eval_bloom.py                    # Evaluation script
├── bloom_training_template.jsonl   # Training data template
├── Modelfile                        # Ollama deployment
└── README.md                        # Complete guide
```

## 🎓 Training Dataset Format

Each training example in JSONL format:

```json
{
  "concept": "Backpropagation",
  "question": "Explain backpropagation in neural networks.",
  "remember": "...",
  "understand": "...",
  "apply": "...",
  "analyze": "...",
  "evaluate": "...",
  "create": "..."
}
```

Or instruction-style:

```json
{
  "instruction": "Use Bloom's taxonomy to explain: Backpropagation",
  "input": "My notes: ...",
  "output": "REMEMBER: ...\nUNDERSTAND: ...\nAPPLY: ...\nANALYZE: ...\nEVALUATE: ...\nCREATE: ..."
}
```

## 🔧 Training Setup for Apple M4

1. **Run on GPU**: `device = "mps"`
2. **Use mixed precision**: `torch.set_float32_matmul_precision("high")`
3. **Hyperparameters**:
   - batch_size = 64
   - learning_rate = 2e-4
   - min_lr = 1e-5
   - warmup_steps = 500
   - training_steps = 60,000
   - optimizer = AdamW
   - schedule = cosine decay
4. **Enable gradient checkpointing** (saves memory)
5. **Train BPE vocab** (8k–16k)
6. **Prepare notes dataset**: Split into chunks of 256 tokens, shuffle, stream training

### Expected Training Times
- 6–10 hours for 20M parameters on M4
- 1–2 hours for 10M parameters
- Very stable

### Evaluation
Stop when: `val_loss < 1.8` → very good for small models

## 🚢 Deployment Options

### Option 1: Ollama (Easiest)
```bash
ollama create bloom-tutor -f Modelfile
ollama run bloom-tutor
```

### Option 2: Local Python
Use the RAG system: `python bloom_rag.py`

### Option 3: Fine-tuned Model
Export as GGUF and use with Ollama or other inference engines

## 📚 Next Steps

Choose what to focus on:
1. Full real model code (training from scratch)
2. Bloom dataset template (fill manually)
3. Tokenizer training code
4. RAG system code for notes
5. Evaluation script to measure Bloom quality
6. Ollama deployment guide

All code is available in `projects/bloom-tutor/` directory.


