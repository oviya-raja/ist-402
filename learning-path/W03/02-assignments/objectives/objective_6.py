# ============================================================================
# OBJECTIVE 6: SYSTEM ANALYSIS & REFLECTION
# ============================================================================
#
# PURPOSE: Analyze results from Objective 5 and provide insights for reflection
#
# 100% REUSE FROM PREVIOUS OBJECTIVES:
#   - env (Objective 0) - Environment configuration and timing
#   - qa_database (Objective 2) - Knowledge base for coverage analysis
#   - faiss_index (Objective 3) - Retrieval system metrics
#   - rankings_df, detailed_df (Objective 5) - Evaluation results
#
# PREREQUISITES: Run Objectives 0-5 first
#
# ============================================================================

import os
import pandas as pd

# Import ObjectiveSupport for DRY (optional - graceful fallback)
try:
    from objective_support import ObjectiveSupport
    _support = ObjectiveSupport()
except ImportError:
    # Fallback if not available (for notebook extraction)
    _support = None

# Output directory (using ObjectiveSupport if available)
OUTPUT_DIR = "data/system_analysis"
if _support:
    OUTPUT_DIR = _support.setup_output_dir(OUTPUT_DIR)
else:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
# SECTION 1: VERIFY DEPENDENCIES
# ============================================================================

def verify_dependencies():
    """Check that Objectives 0-5 have been run."""
    missing = []
    
    if 'env' not in globals():
        missing.append("env (Objective 0)")
    if 'qa_database' not in globals():
        missing.append("qa_database (Objective 2)")
    if 'faiss_index' not in globals():
        missing.append("faiss_index (Objective 3)")
    if 'rankings_df' not in globals():
        missing.append("rankings_df (Objective 5)")
    if 'detailed_df' not in globals():
        missing.append("detailed_df (Objective 5)")
    
    if missing:
        print("❌ MISSING DEPENDENCIES:")
        for m in missing:
            print(f"   • {m}")
        return False
    
    print("✅ All dependencies verified")
    return True


# ============================================================================
# EXECUTION - Uses env from Objective 0, wrapped with timing
# ============================================================================

# Verify prerequisites using ObjectiveSupport (DRY)
if _support:
    _support.ensure_prerequisites({
        'env': 'Objective 0 (Prerequisites & Setup)',
        'qa_database': 'Objective 2',
        'faiss_index': 'Objective 3',
        'rankings_df': 'Objective 5',
        'detailed_df': 'Objective 5'
    }, globals())
    print("✅ Prerequisites validated (env, qa_database, faiss_index, rankings_df, detailed_df)")
else:
    # Fallback to manual checking if ObjectiveSupport not available
    if 'env' not in globals():
        raise RuntimeError("❌ 'env' not found! Please run Objective 0 (Prerequisites & Setup) first.")
    if 'qa_database' not in globals():
        raise RuntimeError("❌ 'qa_database' not found! Please run Objective 2 first.")
    if 'faiss_index' not in globals():
        raise RuntimeError("❌ 'faiss_index' not found! Please run Objective 3 first.")
    if 'rankings_df' not in globals() or 'detailed_df' not in globals():
        raise RuntimeError("❌ 'rankings_df' or 'detailed_df' not found! Please run Objective 5 first.")
    print("✅ Prerequisites validated (env, qa_database, faiss_index, rankings_df, detailed_df)")

# ============================================================================
# EXECUTION - Orchestrates Objective 6 workflow with timing
# ============================================================================

