
import os
import io
import re
import torch
import streamlit as st

# ---- LangChain & friends ----
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ---- PDF parsing ----
from pypdf import PdfReader

# ---- Local LLM (FLAN-T5) ----
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

st.set_page_config(page_title="PDF Q&A (Local RAG)", page_icon="📚")
st.title("📚 PDF Q&A Chatbot — Local RAG (Fixed)")

st.markdown(
    "Upload one or more PDFs. We'll chunk + embed them (MiniLM), build a FAISS index, "
    "then answer questions using retrieved chunks and a local FLAN-T5-Large model (better quality than base)."
)

# ---------------------------
# CACHED MODELS
# ---------------------------

@st.cache_resource
def load_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)

@st.cache_resource
def load_flan():
    # Using flan-t5-large for better answer quality (780M params vs 250M in base)
    # Falls back to base if large fails to load (memory constraints)
    name = "google/flan-t5-large"
    try:
        tok = AutoTokenizer.from_pretrained(name)
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForSeq2SeqLM.from_pretrained(name, torch_dtype=dtype)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        print(f"✅ Loaded {name} successfully")
    except Exception as e:
        print(f"⚠️ Failed to load {name}, falling back to flan-t5-base: {e}")
        name = "google/flan-t5-base"
        tok = AutoTokenizer.from_pretrained(name)
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model = AutoModelForSeq2SeqLM.from_pretrained(name, torch_dtype=dtype)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
    return tok, model, device

embeddings = load_embeddings()
tokenizer, flan, device = load_flan()

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

def clean_text(text):
    """
    Clean extracted text to remove noise that confuses the model.
    """
    # Remove sequences of numbers (like figure axis labels: "0 200 400 600...")
    # Using [0-9] instead of \d to avoid escape sequence warnings
    text = re.sub(r"([0-9]+\s+){4,}", "", text)

    # Remove figure/table references that are just numbers
    text = re.sub(r"Figure\s*[0-9]+[.:]", "Figure: ", text)
    text = re.sub(r"Table\s*[0-9]+[.:]", "Table: ", text)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove lines that are mostly numbers/symbols
    # Use splitlines() to avoid escape sequence issues
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        # Keep line if it has enough alphabetic content
        alpha_ratio = sum(c.isalpha() for c in line) / max(len(line), 1)
        if alpha_ratio > 0.3 or len(line) < 10:
            cleaned_lines.append(line)

    # Join with newline character
    # Join with newline - properly escaped
    return chr(10).join(cleaned_lines).strip()

def read_pdfs(files):
    texts = []
    for f in files:
        data = f.read()
        reader = PdfReader(io.BytesIO(data))
        content = []
        for page in reader.pages:
            try:
                page_text = page.extract_text() or ""
                # Clean each page
                page_text = clean_text(page_text)
                content.append(page_text)
            except Exception:
                content.append("")
        full_text = chr(10).join(content).strip()
        if full_text:
            texts.append(full_text)
    return texts

def build_vectorstore(raw_texts):
    # Increased chunk size for better context
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,     # Larger chunks = more context
        chunk_overlap=200,   # More overlap to preserve continuity
        length_function=len,
    )
    docs = []
    for t in raw_texts:
        docs.extend(splitter.create_documents([t]))
    vs = FAISS.from_documents(docs, embeddings)
    return vs

def make_prompt(question, contexts):
    """
    Create a clear, structured prompt for FLAN-T5.
    Key improvements:
    - Cleaner instruction format
    - Context limited to avoid truncation issues
    - Explicit instruction to answer from context
    """
    # Limit total context length to avoid truncation
    max_context_chars = 1500
    combined_context = ""
    for ctx in contexts:
        if len(combined_context) + len(ctx) < max_context_chars:
            combined_context += ctx + chr(10) + chr(10)
        else:
            # Add partial context if space allows
            remaining = max_context_chars - len(combined_context)
            if remaining > 100:
                combined_context += ctx[:remaining] + "..."
            break

    combined_context = combined_context.strip()

    # FLAN-T5 works better with explicit instruction-following format
    prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say "I don't know".

Context:
{combined_context}

Question: {question}

