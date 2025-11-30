#!/bin/bash
# Run code2prompt with optimized exclusions for lower token count (~265K)
# 
# Excludes:
# - Environment: .venv, .vscode, __pycache__, .env, .env.bak, all dot files
# - Data files: CSV, binary data (.npy, .faiss, .pkl, .pickle)
# - Documentation: PDF, HTML (generated docs)
# - Notebooks: .ipynb (often contain large outputs - remove *.ipynb to include them)
# - Data directories: data/ folders with generated/test data
#
# Usage:
#   ./code2prompt.sh                    # Excludes notebooks (~265K tokens)
#   ./code2prompt.sh --exclude ""       # Remove *.ipynb from exclude to include notebooks (~443K tokens)

code2prompt . \
  --exclude ".venv/**,.vscode/**,__pycache__/**,.env,.env.bak,.*,*.csv,*.npy,*.faiss,*.pkl,*.pickle,*.pdf,*.html,*.ipynb,**/data/**" \
  --tokens \
  "$@"

