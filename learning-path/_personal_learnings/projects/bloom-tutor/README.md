# Bloom Tutor Project

Complete implementation of a Bloom's Taxonomy educational LLM system.

## 📚 Components

1. **bloom_mini_gpt.py** - Real small GPT-style model from scratch (~10-20M params)
2. **bloom_dataset_generator.py** - Generates Bloom training data from notes
3. **train_tokenizer.py** - BPE tokenizer training on your notes
4. **bloom_rag.py** - RAG system combining notes + Bloom prompt
5. **eval_bloom.py** - Evaluation script for Bloom quality
6. **bloom_training_template.jsonl** - Template for Bloom training data
7. **Modelfile** - Ollama deployment configuration

## 🎯 Architecture

### Mini-Bloom LLM Architecture (Recommended for M4)

| Component | Value |
|-----------|-------|
| Layers | 6 |
| Attention Heads | 8 |
| Embedding Size | 256 |
| Context Length | 256 tokens |
| Vocabulary Size | 8k – 16k (BPE tokenizer) |
| Parameters | 12M – 25M |

**Why this is ideal:**
- Big enough to learn complex text
- Small enough to train from scratch
- Perfect for Bloom-level reasoning
- Memory footprint tiny (~100MB)
- Inference extremely fast

## 🚀 Training Pipeline for Apple M4

### Setup
1. Run on GPU: `device = "mps"`
2. Use mixed precision: `torch.set_float32_matmul_precision("high")`

### Hyperparameters
- batch_size = 64
- learning_rate = 2e-4
- min_lr = 1e-5
- warmup_steps = 500
- training_steps = 60,000
- optimizer = AdamW
- schedule = cosine decay

### Training Time
- 6–10 hours for 20M parameters on M4
- 1–2 hours for 10M parameters
- Very stable

### Evaluation
Stop when: `val_loss < 1.8` → very good for small models

## 📝 Usage

### 1. Train Tokenizer
```bash
python train_tokenizer.py
```

### 2. Train Model
```bash
python bloom_mini_gpt.py
```

### 3. Generate Training Data
```bash
python bloom_dataset_generator.py
```

### 4. Use RAG System
```bash
python bloom_rag.py
```

### 5. Evaluate
```bash
python eval_bloom.py
```

### 6. Deploy with Ollama
```bash
ollama create bloom-tutor -f Modelfile
ollama run bloom-tutor
```

## 🔗 Full Roadmap

1. Use Bloom prompt → immediate results
2. Generate Bloom training dataset from your notes
3. Build a mini-LLM architecture (20M params) or pick a small existing LLM
4. Train or fine-tune on Apple M4
5. Deploy a custom Bloom Tutor model

## 📖 Fine-tuning Alternative

If you choose not to train from scratch, use:
- Qwen2-0.5B
- TinyLlama-1.1B
- Gemma-2-2B
- Phi-2

With libraries like:
- HuggingFace TRL
- LLaMA-Factory (easiest!)
- Axolotl

### Example Fine-tuning Command
```bash
llamafactory-cli train \
  --model_name_or_path google/gemma-2-2b \
  --dataset bloom_training_data.jsonl \
  --output_dir bloom-tutor \
  --finetuning_type lora \
  --lora_rank 8 \
  --per_device_train_batch_size 2 \
  --learning_rate 2e-4 \
  --num_train_epochs 4
```