with env.timer.objective(ObjectiveNames.OBJECTIVE_6):
    print("Objective 6: System Analysis & Reflection\n")
    
    if not verify_dependencies():
        print("\n⚠️ Run Objectives 0-5 first, then re-run this cell.")
    else:
        # Get data from previous objectives
        qa_database = globals()['qa_database']
        faiss_index = globals()['faiss_index']
        rankings_df = globals()['rankings_df']
        detailed_df = globals()['detailed_df']
        
        # ------------------------------------------------------------------
        # 1. MODEL RANKINGS
        # ------------------------------------------------------------------
        print("\n" + "-" * 60)
        print("🏆 MODEL RANKINGS")
        print("-" * 60)
        
        display_cols = ['Rank', 'Model', 'Accuracy', 'Quality', 'Speed', 'Final_Score']
        available_cols = [c for c in display_cols if c in rankings_df.columns]
        print(rankings_df[available_cols].to_string(index=False))
        
        best = rankings_df.iloc[0]
        print(f"\n🥇 Best Model: {best['Model']} (Score: {best['Final_Score']:.3f})")
        
        # Fastest model
        fastest_idx = detailed_df['response_time_ms'].idxmin()
        fastest = detailed_df.loc[fastest_idx]
        print(f"⚡ Fastest Model: {fastest['model']} ({fastest['response_time_ms']/1000:.3f}s)")
        
        # ------------------------------------------------------------------
        # 2. PERFORMANCE SUMMARY
        # ------------------------------------------------------------------
        print("\n" + "-" * 60)
        print("📈 PERFORMANCE SUMMARY")
        print("-" * 60)
        
        print(f"  • Avg Accuracy:   {rankings_df['Accuracy'].mean():.1%}")
        print(f"  • Avg Quality:    {rankings_df['Quality'].mean():.1%}")
        print(f"  • Avg Confidence: {rankings_df['Confidence'].mean():.1%}")
        print(f"  • Avg Speed:      {rankings_df['Speed'].mean():.1%}")
        print(f"  • Avg Robustness: {rankings_df['Robustness'].mean():.1%}")
        print(f"  • Avg Response:   {detailed_df['response_time_ms'].mean()/1000:.3f}s")
        
        # ------------------------------------------------------------------
        # 3. ANSWERABLE vs UNANSWERABLE
        # ------------------------------------------------------------------
        print("\n" + "-" * 60)
        print("📊 ANSWERABLE vs UNANSWERABLE PERFORMANCE")
        print("-" * 60)
        
        ans_df = detailed_df[detailed_df['is_answerable'] == True]
        unans_df = detailed_df[detailed_df['is_answerable'] == False]
        
        print(f"\n  Answerable Questions ({len(ans_df)} samples):")
        print(f"    • Avg Accuracy:   {ans_df['accuracy'].mean():.1%}")
        print(f"    • Avg Quality:    {ans_df['quality'].mean():.1%}")
        print(f"    • Avg Confidence: {ans_df['confidence'].mean():.1%}")
        
        print(f"\n  Unanswerable Questions ({len(unans_df)} samples):")
        print(f"    • Avg Robustness: {unans_df['robustness'].mean():.1%}")
        print(f"    • Avg Confidence: {unans_df['confidence'].mean():.1%}")
        
        # False confidence detection
        if 'raw_confidence' in unans_df.columns:
            high_conf = (unans_df['raw_confidence'] > 0.7).sum()
            print(f"    • False Confidence (>0.7): {high_conf}/{len(unans_df)}")
        
        # ------------------------------------------------------------------
        # 4. KNOWLEDGE BASE STATS
        # ------------------------------------------------------------------
        print("\n" + "-" * 60)
        print("📚 KNOWLEDGE BASE")
        print("-" * 60)
        
        total_pairs = len(qa_database)
        categories = {}
        for qa in qa_database:
            cat = qa.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"  • Total Q&A Pairs: {total_pairs}")
        print(f"  • Categories: {len(categories)}")
        print(f"  • FAISS Vectors: {faiss_index.ntotal}")
        print(f"  • Embedding Dim: {faiss_index.d}")
        
        # ------------------------------------------------------------------
        # 5. KEY INSIGHTS
        # ------------------------------------------------------------------
        print("\n" + "-" * 60)
        print("💡 KEY INSIGHTS")
        print("-" * 60)
        
        # Accuracy insight
        avg_acc = rankings_df['Accuracy'].mean()
        if avg_acc < 0.3:
            print(f"  ⚠️ Low accuracy ({avg_acc:.1%}) - models struggle with matching")
        elif avg_acc < 0.6:
            print(f"  📊 Moderate accuracy ({avg_acc:.1%}) - room for improvement")
        else:
            print(f"  ✅ Good accuracy ({avg_acc:.1%}) - models perform well")
        
        # Unanswerable detection insight
        unans_detection = (unans_df['robustness'] > 0.5).mean() if len(unans_df) > 0 else 0
        if unans_detection < 0.5:
            print(f"  ⚠️ Poor unanswerable detection ({unans_detection:.1%}) - may hallucinate")
        else:
            print(f"  ✅ Good unanswerable detection ({unans_detection:.1%})")
        
        # Speed insight
        avg_time = detailed_df['response_time_ms'].mean() / 1000
        if avg_time < 1.0:
            print(f"  ✅ Fast response time ({avg_time:.2f}s)")
        else:
            print(f"  ⚠️ Slow response time ({avg_time:.2f}s) - consider optimization")
        
        # Model spread insight
        score_range = rankings_df['Final_Score'].max() - rankings_df['Final_Score'].min()
        print(f"  📊 Model score range: {score_range:.3f}")
        
        # ------------------------------------------------------------------
        # 6. SAVE SUMMARY CSV
        # ------------------------------------------------------------------
        summary = {
            'Metric': ['Best Model', 'Best Score', 'Avg Accuracy', 'Avg Quality', 
                       'Avg Response Time', 'Total Q&A Pairs', 'FAISS Vectors'],
            'Value': [best['Model'], f"{best['Final_Score']:.3f}", 
                      f"{avg_acc:.1%}", f"{rankings_df['Quality'].mean():.1%}",
                      f"{avg_time:.3f}s", total_pairs, faiss_index.ntotal]
        }
        summary_df = pd.DataFrame(summary)
        summary_df.to_csv(f"{OUTPUT_DIR}/analysis_summary.csv", index=False)
        print(f"\n💾 Saved: {OUTPUT_DIR}/analysis_summary.csv")
        
        # ------------------------------------------------------------------
        # 7. REFLECTION PROMPTS
        # ------------------------------------------------------------------
        print("\n" + "=" * 60)
        print("📝 REFLECTION PROMPTS")
        print("=" * 60)
        print("""
Write your reflection addressing these questions:

1. STRENGTHS: What does this RAG system do well?
   
2. WEAKNESSES: What are the main limitations?
   
3. MODEL COMPARISON: Why did the best model outperform others?
   
4. REAL-WORLD USE: Where could this system be deployed?
   
5. IMPROVEMENTS: What would you change to make it better?
""")
        
        print("=" * 60)
        print("✅ Objective 6 completed successfully!")
        print("=" * 60)
