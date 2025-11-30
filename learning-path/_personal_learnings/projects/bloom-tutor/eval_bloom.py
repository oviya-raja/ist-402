# eval_bloom.py
"""
Simple evaluation script for Bloom quality
We'll do two things:
1. Automatic checks (does the answer contain all 6 sections?)
2. A human rubric printed so you can quickly score.
"""

import json
import re
from bloom_rag import generate_answer


def has_sections(text):
    sections = ["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE", "CREATE"]
    found = {}
    for s in sections:
        found[s] = bool(re.search(rf"\b{s}\b", text.upper()))
    return found


def eval_example(example):
    question = example["question"]
    print("\n====================================")
    print("QUESTION:", question)
    print("CONCEPT:", example["concept"])
    print("EXPECTED (high-level):")
    print(" - Remember:", example.get("remember", "")[:120], "...")
    print(" - Understand:", example.get("understand", "")[:120], "...")

    model_answer = generate_answer(question)
    print("\nMODEL ANSWER:")
    print(model_answer)

    found = has_sections(model_answer)
    print("\nSECTION COVERAGE:")
    for k, v in found.items():
        print(f" {k}: {'OK' if v else 'MISSING'}")

    print("\nHUMAN RUBRIC (1-5):")
    print(" 1. Remember: [ ]")
    print(" 2. Understand: [ ]")
    print(" 3. Apply: [ ]")
    print(" 4. Analyze: [ ]")
    print(" 5. Evaluate: [ ]")
    print(" 6. Create: [ ]")
    print(" Overall: [ ]")


if __name__ == "__main__":
    # load a few examples from your bloom_training_template.jsonl
    path = "bloom_training_template.jsonl"
    with open(path) as f:
        lines = [json.loads(l) for l in f if l.strip()]

    for ex in lines[:3]:
        eval_example(ex)

