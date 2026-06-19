"""
Scoring service for SmartHire AI.
Calculates individual scores for candidates.
Responsible: Team Member 4 (Chaturya/Rohith)
"""

from typing import Dict, List, Any
import numpy as np
from app.utils.logger import get_logger

logger = get_logger("ScoringService")


def calculate_semantic_score(
    jd_embedding: np.ndarray,
    candidate_embedding: np.ndarray
) -> float:
    """
    Calculate semantic similarity score between JD and candidate.
    Uses cosine similarity on normalized embeddings.
    
    Args:
        jd_embedding: JD embedding vector
        candidate_embedding: Candidate embedding vector
        
    Returns:
        float: Semantic score (0-1)
    """
    try:
        jd_vec = np.array(jd_embedding, dtype=np.float32)
        cand_vec = np.array(candidate_embedding, dtype=np.float32)
        
        # Normalize vectors
        jd_norm = np.linalg.norm(jd_vec)
        cand_norm = np.linalg.norm(cand_vec)
        
        if jd_norm == 0 or cand_norm == 0:
            logger.warning("Zero vector encountered in semantic scoring")
            return 0.0
        
        jd_vec = jd_vec / jd_norm
        cand_vec = cand_vec / cand_norm
        
        # Cosine similarity
        similarity = np.dot(jd_vec, cand_vec)
        
        # Map from [-1, 1] to [0, 1]
        score = (similarity + 1) / 2
        
        logger.debug(f"Semantic score: {score:.4f}")
        return min(max(float(score), 0.0), 1.0)
        
    except Exception as e:
        logger.error(f"Error calculating semantic score: {str(e)}")
        return 0.0


def calculate_skill_score(
    required_skills: List[str],
    candidate_skills: List[str]
) -> float:
    """
    Calculate skill match score.
    Score = (matched_skills / total_required_skills) with multipliers
    
    Args:
        required_skills: Required skills list
        candidate_skills: Candidate's skills list
        
    Returns:
        float: Skill score (0-1)
    """
    try:
        if not required_skills:
            return 1.0
        
        # Convert to lowercase and strip whitespace
        required_lower = [skill.lower().strip() for skill in required_skills]
        candidate_lower = [skill.lower().strip() for skill in candidate_skills]
        
        # Count exact matches
        exact_matches = sum(1 for skill in required_lower if skill in candidate_lower)
        
        # Calculate score
        score = exact_matches / len(required_skills) if required_skills else 0.0
        
        logger.debug(f"Skill score: {score:.4f} ({exact_matches}/{len(required_skills)})")
        return min(max(score, 0.0), 1.0)
        
    except Exception as e:
        logger.error(f"Error calculating skill score: {str(e)}")
        return 0.0


def calculate_career_score(
    candidate_experience: int,
    required_experience: int,
    education_match: bool = True,
    certifications_count: int = 0
) -> float:
    """
    Calculate career fit score based on experience, education, certifications.
    
    Args:
        candidate_experience: Years of experience
        required_experience: Required years
        education_match: Whether education matches
        certifications_count: Number of relevant certifications
        
    Returns:
        float: Career score (0-1)
    """
    try:
        # Base score from experience matching
        if candidate_experience >= required_experience:
            # Over-qualified gives bonus up to 1.0
            exp_ratio = min(candidate_experience / max(required_experience, 1), 1.5)
            exp_score = min(exp_ratio / 1.5, 1.0)
        else:
            # Under-qualified gets penalty
            exp_score = candidate_experience / max(required_experience, 1)
        
        # Education bonus (0.1 for match)
        edu_bonus = 0.1 if education_match else 0.0
        
        # Certification bonus (0.05 per cert, max 0.2)
        cert_bonus = min(certifications_count * 0.05, 0.2)
        
        score = min(exp_score + edu_bonus + cert_bonus, 1.0)
        
        logger.debug(f"Career score: {score:.4f}")
        return min(max(score, 0.0), 1.0)
        
    except Exception as e:
        logger.error(f"Error calculating career score: {str(e)}")
        return 0.0


