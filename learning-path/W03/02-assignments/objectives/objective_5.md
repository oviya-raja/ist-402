## Objective 5: Model Evaluation & Ranking

### 🎯 Goal

Evaluate 6 question-answering models using the RAG pipeline, compare their performance using **5 evaluation metrics**, and rank models to identify the best performer based on weighted scoring.

<details>
<summary><b>📥 Prerequisites</b> (Click to expand)</summary>

| Item | Source | Required | Description |
|------|--------|----------|-------------|
| `env` | Objective 0 | ✅ Yes | Environment configuration and timing system |
| `system_prompt` | Objective 1 | ✅ Yes | System prompt for context |
| `qa_database` | Objective 2 | ✅ Yes | Ground truth answers for comparison |
| `embed_query()` | Objective 3 | ✅ Yes | For semantic similarity calculation (Quality metric) |
| `rag_query()` | Objective 4 | ✅ Yes | Complete RAG pipeline for dynamic context retrieval |
| `faiss_index` | Objective 3 | ✅ Yes | Vector index (used via rag_query) |

**Note:** Requires Objectives 0-4 completed. Achieves **100% component reuse**.

</details>

<br>

<details>
<summary><b>📊 The 5 Evaluation Metrics</b> (Click to expand)</summary>

### 1. Accuracy (BERTScore F1) - Weight: 25%
**What it measures:** Semantic similarity between model answer and ground truth using BERTScore

**Why BERTScore instead of token F1:**
- Token F1 fails on paraphrases: "30 day return" vs "30-day refund" = low score
- BERTScore understands semantics: same meaning = high score
- Better for RAG evaluation where answers may be paraphrased

**Implementation:**
- Uses **BERTScore** with **DeBERTa-large-mnli** model
- Calculates semantic F1 score (0-1 range)
- Batch processing for efficiency
- Rescaled with baseline for better calibration

**Only computed for:** Answerable questions (unanswerable have no expected answer)

---

### 2. Confidence (Calibration) - Weight: 20%
**What it measures:** Whether model appropriately indicates uncertainty (calibration)

**Scoring Logic:**

**For Answerable Questions:**
- Empty answer (< 3 chars) → **Score: 0.2** ⚠️
- Non-empty answer → **Score: raw_confidence** (0-1)

**For Unanswerable Questions:**
- Empty answer (abstains) → **Score: 1.0** ✅ (correct behavior)
- Low confidence (< 0.3) → **Score: 0.9** ✅
- Medium confidence (0.3-0.5) → **Score: 0.6** ⚠️
- High confidence (> 0.5) → **Score: 0.2** ❌ (overconfident)

**Computed for:** ALL questions (both answerable and unanswerable)

---

### 3. Quality (Semantic Similarity) - Weight: 25%
**What it measures:** Semantic meaning similarity using embeddings

**Formula:**
```
Quality = cosine_similarity(embed_query(answer), embed_query(expected))
```

**Calculation:**
- Uses `embed_query()` from Objective 3 (component reuse!)
- Embed both answer and expected answer
- Calculate cosine similarity between embeddings
- Range: 0-1 (1 = identical meaning)

**Only computed for:** Answerable questions

**Key Insight:** Reuses `embed_query()` from Objective 3 - same function used in RAG retrieval!

---

### 4. Speed - Weight: 15%
**What it measures:** Response time performance

**Formula:**
```
Speed = 1 - (response_time_ms / 2000)
```

**Calculation:**
- Measure time from query to answer (milliseconds)
- Normalize against 2000ms threshold
- 0ms = 1.0 (perfect), 2000ms+ = 0.0 (too slow)
- Faster responses = higher score
- Range: 0-1 (clamped)

**Computed for:** ALL questions

---

### 5. Robustness - Weight: 15%
**What it measures:** Edge case handling and error recovery

**Scoring Logic:**

**For Answerable Questions:**
- **Error during inference** → Score: 0.0 ❌
- **Empty answer** (< 3 chars) → Score: 0.3 ⚠️
- **Long answer** (> 50 words) → Score: 0.7 ⚠️ (possible verbosity)
- **Normal answer** (3-50 words) → Score: 1.0 ✅

