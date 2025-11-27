# IST402 - AI Agents & RAG Systems Course

Complete guide for **IST402: AI Agents, Retrieval-Augmented Generation (RAG), and Modern LLM Applications**.

## 📁 Project Structure

```
ist-402/
├── README.md                    # This file - Course overview
├── requirements.txt             # Python dependencies
├── setup.sh                     # Virtual environment setup script
└── learning-path/               # Learning materials and assignments
    ├── W03/                     # Week 3: Prompt Engineering & QA
    │   ├── 01-exercises/        # Exercises
    │   │   ├── 01-prompt-engineering/
    │   │   ├── 02-simple-rag/
    │   │   └── 03-rag-with-model-evaluation/
    │   ├── 02-assignments/      # Assignments
    │   ├── 03-learnings/        # Learning notes
    │   └── README.md
    ├── W06/                     # Week 6: AI Agents with n8n
    ├── W07/                     # Week 7: Group Assignment
    ├── W08/                     # Week 8: Multimodal AI Applications
    ├── W09/                     # Week 9: Building Agentic RAG
    ├── W10/                     # Week 10: Advanced Agentic RAG
    └── W11/                     # Week 11: Advanced Topics
```

## 📑 Table of Contents

- [Quick Start](#-quick-start)
- [Recommended Learning Path](#-recommended-learning-path)
- [Week-by-Week Guide](#-week-by-week-guide-chronological-order)
- [Project Structure](#-project-structure)
- [Learning Materials](#-learning-materials)
- [Technologies I've Used](#-technologies-ive-used)
- [Tips for Success](#-tips-for-success)
- [Common Issues](#-common-issues)
- [Resources](#-resources)
- [Progress Checklist](#-progress-checklist)

---

## 🚀 Quick Start

### DevContainer Setup

**Use VS Code Dev Containers or GitHub Codespaces for a pre-configured environment:**

1. **VS Code:**
   - Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - Open command palette (Cmd/Ctrl + Shift + P)
   - Select "Dev Containers: Reopen in Container"

2. **GitHub Codespaces:**
   - Click "Code" → "Codespaces" → "Create codespace"

The devcontainer includes:
- ✅ Python 3.11 with all required packages
- ✅ Node.js 20 for Docusaurus
- ✅ Jupyter Lab for notebooks
- ✅ All dependencies pre-installed

> **Note:** DevContainer configuration is optional. You can also set up a local environment as described below.

### Local Python Environment Setup

**Recommended: Root-level virtual environment**

All assignments share the same dependencies, so use ONE virtual environment at the root level.

**Quick setup with uv (fastest):**
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Or with standard venv:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Or use the setup script (easiest):**
```bash
./setup.sh
```

---

## 📅 Recommended Learning Path

**Note:** While weeks are numbered 3, 6, 7, 8, 9, 10, 11, here's the optimal order to tackle them:

1. **Week 3** - Prompt Engineering & QA (8-12h) ← **START HERE**
2. **Week 8** - Multimodal AI (10-15h)
3. **Week 9** - LlamaIndex Basics (12-16h)
4. **Week 10** - Advanced RAG (12-16h)
5. **Week 7** - Group Project (15-20h)
6. **Week 6** - n8n Agents (4-6h, optional)

---

## 📖 Week-by-Week Guide (Chronological Order)

### **Week 3: Prompt Engineering & QA**
**Location:** [`learning-path/W03/`](./learning-path/W03/)

**Structure:**
- **Exercises:** [`01-exercises/`](./learning-path/W03/01-exercises/)
  - `01-prompt-engineering/` - Prompt engineering basics
  - `02-simple-rag/` - Simple RAG with QA chatbot
  - `03-rag-with-model-evaluation/` - RAG system with evaluation
- **Assignments:** [`02-assignments/`](./learning-path/W03/02-assignments/)
- **Learnings:** [`03-learnings/`](./learning-path/W03/03-learnings/)

**Key Files:**
- `W3__Prompt_Engineering_Basics.ipynb`
- `W3__QA_Chatbot_Activity_w_Prompt_Engineering-1.ipynb`
- `W3_RAG_System_Exercise.ipynb`
- `W3_RAG_Assignment_Final.ipynb`

**What I Have Learned:**
- Designed system prompts for LLMs
- Built Q&A databases using Mistral-7B
- Implemented FAISS vector database
- Created RAG (Retrieval-Augmented Generation) systems
- Compared multiple QA models

**Steps:**
1. Choose a business context (e.g., "Tech Startup - AI Consultant")
2. Create system prompt defining AI role
3. Generate 10-15 Q&A pairs using Mistral
4. Build FAISS index for similarity search
5. Test with answerable/unanswerable questions
6. Compare 4+ QA models and rank them

**Key Concepts:** System prompts, Vector embeddings, FAISS, RAG pipeline

---

### **Week 6: AI Agents with n8n** (Optional)
**Location:** [`learning-path/W06/`](./learning-path/W06/)

**Files:** `W6-AI Agents-n8n to-do-task.pptx`

**What I Have Learned:**
- Workflow automation with n8n
- Task management systems
- Agent orchestration

---

### **Week 7: Group Assignment**
**Location:** [`learning-path/W07/`](./learning-path/W07/)

**Files:** `W7GroupAssignmentAgentsDevwithOpenAI.pdf`

**What I Have Learned:**
- Built production-ready AI agents
- Integrated OpenAI API
- Collaborated on team projects

---

### **Week 8: Multimodal AI Applications**
**Location:** [`learning-path/W08/`](./learning-path/W08/)

**Files:** 
- `W8_image_caption.ipynb` - Image captioning with BLIP
- `W8_pdf_Q&A.ipynb` - PDF Q&A system
- `W8_Speech_to_Image.ipynb` - Speech-to-image pipeline
- `W8_Instructions.pdf` - Assignment instructions

**What I Have Learned:**

**Project 1: Image Captioning** (Easiest - 1h)
- Used BLIP model from Salesforce for image captioning
- Built Streamlit web interface for image upload
- Created image-to-text pipeline

**Project 2: PDF Q&A** (Medium - 2h)
- Processed PDFs and built FAISS index
- Implemented Q&A system with FLAN-T5 model
- Created local RAG system for document querying

**Project 3: Speech-to-Image** (Hardest - 3h)
- Integrated Whisper for speech-to-text conversion
- Combined with Stable Diffusion for text-to-image generation
- Built dual-input system (audio upload or text input)

**Key Concepts:** Multimodal AI, Streamlit, Model integration, Web deployment

---

### **Week 9: Building Agentic RAG with LlamaIndex**
**Location:** [`learning-path/W09/`](./learning-path/W09/)

**Files:** 
- `W9_Building_Agentic_RAG_LlamaIndex_3_4.ipynb`
- `W9_L2.pdf` - Lecture materials

**Prerequisites:** OpenAI API key (paid account)

**What I Have Learned:**

1. **Router Engine** - Routed queries to summary vs vector search engines
2. **Tool Calling** - Implemented LLMs calling functions automatically
3. **Agent Reasoning** - Built multi-step reasoning with FunctionAgent
4. **Multi-Document Agent** - Created agents that query across multiple papers

**Key Concepts:** LlamaIndex framework, Query routing, Tool development, Agent reasoning

---

### **Week 10: Advanced Agentic RAG**
**Location:** [`learning-path/W10/`](./learning-path/W10/)

**Files:** 
- `W10_Building_Agentic_RAG_LlamaIndex_3_4.ipynb`
- `W10_L1.pdf` - Lecture materials

**What I Have Learned:**
- Built multi-document agent (scaled from 3 papers to 11 papers)
- Implemented tool retrieval system
- Handled complex queries across multiple documents
- Optimized system performance and scaling

**Key Concepts:** Tool retrieval, System scaling, Performance optimization

---

### **Week 11: Advanced Topics**
**Location:** [`learning-path/W11/`](./learning-path/W11/)

**Files:** 
- `W11_L1.ps` - Lecture 1 materials
- `W11_L2.pdf` - Lecture 2 materials

**What I Have Learned:**
- Advanced concepts and topics
- Additional materials and techniques

---

## 📂 Learning Materials

All learning materials and assignments are located in [`learning-path/`](./learning-path/):

- **Week 3:** [`W03/`](./learning-path/W03/) - Prompt Engineering & QA
  - Exercises: Prompt engineering, Simple RAG, RAG with evaluation
  - Assignments: RAG assignment notebook
  - Learnings: Learning notes and reflections
- **Week 6:** [`W06/`](./learning-path/W06/) - AI Agents with n8n (PowerPoint presentation)
- **Week 7:** [`W07/`](./learning-path/W07/) - Group Assignment (PDF specification)
- **Week 8:** [`W08/`](./learning-path/W08/) - Multimodal AI Applications
  - Image captioning notebook
  - PDF Q&A notebook
  - Speech-to-image notebook
- **Week 9:** [`W09/`](./learning-path/W09/) - Building Agentic RAG with LlamaIndex
- **Week 10:** [`W10/`](./learning-path/W10/) - Advanced Agentic RAG
- **Week 11:** [`W11/`](./learning-path/W11/) - Advanced Topics (Lecture materials)

---

## 🛠️ Technologies I've Used

- **Transformers** (Hugging Face) - Pre-trained models
- **LangChain** - LLM application framework
- **LlamaIndex** - Advanced RAG framework
- **FAISS** - Vector similarity search
- **Streamlit** - Web app framework
- **PyTorch** - Deep learning backend

**Models:** Mistral-7B, BLIP, Whisper, Stable Diffusion, GPT-3.5/GPT-4

---

## 💡 Tips for Success

1. **Start with Week 3** - It's the foundation for everything
2. **Run every cell** - Don't just read, execute and experiment
3. **Understand the why** - Don't copy-paste, learn the concepts
4. **Document your work** - Save prompts, note what works
5. **Build incrementally** - Master basics before advanced topics
6. **Use free resources** - Google Colab GPU, Hugging Face free tier

---

## ⚠️ Common Issues

**"CUDA out of memory"** → Use smaller models or `torch_dtype=torch.float16`

**"Token expired"** → Regenerate token in account settings

**"Module not found"** → Run `!pip install package_name` in Colab

**"API rate limit"** → Add delays: `import time; time.sleep(1)`

---

## 📚 Resources

- [Hugging Face Docs](https://huggingface.co/docs)
- [LangChain Docs](https://python.langchain.com)
- [LlamaIndex Docs](https://docs.llamaindex.ai)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)

---

## ✅ Progress Checklist

- [ ] Week 3: Built RAG system with FAISS
- [ ] Week 6: Completed n8n workflow (optional)
- [ ] Week 7: Completed group project
- [ ] Week 8: Deployed 3 multimodal apps
- [ ] Week 9: Created agentic RAG with LlamaIndex
- [ ] Week 10: Built multi-document agent

---

**Ready to start? Begin with Week 3! 🚀**