Answer:"""

    return prompt

def generate_answer(prompt, max_new_tokens=256):
    """
    Generate answer using FLAN-T5 with fixed parameters.
    Key fixes:
    - Removed min_length (was causing garbage output)
    - Better temperature settings
    - Proper handling of edge cases
    """
    # Tokenize with proper truncation
    inputs = tokenizer(
        prompt, 
        return_tensors="pt", 
        truncation=True,
        max_length=512,
        padding=False
    ).to(device)

    with torch.no_grad():
        output = flan.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            min_length=5,            # Ensure minimum answer length (5 tokens)
            temperature=0.5,          # Lower temperature for more focused answers
            do_sample=True,           # Enable sampling for better quality
            top_p=0.95,               # Nucleus sampling (slightly higher)
            top_k=50,                 # Limit vocabulary
            repetition_penalty=1.1,   # Reduce repetition (slightly lower)
            no_repeat_ngram_size=2,   # Prevent 2-gram repetition
            early_stopping=False,     # Don't stop early - let it generate fully
            num_beams=3,              # Use beam search for better quality
        )

    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    answer = answer.strip()

    # Remove common prefixes that FLAN-T5 might add
    prefixes_to_remove = ["answer:", "answer is:", "the answer is:", "answer:", "a:"]
    for prefix in prefixes_to_remove:
        if answer.lower().startswith(prefix):
            answer = answer[len(prefix):].strip()
            break

    # Post-process: only reject clearly invalid answers
    if not answer:
        return "I couldn't generate an answer from the provided context."

    # Only reject if answer is suspiciously short AND mostly non-alphabetic
    if len(answer) < 5:
        # Very short answers might still be valid (like "Yes", "No", "3")
        # Only reject if it's completely empty or just whitespace
        if not answer.strip():
            return "I couldn't generate an answer from the provided context."

    # Check for suspiciously numeric-only answers (but allow short numeric answers)
    if len(answer) > 15:  # Only check longer answers
        alpha_ratio = sum(c.isalpha() for c in answer) / max(len(answer), 1)
        if alpha_ratio < 0.2:  # More lenient threshold
            # Answer is mostly numbers/symbols - likely garbage
            return "I couldn't find a clear answer in the provided context. Please try rephrasing your question or check if the document contains relevant information."

    return answer

# ---------------------------
# UI
# ---------------------------
st.subheader("📤 Upload PDFs")
uploaded = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

col_a, col_b = st.columns([1,1])
with col_a:
    build_btn = st.button("🔧 Build / Rebuild Index")
with col_b:
    clear_btn = st.button("🗑️ Clear Index")

if clear_btn:
    st.session_state.vectorstore = None
    st.success("Cleared vector index.")

if build_btn:
    if not uploaded:
        st.warning("Please upload at least one PDF.")
    else:
        with st.spinner("Reading PDFs and building FAISS index..."):
            texts = read_pdfs(uploaded)
            if not any(texts):
                st.error("No extractable text found in the PDFs.")
            else:
                st.session_state.vectorstore = build_vectorstore(texts)
                st.success(f"Index ready! Processed {len(texts)} document(s). Ask questions below.")

st.divider()
st.subheader("❓ Ask a Question")

q = st.text_input("Your question", placeholder="Enter your question here...")

k = st.slider("Top-k chunks", 2, 8, 4)
max_tokens = st.slider("Max new tokens (answer length)", 64, 512, 256, step=32)

# Always show the button, but disable it if no index or no question
button_disabled = st.session_state.vectorstore is None or not q.strip()

if st.session_state.vectorstore is None:
    st.warning("⚠️ Please upload PDFs and click **Build / Rebuild Index** first!")

# Show the button always
if st.button("🔍 Retrieve & Answer", disabled=button_disabled, type="primary"):
    if st.session_state.vectorstore is None:
        st.error("❌ No index found! Please upload PDFs and build the index first.")
    elif not q.strip():
        st.error("❌ Please enter a question first.")
    else:
        with st.spinner("Retrieving relevant chunks..."):
            docs = st.session_state.vectorstore.similarity_search(q, k=k)
            contexts = [d.page_content for d in docs]

        st.write("**Retrieved Chunks:**")
        for i, c in enumerate(contexts, 1):
            with st.expander(f"Chunk {i}"):
                st.write(c)

        with st.spinner("Generating answer with FLAN-T5..."):
            prompt = make_prompt(q, contexts)
            ans = generate_answer(prompt, max_new_tokens=max_tokens)

        st.success("**Answer:**")
        st.write(ans)

        # Debug info (collapsible)
        with st.expander("🔧 Debug: View prompt sent to model"):
            st.code(prompt, language="text")
