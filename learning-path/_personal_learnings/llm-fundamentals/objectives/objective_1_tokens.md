# Objective 1: Tokens

## 🎯 Learning Goal

Understand how text is split into tokens - the basic units that LLMs process.

## 📚 Concepts

### What are Tokens?

Tokens are subword units that represent text in a format that language models can process. They are the bridge between human-readable text and machine-readable numbers.

### Key Points

1. **Text → Tokens**: Text is split into smaller units (tokens)
2. **Token IDs**: Each token has a unique numerical ID in the vocabulary
3. **Vocabulary**: The set of all possible tokens a model knows
4. **Special Tokens**: Special markers like `<BOS>`, `<EOS>`, `<PAD>`, etc.

### Tokenization Strategies

- **BPE (Byte Pair Encoding)**: Used by GPT models
- **WordPiece**: Used by BERT
- **SentencePiece**: Used by some multilingual models

## 💻 Code Structure

The `objective_1_tokens.py` script demonstrates:

1. **Basic Tokenization**: How to tokenize text
2. **Token Examples**: Real-world examples
3. **Special Tokens**: Understanding special markers
4. **Different Tokenizers**: Comparing tokenization strategies

## 🔗 Flow

```
Text → Tokenizer → Tokens → Token IDs
```

## ➡️ Next Objective

After understanding tokens, we move to **Objective 2: Embeddings** where tokens are converted to numerical vectors.


