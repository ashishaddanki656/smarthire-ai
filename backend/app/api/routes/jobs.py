"""
Jobs endpoint for SmartHire AI.
"""

from fastapi import APIRouter

from app.db.database import get_jobs
from app.utils.logger import get_logger

logger = get_logger("JobsRoute")

router = APIRouter()


@router.get("/jobs", tags=["Jobs"])
def get_all_jobs():
    """
    Get all jobs from data/jobs.csv.

    Returns:
        dict: Total count and job rows
    """
    try:
        logger.info("Fetching all jobs")
        jobs = get_jobs()

        logger.info(f"Retrieved {len(jobs)} jobs")
        return {
            "total": len(jobs),
            "jobs": jobs,
        }

    except Exception as e:
        logger.error(f"Error in get_jobs endpoint: {str(e)}")
        raise
