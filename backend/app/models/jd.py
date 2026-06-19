"""Job Description model for SmartHire AI."""

from typing import List, Optional


class JobDescription:
    """Job Description data model."""
    
    def __init__(
        self,
        role: str,
        skills: List[str],
        experience: int,
        education: Optional[str] = None,
        seniority: Optional[str] = None,
        certifications: Optional[List[str]] = None,
    ):
        self.role = role
        self.skills = skills
        self.experience = experience
        self.education = education or ""
        self.seniority = seniority or "Mid-level"
        self.certifications = certifications or []
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "role": self.role,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "seniority": self.seniority,
            "certifications": self.certifications,
        }
