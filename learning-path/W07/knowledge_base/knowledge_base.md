# IST402 Course Knowledge Base

This knowledge base contains structured course content for IST402.

## Tokens and Tokenization (KB-W00-001)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** Text split into small units (tokens). Foundation of all LLM processing. Understand BPE subword and character tokenization.

**Learning Objectives:**
- Understand token units
- Compare tokenization methods
- Analyze token efficiency

**Difficulty Level:** beginner

**Estimated Time:** 45 minutes

---

## Embeddings (KB-W00-002)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** Tokens converted to vectors (numerical representations). Semantic meaning encoded in high-dimensional space.

**Learning Objectives:**
- Convert tokens to vectors
- Visualize embedding space
- Measure semantic similarity

**Difficulty Level:** beginner

**Estimated Time:** 60 minutes

---

## Vector Relationships and Attention (KB-W00-003)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** How each token/vector relates to every other. Self-attention mechanism computes contextual relationships.

**Learning Objectives:**
- Understand attention mechanism
- Visualize attention patterns
- Compute attention scores

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Transformer Layers (KB-W00-004)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** Stacked attention + feedforward blocks. Multiple layers apply attention and transformations repeatedly.

**Learning Objectives:**
- Understand layer composition
- Trace data through layers
- Analyze layer outputs

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Tensors (KB-W00-005)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** Data and weights stored and computed in tensors (multi-dimensional arrays). Core data structure for deep learning.

**Learning Objectives:**
- Manipulate tensor shapes
- Understand broadcasting
- Perform tensor operations

**Difficulty Level:** beginner

**Estimated Time:** 45 minutes

---

## Parameters and Weights (KB-W00-006)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** Learned numerical values inside tensors updated during training. The knowledge of the model.

**Learning Objectives:**
- Count model parameters
- Inspect weight matrices
- Understand parameter updates

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## LLM Architecture Overview (KB-W00-007)

**Week:** W00 - Core AI Concepts

**Category:** concept

**Description:** Complete picture: Tokens → Embeddings → Attention → Layers → Tensors → Parameters. End-to-end understanding.

**Learning Objectives:**
- Trace full LLM pipeline
- Inspect model components
- Extract architecture details

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Model Inspection Exercise (KB-W00-008)

**Week:** W00 - Core AI Concepts

**Category:** exercise

**Description:** Retrieve hidden size number of layers attention heads tensor shapes embedding size vocabulary size from any model.

**Learning Objectives:**
- Extract model config
- Analyze architecture
- Compare model sizes

**Difficulty Level:** beginner

**Estimated Time:** 60 minutes

---

## Build Mini GPT from Scratch (KB-W00-009)

**Week:** W00 - Core AI Concepts

**Category:** exercise

**Description:** Build a real small GPT-style model (10-20M params) from scratch. Implements attention layers and training loop.

**Learning Objectives:**
- Implement transformer blocks
- Train from scratch
- Generate text

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## Custom Tokenizer Training (KB-W00-010)

**Week:** W00 - Core AI Concepts

**Category:** exercise

**Description:** Train a BPE tokenizer on custom corpus. Understand vocabulary construction and subword segmentation.

**Learning Objectives:**
- Train BPE tokenizer
- Configure vocab size
- Test tokenization

**Difficulty Level:** intermediate

**Estimated Time:** 45 minutes

---

## Bloom Taxonomy Educational LLM (KB-W00-011)

**Week:** W00 - Core AI Concepts

**Category:** project

**Description:** Build a tutor that answers using Bloom's Taxonomy levels: remember understand apply analyze evaluate create.

**Learning Objectives:**
- Design Bloom prompts
- Generate training data
- Build educational RAG

**Difficulty Level:** advanced

**Estimated Time:** 240 minutes

---

## Bloom RAG System (KB-W00-012)

**Week:** W00 - Core AI Concepts

**Category:** project

**Description:** RAG system that retrieves from learning notes and answers in Bloom's Taxonomy format with 6 cognitive levels.

**Learning Objectives:**
- Build note retrieval
- Implement Bloom prompt
- Ground answers in context

**Difficulty Level:** advanced

**Estimated Time:** 120 minutes

---

## Bloom Dataset Generator (KB-W00-013)

**Week:** W00 - Core AI Concepts

**Category:** project

