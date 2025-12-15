# W8 L1 Group Task
## PDF Q&A, Speech-to-Image, and Image Captioning

This repository contains three AI-powered applications demonstrating different aspects of modern AI systems:
1. **PDF Q&A**: RAG system for document-based question answering
2. **Speech-to-Image**: Multimodal pipeline converting speech to AI-generated images
3. **Image Captioning**: Automatic caption generation for images using BLIP

---

## 📁 Repository Structure

```
W08/
├── W8_pdf_Q&A.ipynb          # PDF Q&A RAG system
├── W8_Speech_to_Image.ipynb   # Speech-to-Image pipeline
├── W8_image_caption.ipynb     # Image captioning system
├── W8_L1_Report.md           # Comprehensive project report
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── A_PLUS_GUIDE.md           # Detailed A+ achievement guide
└── QUICK_CHECKLIST.md        # Quick reference checklist
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Colab (recommended) or local Jupyter environment
- GPU access recommended for faster performance (especially image generation)

### Installation

#### Option 1: Google Colab (Recommended)

1. Open the notebook in Google Colab
2. Run the first cell - it will automatically install all dependencies
3. For Speech-to-Image and Image Caption notebooks, set your ngrok token:
   - Get token from: https://dashboard.ngrok.com/get-started/your-authtoken
   - Replace the token in the notebook code

#### Option 2: Local Installation

```bash
# Clone or download this repository
cd W08

# Install dependencies
pip install -r requirements.txt

# Run notebooks in Jupyter
jupyter notebook
```

---

## 📚 Notebook Details

### 1. PDF Q&A (`W8_pdf_Q&A.ipynb`)

**Purpose**: Answer questions from PDF documents using RAG (Retrieval-Augmented Generation)

**Features**:
- Upload multiple PDF documents
- Semantic search for relevant content
- Context-aware answer generation
- Adjustable retrieval parameters

**Usage**:
1. Run the notebook cell to launch Streamlit app
2. Upload PDF files
3. Click "Build / Rebuild Index"
4. Ask questions about the documents

**Technical Stack**:
- LangChain for text processing
- FAISS for vector search
- sentence-transformers for embeddings
- FLAN-T5 for answer generation

---

### 2. Speech-to-Image (`W8_Speech_to_Image.ipynb`)

**Purpose**: Convert spoken descriptions into AI-generated images

**Features**:
- Audio file upload (WAV, MP3, M4A, FLAC)
- Direct text input option
- High-quality image generation
- Adjustable quality settings

**Usage**:
1. Run the notebook cell to launch Streamlit app
2. Choose input method:
   - Upload audio file and transcribe
   - Type text directly
3. Adjust quality settings (optional)
4. Generate image

**Technical Stack**:
- OpenAI Whisper for speech-to-text
- Stable Diffusion v1.5 for image generation
- Streamlit for UI

**Note**: Requires ngrok token for public access in Colab

---

### 3. Image Caption (`W8_image_caption.ipynb`)

**Purpose**: Generate automatic captions for uploaded images

**Features**:
- Support for JPG, JPEG, PNG formats
- Fast processing (~2-5 seconds)
- Accurate object and scene recognition
- User-friendly interface

**Usage**:
1. Run the notebook cell to launch Streamlit app
2. Upload an image
3. View the generated caption

**Technical Stack**:
- BLIP (Salesforce) for image captioning
- PIL for image processing
- Streamlit for UI

**Note**: Requires ngrok token for public access in Colab

---

## 📊 Project Report

See `W8_L1_Report.md` for comprehensive documentation including:
- Objectives for each system
- Detailed methodology and architecture
- Results with examples and performance metrics
- Learning outcomes and future work
- Connections to course concepts

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: Models not loading
- **Solution**: Ensure you have sufficient RAM/GPU memory. Try restarting the runtime.

**Issue**: ngrok connection failed
- **Solution**: Verify your ngrok token is correct and active.

**Issue**: Slow image generation
- **Solution**: This is expected on CPU. GPU acceleration is 5-10x faster.

**Issue**: PDF text extraction fails
- **Solution**: Some PDFs may be image-based or encrypted. Try a different PDF.

**Issue**: Import errors
- **Solution**: Run the installation cell again or restart the kernel.

### Performance Tips

- **GPU Acceleration**: Enable GPU in Colab (Runtime → Change runtime type → GPU)
- **Model Caching**: Models are cached after first load for faster subsequent use
- **Batch Processing**: For multiple images/documents, process in batches

---

## 📝 Dependencies

Key dependencies (see `requirements.txt` for complete list):

- `streamlit`: Web interface framework
- `transformers`: Hugging Face model library
- `langchain-community`: RAG pipeline components
- `faiss-cpu`: Vector similarity search
- `sentence-transformers`: Text embeddings
- `diffusers`: Stable Diffusion models
- `pypdf`: PDF text extraction
- `pillow`: Image processing
- `pyngrok`: Public URL tunneling

---

## 🎯 Getting an A+

Refer to `A_PLUS_GUIDE.md` for detailed breakdown of rubric requirements and `QUICK_CHECKLIST.md` for a quick reference.

**Key Requirements**:
1. ✅ Clear objectives for all three systems
2. ✅ Detailed methods documentation
3. ✅ Comprehensive results with evidence
4. ✅ Learning reflection and future work
5. ✅ Functional, well-documented code
6. ✅ Multiple examples and test cases

---

## 📖 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Stable Diffusion Guide](https://huggingface.co/docs/diffusers/)
- [BLIP Paper](https://arxiv.org/abs/2201.12086)

---

## 👥 Group Information

**Course**: IST-402  
**Assignment**: W8 L1 Group Task  
**Date**: [Current Date]

---

## 📄 License

This project is for educational purposes as part of IST-402 coursework.

---

## 🙏 Acknowledgments

- OpenAI for Whisper model
- Salesforce for BLIP model
- Stability AI for Stable Diffusion
- Hugging Face for model hosting and libraries
- LangChain team for RAG framework

---

**For questions or issues, refer to the comprehensive report or contact the course instructor.**

