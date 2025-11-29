"""
Scoring system for model evaluation and ranking.
"""

from typing import List, Dict, Tuple
from .environment import EnvironmentConfig
from .models import FitmentResult


class FitmentScorer:
    """
    Scoring system for model evaluation and ranking.
    Similar to ScorePack from the original RAG pipeline.
    """
    
    METRIC_WEIGHTS = {
        'skill_match': 0.30,
        'experience_match': 0.20,
        'education_match': 0.15,
        'response_quality': 0.20,
        'speed': 0.15
    }
    
    def __init__(self, env: EnvironmentConfig):
        self.env = env
        self.embeddings_cache = {}
    
    def score_skill_match(self, matched: int, total: int) -> float:
        """Score based on skill coverage."""
        if total == 0:
            return 1.0
        return min(matched / total, 1.0)
    
    def score_experience(self, profile_years: float, required_years: Tuple[int, int]) -> float:
        """Score based on experience fit."""
        min_req, max_req = required_years
        if min_req <= profile_years <= max_req:
            return 1.0
        elif profile_years < min_req:
            return max(0, 1 - (min_req - profile_years) * 0.2)
        else:
            return max(0.7, 1 - (profile_years - max_req) * 0.05)
    
    def score_speed(self, latency_ms: float, threshold_ms: float = 2000) -> float:
        """Score based on response time."""
        return max(0, 1 - (latency_ms / threshold_ms))
    
    def calculate_final_score(self, metrics: Dict[str, float]) -> float:
        """Calculate weighted final score."""
        score = 0
        for metric, weight in self.METRIC_WEIGHTS.items():
            score += metrics.get(metric, 0) * weight
        return round(score * 100, 1)
    
    def rank_results(self, results: List[FitmentResult]) -> List[FitmentResult]:
        """Rank results by multiple criteria."""
        # Sort by: priority (asc), fitment_score (desc)
        return sorted(results, key=lambda r: (r.priority_level, -r.fitment_score))

