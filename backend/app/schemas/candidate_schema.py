"""
Pydantic schemas for candidate related requests and responses.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Candidate(BaseModel):
    """
    Candidate profile model.

    Attributes:
        id (str): Unique candidate identifier
        name (str): Candidate name
        skills (List[str]): Technical skills
        experience (int): Years of experience
        education (str): Education level
        projects (List[str]): Notable projects
        certifications (List[str]): Certifications
        activity_score (float): Clean activity score
    """

    id: str
    name: str
    skills: List[str]
    experience: int
    education: str
    projects: Optional[List[str]] = Field(default_factory=list)
    certifications: Optional[List[str]] = Field(default_factory=list)
    activity_score: Optional[float] = 1.0

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "cand_001",
                "name": "John Doe",
                "skills": ["Python", "FastAPI", "Docker"],
                "experience": 5,
                "education": "BTech",
                "projects": ["Project A", "Project B"],
                "certifications": ["AWS Certified"],
                "activity_score": 0.95,
            }
        }
    )


class CandidateList(BaseModel):
    """
    Response model for candidate list.

    Attributes:
        total (int): Total number of candidates
        candidates (List[Dict[str, Any]]): List of candidates
    """

    total: int
    candidates: List[Dict[str, Any]]


class RankingResponse(BaseModel):
    """
    Response model for ranking endpoint.

    Attributes:
        total (int): Total candidates ranked
        results (List[Dict[str, Any]]): Ranked candidates with scores
        jd_parsed (Dict[str, Any]): Parsed job description used for ranking
    """

    total: int
    results: List[Dict[str, Any]]
    jd_parsed: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 100,
                "results": [
                    {
                        "rank": 1,
                        "id": "cand_001",
                        "name": "John Doe",
                        "semantic_score": 0.92,
                        "skill_score": 0.88,
                        "career_score": 0.84,
                        "clean_activity": 0.95,
                        "final_score": 0.90,
                        "explanation": "Strong backend experience with Python, FastAPI...",
                    }
                ],
                "jd_parsed": {
                    "role": "Backend Engineer",
                    "skills": ["Python", "FastAPI", "Docker", "AWS"],
                    "experience": 5,
                    "education": "BTech",
                    "seniority": "Senior",
                    "certifications": [],
                },
            }
        }
    )
