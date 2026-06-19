"""Test bias removal functionality."""

import pytest
from app.services.bias_removal_service import remove_bias


def test_remove_bias_fields():
    """Test that bias fields are removed."""
    candidate = {
        "name": "John Doe",
        "skills": ["Python", "FastAPI"],
        "experience": 5,
        "employee_id": "EMP123",
        "referred_by": "Manager",
        "referral_flag": 1,
        "manager_name": "Jane Smith"
    }
    
    clean = remove_bias(candidate.copy())
    
    assert "employee_id" not in clean
    assert "referred_by" not in clean
    assert "referral_flag" not in clean
    assert "manager_name" not in clean
    assert clean["name"] == "John Doe"
    assert clean["skills"] == ["Python", "FastAPI"]


def test_remove_bias_preserves_other_fields():
    """Test that other fields are preserved."""
    candidate = {
        "name": "Jane Smith",
        "skills": ["Java", "Spring"],
        "experience": 8,
        "education": "BTech",
        "certifications": ["AWS"],
        "referred_by": "HR"
    }
    
    clean = remove_bias(candidate.copy())
    
    assert clean["name"] == "Jane Smith"
    assert clean["education"] == "BTech"
    assert clean["certifications"] == ["AWS"]
    assert "referred_by" not in clean


def test_remove_bias_idempotent():
    """Test that removing bias twice gives same result."""
    candidate = {
        "name": "Bob",
        "skills": ["C++"],
        "referred_by": "Someone"
    }
    
    clean1 = remove_bias(candidate.copy())
    clean2 = remove_bias(clean1.copy())
    
    assert clean1 == clean2
