"""Candidate model for SmartHire AI."""

from typing import List, Optional, Dict, Any


class Candidate:
    """Candidate data model."""
    
    def __init__(
        self,
        name: str,
        skills: List[str],
        experience: int,
        education: Optional[str] = None,
        certifications: Optional[List[str]] = None,
        projects: Optional[List[str]] = None,
        referred_by: Optional[str] = None,
        employee_id: Optional[str] = None,
        referral_flag: Optional[int] = None,
        manager_name: Optional[str] = None,
        activity_score: Optional[float] = None,
    ):
        self.name = name
        self.skills = skills
        self.experience = experience
        self.education = education or ""
        self.certifications = certifications or []
        self.projects = projects or []
        
        # Referral metadata (will be removed before ranking)
        self.referred_by = referred_by
        self.employee_id = employee_id
        self.referral_flag = referral_flag
        self.manager_name = manager_name
        self.activity_score = activity_score or 0.8
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "certifications": self.certifications,
            "projects": self.projects,
            "referred_by": self.referred_by,
            "employee_id": self.employee_id,
            "referral_flag": self.referral_flag,
            "manager_name": self.manager_name,
            "activity_score": self.activity_score,
        }
    
    def to_clean_dict(self) -> Dict[str, Any]:
        """Convert to dictionary without referral bias fields."""
        return {
            "name": self.name,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "certifications": self.certifications,
            "projects": self.projects,
            "activity_score": self.activity_score,
        }