def calculate_clean_activity_score(
    candidate_profile: Dict[str, Any]
) -> float:
    """
    Calculate clean activity score.
    Penalizes suspicious profiles (incomplete, keyword stuffing, etc.)
    
    Args:
        candidate_profile: Candidate profile dictionary
        
    Returns:
        float: Clean activity score (0-1)
    """
    try:
        score = 1.0  # Start with perfect score
        
        # Penalty for missing name
        if not candidate_profile.get('name'):
            score -= 0.3
        
        # Penalty for missing skills
        skills = candidate_profile.get('skills', [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',')]
        
        if not skills:
            score -= 0.3
        
        # Penalty for missing experience
        experience = candidate_profile.get('experience', 0)
        if experience == 0:
            score -= 0.2
        
        # Penalty for missing education
        if not candidate_profile.get('education'):
            score -= 0.1
        
        # Penalty for keyword stuffing (too many skills)
        if len(skills) > 25:
            score -= 0.2
        
        # Bonus for certifications
        certifications = candidate_profile.get('certifications', [])
        if isinstance(certifications, str):
            certifications = [c.strip() for c in certifications.split(',')]
        
        if certifications and any(c for c in certifications if c):
            score += 0.1
        
        # Bonus for projects
        projects = candidate_profile.get('projects', [])
        if isinstance(projects, str):
            projects = [p.strip() for p in projects.split(',')]
        
        if projects and any(p for p in projects if p):
            score += 0.1
        
        logger.debug(f"Clean activity score: {score:.4f}")
        return min(max(score, 0.0), 1.0)
        
    except Exception as e:
        logger.error(f"Error calculating clean activity score: {str(e)}")
        return 0.5


def calculate_scores(
    semantic_score: float,
    skill_score: float,
    career_score: float,
    clean_activity_score: float,
    weights: Dict[str, float] = None
) -> Dict[str, float]:
    """
    Calculate final score using weighted sum.
    final_score = alpha*semantic + beta*skill + gamma*career + delta*clean_activity
    
    Args:
        semantic_score: Semantic score (0-1)
        skill_score: Skill match score (0-1)
        career_score: Career fit score (0-1)
        clean_activity_score: Clean activity score (0-1)
        weights: Dictionary with keys 'alpha', 'beta', 'gamma', 'delta'
        
    Returns:
        Dict with individual scores and final_score
    """
    try:
        if weights is None:
            weights = {'alpha': 0.4, 'beta': 0.3, 'gamma': 0.2, 'delta': 0.1}
        
        alpha = weights.get('alpha', 0.4)
        beta = weights.get('beta', 0.3)
        gamma = weights.get('gamma', 0.2)
        delta = weights.get('delta', 0.1)

        total_weight = alpha + beta + gamma + delta
        if total_weight <= 0:
            logger.warning("Invalid score weights supplied; using defaults")
            alpha, beta, gamma, delta = 0.4, 0.3, 0.2, 0.1
            total_weight = 1.0
        
        final_score = (
            alpha * semantic_score +
            beta * skill_score +
            gamma * career_score +
            delta * clean_activity_score
        ) / total_weight
        
        logger.debug(f"Final score: {final_score:.4f}")
        
        return {
            "semantic_score": min(max(semantic_score, 0.0), 1.0),
            "skill_score": min(max(skill_score, 0.0), 1.0),
            "career_score": min(max(career_score, 0.0), 1.0),
            "clean_activity": min(max(clean_activity_score, 0.0), 1.0),
            "final_score": min(max(final_score, 0.0), 1.0),
        }
        
    except Exception as e:
        logger.error(f"Error calculating final scores: {str(e)}")
        return {
            "semantic_score": 0.0,
            "skill_score": 0.0,
            "career_score": 0.0,
            "clean_activity": 0.0,
            "final_score": 0.0,
        }
