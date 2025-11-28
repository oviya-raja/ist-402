## Objective 5: Model Evaluation & Ranking

### 🎯 Goal

Evaluate 6 question-answering models using the RAG pipeline, compare their performance using **5 evaluation metrics**, and rank models to identify the best performer based on weighted scoring.

<details>
<summary><b>📥 Prerequisites</b> (Click to expand)</summary>

| Item | Source | Required | Description |
|------|--------|----------|-------------|
| `qa_database` | Objective 2 | ✅ Yes | Ground truth answers for comparison |
| `embed_query()` | Objective 3 | ✅ Yes | For semantic similarity calculation |
| `rag_query()` | Objective 4 | ✅ Yes | Complete RAG pipeline for dynamic context |
| `search_faiss()`, `format_context()` | Objective 4 | ✅ Yes | RAG pipeline components |

**Note:** Requires Objectives 1-4 completed. Achieves **100% component reuse**.

</details>

<br>

<details>
<summary><b>📊 The 5 Evaluation Metrics</b> (Click to expand)</summary>

### 1. Accuracy (F1 Score) - Weight: 25%
**What it measures:** Token-level overlap between model answer and ground truth

**Formula:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**Calculation:**
- Tokenize both answer and expected answer
- Calculate precision: (matching tokens) / (total tokens in answer)
- Calculate recall: (matching tokens) / (total tokens in expected)
- Compute F1 score (0-1 range)

**Only computed for:** Answerable questions (unanswerable have no expected answer)

---

### 2. Confidence Handling - Weight: 20%
**What it measures:** Whether model appropriately indicates uncertainty

**Scoring Logic:**

**For Answerable Questions:**
- Higher raw confidence → Higher score
- Score = raw_confidence (0-1)

**For Unanswerable Questions:**
- Model abstains ("I don't know", "unknown", "cannot answer") → **Score: 1.0** ✅
- Low confidence (< 0.3) → **Score: 0.8** ✅
- Medium confidence (0.3-0.5) → **Score: 0.5** ⚠️
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
Speed = 1 - (response_time_ms / max_acceptable_time_ms)
```

**Calculation:**
- Measure time from query to answer (milliseconds)
- Normalize against max acceptable time (e.g., 5000ms)
- Faster responses = higher score
- Range: 0-1 (1 = instant, 0 = very slow)

**Computed for:** ALL questions

---

### 5. Robustness - Weight: 15%
**What it measures:** Edge case handling and error recovery

**Scoring Logic:**
- **Error during inference** → Score: 0.0 ❌
- **Answer too short** (< 2 words) → Score: 0.2 ⚠️
- **Answer too long** (> 100 words) → Score: 0.5 ⚠️ (possible hallucination)
- **Unanswerable + abstains** → Score: 1.0 ✅ (correct behavior)
- **Unanswerable + long answer** (> 50 words) → Score: 0.2 ❌ (hallucinating)
- **Normal answer** → Score: 1.0 ✅

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

| Rank | Model Name | Model ID | Type | Size |
|------|-----------|----------|------|------|
| - | T5-QA-Generative | consciousAI/question-answering-generative-t5-v1-base-s-q-c | text2text-generation | base |
| - | RoBERTa-SQuAD2 | deepset/roberta-base-squad2 | question-answering | base |
| - | BERT-Large-SQuAD | google-bert/bert-large-cased-whole-word-masking-finetuned-squad | question-answering | large |
| - | DistilBERT-SQuAD | distilbert-base-uncased-distilled-squad | question-answering | small |
| - | BERT-Tiny-SQuAD | mrm8488/bert-tiny-finetuned-squadv2 | question-answering | tiny |
| - | MiniLM-SQuAD | deepset/minilm-uncased-squad2 | question-answering | small |

**Note:** Rankings determined by Final Score after evaluation.

</details>

<br>

<details>
<summary><b>📋 Test Questions</b> (Click to expand)</summary>

**Answerable (5 questions):**
1. "What is your return policy?"
2. "How long does shipping take?"
3. "What are your customer service hours?"
4. "Do you offer warranty on products?"
5. "How can I track my order?"

**Unanswerable (3 questions):**
1. "What is the CEO's phone number?"
2. "Will you have a Black Friday sale?"
3. "How do prices compare to Amazon?"

**Why this split:**
- Answerable questions test: Accuracy, Quality
- Unanswerable questions test: Confidence Handling, Robustness
- All questions test: Speed

</details>

<br>

<details>
<summary><b>🔄 Evaluation Process</b> (Click to expand)</summary>

**For Each Model:**
1. Load model from HuggingFace
2. For each test question:
   - Get RAG context using `rag_query()` (reuses Obj 4)
   - Run model inference with retrieved context
   - Calculate all 5 metrics
   - Store results

**For Each Question:**
- **Context Retrieval:** `rag_query()` → uses `embed_query()` (Obj 3) + `search_faiss()` (Obj 4)
- **Answer Generation:** Model inference with context
- **Metric Calculation:**
  - Accuracy: F1 score vs ground truth
  - Confidence: Extract from model output
  - Quality: `embed_query()` for semantic similarity (reuses Obj 3)
  - Speed: Measure response time
  - Robustness: Check answer length, errors, abstention

**After All Models:**
- Aggregate metrics per model
- Calculate Final Scores
- Rank models
- Save to `model_rankings.csv`

</details>

<br>

<details>
<summary><b>📤 Outputs</b> (Click to expand)</summary>

**Files Created:**
- `model_rankings.csv` - Final rankings with all metrics

**Global Variables:**
- `rankings_df` - DataFrame with model rankings
- `model_evaluations` - List of ModelMetrics objects

**CSV Columns:**
| Rank | Model | Accuracy | Confidence | Quality | Speed | Robustness | Final_Score |

</details>

<br>

<details>
<summary><b>🔗 Component Reuse</b> (Click to expand)</summary>

**100% Reuse from Previous Objectives:**

| Component | From | Used For |
|-----------|------|----------|
| `rag_query()` | Obj 4 | Dynamic context retrieval per question |
| `embed_query()` | Obj 3 | **Semantic similarity metric** (Quality) |
| `search_faiss()` | Obj 4 | Via `rag_query()` |
| `format_context()` | Obj 4 | Via `rag_query()` |
| `qa_database` | Obj 2 | Ground truth answers |
| `faiss_index` | Obj 3 | Via `search_faiss()` |

**Key Insight:** The `embed_query()` function is reused for BOTH:
1. RAG retrieval (Objective 4)
2. Semantic similarity calculation (Objective 5)

This demonstrates true modular design with zero code duplication.

</details>

<br>

<details>
<summary><b>✅ Verification</b> (Click to expand)</summary>

Run `verify_objective5()` to check:
- ✅ `rankings_df` exists with 6 models
- ✅ `model_rankings.csv` file created
- ✅ All 5 metrics present (Accuracy, Confidence, Quality, Speed, Robustness)
- ✅ Final_Score calculated
- ✅ Models ranked by Final_Score (descending)

</details>

<br>

---
**Next Step:** Proceed to Objective 6 for system analysis and recommendations.
