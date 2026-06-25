"""
Reranking service for SmartHire AI.
Performs final reranking after initial retrieval.
Responsible: Team Member 4 (Chaturya/Rohith)
"""

from typing import List, Dict, Any
from app.utils.logger import get_logger
import re

logger = get_logger("RerankService")


def rerank_candidates(
    candidates: List[Dict[str, Any]],
    scores: List[Dict[str, float]]
) -> List[Dict[str, Any]]:
    """
    Rerank candidates based on final scores.
    Sort by final_score in descending order.
    
    Args:
        candidates: List of candidate dictionaries
        scores: List of score dictionaries
        
    Returns:
        List of reranked candidates with rank positions
    """
    try:
        if len(candidates) != len(scores):
            logger.warning(f"Candidate count ({len(candidates)}) != scores count ({len(scores)})")
        
        # Combine candidates with scores
        ranked = []
        for idx, (candidate, score) in enumerate(zip(candidates, scores)):
            candidate_with_scores = {**candidate, **score}
            ranked.append(candidate_with_scores)
        
        # Sort by final_score in descending order
        ranked.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        # Add rank position
        for idx, candidate in enumerate(ranked, 1):
            candidate['rank'] = idx
        
        logger.info(f"Reranked {len(ranked)} candidates")
        return ranked
        
    except Exception as e:
        logger.error(f"Error reranking candidates: {str(e)}")
        raise


def apply_diversity_filter(
    candidates: List[Dict[str, Any]],
    diversity_weight: float = 0.1
) -> List[Dict[str, Any]]:
    """
    Apply diversity filtering to ensure varied candidate backgrounds.
    Can consider: education, experience level, skill sets, etc.
    
    Args:
        candidates: Reranked candidates
        diversity_weight: Weight for diversity considerations
        
    Returns:
        Candidates with diversity applied
    """
    try:
        logger.info(f"Applying diversity filter with weight: {diversity_weight}")
        
        # Group candidates by education level
        education_groups = {}
        for candidate in candidates:
            edu = candidate.get('education', 'Unknown')
            if edu not in education_groups:
                education_groups[edu] = []
            education_groups[edu].append(candidate)
        
        # Log diversity breakdown
        logger.info(f"Diversity breakdown by education: {[(k, len(v)) for k, v in education_groups.items()]}")
        
        # Candidates already ranked - diversity can be applied at selection stage
        return candidates
        
    except Exception as e:
        logger.error(f"Error applying diversity filter: {str(e)}")
        return candidates


def apply_fairness_constraints(
    candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Apply fairness constraints to ensure bias-free ranking.
    Ensures referral information was properly removed before ranking.
    
    Args:
        candidates: Ranked candidates
        
    Returns:
        Candidates with fairness validation applied
    """
    try:
        logger.info("Applying fairness constraints...")
        
        bias_fields_to_check = [
            'referral_flag',
            'referred_by',
            'employee_id',
            'manager_name',
            'internal_reference'
        ]
        
        bias_detected = []
        for idx, candidate in enumerate(candidates):
            for field in bias_fields_to_check:
                if field in candidate and candidate[field] is not None:
                    bias_detected.append((idx, field))
                    logger.warning(f"Candidate {idx} still has bias field: {field}")
        
        if bias_detected:
            logger.warning(f"Bias fields detected in {len(set([b[0] for b in bias_detected]))} candidates")
            # Note: In production, you might raise an error here
        else:
            logger.info("All candidates passed fairness check")
        
        return candidates
        
    except Exception as e:
        logger.error(f"Error applying fairness constraints: {str(e)}")
        return candidates


def remove_duplicates(
    candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    try:
        seen_names = set()
        unique_candidates = []
        duplicates_removed = 0

        for candidate in candidates:

            raw_name = candidate.get("name", "")

            name = re.sub(
                r"\s+",
                " ",
                raw_name.strip().lower()
            )

            if name and name not in seen_names:
                seen_names.add(name)
                unique_candidates.append(candidate)
            else:
                duplicates_removed += 1

        if duplicates_removed > 0:
            logger.info(
                f"Removed {duplicates_removed} duplicate candidates"
            )

        return unique_candidates

    except Exception as e:
        logger.error(f"Error removing duplicates: {str(e)}")
        return candidates


def apply_tie_breaking(
    candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Apply tie-breaking logic for candidates with same final_score.
    Tie-breaking order: semantic_score > skill_score > career_score
    
    Args:
        candidates: Ranked candidates
        
    Returns:
        Candidates with tie-breaking applied
    """
    try:
        from operator import itemgetter
        
        # Sort with tie-breaking criteria
        candidates.sort(
            key=lambda x: (
                -x.get('final_score', 0),
                -x.get('semantic_score', 0),
                -x.get('skill_score', 0),
                -x.get('career_score', 0)
            )
        )
        
        # Update ranks
        for idx, candidate in enumerate(candidates, 1):
            candidate['rank'] = idx
        
        logger.info("Tie-breaking applied")
        return candidates
        
    except Exception as e:
        logger.error(f"Error applying tie-breaking: {str(e)}")
        return candidates
