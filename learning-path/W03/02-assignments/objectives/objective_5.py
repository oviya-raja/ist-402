# ============================================================================
# OBJECTIVE 5: MODEL EVALUATION (ScorePack)
# ============================================================================
#
# WHAT THIS DOES:
#   - Evaluates 6 QA models on our RAG pipeline
#   - Uses 5 metrics: Accuracy, Quality, Confidence, Speed, Robustness
#   - Ranks models by weighted final score
#
# 100% REUSE FROM PREVIOUS OBJECTIVES:
#   - env (Objective 0) - Environment configuration and timing
#   - system_prompt (Objective 1) - System prompt for context
#   - qa_database (Objective 2) - Ground truth answers
#   - embed_query() (Objective 3) - For semantic similarity metric
#   - rag_query() (Objective 4) - Complete RAG pipeline for dynamic context
#
# WHY SCOREPACK:
#   - Uses BERTScore (semantic F1) instead of token F1 for better RAG evaluation
#   - Token F1 fails on paraphrases: "30 day return" vs "30-day refund" = low score
#   - BERTScore understands semantics: same meaning = high score
#
# CACHING:
#   - First run: ~10-15 min (downloads models, runs inference)
#   - Subsequent runs: ~30 sec (loads cached responses, recalculates metrics)
#
# USAGE:
#   rankings_df, detailed_df = run_evaluation()           # Full run
#   rankings_df, detailed_df = recalculate_metrics_only() # Recalc metrics only
#   clean()                                               # Delete cache
#
# ============================================================================

import os
import time
import json
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List, Optional, Callable
import torch
from transformers import pipeline

# ============================================================================
# VERIFY DEPENDENCIES FROM OBJECTIVES 0-4
# ============================================================================
def verify_dependencies():
    """Check that Objectives 0-4 have been run."""
    missing = []
    
    # Objective 0: Environment
    if 'env' not in globals():
        missing.append("env (Objective 0)")
    
    # Objective 1: System prompt
    if 'system_prompt' not in globals():
        missing.append("system_prompt (Objective 1)")
    
    # Objective 2: Q&A database
    if 'qa_database' not in globals():
        missing.append("qa_database (Objective 2)")
    
    # Objective 3: Embeddings
    if 'embed_query' not in globals():
        missing.append("embed_query() (Objective 3)")
    if 'faiss_index' not in globals():
        missing.append("faiss_index (Objective 3)")
    
    # Objective 4: RAG pipeline
    if 'rag_query' not in globals():
        missing.append("rag_query() (Objective 4)")
    
    if missing:
        print("❌ MISSING DEPENDENCIES - Run previous objectives first:")
        for m in missing:
            print(f"   • {m}")
        return False
    
    print("✅ All dependencies from Objectives 0-4 verified")
    return True

# ============================================================================
# SCOREPACK: UNIFIED SCORING CLASS
# ============================================================================
# Why inline? Self-contained notebook, no separate file needed.
# Why a class? Groups 5 metrics, caches embeddings, batch processing.
#
# METRICS:
#   accuracy   - BERTScore F1 (semantic similarity via DeBERTa)
#   quality    - Cosine similarity (same embedder as FAISS from Obj 3)
#   confidence - Calibration (rewards correct confidence levels)
#   speed      - Normalized latency (0ms=1.0, 2000ms=0.0)
#   robustness - Error handling (penalizes crashes, empty, verbose)
# ============================================================================

try:
    from bert_score import score as bert_score
    _HAS_BERT = True
    print("✅ BERTScore available")
except ImportError:
    _HAS_BERT = False
    print("⚠️ BERTScore not installed - run: pip install bert-score")