**Description:** Auto-generate Bloom's Taxonomy training data from notes. Creates instruction dataset for fine-tuning.

**Learning Objectives:**
- Parse learning notes
- Generate Q&A pairs
- Format for training

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Bloom Evaluation Script (KB-W00-014)

**Week:** W00 - Core AI Concepts

**Category:** project

**Description:** Evaluate Bloom quality: checks for all 6 sections provides human rubric scores measures completeness.

**Learning Objectives:**
- Check section coverage
- Score with rubric
- Measure quality

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Ollama Bloom Tutor Deployment (KB-W00-015)

**Week:** W00 - Core AI Concepts

**Category:** deployment

**Description:** Deploy Bloom tutor via Ollama Modelfile. Bakes Bloom's Taxonomy prompt into local model.

**Learning Objectives:**
- Create Modelfile
- Build Ollama model
- Run locally

**Difficulty Level:** intermediate

**Estimated Time:** 30 minutes

---

## LLM Fundamentals (KB-W01-001)

**Week:** W01 - Prompt Engineering

**Category:** concept

**Description:** Understanding how LLMs work: tokenization attention mechanisms and generation strategies. Foundation for building AI applications.

**Learning Objectives:**
- Understand tokenization
- Learn attention mechanisms
- Explore generation strategies

**Difficulty Level:** beginner

**Estimated Time:** 60 minutes

---

## Prompt Design Patterns (KB-W01-002)

**Week:** W01 - Prompt Engineering

**Category:** concept

**Description:** Common prompt patterns: zero-shot few-shot chain-of-thought and instruction following. Core skill for application builders.

**Learning Objectives:**
- Master zero-shot prompting
- Implement few-shot examples
- Apply chain-of-thought

**Difficulty Level:** beginner

**Estimated Time:** 45 minutes

---

## Prompt Engineering Exercise (KB-W01-003)

**Week:** W01 - Prompt Engineering

**Category:** exercise

**Description:** Introduction to prompt engineering with Mistral-7B model. Learn system prompts and prompt engineering techniques.

**Learning Objectives:**
- Design effective system prompts
- Test prompt variations
- Measure output quality

**Difficulty Level:** beginner

**Estimated Time:** 90 minutes

---

## Temperature and Sampling (KB-W01-004)

**Week:** W01 - Prompt Engineering

**Category:** exercise

**Description:** Explore temperature top-p top-k sampling and their effects on generation diversity and quality.

**Learning Objectives:**
- Understand temperature effects
- Compare sampling strategies
- Tune generation parameters

**Difficulty Level:** beginner

**Estimated Time:** 60 minutes

---

## Data Engineering for RAG (KB-W02-001)

**Week:** W02 - RAG Foundations

**Category:** concept

**Description:** Data pipelines for RAG: ETL processes data quality validation lineage tracking and ingestion patterns.

**Learning Objectives:**
- Build data pipelines
- Validate data quality
- Track data lineage

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Embeddings Deep Dive (KB-W02-002)

**Week:** W02 - RAG Foundations

**Category:** concept

**Description:** Understanding embeddings: how they work semantic similarity and choosing embedding models for applications.

**Learning Objectives:**
- Understand vector representations
- Calculate similarity scores
- Visualize embedding spaces

**Prerequisites:** W01

**Difficulty Level:** beginner

**Estimated Time:** 75 minutes

---

## Embedding Models Comparison (KB-W02-003)

**Week:** W02 - RAG Foundations

**Category:** concept

**Description:** Compare embedding models: all-MiniLM-L6 vs BGE vs E5. Practical guide for application developers.

**Learning Objectives:**
- Benchmark embedding models
- Analyze dimensionality tradeoffs
- Select optimal embeddings

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Chunking Strategies (KB-W02-004)

**Week:** W02 - RAG Foundations

**Category:** concept

**Description:** Document chunking methods: fixed-size recursive semantic and token-aware. Critical for RAG application quality.

**Learning Objectives:**
- Implement chunking methods
- Compare chunk quality
- Optimize chunk sizes

**Prerequisites:** W01

**Difficulty Level:** beginner

**Estimated Time:** 60 minutes

---

## Simple RAG System (KB-W02-005)

**Week:** W02 - RAG Foundations

**Category:** exercise

**Description:** Build a simple RAG chatbot using LangChain and FAISS for FAQ-based question answering. First complete AI application.

