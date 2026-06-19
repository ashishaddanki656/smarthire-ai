"""
Pydantic schemas for job description related requests and responses.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JDRequest(BaseModel):
    """
    Request model for JD parsing endpoint.

    Attributes:
        jd (str): Job description text to parse
    """

    jd: str

    @field_validator("jd")
    @classmethod
    def validate_jd(cls, value: str) -> str:
        """Normalize incoming job description text."""
        return value.strip() if value else ""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "jd": "Senior Backend Engineer with 5+ years experience in Python, FastAPI, Docker, AWS..."
            }
        }
    )


class ParsedJD(BaseModel):
    """
    Response model for parsed job description.

    Attributes:
        role (str): Job role/title
        skills (List[str]): Required technical skills
        experience (int): Years of experience required
        education (str): Required education level
        seniority (str): Seniority level
        certifications (List[str]): Required certifications
    """

    role: str
    skills: List[str]
    experience: int
    education: str
    seniority: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "Backend Engineer",
                "skills": ["Python", "FastAPI", "Docker", "AWS"],
                "experience": 5,
                "education": "BTech",
                "seniority": "Senior",
                "certifications": [],
            }
        }
    )