class ScorePack:
    """
    Unified scoring for RAG model evaluation.
    
    Usage:
        scorer = ScorePack(embeddings=cached_embs, embed_fn=embed_query)
        scores = scorer.score_all(pred, ref, conf, latency, is_ans, error)
    """
    
    def __init__(self, embeddings: Dict[str, np.ndarray] = None, 
                 embed_fn: Callable[[str], np.ndarray] = None):
        self.embeddings = embeddings or {}
        self.embed_fn = embed_fn  # Reuses embed_query from Objective 3
        self.device = 0 if torch.cuda.is_available() else "cpu"
    
    def _get_emb(self, text: str) -> Optional[np.ndarray]:
        """Get embedding from cache or compute via embed_query (Obj 3)."""
        if not text or len(text.strip()) < 2:
            return None
        if text in self.embeddings:
            return self.embeddings[text]
        if self.embed_fn:
            emb = self.embed_fn(text)
            self.embeddings[text] = emb
            return emb
        return None
    
    # --- ACCURACY: BERTScore (semantic F1) ---
    def accuracy(self, pred: str, ref: str) -> float:
        """BERTScore F1 using DeBERTa-large-mnli."""
        if not _HAS_BERT or not pred or not ref:
            return 0.0
        P, R, F1 = bert_score(
            [pred], [ref], lang="en",
            model_type="microsoft/deberta-large-mnli",
            rescale_with_baseline=True,
            device=self.device, verbose=False
        )
        return float(F1[0])
    
    def accuracy_batch(self, preds: List[str], refs: List[str]) -> List[float]:
        """Batch BERTScore - faster than loop."""
        if not _HAS_BERT:
            return [0.0] * len(preds)
        valid_idx = [i for i, (p, r) in enumerate(zip(preds, refs))
                     if p and p.strip() and r and r.strip()]
        if not valid_idx:
            return [0.0] * len(preds)
        P, R, F1 = bert_score(
            [preds[i] for i in valid_idx],
            [refs[i] for i in valid_idx],
            lang="en", model_type="microsoft/deberta-large-mnli",
            rescale_with_baseline=True,
            device=self.device, verbose=False
        )
        result = [0.0] * len(preds)
        for j, i in enumerate(valid_idx):
            result[i] = float(F1[j])
        return result
    
    # --- QUALITY: Embedding similarity (reuses Objective 3 embedder) ---
    def quality(self, pred: str, ref: str) -> float:
        """Cosine similarity using same embedder as FAISS (Obj 3)."""
        if not pred or not ref:
            return 0.0
        emb_p, emb_r = self._get_emb(pred), self._get_emb(ref)
        if emb_p is None or emb_r is None:
            return 0.0
        return max(0.0, float(np.dot(emb_p, emb_r) / 
                              (np.linalg.norm(emb_p) * np.linalg.norm(emb_r))))
    
    # --- CONFIDENCE: Calibration ---
    def confidence(self, raw_conf: float, answer: str, is_answerable: bool) -> float:
        """Rewards well-calibrated confidence."""
        is_empty = not answer or len(answer.strip()) < 3
        conf = raw_conf if raw_conf else 0.5
        if is_answerable:
            return 0.2 if is_empty else conf
        return 1.0 if is_empty else (0.9 if conf < 0.3 else (0.6 if conf < 0.5 else 0.2))
    
    # --- SPEED: Normalized latency ---
    @staticmethod
    def speed(latency_ms: float) -> float:
        """0ms=1.0, 2000ms+=0.0"""
        return max(0.0, min(1.0, 1 - (latency_ms / 2000)))
    
    # --- ROBUSTNESS: Error handling ---
    @staticmethod
    def robustness(answer: str, is_answerable: bool, had_error: bool) -> float:
        """Penalizes errors, empty answers, verbosity."""
        if had_error:
            return 0.0
        is_empty = not answer or len(answer.strip()) < 3
        length = len(answer.split()) if answer else 0
        if is_answerable:
            return 0.3 if is_empty else (0.7 if length > 50 else 1.0)
        return 1.0 if is_empty else (0.2 if length > 30 else 0.6)
    
    # --- BATCH SCORING ---
    def score_all_batch(self, preds: List[str], refs: List[str],
                        confs: List[float], latencies: List[float],
                        answerables: List[bool], errors: List[bool]) -> List[Dict[str, float]]:
        """Batch score all 5 metrics."""
        batch_preds = [p if a else "" for p, a in zip(preds, answerables)]
        batch_refs = [r if a else "" for r, a in zip(refs, answerables)]
        accuracies = self.accuracy_batch(batch_preds, batch_refs)
        
        results = []
        for i in range(len(preds)):
            results.append({
                'accuracy': accuracies[i] if answerables[i] else 0.0,
                'quality': self.quality(preds[i], refs[i]) if answerables[i] else 0.0,
                'confidence': self.confidence(confs[i], preds[i], answerables[i]),
                'speed': self.speed(latencies[i]),
                'robustness': self.robustness(preds[i], answerables[i], errors[i])
            })
        return results

