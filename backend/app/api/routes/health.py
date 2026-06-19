"""
Health check endpoint for SmartHire AI.
"""

from fastapi import APIRouter
from app.utils.logger import get_logger

logger = get_logger("HealthRoute")

router = APIRouter()


@router.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "SmartHire AI",
        "version": "1.0.0"
    }
