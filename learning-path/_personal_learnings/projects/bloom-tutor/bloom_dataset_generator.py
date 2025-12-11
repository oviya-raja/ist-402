# bloom_dataset_generator.py
"""
Dataset Generator (Turns Your Notes → Bloom Training Data)
This script automatically builds a training dataset from your notes where each concept is expanded in Bloom levels.
Works with any text file.
"""

import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Use a small LLM (Phi-3-mini or Gemma-2B recommended)
model_name = "google/gemma-2-2b"  # or "microsoft/phi-2"

generator = pipeline(
    "text-generation",
    model=model_name,
    tokenizer=model_name,
    max_new_tokens=350
)


def generate_bloom_examples(concept, notes):
    prompt = f"""
Create Bloom's Taxonomy Q&A for this concept based only on the notes.

Concept: {concept}

Notes: {notes}

Produce JSON with:
- question
- remember
- understand
- apply
- analyze
- evaluate
- create
"""
    out = generator(prompt)[0]["generated_text"]
    return out


notes_file = "notes.txt"
notes = open(notes_file).read()

concepts = [c.strip() for c in notes.split("\n") if c.strip()]

dataset = []

for concept in concepts:
    example = generate_bloom_examples(concept, notes)
    dataset.append(example)

with open("bloom_training_data.jsonl", "w") as f:
    for ex in dataset:
        f.write(ex + "\n")