print("✅ ScorePack loaded")

# ============================================================================
# CONFIGURATION
# ============================================================================
OUTPUT_DIR = "data/model_evaluation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cache files
CONTEXTS_FILE = os.path.join(OUTPUT_DIR, "contexts.csv")
EMBEDDINGS_FILE = os.path.join(OUTPUT_DIR, "embeddings.csv")
RAW_RESPONSES_FILE = os.path.join(OUTPUT_DIR, "raw_responses.csv")

# Output files
RANKINGS_FILE = os.path.join(OUTPUT_DIR, "model_rankings.csv")
DETAILED_FILE = os.path.join(OUTPUT_DIR, "model_responses.csv")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "evaluation_summary.txt")

print(f"📁 Output: {OUTPUT_DIR}/")

DEVICE = 0 if torch.cuda.is_available() else -1
print(f"🖥️  Device: {'GPU' if DEVICE == 0 else 'CPU'}")

# ============================================================================
# MODELS TO EVALUATE (6 models: 5 extractive + 1 generative)
# ============================================================================
MODELS_CONFIG = [
    ("T5-QA-Generative", "consciousAI/question-answering-generative-t5-v1-base-s-q-c", "text2text-generation"),
    ("RoBERTa-SQuAD2", "deepset/roberta-base-squad2", "question-answering"),
    ("BERT-Large-SQuAD", "google-bert/bert-large-cased-whole-word-masking-finetuned-squad", "question-answering"),
    ("DistilBERT-SQuAD", "distilbert-base-uncased-distilled-squad", "question-answering"),
    ("BERT-Tiny-SQuAD", "mrm8488/bert-tiny-finetuned-squadv2", "question-answering"),
    ("MiniLM-SQuAD", "deepset/minilm-uncased-squad2", "question-answering"),
]

# ============================================================================
# TEST QUESTIONS (5 answerable + 3 unanswerable)
# ============================================================================
TEST_QUESTIONS = [
    # Answerable - should find in knowledge base (Objective 2)
    ("What is your return policy?", "30-day return policy with full refund", True),
    ("How long does shipping take?", "Standard shipping takes 5-7 business days", True),
    ("What are your customer service hours?", "Monday to Friday 9am to 5pm", True),
    ("Do you offer warranty on products?", "1 year warranty on all electronics", True),
    ("How can I track my order?", "Use tracking number on our website", True),
    # Unanswerable - not in knowledge base
    ("What is the CEO's phone number?", "", False),
    ("Will you have a Black Friday sale?", "", False),
    ("How do prices compare to Amazon?", "", False),
]

# ============================================================================
# METRIC WEIGHTS (total = 100%)
# ============================================================================
METRIC_WEIGHTS = {
    'accuracy': 0.25,    # Semantic correctness (BERTScore)
    'quality': 0.25,     # Embedding similarity (reuses Obj 3)
    'confidence': 0.20,  # Calibration
    'speed': 0.15,       # Latency
    'robustness': 0.15   # Error handling
}

MODEL_SIZES = {
    'BERT-Large-SQuAD': ('Large', '340M'),
    'RoBERTa-SQuAD2': ('Base', '125M'),
    'T5-QA-Generative': ('Base', '220M'),
    'DistilBERT-SQuAD': ('Small', '66M'),
    'MiniLM-SQuAD': ('Small', '33M'),
    'BERT-Tiny-SQuAD': ('Tiny', '4M'),
}

