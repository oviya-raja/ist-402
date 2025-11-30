# ============================================================================
# Objective 1: Tokens - Text → Tokens
# ============================================================================
# Understanding how text is split into tokens (the basic units of LLMs)

import sys
from pathlib import Path

# Add support module if available
try:
    from llm_fundamentals_support import LLMFundamentalsSupport
    support = LLMFundamentalsSupport()
except ImportError:
    support = None
    print("Note: Running without support module")

print("=" * 80)
print("OBJECTIVE 1: TOKENS")
print("=" * 80)
print("\n🧠 Learning Goal: Understand how text is split into tokens")
print("   Tokens are the basic units that LLMs process.\n")

# ============================================================================
# Part 1: Basic Tokenization
# ============================================================================
print("\n" + "-" * 80)
print("Part 1: Basic Tokenization")
print("-" * 80)

try:
    from transformers import AutoTokenizer
    
    # Use a small model for demonstration
    model_name = "gpt2"  # Small, fast model for learning
    
    print(f"\n📥 Loading tokenizer from: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Example text
    text = "Hello! How are you today?"
    print(f"\n📝 Original text: '{text}'")
    
    # Tokenize
    tokens = tokenizer.tokenize(text)
    token_ids = tokenizer.encode(text, return_tensors=None)
    
    print(f"\n🔤 Tokens: {tokens}")
    print(f"🔢 Token IDs: {token_ids}")
    print(f"📊 Number of tokens: {len(tokens)}")
    print(f"📊 Number of characters: {len(text)}")
    print(f"📈 Ratio: {len(tokens) / len(text):.2f} tokens per character")
    
    # Decode back
    decoded = tokenizer.decode(token_ids)
    print(f"\n↩️  Decoded back: '{decoded}'")
    
except ImportError:
    print("⚠️  transformers library not installed")
    print("   Install with: pip install transformers")
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 2: Tokenization Examples
# ============================================================================
print("\n" + "-" * 80)
print("Part 2: Tokenization Examples")
print("-" * 80)

if 'tokenizer' in locals():
    examples = [
        "The quick brown fox jumps over the lazy dog.",
        "I love machine learning!",
        "What is a transformer?",
        "Tokenization splits text into smaller units.",
    ]
    
    print("\n📚 Example tokenizations:")
    for example in examples:
        tokens = tokenizer.tokenize(example)
        print(f"\n  Text: '{example}'")
        print(f"  Tokens ({len(tokens)}): {tokens[:10]}{'...' if len(tokens) > 10 else ''}")

# ============================================================================
# Part 3: Special Tokens
# ============================================================================
print("\n" + "-" * 80)
print("Part 3: Special Tokens")
print("-" * 80)

if 'tokenizer' in locals():
    print("\n🔑 Special tokens in vocabulary:")
    special_tokens = {
        'bos_token': tokenizer.bos_token,
        'eos_token': tokenizer.eos_token,
        'unk_token': tokenizer.unk_token,
        'pad_token': tokenizer.pad_token,
        'sep_token': tokenizer.sep_token,
        'cls_token': tokenizer.cls_token,
    }
    
    for name, token in special_tokens.items():
        if token:
            print(f"  {name}: '{token}'")
    
    print(f"\n📊 Vocabulary size: {len(tokenizer)}")

# ============================================================================
# Part 4: Different Tokenizers
# ============================================================================
print("\n" + "-" * 80)
print("Part 4: Comparing Different Tokenizers")
print("-" * 80)

if 'tokenizer' in locals():
    text = "Hello world! How are you?"
    
    try:
        from transformers import AutoTokenizer
        
        models = ["gpt2", "bert-base-uncased"]
        print(f"\n📝 Text: '{text}'\n")
        
        for model_name in models:
            try:
                tok = AutoTokenizer.from_pretrained(model_name)
                tokens = tok.tokenize(text)
                print(f"  {model_name}:")
                print(f"    Tokens ({len(tokens)}): {tokens}")
            except Exception as e:
                print(f"  {model_name}: Error - {e}")
    except Exception as e:
        print(f"⚠️  Could not compare tokenizers: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ Objective 1 Complete: Tokens")
print("=" * 80)
print("\n📚 Key Takeaways:")
print("  1. Text is split into tokens (subword units)")
print("  2. Each token has a unique ID in the vocabulary")
print("  3. Different models use different tokenization strategies")
print("  4. Special tokens mark sentence boundaries, padding, etc.")
print("\n➡️  Next: Objective 2 - Embeddings (Tokens → Vectors)")

# Store tokenizer for next objective
if 'tokenizer' in locals():
    globals()['tokenizer'] = tokenizer
    print("\n💾 Tokenizer saved for next objective")

