#!/usr/bin/env python
"""
Quick verification script for SmartHire AI backend modules.
"""

import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))


def run_check(name, callback):
    """Run one module check and keep the report readable."""
    print(f"\n[CHECK] {name}")
    try:
        callback()
        print(f"[PASS] {name}")
    except Exception as exc:
        print(f"[FAIL] {name}: {exc}")


print("=" * 70)
print("SMARTHIRE AI - MODULE VERIFICATION TEST")
print("=" * 70)


def check_config():
    from app.utils.config import ALPHA, BETA, DELTA, GAMMA, MODEL_NAME, TOP_K

    print(f"  - Model: {MODEL_NAME}")
    print(f"  - Top-K: {TOP_K}")
    print(f"  - Weights: alpha={ALPHA}, beta={BETA}, gamma={GAMMA}, delta={DELTA}")


def check_logger():
    from app.utils.logger import get_logger

    test_logger = get_logger("TestModule")
    test_logger.info("Logger test message")
    print("  - Logger initialized successfully")


def check_schemas():
    from app.schemas.candidate_schema import Candidate, RankingResponse
    from app.schemas.jd_schema import JDRequest, ParsedJD

    assert Candidate
    assert RankingResponse
    assert JDRequest
    assert ParsedJD
    print("  - All schemas imported successfully")


def check_models():
    from app.models.candidate import Candidate
    from app.models.jd import JobDescription

    assert Candidate
    assert JobDescription
    print("  - All models imported successfully")


def check_jd_parser():
    from app.services.jd_parser import parse_jd

    test_jd = (
        "Senior Python Developer with 5+ years FastAPI and Docker experience. "
        "Bachelor's degree required. AWS certified."
    )
    parsed = parse_jd(test_jd)
    print(f"  - Parsed role: {parsed['role']}")
    print(f"  - Found skills: {parsed['skills']}")
    print(f"  - Experience: {parsed['experience']}+ years")
    print(f"  - Education: {parsed['education']}")


def check_bias_removal():
    from app.services.bias_removal_service import remove_bias

    test_candidate = {
        "name": "John Doe",
        "skills": "Python, FastAPI",
        "experience": 5,
        "referred_by": "Manager",
        "employee_id": "EMP123",
        "referral_flag": 1,
    }
    clean = remove_bias(test_candidate.copy())
    print(f"  - Original fields: {list(test_candidate.keys())}")
    print(f"  - Clean fields: {list(clean.keys())}")
    print(f"  - Removed: {set(test_candidate.keys()) - set(clean.keys())}")


def check_scoring_service():
    import numpy as np

    from app.services.scoring_service import (
        calculate_career_score,
        calculate_clean_activity_score,
        calculate_scores,
        calculate_semantic_score,
        calculate_skill_score,
    )

    jd_emb = np.random.rand(1024).astype(np.float32)
    cand_emb = np.random.rand(1024).astype(np.float32)
    sem_score = calculate_semantic_score(jd_emb, cand_emb)
    skill_score = calculate_skill_score(["Python", "FastAPI", "Docker"], ["Python", "Docker"])
    career_score = calculate_career_score(5, 3, True, 1)
    profile = {"name": "John", "skills": ["Python"], "experience": 5, "education": "BTech"}
    clean_score = calculate_clean_activity_score(profile)
    combined = calculate_scores(sem_score, skill_score, career_score, clean_score)

    print(f"  - Semantic score: {sem_score:.4f}")
    print(f"  - Skill score: {skill_score:.4f} (2/3 skills)")
    print(f"  - Career score: {career_score:.4f}")
    print(f"  - Clean activity: {clean_score:.4f}")
    print(f"  - Final score: {combined['final_score']:.4f}")


def check_reranking_service():
    from app.services.rerank_service import rerank_candidates

    test_candidates = [
        {"name": "Alice", "final_score": 0.70},
        {"name": "Bob", "final_score": 0.90},
        {"name": "Charlie", "final_score": 0.80},
    ]
    test_scores = [
        {"semantic_score": 0.7},
        {"semantic_score": 0.9},
        {"semantic_score": 0.8},
    ]
    ranked = rerank_candidates(test_candidates, test_scores)
    print(f"  - Ranking order: {[candidate['name'] for candidate in ranked]}")
    print(f"  - Rank assignments: {[(candidate['name'], candidate.get('rank')) for candidate in ranked]}")


def check_explanation_service():
    from app.services.explanation_service import generate_explanation, get_recommendation

    test_candidate_with_scores = {
        "name": "John Doe",
        "skills": ["Python", "FastAPI"],
        "experience": 5,
        "semantic_score": 0.85,
        "skill_score": 0.75,
        "career_score": 0.80,
        "clean_activity": 0.90,
        "final_score": 0.82,
    }
    explanation = generate_explanation(test_candidate_with_scores)
    recommendation = get_recommendation(0.82)
    print(f"  - Explanation: {explanation[:80]}...")
    print(f"  - Recommendation: {recommendation}")


def check_database():
    from app.db.database import get_candidates

    candidates = get_candidates()
    print(f"  - Candidates loaded: {len(candidates)}")
    if candidates:
        print(f"  - First candidate: {candidates[0].get('name', 'Unknown')}")


checks = [
    ("Config", check_config),
    ("Logger", check_logger),
    ("Schemas", check_schemas),
    ("Models", check_models),
    ("JD Parser", check_jd_parser),
    ("Bias Removal", check_bias_removal),
    ("Scoring Service", check_scoring_service),
    ("Reranking Service", check_reranking_service),
    ("Explanation Service", check_explanation_service),
    ("Database", check_database),
]

for check_name, check_callback in checks:
    run_check(check_name, check_callback)

print("\n" + "=" * 70)
print("ALL MODULE CHECKS COMPLETED")
print("=" * 70)
print("\nReady to:")
print("  1. Start FastAPI server")
print("  2. Test endpoints")
print("  3. Rank candidates")
print("\n" + "=" * 70)