# ============================================================================
# CACHE FUNCTIONS (3-stage caching)
# ============================================================================
def show_cache_status():
    """Display cache status."""
    print("\n" + "="*60)
    print("📁 CACHE STATUS")
    print("="*60)
    for name, path in [('contexts.csv', CONTEXTS_FILE), 
                       ('embeddings.csv', EMBEDDINGS_FILE),
                       ('raw_responses.csv', RAW_RESPONSES_FILE)]:
        print(f"   {'✅' if os.path.exists(path) else '❌'} {name}")


def load_or_fetch_contexts(force_refresh: bool = False) -> pd.DataFrame:
    """Fetch contexts using rag_query from Objective 4."""
    if not force_refresh and os.path.exists(CONTEXTS_FILE):
        print("\n📂 Loading contexts from cache...")
        return pd.read_csv(CONTEXTS_FILE)
    
    print("\n📥 Fetching contexts via rag_query (Objective 4)...")
    
    data = []
    for i, (q, expected, is_ans) in enumerate(TEST_QUESTIONS):
        # REUSE: rag_query from Objective 4
        result = rag_query(q, verbose=False)
        context = " ".join([f"{c.get('question','')} {c.get('answer','')}" 
                           for c in result.retrieved_context]) if result.success else ""
        data.append({
            'question': q, 
            'expected': expected, 
            'is_answerable': is_ans,
            'context': context or "No relevant information found.",
            'num_sources': len(result.retrieved_context) if result.success else 0
        })
        print(f"   [{i+1}/{len(TEST_QUESTIONS)}] ✅ {q[:40]}...")
    
    df = pd.DataFrame(data)
    df.to_csv(CONTEXTS_FILE, index=False)
    return df


def load_or_compute_embeddings(contexts_df: pd.DataFrame, force_refresh: bool = False) -> Dict[str, np.ndarray]:
    """Compute embeddings using embed_query from Objective 3."""
    if not force_refresh and os.path.exists(EMBEDDINGS_FILE):
        print("\n📂 Loading embeddings from cache...")
        df = pd.read_csv(EMBEDDINGS_FILE)
        return {row['text']: np.array(json.loads(row['embedding'])) for _, row in df.iterrows()}
    
    print("\n📥 Computing embeddings via embed_query (Objective 3)...")
    
    texts = list(set([row['expected'] for _, row in contexts_df.iterrows() 
                      if row['is_answerable'] and row['expected']]))
    
    embeddings = {}
    data = []
    for i, text in enumerate(texts):
        # REUSE: embed_query from Objective 3
        emb = embed_query(text)
        embeddings[text] = emb
        data.append({'text': text, 'embedding': json.dumps(emb.tolist())})
        print(f"   [{i+1}/{len(texts)}] ✅ {text[:40]}...")
    
    pd.DataFrame(data).to_csv(EMBEDDINGS_FILE, index=False)
    return embeddings


def load_or_collect_responses(contexts_df: pd.DataFrame, force_refresh: bool = False) -> pd.DataFrame:
    """Run all 6 models on test questions."""
    if not force_refresh and os.path.exists(RAW_RESPONSES_FILE):
        print("\n📂 Loading responses from cache...")
        return pd.read_csv(RAW_RESPONSES_FILE)
    
    print("\n🤖 Running model inference (6 models × 8 questions)...")
    all_responses = []
    
    for idx, (name, model_id, task_type) in enumerate(MODELS_CONFIG):
        print(f"\n[{idx+1}/{len(MODELS_CONFIG)}] 📊 {name}")
        
        try:
            pipe = pipeline(task_type, model=model_id, device=DEVICE,
                          torch_dtype=torch.float16 if DEVICE == 0 else torch.float32)
        except Exception as e:
            print(f"   ❌ Failed to load: {str(e)[:50]}")
            for _, row in contexts_df.iterrows():
                all_responses.append({'model': name, 'question': row['question'],
                                     'answer': '', 'raw_confidence': 0.0,
                                     'response_time_ms': 0.0, 'had_error': True})
            continue
        
        for _, row in contexts_df.iterrows():
            t0 = time.time()
            try:
                if task_type == "text2text-generation":
                    out = pipe(f"question: {row['question']} context: {row['context']}", max_length=50)
                    answer, raw_conf = out[0]['generated_text'].strip(), 0.7
                else:
                    out = pipe(question=row['question'], context=row['context'], max_answer_len=50)
                    answer, raw_conf = out['answer'].strip(), out.get('score', 0.5)
                had_error = False
            except:
                answer, raw_conf, had_error = '', 0.0, True
            
            all_responses.append({
                'model': name, 'question': row['question'], 'answer': answer,
                'raw_confidence': raw_conf, 'response_time_ms': (time.time() - t0) * 1000,
                'had_error': had_error
            })
            print(f"   ✅ {row['question'][:30]}... → {answer[:25] if answer else '(empty)'}...")
        
        del pipe
        if DEVICE == 0: torch.cuda.empty_cache()
    
    df = pd.DataFrame(all_responses)
    df.to_csv(RAW_RESPONSES_FILE, index=False)
    return df