**Learning Objectives:**
- Build basic RAG pipeline
- Implement vector retrieval
- Generate contextual responses

**Prerequisites:** W01

**Difficulty Level:** beginner

**Estimated Time:** 120 minutes

---

## Retrieval Strategies (KB-W03-001)

**Week:** W03 - RAG Production

**Category:** concept

**Description:** Advanced retrieval: hybrid search combining BM25 sparse retrieval with dense embeddings and reranking.

**Learning Objectives:**
- Implement hybrid search
- Apply cross-encoder reranking
- Optimize retrieval quality

**Prerequisites:** W02

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Context Window Management (KB-W03-002)

**Week:** W03 - RAG Production

**Category:** concept

**Description:** Handling long contexts: summarization chains map-reduce and context compression techniques.

**Learning Objectives:**
- Manage context limits
- Implement summarization
- Apply compression techniques

**Prerequisites:** W02

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## RAG Evaluation Metrics (KB-W03-003)

**Week:** W03 - RAG Production

**Category:** concept

**Description:** Understanding RAG metrics: retrieval (MRR NDCG Recall@K) and generation (faithfulness relevance).

**Learning Objectives:**
- Calculate retrieval metrics
- Measure generation quality
- Interpret evaluation scores

**Prerequisites:** W02

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## RAG System with Evaluation (KB-W03-004)

**Week:** W03 - RAG Production

**Category:** exercise

**Description:** Complete RAG system with model evaluation framework. Production-ready RAG application.

**Learning Objectives:**
- Build complete RAG system
- Evaluate multiple models
- Rank by composite scores

**Prerequisites:** W01 W02

**Difficulty Level:** intermediate

**Estimated Time:** 150 minutes

---

## Hallucination Detection (KB-W03-005)

**Week:** W03 - RAG Production

**Category:** exercise

**Description:** Implement hallucination detection: faithfulness scoring factual consistency and citation verification.

**Learning Objectives:**
- Detect hallucinations
- Score faithfulness
- Verify factual consistency

**Prerequisites:** W02

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## GreenTech RAG Assignment (KB-W03-006)

**Week:** W03 - RAG Production

**Category:** assignment

**Description:** Complete RAG assignment for GreenTech Marketplace customer support. Real-world business application.

**Learning Objectives:**
- Complete all 6 objectives
- Build production RAG
- Document findings

**Prerequisites:** W01 W02

**Difficulty Level:** intermediate

**Estimated Time:** 240 minutes

---

## Job Fitment Agent (KB-W03-007)

**Week:** W03 - RAG Production

**Category:** project

**Description:** AI-powered job fitment analysis agent. Analyzes job postings and provides fitment scores with skill gap identification.

**Learning Objectives:**
- Scrape job postings
- Analyze skill fitment
- Identify skill gaps

**Prerequisites:** W01 W02

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## LLM Security Fundamentals (KB-W06-001)

**Week:** W06 - Safety and Guardrails

**Category:** concept

**Description:** Understanding LLM vulnerabilities: prompt injection jailbreaks and data leakage.

**Learning Objectives:**
- Understand attack vectors
- Identify vulnerabilities
- Plan mitigations

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Content Moderation Strategies (KB-W06-002)

**Week:** W06 - Safety and Guardrails

**Category:** concept

**Description:** Approaches to content moderation: classification filtering and human-in-the-loop.

**Learning Objectives:**
- Implement classification
- Design filters
- Plan human review

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Input Validation Guards (KB-W06-003)

**Week:** W06 - Safety and Guardrails

**Category:** exercise

**Description:** Implement input validation: prompt injection detection PII filtering and input sanitization.

**Learning Objectives:**
- Detect prompt injection
- Filter PII
- Sanitize inputs

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Output Validation Guards (KB-W06-004)

**Week:** W06 - Safety and Guardrails

**Category:** exercise

**Description:** Implement output validation: toxicity filtering factuality checking and format enforcement.

**Learning Objectives:**
- Filter toxic content
- Check factuality
- Enforce output format

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Async Patterns for Agents (KB-W07-001)

**Week:** W07 - AI Agents

**Category:** concept

**Description:** AsyncIO patterns for concurrent agent execution. Parallel tool calls and non-blocking workflows.

**Learning Objectives:**
- Implement async/await
- Run parallel tool calls
- Design non-blocking agents

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Agent Architecture Patterns (KB-W07-002)

