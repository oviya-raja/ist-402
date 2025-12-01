# ============================================================================
# Objective 1: Tokens - Text → Tokens
# ============================================================================
# Understanding how text is split into tokens (the basic units of Large Language Models)

from llm_fundamentals_support import (
    LLMFundamentalsSupport, ModelLoader, TextProcessor, Formatter, StateManager
)

support = LLMFundamentalsSupport()
formatter = Formatter()
state_mgr = StateManager()

print(formatter.header("OBJECTIVE 1: TOKENS"))
print(formatter.learning_intro(
    concept="Tokenization",
    description="Text is split into tokens - subword units that Large Language Models can process. Each token has a unique Identifier in the model's vocabulary.",
    what_we_learn=[
        "How text is converted to tokens (subword units)",
        "Token Identifiers and vocabulary mapping",
        "Different tokenization strategies (Byte Pair Encoding, WordPiece, etc.)",
        "Special tokens and their purposes"
    ],
    what_we_do=[
        "Load a tokenizer from Hugging Face",
        "Tokenize example text and see the tokens",
        "Compare tokenization across different models",
        "Examine special tokens in the vocabulary"
    ],
    hands_on=[
        "Use AutoTokenizer to load Qwen tokenizer",
        "Tokenize text: 'Hello! How are you today?'",
        "See tokens: ['Hello', '!', 'ĠHow', 'Ġare', 'Ġyou', 'Ġtoday', '?']",
        "Compare Qwen vs other tokenizers",
        "Inspect vocabulary size and special tokens"
    ]
))

# ============================================================================
# Part 1: Basic Tokenization
# ============================================================================
print(formatter.section("Part 1: Basic Tokenization - Hands-On Code"))

loader = ModelLoader()
try:
    tokenizer = loader.load_tokenizer(globals())
    print(f"\n📥 Loaded tokenizer from: {loader.model_name}")
    
    processor = TextProcessor(tokenizer)
    
    # Display tokenizer type information
    tokenizer_info = processor.get_tokenizer_type_info()
    print(f"\n🔍 Tokenizer Type Information:")
    print(f"   Class: {tokenizer_info['class_name']}")
    if tokenizer_info['algorithm']:
        print(f"   Algorithm: {tokenizer_info['algorithm']}")
    print(f"   Type: {tokenizer_info['tokenizer_type']} ({'Fast' if tokenizer_info['is_fast'] else 'Slow'})")
    print(f"\n💡 Note: AutoTokenizer automatically detected and loaded the correct tokenizer")
    print(f"   for this model - it's the generic tokenizer that works with any model!")
    
    text = "Hello! How are you today?"
    info = processor.get_token_info(text)
    
    print(f"\n📝 Original text: '{info['text']}'")
    print(f"🔤 Tokens: {info['tokens']}")
    print(f"🔢 Token Identifiers: {info['token_ids']}")
    print(f"📊 Number of tokens: {info['num_tokens']}")
    print(f"📊 Number of characters: {info['num_chars']}")
    print(f"📈 Ratio: {info['ratio']:.2f} tokens per character")
    print(f"\n↩️  Decoded back: '{processor.decode(info['token_ids'])}'")
    
    # Output summary
    print(formatter.output_summary([
        f"Text '{text}' was split into {info['num_tokens']} tokens",
        f"Each token has a unique Identifier (e.g., 'Hello' = {info['token_ids'][0]})",
        f"Tokenization ratio: {info['ratio']:.2f} tokens per character",
        "Decoding token Identifiers back produces the original text"
    ]))
    
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 2: Tokenization Examples
# ============================================================================
print(formatter.section("Part 2: Tokenization Examples - Different Texts"))

if 'tokenizer' in locals():
    examples = [
        "The quick brown fox jumps over the lazy dog.",
        "I love machine learning!",
        "What is a transformer?",
        "Tokenization splits text into smaller units.",
    ]
    
    print("\n📚 Example tokenizations:")
    for example in examples:
        tokens = processor.tokenize(example)
        print(f"\n  Text: '{example}'")
        print(f"  Tokens ({len(tokens)}): {tokens[:10]}{'...' if len(tokens) > 10 else ''}")
    
    print(formatter.output_summary([
        "Different texts produce different numbers of tokens",
        "Longer words may be split (e.g., 'Tokenization' → 'Token' + 'ization')",
        "Punctuation is often separate tokens",
        "Spaces are represented as 'Ġ' prefix in Byte Pair Encoding tokenizers (like Qwen)"
    ]))

# ============================================================================
# Part 3: Special Tokens
# ============================================================================
print(formatter.section("Part 3: Special Tokens - Vocabulary Features"))

if 'tokenizer' in locals():
    print("\n🔑 Special tokens in vocabulary:")
    special_tokens = {
        'Beginning of Sequence token': tokenizer.bos_token,
        'End of Sequence token': tokenizer.eos_token,
        'Unknown token': tokenizer.unk_token,
        'Padding token': tokenizer.pad_token,
        'Separator token': tokenizer.sep_token,
        'Classification token': tokenizer.cls_token,
    }
    
    for name, token in special_tokens.items():
        if token:
            print(f"  {name}: '{token}'")
    
    print(f"\n📊 Vocabulary size: {len(tokenizer)}")
    
    print(formatter.output_summary([
        f"Vocabulary contains {len(tokenizer)} unique tokens",
        "Special tokens mark boundaries (Beginning of Sequence/End of Sequence), unknown words (Unknown), padding (Padding)",
        "Different models use different special token sets"
    ]))

# ============================================================================
# Part 4: Different Tokenizers
# ============================================================================
print(formatter.section("Part 4: Comparing Different Tokenizers - Strategy Differences"))

if 'tokenizer' in locals():
    text = "Hello world! How are you?"
    try:
        from transformers import AutoTokenizer
        # Compare modern open-source models (using latest Qwen 2.5)
        models = ["Qwen/Qwen2.5-1.5B", "microsoft/Phi-3-mini-4k-instruct"]
        print(f"\n📝 Text: '{text}'\n")
        
        for model_name in models:
            try:
                loader_temp = ModelLoader(model_name)
                tok = loader_temp.load_tokenizer(use_cache=True)
                tokens = tok.tokenize(text)
                print(f"  {model_name}:")
                print(f"    Tokens ({len(tokens)}): {tokens}")
            except Exception as e:
                print(f"  {model_name}: Error - {e}")
        
        print(formatter.output_summary([
            "Qwen2 uses modern Byte Pair Encoding tokenization - efficient and preserves meaning",
            "Phi-3 uses similar tokenization with optimized vocabulary",
            "Same text produces different tokens with different tokenizers",
            "Tokenization strategy affects model performance and vocabulary size",
            "Modern models use larger vocabularies (100K+ tokens) for better coverage"
        ]))
    except Exception as e:
        print(f"⚠️  Could not compare tokenizers: {e}")

# ============================================================================
# Summary
# ============================================================================
takeaways = [
    "Text is split into tokens (subword units)",
    "Each token has a unique Identifier in the vocabulary",
    "Different models use different tokenization strategies",
    "Special tokens mark sentence boundaries, padding, etc."
]
print(formatter.summary("Objective 1 Complete: Tokens", takeaways, "Objective 2 - Embeddings (Tokens → Vectors)"))

# Save state
if 'tokenizer' in locals():
    state_mgr.save_to_globals(globals(), tokenizer=tokenizer)
    print("\n💾 Tokenizer saved for next objective")