**For Unanswerable Questions:**
- **Error during inference** → Score: 0.0 ❌
- **Empty answer** (abstains) → Score: 1.0 ✅ (correct behavior)
- **Long answer** (> 30 words) → Score: 0.2 ❌ (hallucinating)
- **Short answer** (3-30 words) → Score: 0.6 ⚠️

**Computed for:** ALL questions

</details>

<br>

<details>
<summary><b>🏆 Ranking Calculation</b> (Click to expand)</summary>

### Step 1: Calculate Per-Question Metrics
For each question, compute all 5 metrics:
- Accuracy (F1) - if answerable
- Confidence - always
- Quality (Semantic) - if answerable
- Speed - always
- Robustness - always

### Step 2: Aggregate Per Model
For each model, average each metric across all questions:
```
avg_accuracy = mean(accuracy_scores for answerable questions)
avg_confidence = mean(confidence_scores for all questions)
avg_quality = mean(quality_scores for answerable questions)
avg_speed = mean(speed_scores for all questions)
avg_robustness = mean(robustness_scores for all questions)
```

### Step 3: Calculate Final Score
Weighted combination of all 5 metrics:

```
Final Score = (Accuracy × 0.25) + 
              (Confidence × 0.20) + 
              (Quality × 0.25) + 
              (Speed × 0.15) + 
              (Robustness × 0.15)
```

**Weight Distribution:**
- **Accuracy + Quality = 50%** (correctness and meaning)
- **Confidence = 20%** (uncertainty handling)
- **Speed + Robustness = 30%** (performance and reliability)

### Step 4: Rank Models
Sort all models by Final Score (descending):
- Rank 1 = Highest Final Score (Best Model)
- Rank 2 = Second highest
- ... and so on

### Example Calculation:

**Model: RoBERTa-SQuAD2**
- Accuracy: 0.847
- Confidence: 0.756
- Quality: 0.891
- Speed: 0.823
- Robustness: 0.950

**Final Score:**
```
(0.847 × 0.25) + (0.756 × 0.20) + (0.891 × 0.25) + (0.823 × 0.15) + (0.950 × 0.15)
= 0.212 + 0.151 + 0.223 + 0.123 + 0.143
= 0.852
```

</details>

<br>

<details>
<summary><b>🤖 Models Evaluated</b> (Click to expand)</summary>

| Rank | Model Name | Model ID | Type | Size | Params |
|------|-----------|----------|------|------|--------|
| - | T5-QA-Generative | consciousAI/question-answering-generative-t5-v1-base-s-q-c | text2text-generation | Base | 220M |
| - | RoBERTa-SQuAD2 | deepset/roberta-base-squad2 | question-answering | Base | 125M |
| - | BERT-Large-SQuAD | google-bert/bert-large-cased-whole-word-masking-finetuned-squad | question-answering | Large | 340M |
| - | DistilBERT-SQuAD | distilbert-base-uncased-distilled-squad | question-answering | Small | 66M |
| - | BERT-Tiny-SQuAD | mrm8488/bert-tiny-finetuned-squadv2 | question-answering | Tiny | 4M |
| - | MiniLM-SQuAD | deepset/minilm-uncased-squad2 | question-answering | Small | 33M |

**Note:** Rankings determined by Final Score after evaluation.

</details>

<br>

<details>
<summary><b>📋 Test Questions</b> (Click to expand)</summary>

**Answerable (5 questions):**
1. "What is your return policy?" → Expected: "30-day return policy with full refund"
2. "How long does shipping take?" → Expected: "Standard shipping takes 5-7 business days"
3. "What are your customer service hours?" → Expected: "Monday to Friday 9am to 5pm"
4. "Do you offer warranty on products?" → Expected: "1 year warranty on all electronics"
5. "How can I track my order?" → Expected: "Use tracking number on our website"

**Unanswerable (3 questions):**
1. "What is the CEO's phone number?" → Not in knowledge base
2. "Will you have a Black Friday sale?" → Not in knowledge base
3. "How do prices compare to Amazon?" → Not in knowledge base

**Why this split:**
- Answerable questions test: Accuracy, Quality
- Unanswerable questions test: Confidence Handling, Robustness
- All questions test: Speed

</details>

<br>

<details>
<summary><b>🔄 Evaluation Process</b> (Click to expand)</summary>