**Week:** W07 - AI Agents

**Category:** concept

**Description:** Understanding agent architectures: ReAct function calling and tool use patterns. Core of agentic workflows.

**Learning Objectives:**
- Understand ReAct pattern
- Implement function calling
- Design tool interfaces

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Agent Memory Systems (KB-W07-003)

**Week:** W07 - AI Agents

**Category:** concept

**Description:** Memory for agents: buffer memory summary memory vector-backed memory and episodic memory.

**Learning Objectives:**
- Implement memory types
- Compare memory strategies
- Design memory architecture

**Prerequisites:** W02

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Planning and Reasoning (KB-W07-004)

**Week:** W07 - AI Agents

**Category:** concept

**Description:** Agent planning: chain-of-thought tree-of-thought and plan-and-execute patterns.

**Learning Objectives:**
- Implement CoT prompting
- Apply tree-of-thought
- Design planning systems

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Tool Design Principles (KB-W07-005)

**Week:** W07 - AI Agents

**Category:** concept

**Description:** Designing effective tools: API design error handling and tool descriptions for agents.

**Learning Objectives:**
- Design tool interfaces
- Handle errors gracefully
- Write clear descriptions

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Basic Agent Implementation (KB-W07-006)

**Week:** W07 - AI Agents

**Category:** exercise

**Description:** Build a basic ReAct agent with tools using LangChain or OpenAI function calling.

**Learning Objectives:**
- Build ReAct agent
- Implement tool calling
- Test agent behavior

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## Multi-Tool Agent (KB-W07-007)

**Week:** W07 - AI Agents

**Category:** exercise

**Description:** Build an agent with multiple tools: search calculator code execution and file operations.

**Learning Objectives:**
- Integrate multiple tools
- Handle tool selection
- Manage tool errors

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 150 minutes

---

## MCP Integration (KB-W07-008)

**Week:** W07 - AI Agents

**Category:** exercise

**Description:** Integrate Model Context Protocol (MCP) servers for extended agent capabilities.

**Learning Objectives:**
- Connect MCP servers
- Use MCP tools
- Build MCP-enabled agent

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 120 minutes

---

## OpenAI Agent Builder Project (KB-W07-009)

**Week:** W07 - AI Agents

**Category:** assignment

**Description:** OpenAI Agent Builder project for automating workflows. Demonstrates agentic workflow mastery.

**Learning Objectives:**
- Build production agent
- Automate complex workflow
- Generate actionable outputs

**Prerequisites:** W03

**Difficulty Level:** advanced

**Estimated Time:** 300 minutes

---

## Vision-Language Models (KB-W08-001)

**Week:** W08 - Multimodal AI

**Category:** concept

**Description:** Understanding VLMs: architecture training and capabilities of models like BLIP LLaVA and GPT-4V.

**Learning Objectives:**
- Understand VLM architecture
- Compare model capabilities
- Select appropriate models

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Audio Processing with LLMs (KB-W08-002)

**Week:** W08 - Multimodal AI

**Category:** concept

**Description:** Speech-to-text text-to-speech and audio understanding with Whisper and similar models.

**Learning Objectives:**
- Process audio input
- Generate speech output
- Understand audio models

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Document Understanding (KB-W08-003)

**Week:** W08 - Multimodal AI

**Category:** concept

**Description:** Processing documents: OCR layout analysis and document Q&A with multimodal models.

**Learning Objectives:**
- Extract text from images
- Analyze document layout
- Answer document questions

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Image Captioning (KB-W08-004)

**Week:** W08 - Multimodal AI

**Category:** exercise

**Description:** Generate captions for images using vision-language models. Practical multimodal application.

**Learning Objectives:**
- Generate image captions
- Fine-tune captioning
- Evaluate caption quality

**Difficulty Level:** beginner

**Estimated Time:** 90 minutes

---

## PDF Q&A System (KB-W08-005)

**Week:** W08 - Multimodal AI

**Category:** exercise

**Description:** Question answering system for PDF documents using RAG. Document intelligence application.

**Learning Objectives:**
- Parse PDF documents
- Build document RAG
- Answer document questions

**Prerequisites:** W02

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## Speech to Image Pipeline (KB-W08-006)

**Week:** W08 - Multimodal AI

**Category:** exercise

