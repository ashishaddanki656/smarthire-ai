"""
JD (Job Description) Parsing endpoint for SmartHire AI.
"""

from fastapi import APIRouter
from app.schemas.jd_schema import JDRequest, ParsedJD
from app.services.jd_parser import parse_jd
from app.utils.logger import get_logger

logger = get_logger("JDRoute")

router = APIRouter()


@router.post("/parse-jd", response_model=ParsedJD, tags=["JD Parsing"])
def parse_jd_endpoint(request: JDRequest):
    """
    Parse job description and extract structured information.
    
    Args:
        request (JDRequest): Job description request
        
    Returns:
        ParsedJD: Parsed JD with role, skills, experience, education, seniority, certifications
    """
    try:
        logger.info("Received JD parsing request")
        logger.debug(f"JD text length: {len(request.jd)} characters")

        parsed_data = parse_jd(request.jd)

        logger.info(f"JD parsed successfully. Role: {parsed_data['role']}, Skills: {len(parsed_data['skills'])}")
        return parsed_data

    except Exception as e:
        logger.error(f"Error in parse_jd endpoint: {str(e)}")
        raise
