"""Test JD Parser functionality."""

import pytest
from app.services.jd_parser import parse_jd


def test_parse_jd_basic():
    """Test basic JD parsing."""
    jd_text = "Senior Backend Engineer with 5 years Python and FastAPI experience"
    result = parse_jd(jd_text)
    
    assert result['experience'] == 5
    assert 'Python' in result['skills']
    assert 'FastAPI' in result['skills']


def test_parse_jd_empty():
    """Test parsing empty JD."""
    result = parse_jd("")
    assert result['skills'] == []
    assert result['experience'] == 0


def test_parse_jd_with_certifications():
    """Test JD with certifications."""
    jd_text = "AWS certified professional needed for DevOps role"
    result = parse_jd(jd_text)
    
    assert 'AWS' in result['skills']


def test_parse_jd_extracts_years():
    """Test experience extraction."""
    jd_text = "We need someone with 7-10 years of experience in backend development"
    result = parse_jd(jd_text)
    
    # Should extract at least one year number
    assert result['experience'] > 0