**Description:** Convert speech to images using Whisper and Stable Diffusion. Creative multimodal application.

**Learning Objectives:**
- Transcribe speech
- Generate images
- Build multimodal pipeline

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 150 minutes

---

## Agentic RAG Architecture (KB-W09-001)

**Week:** W09 - Agentic RAG

**Category:** concept

**Description:** Understanding agentic RAG: query routing self-correction and adaptive retrieval. Next-gen RAG applications.

**Learning Objectives:**
- Understand agentic RAG
- Design routing logic
- Implement self-correction

**Prerequisites:** W03 W07

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Query Understanding (KB-W09-002)

**Week:** W09 - Agentic RAG

**Category:** concept

**Description:** Advanced query processing: decomposition rewriting and intent classification for RAG.

**Learning Objectives:**
- Decompose complex queries
- Rewrite for retrieval
- Classify query intent

**Prerequisites:** W03

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Retrieval Agents (KB-W09-003)

**Week:** W09 - Agentic RAG

**Category:** concept

**Description:** Building retrieval agents: when to retrieve what to retrieve and how to combine results.

**Learning Objectives:**
- Build retrieval agents
- Implement adaptive retrieval
- Combine multiple sources

**Prerequisites:** W03 W07

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Agentic RAG with LlamaIndex (KB-W09-004)

**Week:** W09 - Agentic RAG

**Category:** exercise

**Description:** Build agentic RAG systems with LlamaIndex framework including query routing and tool calling.

**Learning Objectives:**
- Build with LlamaIndex
- Implement query routing
- Add tool calling

**Prerequisites:** W03

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## Self-Correcting RAG (KB-W09-005)

**Week:** W09 - Agentic RAG

**Category:** exercise

**Description:** Implement self-correcting RAG with hallucination detection and query refinement loops.

**Learning Objectives:**
- Detect retrieval failures
- Implement correction loops
- Refine queries

**Prerequisites:** W03

**Difficulty Level:** advanced

**Estimated Time:** 150 minutes

---

## Multi-Agent Architecture (KB-W10-001)

**Week:** W10 - Multi-Agent Systems

**Category:** concept

**Description:** Designing multi-agent systems: coordination communication and task delegation.

**Learning Objectives:**
- Design multi-agent architectures
- Implement coordination
- Handle communication

**Prerequisites:** W07 W09

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Agent Orchestration Patterns (KB-W10-002)

**Week:** W10 - Multi-Agent Systems

**Category:** concept

**Description:** Orchestration patterns: supervisor hierarchical and collaborative agent coordination.

**Learning Objectives:**
- Implement supervisor pattern
- Design hierarchies
- Enable collaboration

**Prerequisites:** W07

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## State Management for Agents (KB-W10-003)

**Week:** W10 - Multi-Agent Systems

**Category:** concept

**Description:** Managing state in agent systems: checkpointing rollback and persistent state.

**Learning Objectives:**
- Implement checkpointing
- Handle rollback
- Persist agent state

**Prerequisites:** W07

**Difficulty Level:** advanced

**Estimated Time:** 75 minutes

---

## Advanced Agentic RAG (KB-W10-004)

**Week:** W10 - Multi-Agent Systems

**Category:** exercise

**Description:** Advanced agentic RAG with multi-document agents and complex reasoning.

**Learning Objectives:**
- Build multi-document agents
- Implement complex reasoning
- Handle advanced queries

**Prerequisites:** W09

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## Multi-Agent RAG System (KB-W10-005)

**Week:** W10 - Multi-Agent Systems

**Category:** exercise

**Description:** Build multi-agent RAG with specialized retrieval analysis and synthesis agents.

**Learning Objectives:**
- Design specialized agents
- Coordinate retrieval
- Synthesize results

**Prerequisites:** W07 W09

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## Research Assistant System (KB-W10-006)

**Week:** W10 - Multi-Agent Systems

**Category:** project

**Description:** Multi-agent research assistant that searches analyzes and synthesizes information autonomously.

**Learning Objectives:**
- Build autonomous researcher
- Coordinate multiple agents
- Generate research reports

**Prerequisites:** W07 W09

**Difficulty Level:** advanced

**Estimated Time:** 300 minutes

---

## Vector Database Fundamentals (KB-W02-006)

**Week:** W02 - Vector Infrastructure

**Category:** concept

