# LangChain Learning Notebooks

This directory contains LangChain tutorial notebooks covering:
- L1: Models, Prompts, and Output Parsers
- L2: Memory
- L3: Chains
- L4: Question & Answering
- L5: Evaluation
- L6: Agents

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install langchain langchain-openai langchain-core langchain-community python-dotenv openai pandas tiktoken
```

## Note on IDE/Linter Warnings

If you see import errors in your IDE (like "Import 'langchain_openai' could not be resolved"), this usually means:

1. The packages aren't installed in your IDE's Python environment
2. Your IDE is using a different Python interpreter than where packages are installed

**To fix:**
- Make sure you've installed the packages: `pip install -r requirements.txt`
- Configure your IDE to use the correct Python interpreter where the packages are installed
- Restart your IDE after installing packages

The imports are correct - the packages just need to be installed in your Python environment.

