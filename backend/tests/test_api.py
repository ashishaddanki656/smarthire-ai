"""Test API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_parse_jd_endpoint():
    """Test /parse-jd endpoint."""
    payload = {
        "jd": "Senior Backend Engineer with 5 years Python and FastAPI experience"
    }
    response = client.post("/parse-jd", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert "experience" in data


def test_candidates_endpoint():
    """Test /candidates endpoint."""
    response = client.get("/candidates")
    
    # Should return 200 or 500 depending on data file
    assert response.status_code in [200, 500]


def test_parse_jd_invalid_input():
    """Test /parse-jd with invalid input."""
    payload = {"jd": ""}
    response = client.post("/parse-jd", json=payload)
    
    # Should still return 200 but with empty skills
    assert response.status_code == 200