**Description:** Introduction to vector databases: indexing algorithms ANN search and FAISS internals. Core inference infrastructure.

**Learning Objectives:**
- Understand ANN algorithms
- Configure FAISS indices
- Optimize search parameters

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Vector DB Comparison (KB-W02-007)

**Week:** W02 - Vector Infrastructure

**Category:** exercise

**Description:** Compare vector databases: FAISS vs ChromaDB vs Qdrant. Benchmark performance for inference optimization.

**Learning Objectives:**
- Benchmark vector databases
- Compare query latencies
- Evaluate feature sets

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Quantization Fundamentals (KB-W05-001)

**Week:** W05 - Inference Optimization

**Category:** concept

**Description:** Understanding quantization: INT8 INT4 GGUF AWQ and GPTQ formats. Critical for inference cost reduction.

**Learning Objectives:**
- Understand quantization types
- Compare format tradeoffs
- Select appropriate format

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Inference Optimization Techniques (KB-W05-002)

**Week:** W05 - Inference Optimization

**Category:** concept

**Description:** Optimizing LLM inference: KV caching batching speculative decoding and continuous batching.

**Learning Objectives:**
- Understand KV caching
- Implement batching
- Apply optimization techniques

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Cost Optimization Strategies (KB-W05-003)

**Week:** W05 - Inference Optimization

**Category:** concept

**Description:** Token budgeting caching strategies model routing and cost-aware architecture design.

**Learning Objectives:**
- Calculate token costs
- Implement caching
- Design cost-aware systems

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Inference Throughput Analysis (KB-W05-004)

**Week:** W05 - Inference Optimization

**Category:** concept

**Description:** Understanding throughput: tokens per second batching efficiency and latency vs throughput tradeoffs.

**Learning Objectives:**
- Measure throughput
- Analyze batching efficiency
- Optimize for workload

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Model Quantization (KB-W05-005)

**Week:** W05 - Inference Optimization

**Category:** exercise

**Description:** Quantize models using GGUF and AWQ. Measure latency and quality tradeoffs for production deployment.

**Learning Objectives:**
- Quantize models
- Benchmark performance
- Analyze quality impact

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## Inference Server Setup (KB-W05-006)

**Week:** W05 - Inference Optimization

**Category:** exercise

**Description:** Set up vLLM or TGI for production inference with benchmarking. Core infrastructure skill.

**Learning Objectives:**
- Deploy inference server
- Configure optimization
- Benchmark throughput

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 150 minutes

---

## Latency Profiling (KB-W05-007)

**Week:** W05 - Inference Optimization

**Category:** exercise

**Description:** Profile and optimize LLM pipeline latency: tokenization inference and decoding.

**Learning Objectives:**
- Profile pipeline stages
- Identify bottlenecks
- Optimize latency

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Streaming with SSE (KB-W05-008)

**Week:** W05 - Inference Optimization

**Category:** exercise

**Description:** Implement Server-Sent Events for streaming LLM responses. Real-time token-by-token output to clients.

**Learning Objectives:**
- Implement SSE endpoints
- Stream LLM tokens
- Handle client connections

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## WebSocket Real-time AI (KB-W05-009)

**Week:** W05 - Inference Optimization

**Category:** exercise

**Description:** Build bidirectional real-time AI communication with WebSockets. Interactive agent conversations.

**Learning Objectives:**
- Implement WebSocket server
- Handle bidirectional messages
- Build interactive AI

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## Token Cost Calculator (KB-W05-010)

**Week:** W05 - Inference Optimization

**Category:** exercise

**Description:** Build token cost calculator and optimizer for production LLM applications.

**Learning Objectives:**
- Calculate token costs
- Optimize prompts
- Budget for production

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## Inference Benchmark Dashboard (KB-W05-011)

**Week:** W05 - Inference Optimization

**Category:** project

**Description:** Interactive dashboard comparing inference providers: latency cost and quality metrics.

**Learning Objectives:**
- Benchmark providers
- Visualize metrics
- Compare cost-performance

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## GRPO Fundamentals (KB-W11-001)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** concept

**Description:** Understanding Group Relative Policy Optimization (GRPO): reinforcement learning fine-tuning for LLMs. Alternative to RLHF for aligning models.

**Learning Objectives:**
- Understand GRPO algorithm
- Compare to RLHF
- Learn policy optimization

