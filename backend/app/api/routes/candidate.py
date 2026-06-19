
"""
Candidates endpoint for SmartHire AI.
"""

from fastapi import APIRouter
from app.db.database import get_candidates
from app.schemas.candidate_schema import CandidateList
from app.utils.logger import get_logger

logger = get_logger("CandidateRoute")

router = APIRouter()


@router.get("/candidates", response_model=CandidateList, tags=["Candidates"])
def get_all_candidates():
    """
    Get all candidates from database.
    
    Returns:
        CandidateList: List of candidates
    """
    try:
        logger.info("Fetching all candidates")
        candidates = get_candidates()

        logger.info(f"Retrieved {len(candidates)} candidates")
        return {
            "total": len(candidates),
            "candidates": candidates
        }

    except Exception as e:
        logger.error(f"Error in get_candidates endpoint: {str(e)}")
        raise
