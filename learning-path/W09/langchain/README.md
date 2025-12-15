# LangChain Learning Notebooks

This directory contains LangChain tutorial notebooks covering:

| Notebook | Description | Open in Colab |
|----------|-------------|---------------|
| L1 | Models, Prompts, and Output Parsers | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oviya-raja/ist-402/blob/main/learning-path/W09/langchain/L1-Model_prompt_parser.ipynb) |
| L2 | Memory | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oviya-raja/ist-402/blob/main/learning-path/W09/langchain/L2-Memory.ipynb) |
| L3 | Chains | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oviya-raja/ist-402/blob/main/learning-path/W09/langchain/L3-Chains.ipynb) |
| L4 | Question & Answering | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oviya-raja/ist-402/blob/main/learning-path/W09/langchain/L4-QnA.ipynb) |
| L5 | Evaluation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oviya-raja/ist-402/blob/main/learning-path/W09/langchain/L5-Evaluation.ipynb) |
| L6 | Agents | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oviya-raja/ist-402/blob/main/learning-path/W09/langchain/L6-Agents.ipynb) |

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