**Prerequisites:** W04

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Reward Functions (KB-W11-002)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** concept

**Description:** Designing reward functions for reinforcement learning: explicit rewards implicit rewards and reward shaping.

**Learning Objectives:**
- Design reward functions
- Implement reward shaping
- Evaluate reward quality

**Prerequisites:** W04

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## LLM as Judge (KB-W11-003)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** concept

**Description:** Using LLMs as reward models: LLM-as-a-judge pattern for evaluating model outputs without explicit reward functions.

**Learning Objectives:**
- Implement LLM judge
- Design evaluation prompts
- Use for reward signals

**Prerequisites:** W04

**Difficulty Level:** intermediate

**Estimated Time:** 90 minutes

---

## Reward Hacking (KB-W11-004)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** concept

**Description:** Understanding reward hacking: when models optimize for reward signal instead of intended behavior. Mitigation strategies.

**Learning Objectives:**
- Identify reward hacking
- Design robust rewards
- Mitigate gaming

**Prerequisites:** W04

**Difficulty Level:** advanced

**Estimated Time:** 60 minutes

---

## GRPO Loss Calculation (KB-W11-005)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** concept

**Description:** Calculating loss in GRPO: policy gradient computation group relative comparisons and optimization objective.

**Learning Objectives:**
- Calculate GRPO loss
- Implement policy gradients
- Optimize objective

**Prerequisites:** W04

**Difficulty Level:** advanced

**Estimated Time:** 90 minutes

---

## Wordle Master with GRPO (KB-W11-006)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** exercise

**Description:** Complete GRPO training project: train an LLM to master Wordle using reinforcement fine-tuning with GRPO algorithm.

**Learning Objectives:**
- Implement GRPO training
- Train Wordle model
- Evaluate performance

**Prerequisites:** W04

**Difficulty Level:** advanced

**Estimated Time:** 240 minutes

---

## GRPO Group Task (KB-W11-007)

**Week:** W11 - Reinforcement Fine-Tuning

**Category:** assignment

**Description:** Group assignment: practice reinforcement fine-tuning with GRPO by modifying DeepLearning.AI lessons. Complete Wordle training project.

**Learning Objectives:**
- Complete GRPO lessons
- Modify training code
- Train Wordle model

**Prerequisites:** W04

**Difficulty Level:** advanced

**Estimated Time:** 300 minutes

---

## Transfer Learning for LLMs (KB-W04-001)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Understanding transfer learning: pre-training vs fine-tuning when to fine-tune vs use RAG.

**Learning Objectives:**
- Understand transfer learning
- Compare fine-tuning vs RAG
- Choose appropriate approach

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## PEFT Techniques Overview (KB-W04-002)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Parameter-efficient fine-tuning: LoRA QLoRA adapters and prefix tuning explained.

**Learning Objectives:**
- Understand PEFT methods
- Compare adapter approaches
- Select optimal technique

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Dataset Preparation (KB-W04-003)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Preparing datasets for fine-tuning: formatting cleaning and creating instruction datasets.

**Learning Objectives:**
- Format training data
- Clean datasets
- Create instruction sets

**Prerequisites:** W01

**Difficulty Level:** beginner

**Estimated Time:** 60 minutes

---

## Training Dynamics (KB-W04-004)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Understanding training: loss curves learning rates and convergence analysis.

**Learning Objectives:**
- Analyze loss curves
- Tune learning rates
- Monitor convergence

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## LoRA Fine-tuning (KB-W04-005)

**Week:** W04 - Fine-tuning

**Category:** exercise

**Description:** Fine-tune a model using LoRA on a custom dataset. Understand rank alpha and target modules.

**Learning Objectives:**
- Configure LoRA parameters
- Fine-tune on custom data
- Evaluate improvements

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 180 minutes

---

## QLoRA Fine-tuning (KB-W04-006)

**Week:** W04 - Fine-tuning

**Category:** exercise

**Description:** Memory-efficient fine-tuning with QLoRA using 4-bit quantization.

**Learning Objectives:**
- Apply 4-bit quantization
- Configure QLoRA
- Train on limited hardware

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 180 minutes

---

## Fine-tuning vs RAG Analysis (KB-W04-007)

**Week:** W04 - Fine-tuning

**Category:** exercise

**Description:** Empirical comparison: when fine-tuning beats RAG and vice versa with cost-benefit analysis.

