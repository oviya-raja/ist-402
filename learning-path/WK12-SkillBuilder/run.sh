#!/bin/bash

# Fix OpenMP library conflict on macOS (required for FAISS)
export KMP_DUPLICATE_LIB_OK=TRUE

# Run Streamlit app
streamlit run app.py
