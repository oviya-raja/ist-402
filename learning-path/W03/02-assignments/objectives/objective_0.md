## Objective 0: Setup & Prerequisites

### 🎯 Goal
I will set up my environment with all required packages, configure authentication, and verify system capabilities before starting the RAG system implementation.

<details>
<summary><b>Prerequisites Checklist</b> (Click to expand)</summary>

**Knowledge Prerequisites:**

| Requirement | Level | Description |
|-------------|-------|-------------|
| **Python Programming** | Basic | Variables, functions, data structures, imports |
| **Jupyter Notebooks** | Basic | Running cells, markdown formatting, code execution |
| **Machine Learning Concepts** | High-level | Neural networks, transformers, embeddings, model inference |
| **Evaluation Metrics** | Basic | Understanding of accuracy, confidence scores |

**Technical Prerequisites:**

| Item | Required | How to Get |
|------|----------|------------|
| **Hugging Face Account** | ✅ Yes | Sign up at [huggingface.co](https://huggingface.co) |
| **Hugging Face Token** | ✅ Yes | Get from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| **Google Colab Account** | ⚠️ Recommended | Free account at [colab.research.google.com](https://colab.research.google.com) |
| **GPU Access** | ⚠️ Optional | Colab provides free GPU, or local GPU setup |
| **Python 3.8+** | ✅ Yes | Pre-installed in Colab, or install locally |

</details>

<br>

<details>
<summary><b>📦 Required Packages</b> (Click to expand)</summary>

**Core Packages:**

| Package | Purpose | Version |
|---------|---------|---------|
| `transformers` | Load and use Hugging Face models (Mistral, QA models) | Latest |
| `torch` | Deep learning framework for model inference | Latest |
| `sentence-transformers` | Generate embeddings for semantic search | Latest |
| `faiss-cpu` | Vector similarity search library | Latest |
| `huggingface_hub` | Hugging Face authentication and model access | Latest |
| `numpy` | Numerical operations | Latest |
| `pandas` | DataFrames for Q&A database | Latest |

**Evaluation & Utilities:**

| Package | Purpose | Version |
|---------|---------|---------|
| `bert-score` | BERTScore for accuracy evaluation | Latest |
| `python-dotenv` | Load environment variables from .env files | Latest |

**Installation Command:**
```python
!pip install transformers torch sentence-transformers faiss-cpu huggingface_hub numpy pandas bert-score python-dotenv
```

**Note:** All packages will be installed automatically by the setup code cell.

</details>

<br>

<details>
<summary><b>🖥️ Environment Setup</b> (Click to expand)</summary>

**Option 1: Google Colab (Recommended)**

**Advantages:**
- ✅ Free GPU access (T4 GPU)
- ✅ No local installation needed
- ✅ Pre-configured environment
- ✅ Easy sharing and collaboration

**Setup Steps:**
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Create a new notebook
3. Enable GPU: **Runtime → Change runtime type → GPU → Save**
4. Upload or create the notebook file
5. Run the setup cell

**Option 2: Local Jupyter Notebook**

**Requirements:**
- Python 3.8 or higher
- Jupyter Notebook installed
- GPU optional (CPU works but slower)

**Setup Steps:**
1. Install Python 3.8+
2. Install Jupyter: `pip install jupyter`
3. Install required packages (see above)
4. Launch: `jupyter notebook`
5. Open the notebook file

**GPU Setup (Optional but Recommended):**

| Platform | GPU Type | Setup |
|----------|----------|-------|
| **Colab** | T4 (Free) | Runtime → Change runtime type → GPU |
| **Local** | NVIDIA GPU | Install CUDA toolkit, PyTorch with CUDA |
| **CPU Only** | N/A | Works but 2-3x slower |

</details>

<br>

<details>
<summary><b>🔑 Hugging Face Authentication</b> (Click to expand)</summary>

**Step 1: Get Your Token**

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Name it (e.g., "RAG Assignment")
4. Select **"Read"** access (sufficient for this assignment)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

**Step 2: Store Your Token**

**In Google Colab:**
```python
from google.colab import userdata
userdata.set('HUGGINGFACE_HUB_TOKEN', 'your_token_here')
```

**Or use Colab Secrets:**
1. Click the 🔑 icon in the left sidebar
2. Add secret: `HUGGINGFACE_HUB_TOKEN` = `your_token_here`

**Locally (Environment Variable):**
```bash
export HUGGINGFACE_HUB_TOKEN=your_token_here
```

**Or create `.env` file:**
```
HUGGINGFACE_HUB_TOKEN=your_token_here
```

**Step 3: Verify Authentication**

The setup code will automatically:
- Try Colab userdata first
- Try environment variables
- Prompt for manual input if needed
- Authenticate with Hugging Face Hub

</details>

<br>

<details>
<summary><b>✅ Setup Verification</b> (Click to expand)</summary>

After running the setup cell, verify these are set:

**Environment Variables:**
- ✅ `IN_COLAB` - True if running in Colab
- ✅ `HAS_GPU` - True if GPU is available
- ✅ `hf_token` - Your Hugging Face token

**Verification Code:**
```python
# Check setup
print("🔍 Setup Verification:")
print(f"   IN_COLAB: {IN_COLAB}")
print(f"   HAS_GPU: {HAS_GPU}")
print(f"   hf_token: {'✅ Set' if hf_token else '❌ Not set'}")

if HAS_GPU:
    import torch
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
```

**Expected Output:**
```
🔍 Setup Verification:
   IN_COLAB: True
   HAS_GPU: True
   hf_token: ✅ Set
   GPU: Tesla T4
```

</details>

<br>

<details>
<summary><b>⚙️ Setup Functions</b> (Click to expand)</summary>

The setup code provides modular functions following SOLID principles:

**Available Functions:**

| Function | Purpose | Returns |
|----------|---------|---------|
| `check_environment()` | Detect Colab and GPU availability | `(is_colab, has_gpu)` |
| `get_hf_token()` | Retrieve Hugging Face token from various sources | `str` (token) |
| `install_packages()` | Install required packages if missing | None |
| `import_libraries()` | Import all required libraries with error handling | `bool` (success) |
| `authenticate_hf(token)` | Authenticate with Hugging Face Hub | `bool` (success) |

**Design Principles:**
- **KISS** (Keep It Simple, Stupid) - Each function has single responsibility
- **DRY** (Don't Repeat Yourself) - Reusable functions
- **SOLID** - Modular, extensible design

</details>

<br>

<details>
<summary><b>🚀 Quick Start Guide</b> (Click to expand)</summary>

**Step-by-Step Setup:**

1. **Open Environment**
   - Colab: Create new notebook
   - Local: Launch Jupyter Notebook

2. **Enable GPU (Recommended)**
   - Colab: Runtime → Change runtime type → GPU
   - Local: Ensure CUDA is installed

3. **Run Setup Cell**
   - Execute the "Prerequisites & Setup" code cell
   - Wait for packages to install (~2-3 minutes first time)

4. **Authenticate**
   - Enter Hugging Face token when prompted
   - Or set it in Colab secrets/environment variable

5. **Verify**
   - Check console output for ✅ marks
   - Verify `hf_token` is set
   - Confirm GPU is detected (if available)

**Expected Setup Time:**
- First run: 2-3 minutes (package installation)
- Subsequent runs: <30 seconds (packages cached)

</details>

<br>

<details>
<summary><b>⚠️ Troubleshooting</b> (Click to expand)</summary>

**Common Issues:**

| Issue | Solution |
|-------|----------|
| **Token not found** | Check Colab secrets or environment variables. Re-enter token manually. |
| **GPU not detected** | In Colab: Runtime → Change runtime type → GPU. Local: Install CUDA toolkit. |
| **Package installation fails** | Restart runtime/kernel and try again. Check internet connection. |
| **Import errors** | Run `pip install --upgrade <package>` for the failing package. |
| **Out of memory** | Use CPU instead of GPU, or restart runtime to clear memory. |

**Getting Help:**
- Check error messages carefully - they usually indicate the issue
- Verify all prerequisites are met
- Ensure internet connection is stable
- Restart runtime/kernel if issues persist

</details>

<br>

<details>
<summary><b>📊 System Requirements</b> (Click to expand)</summary>

**Minimum Requirements (CPU):**
- Python 3.8+
- 8GB RAM
- 20GB free disk space (for model downloads)
- Stable internet connection

**Recommended (GPU):**
- Python 3.8+
- 16GB+ RAM
- NVIDIA GPU with 8GB+ VRAM
- 30GB+ free disk space
- Fast internet connection

**Colab Specifications:**
- **Free Tier:** T4 GPU (16GB VRAM), 12GB RAM
- **Pro Tier:** V100/A100 GPU, more RAM
- **Storage:** 15GB free space

**Model Download Sizes:**
- Mistral-7B: ~14GB (first download)
- QA Models: ~500MB - 3GB each
- Embedding Model: ~90MB
- **Total:** ~20-25GB for all models

</details>

---

**Next Step:** After setup is complete, proceed to **Objective 1: Design System Prompts** to load the Mistral model.