**Learning Objectives:**
- Compare approaches empirically
- Analyze cost-benefit
- Document tradeoffs

**Prerequisites:** W02 W03

**Difficulty Level:** advanced

**Estimated Time:** 120 minutes

---

## Evaluation for Fine-tuned Models (KB-W04-008)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Evaluating fine-tuned models: benchmark selection metrics and A/B testing.

**Learning Objectives:**
- Select benchmarks
- Compute metrics
- Design A/B tests

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 75 minutes

---

## Domain-Specific Fine-tuning (KB-W04-009)

**Week:** W04 - Fine-tuning

**Category:** project

**Description:** Fine-tune a model for a specific domain with full evaluation pipeline.

**Learning Objectives:**
- Fine-tune for domain
- Evaluate thoroughly
- Document improvements

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 360 minutes

---

## Constitutional AI Principles (KB-W04-010)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Understanding constitutional AI: self-critique RLHF and alignment techniques.

**Learning Objectives:**
- Understand RLHF
- Learn constitutional AI
- Apply alignment principles

**Prerequisites:** W01

**Difficulty Level:** advanced

**Estimated Time:** 75 minutes

---

## Open vs Closed Models (KB-W04-011)

**Week:** W04 - Fine-tuning

**Category:** concept

**Description:** Comparing open-source vs closed models: capabilities costs and strategic considerations.

**Learning Objectives:**
- Compare model types
- Analyze costs
- Make strategic decisions

**Prerequisites:** W01

**Difficulty Level:** intermediate

**Estimated Time:** 60 minutes

---

## RAG vs Fine-tuning Decision Framework (KB-N/A-001)

**Week:** N/A - Blog

**Category:** article

**Description:** Technical blog post on when to use RAG vs fine-tuning with real-world examples.

**Learning Objectives:**
- Articulate tradeoffs
- Provide framework
- Share examples

**Prerequisites:** W03 W04

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## Agentic Workflows in Production (KB-N/A-002)

**Week:** N/A - Blog

**Category:** article

**Description:** Article on deploying agentic workflows: lessons learned and best practices.

**Learning Objectives:**
- Share production insights
- Document patterns
- Provide guidance

**Prerequisites:** W07 W09 W10

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## The Three Layers of AI (KB-N/A-003)

**Week:** N/A - Blog

**Category:** article

**Description:** Article explaining AI stack layers based on Andrew Ng's framework with portfolio perspective.

**Learning Objectives:**
- Explain AI stack
- Connect to portfolio
- Provide perspective

**Prerequisites:** W01-W11

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## LLM Inference Economics (KB-N/A-004)

**Week:** N/A - Blog

**Category:** article

**Description:** Deep dive into inference costs throughput and optimization strategies for practitioners.

**Learning Objectives:**
- Analyze economics
- Provide optimization guide
- Share data

**Prerequisites:** W05 W11

**Difficulty Level:** advanced

**Estimated Time:** 180 minutes

---

## Product Case Study - Job Fitment Agent (KB-N/A-005)

**Week:** N/A - Blog

**Category:** article

**Description:** User research to AI solution case study. Demonstrates user empathy and product thinking.

**Learning Objectives:**
- Document user needs
- Show solution process
- Measure outcomes

**Prerequisites:** W03 W07

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## Product Case Study - GreenTech RAG (KB-N/A-006)

**Week:** N/A - Blog

**Category:** article

**Description:** End-to-end case study of building customer support RAG. From problem to production.

**Learning Objectives:**
- Document business problem
- Show technical solution
- Present results

**Prerequisites:** W03

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## Core LLM Concepts Explained (KB-N/A-007)

**Week:** N/A - Blog

**Category:** article

**Description:** Educational article: Tokens Embeddings Attention Layers Tensors Parameters - the complete LLM pipeline.

**Learning Objectives:**
- Explain fundamentals
- Use clear analogies
- Provide code examples

**Prerequisites:** W00

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

## AI Portfolio Overview (KB-N/A-008)

**Week:** N/A - Talks

**Category:** presentation

**Description:** Presentation deck showcasing AI portfolio using three-layer framework.

**Learning Objectives:**
- Create compelling narrative
- Showcase projects
- Demonstrate expertise

**Prerequisites:** W00-W11

**Difficulty Level:** intermediate

**Estimated Time:** 120 minutes

---