**3-Stage Caching System:**
1. **Contexts Cache** (`contexts.csv`) - RAG contexts from `rag_query()` (Obj 4)
2. **Embeddings Cache** (`embeddings.csv`) - Embeddings computed via `embed_query()` (Obj 3)
3. **Responses Cache** (`raw_responses.csv`) - Model inference results (6 models × 8 questions)

**For Each Model:**
1. Load model from HuggingFace
2. For each test question:
   - Get RAG context using `rag_query()` (reuses Obj 4, cached)
   - Run model inference with retrieved context
   - Measure response time
   - Store raw response and confidence

**Metric Calculation (Batch Processing):**
- Uses **ScorePack** class for unified scoring
- **Accuracy:** BERTScore F1 (DeBERTa-large-mnli) - batch processed
- **Quality:** Cosine similarity using `embed_query()` (reuses Obj 3)
- **Confidence:** Calibration scoring based on answerability
- **Speed:** Normalized latency (2000ms threshold)
- **Robustness:** Error handling and answer length checks

**After All Models:**
- Aggregate metrics per model (average across questions)
- Calculate Final Scores (weighted combination)
- Rank models by Final Score
- Save to `model_rankings.csv`, `model_responses.csv`, `evaluation_summary.txt`

</details>

<br>

<details>
<summary><b>📤 Outputs</b> (Click to expand)</summary>

**Files Created:**
- `model_rankings.csv` - Final rankings with all metrics
- `model_responses.csv` - Detailed per-question results
- `evaluation_summary.txt` - Text summary with winner
- `contexts.csv` - Cached RAG contexts (cache)
- `embeddings.csv` - Cached embeddings (cache)
- `raw_responses.csv` - Cached model responses (cache)

**Global Variables:**
- `rankings_df` - DataFrame with model rankings (sorted by Final_Score)
- `detailed_df` - DataFrame with per-question detailed results

**CSV Columns (model_rankings.csv):**
| Rank | Model | Accuracy | Quality | Confidence | Speed | Robustness | Final_Score |

**Helper Functions:**
- `run_evaluation(force_refresh=False)` - Full evaluation pipeline
- `recalculate_metrics_only()` - Recalculate metrics from cache (~30 sec)
- `clean()` - Delete all cache files
- `show_cache_status()` - Display cache file status

</details>

<br>

<details>
<summary><b>🔗 Component Reuse</b> (Click to expand)</summary>

**100% Reuse from Previous Objectives:**

| Component | From | Used For |
|-----------|------|----------|
| `env` | Obj 0 | Environment configuration and timing system |
| `rag_query()` | Obj 4 | Dynamic context retrieval per question (cached) |
| `embed_query()` | Obj 3 | **Semantic similarity metric** (Quality) + embeddings cache |
| `qa_database` | Obj 2 | Ground truth answers |
| `faiss_index` | Obj 3 | Via `rag_query()` → `search_faiss()` |
| `system_prompt` | Obj 1 | Context for RAG pipeline |

**Key Insights:**
1. **`embed_query()` dual use:** Reused for BOTH RAG retrieval (Obj 4) AND semantic similarity (Obj 5)
2. **ScorePack class:** Unified scoring system with batch processing and embedding caching
3. **3-stage caching:** Contexts, embeddings, and responses cached for fast re-runs
4. **Batch BERTScore:** Efficient batch processing using DeBERTa-large-mnli model

This demonstrates true modular design with zero code duplication and efficient caching.

</details>

<br>

<details>
<summary><b>✅ Verification</b> (Click to expand)</summary>

**Verification:**
- ✅ `rankings_df` exists with 6 models
- ✅ `model_rankings.csv` file created
- ✅ `model_responses.csv` with detailed per-question results
- ✅ All 5 metrics present (Accuracy, Quality, Confidence, Speed, Robustness)
- ✅ Final_Score calculated using weighted combination
- ✅ Models ranked by Final_Score (descending)

**Performance:**
- **First run:** ~10-15 min (downloads models, runs inference, computes metrics)
- **Subsequent runs:** ~30 sec (loads from cache, recalculates metrics only)
- **Recalculate only:** Use `recalculate_metrics_only()` to update metrics from cached responses

</details>

<br>

---
**Next Step:** Proceed to Objective 6 for system analysis and recommendations.
