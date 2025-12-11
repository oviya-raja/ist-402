# bloom_rag.py
"""
Simple RAG system over your notes + Bloom prompt
This will:
- embed chunks of your notes
- retrieve top-k relevant passages
- call a model with the Bloom prompt.
"""

from sentence_transformers import SentenceTransformer
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import textwrap

# 1. Load embedding model
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 2. Load your base LLM (can be local or small HF model)
llm_name = "google/gemma-2-2b"  # or another small instruct model
tok = AutoTokenizer.from_pretrained(llm_name)
llm = AutoModelForCausalLM.from_pretrained(llm_name, torch_dtype=torch.float16, device_map="auto")

# 3. Build index from your notes
notes_text = open("notes.txt").read()
chunk_size = 512  # characters
overlap = 128
chunks = []

for i in range(0, len(notes_text), chunk_size - overlap):
    chunk = notes_text[i:i+chunk_size]
    if len(chunk.strip()) > 0:
        chunks.append(chunk)

embs = embed_model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
dim = embs.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embs)


def retrieve(query, k=3):
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, k)
    return [chunks[i] for i in I[0]]


# 4. Bloom prompt
BLOOM_PROMPT = """You are a tutor using Bloom's Taxonomy.

Context (notes):

{context}

Question:

{question}

Answer in 6 sections:

1. REMEMBER:

2. UNDERSTAND:

3. APPLY:

4. ANALYZE:

5. EVALUATE:

6. CREATE:

Each section should be 2-4 sentences. If context is missing, say "Not enough information in notes" in that section.

"""


def generate_answer(question, max_new_tokens=512):
    ctx = "\n\n".join(retrieve(question, k=3))
    prompt = BLOOM_PROMPT.format(context=ctx, question=question)
    inputs = tok(prompt, return_tensors="pt").to(llm.device)

    with torch.no_grad():
        out = llm.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )

    text = tok.decode(out[0], skip_special_tokens=True)
    # Optionally strip prompt
    return text[text.find("1. REMEMBER"):]


if __name__ == "__main__":
    q = "Explain backpropagation and its problems in deep networks."
    ans = generate_answer(q)
    print(textwrap.indent(ans, prefix="> "))