# ============================================================================
# METRIC CALCULATION
# ============================================================================
def calculate_metrics(contexts_df: pd.DataFrame, responses_df: pd.DataFrame,
                      embeddings: Dict[str, np.ndarray]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate all 5 metrics using ScorePack."""
    print("\n📊 Calculating metrics (ScorePack + BERTScore)...")
    
    # REUSE: embed_query from Objective 3
    scorer = ScorePack(embeddings=embeddings, embed_fn=embed_query)
    
    context_lookup = {row['question']: {'expected': row['expected'], 'is_answerable': row['is_answerable']}
                      for _, row in contexts_df.iterrows()}
    
    # Prepare batch data
    preds, refs, confs, latencies, answerables, errors = [], [], [], [], [], []
    for _, resp in responses_df.iterrows():
        ctx = context_lookup[resp['question']]
        preds.append(resp['answer'] if resp['answer'] else "")
        refs.append(ctx['expected'] if ctx['expected'] else "")
        confs.append(resp['raw_confidence'])
        latencies.append(resp['response_time_ms'])
        answerables.append(ctx['is_answerable'])
        errors.append(resp['had_error'])
    
    # Batch scoring
    print("   🔄 Running BERTScore (DeBERTa-large-mnli)...")
    all_scores = scorer.score_all_batch(preds, refs, confs, latencies, answerables, errors)
    print(f"   ✅ Scored {len(all_scores)} responses")
    
    # Build detailed results
    detailed_results = []
    for i, (_, resp) in enumerate(responses_df.iterrows()):
        ctx = context_lookup[resp['question']]
        scores = all_scores[i]
        detailed_results.append({
            'model': resp['model'],
            'question': resp['question'],
            'answer': resp['answer'],
            'expected': ctx['expected'],
            'is_answerable': ctx['is_answerable'],
            'raw_confidence': resp['raw_confidence'],
            'response_time_ms': resp['response_time_ms'],
            **{k: round(v, 3) for k, v in scores.items()}
        })
    detailed_df = pd.DataFrame(detailed_results)
    
    # Aggregate by model
    print("   🔄 Aggregating by model...")
    model_results = []
    for name, _, _ in MODELS_CONFIG:
        model_data = detailed_df[detailed_df['model'] == name]
        answerable = model_data[model_data['is_answerable'] == True]
        
        metrics = {
            'Accuracy': answerable['accuracy'].mean() if len(answerable) > 0 else 0,
            'Quality': answerable['quality'].mean() if len(answerable) > 0 else 0,
            'Confidence': model_data['confidence'].mean(),
            'Speed': model_data['speed'].mean(),
            'Robustness': model_data['robustness'].mean()
        }
        
        final = sum(metrics[m.capitalize()] * w for m, w in METRIC_WEIGHTS.items())
        model_results.append({'Model': name, **{k: round(v, 3) for k, v in metrics.items()},
                             'Final_Score': round(final, 3)})
        print(f"   ✅ {name}: {final:.3f}")
    
    rankings_df = pd.DataFrame(model_results)
    rankings_df = rankings_df.sort_values('Final_Score', ascending=False).reset_index(drop=True)
    rankings_df.insert(0, 'Rank', range(1, len(rankings_df) + 1))
    
    return rankings_df, detailed_df


# ============================================================================
# OUTPUT
# ============================================================================
def save_outputs(rankings_df: pd.DataFrame, detailed_df: pd.DataFrame):
    """Save results to CSV and text summary."""
    rankings_df.to_csv(RANKINGS_FILE, index=False)
    detailed_df.to_csv(DETAILED_FILE, index=False)
    
    with open(SUMMARY_FILE, 'w') as f:
        f.write("="*60 + "\n")
        f.write("OBJECTIVE 5: MODEL EVALUATION SUMMARY\n")
        f.write("="*60 + "\n\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Scoring: ScorePack (BERTScore DeBERTa-large-mnli)\n\n")
        f.write("REUSES FROM PREVIOUS OBJECTIVES:\n")
        f.write("  • Objective 3: embed_query() for quality metric\n")
        f.write("  • Objective 4: rag_query() for context retrieval\n\n")
        f.write("METRIC WEIGHTS:\n")
        for m, w in METRIC_WEIGHTS.items():
            f.write(f"  {m}: {w*100:.0f}%\n")
        f.write("\n" + "="*60 + "\nRANKINGS:\n" + "="*60 + "\n\n")
        f.write(rankings_df.to_string(index=False))
        f.write(f"\n\n🥇 WINNER: {rankings_df.iloc[0]['Model']} ({rankings_df.iloc[0]['Final_Score']})\n")
    
    print(f"\n✅ Saved: {RANKINGS_FILE}")
    print(f"✅ Saved: {DETAILED_FILE}")
    print(f"✅ Saved: {SUMMARY_FILE}")


def print_analysis(rankings_df: pd.DataFrame):
    """Print winner summary and model insights."""
    winner = rankings_df.iloc[0]
    
    print("\n" + "="*60)
    print("🏆 WINNER SUMMARY")
    print("="*60)
    print(f"""
    🥇 BEST MODEL: {winner['Model']}
    
    Final Score: {winner['Final_Score']:.3f}
    
    SCORES:
    ├── Accuracy (BERTScore): {winner['Accuracy']:.3f}
    ├── Quality (Embedding):  {winner['Quality']:.3f}
    ├── Confidence:           {winner['Confidence']:.3f}
    ├── Speed:                {winner['Speed']:.3f}
    └── Robustness:           {winner['Robustness']:.3f}
    """)
    
    print("="*60)
    print("🔍 MODEL INSIGHTS: SIZE vs PERFORMANCE")
    print("="*60)
    print(f"\n   {'Model':<20} {'Size':<8} {'Params':<10} {'Score':<8}")
    print("   " + "─"*46)
    for _, row in rankings_df.iterrows():
        size_info = MODEL_SIZES.get(row['Model'], ('?', '?'))
        print(f"   {row['Model']:<20} {size_info[0]:<8} {size_info[1]:<10} {row['Final_Score']:.3f}")
    
    print(f"\n   RECOMMENDATIONS:")
    print(f"   • Speed-critical:    {rankings_df.loc[rankings_df['Speed'].idxmax(), 'Model']}")
    print(f"   • Accuracy-critical: {rankings_df.loc[rankings_df['Accuracy'].idxmax(), 'Model']}")
    print(f"   • Best overall:      {rankings_df.iloc[0]['Model']}")


# ============================================================================
# MAIN ENTRY POINTS
# ============================================================================
def run_evaluation(force_refresh: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run full evaluation pipeline."""
    print("\n" + "="*60)
    print("🚀 OBJECTIVE 5: MODEL EVALUATION")
    print("="*60)
    print("   Reusing: embed_query (Obj 3), rag_query (Obj 4)")
    
    start_time = time.time()
    
    cache_complete = all(os.path.exists(f) for f in [CONTEXTS_FILE, EMBEDDINGS_FILE, RAW_RESPONSES_FILE])
    
    if cache_complete and not force_refresh:
        print("\n💡 Loading from cache (use force_refresh=True to rebuild)...")
        contexts_df = pd.read_csv(CONTEXTS_FILE)
        responses_df = pd.read_csv(RAW_RESPONSES_FILE)
        emb_df = pd.read_csv(EMBEDDINGS_FILE)
        embeddings = {row['text']: np.array(json.loads(row['embedding'])) for _, row in emb_df.iterrows()}
    else:
        contexts_df = load_or_fetch_contexts(force_refresh)
        embeddings = load_or_compute_embeddings(contexts_df, force_refresh)
        responses_df = load_or_collect_responses(contexts_df, force_refresh)
    
    rankings_df, detailed_df = calculate_metrics(contexts_df, responses_df, embeddings)
    save_outputs(rankings_df, detailed_df)
    
    print(f"\n⏱️  Total time: {time.time() - start_time:.1f}s")
    return rankings_df, detailed_df


def recalculate_metrics_only() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Recalculate metrics from cached responses (~30 sec)."""
    print("\n📊 Recalculating metrics from cache...")
    contexts_df = pd.read_csv(CONTEXTS_FILE)
    responses_df = pd.read_csv(RAW_RESPONSES_FILE)
    emb_df = pd.read_csv(EMBEDDINGS_FILE)
    embeddings = {row['text']: np.array(json.loads(row['embedding'])) for _, row in emb_df.iterrows()}
    rankings_df, detailed_df = calculate_metrics(contexts_df, responses_df, embeddings)
    save_outputs(rankings_df, detailed_df)
    return rankings_df, detailed_df


def clean():
    """Delete all cache files."""
    print("\n🗑️  Cleaning cache...")
    for f in [CONTEXTS_FILE, EMBEDDINGS_FILE, RAW_RESPONSES_FILE, RANKINGS_FILE, DETAILED_FILE, SUMMARY_FILE]:
        if os.path.exists(f):
            os.remove(f)
            print(f"   Deleted: {os.path.basename(f)}")


# ============================================================================
# EXECUTION - Uses env from Objective 0, wrapped with timing
# ============================================================================

# Verify env is available from Objective 0
if 'env' not in globals():
    raise RuntimeError("❌ 'env' not found! Please run Objective 0 (Prerequisites & Setup) first.")

# Verify prerequisites from Objectives 1-4
if 'system_prompt' not in globals():
    raise RuntimeError("❌ 'system_prompt' not found! Please run Objective 1 first.")

if 'qa_database' not in globals():
    raise RuntimeError("❌ 'qa_database' not found! Please run Objective 2 first.")

if 'embed_query' not in globals():
    raise RuntimeError("❌ 'embed_query' not found! Please run Objective 3 first.")

if 'rag_query' not in globals():
    raise RuntimeError("❌ 'rag_query' not found! Please run Objective 4 first.")

print("✅ Prerequisites validated (env, system_prompt, qa_database, embed_query, rag_query)")

# ============================================================================
# EXECUTION - Orchestrates Objective 5 workflow with timing
# ============================================================================

with env.timer.objective(ObjectiveNames.OBJECTIVE_5):
    print("Objective 5: Model Evaluation & Ranking\n")
    
    # Verify all dependencies
    if verify_dependencies():
        show_cache_status()
        rankings_df, detailed_df = run_evaluation()
        
        print("\n" + "="*60)
        print("🏆 FINAL RANKINGS")
        print("="*60)
        print(rankings_df.to_string(index=False))
        print(f"\n🥇 WINNER: {rankings_df.iloc[0]['Model']} ({rankings_df.iloc[0]['Final_Score']})")
        
        print_analysis(rankings_df)
        
        # Store in globals for other objectives
        globals()['rankings_df'] = rankings_df
        globals()['detailed_df'] = detailed_df
        globals()['ScorePack'] = ScorePack
        globals()['run_evaluation'] = run_evaluation
        globals()['recalculate_metrics_only'] = recalculate_metrics_only
        globals()['clean'] = clean
        globals()['show_cache_status'] = show_cache_status
        
        print("\n✅ Objective 5 complete - Model rankings ready for Objective 6!")
    else:
        print("\n⚠️ Please run Objectives 0-4 first, then re-run this cell.")