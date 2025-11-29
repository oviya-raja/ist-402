from typing import List
from .environment import EnvironmentConfig
from .prompts import JobFitmentPromptEngineer
from .knowledge_base import KnowledgeBaseGenerator
from .vector_db import JobFitmentVectorDB
from .analyzer import JobFitmentAnalyzer
from .pipeline import JobFitmentRAGPipeline
from .scorer import FitmentScorer
from .models import StudentProfile, JobPosting, FitmentResult
from .config import OUTPUT_DIR

class JobFitmentAgent:
    """
    Main application class that orchestrates all components.
    Provides a unified interface for job fitment analysis.
    """
    
    def __init__(self):
        self.env = None
        self.prompt_engineer = None
        self.knowledge_base_gen = None
        self.vector_db = None
        self.analyzer = None
        self.pipeline = None
        self.scorer = None
        self.initialized = False
    
    def setup(self, skip_packages: bool = False):
        """Initialize all components."""
        print("=" * 80)
        print("🚀 JOB FITMENT ANALYSIS AGENT - SETUP")
        print("=" * 80)
        
        # Step 0: Environment
        print("\n📋 Objective 0: Environment Setup")
        print("-" * 40)
        self.env = EnvironmentConfig()
        
        if not skip_packages:
            self.env.install_packages()
        
        if not self.env.import_libraries():
            raise RuntimeError("Failed to import required libraries")
        
        self.env.get_token("HUGGINGFACE_HUB_TOKEN")
        self.env.get_token("OPENAI_API_KEY")
        
        if self.env.hf_token:
            self.env.authenticate_hf()
        
        self.env.print_summary()
        
        # Step 1: System Prompts
        print("\n📋 Objective 1: System Prompt Engineering")
        print("-" * 40)
        self.prompt_engineer = JobFitmentPromptEngineer(self.env)
        system_prompt = self.prompt_engineer.create_system_prompt()
        print(f"   ✅ System prompt created ({len(system_prompt)} chars)")
        
        # Step 2: Knowledge Base
        print("\n📋 Objective 2: Knowledge Base Generation")
        print("-" * 40)
        self.knowledge_base_gen = KnowledgeBaseGenerator(self.env)
        knowledge_base = self.knowledge_base_gen.generate_full_knowledge_base()
        
        # Step 3: Vector Database
        print("\n📋 Objective 3: Vector Database")
        print("-" * 40)
        self.vector_db = JobFitmentVectorDB(self.env)
        self.vector_db.load_embedding_model()
        self.vector_db.build_index(knowledge_base)
        
        # Step 4: Analyzer
        print("\n📋 Objective 4: Job Fitment Analyzer")
        print("-" * 40)
        self.analyzer = JobFitmentAnalyzer(self.env, self.vector_db)
        print("   ✅ Analyzer initialized")
        
        # Step 5: RAG Pipeline
        print("\n📋 Objective 5: RAG Pipeline")
        print("-" * 40)
        self.pipeline = JobFitmentRAGPipeline(
            self.env, self.prompt_engineer, self.vector_db, self.analyzer
        )
        print("   ✅ RAG Pipeline ready")
        
        # Step 6: Scorer
        print("\n📋 Objective 6: Scoring System")
        print("-" * 40)
        self.scorer = FitmentScorer(self.env)
        print("   ✅ Scoring system ready")
        
        self.initialized = True
        
        print("\n" + "=" * 80)
        print("✅ JOB FITMENT AGENT READY!")
        print("=" * 80)
    
    def analyze(
        self,
        profile: StudentProfile,
        jobs: List[JobPosting],
        generate_report: bool = True,
        verbose: bool = True
    ) -> List[FitmentResult]:
        """Run complete job fitment analysis."""
        if not self.initialized:
            raise RuntimeError("Agent not initialized. Call setup() first.")
        
        if self.pipeline is None or self.scorer is None:
            raise RuntimeError("Pipeline or scorer not initialized. Call setup() first.")
        
        print("\n" + "=" * 80)
        print("🔍 RUNNING JOB FITMENT ANALYSIS")
        print("=" * 80)
        
        # Analyze all jobs
        results = self.pipeline.batch_analyze(profile, jobs, verbose=verbose)
        
        # Rank results
        ranked_results = self.scorer.rank_results(results)
        
        # Print summary
        print("\n" + "-" * 80)
        print("📊 FITMENT RANKINGS")
        print("-" * 80)
        print(f"\n{'Rank':<6}{'Company':<15}{'Position':<35}{'Fitment':<10}{'Priority'}")
        print("-" * 80)
        
        for i, result in enumerate(ranked_results, 1):
            print(f"{i:<6}{result.job.company:<15}{result.job.title[:33]:<35}"
                  f"{result.fitment_score}%{'':<5}P{result.priority_level}")
        
        # Generate report
        if generate_report and self.pipeline is not None:
            self.pipeline.generate_report(profile, ranked_results)
        
        return ranked_results
    
    def quick_analyze(self, profile: StudentProfile, job: JobPosting) -> FitmentResult:
        """Quick analysis for a single job."""
        if not self.initialized:
            raise RuntimeError("Agent not initialized. Call setup() first.")
        
        if self.analyzer is None:
            raise RuntimeError("Analyzer not initialized. Call setup() first.")
        
        return self.analyzer.analyze_fitment(profile, job)
    
    def save_all(self):
        """Save all artifacts."""
        if not self.initialized:
            return
        
        print("\n💾 Saving artifacts...")
        if self.prompt_engineer is not None:
            self.prompt_engineer.save_system_prompt()
        if self.knowledge_base_gen is not None:
            self.knowledge_base_gen.save_knowledge_base()
        if self.vector_db is not None:
            self.vector_db.save_index()
        print("✅ All artifacts saved to:", OUTPUT_DIR)

