"""
Ranking endpoint for SmartHire AI.
Core endpoint that orchestrates the ranking pipeline.
Integrates AS (AI & Backend) with CH (Chaturya & Rohith) modules.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import numpy as np
from app.schemas.jd_schema import JDRequest
from app.schemas.candidate_schema import RankingResponse
from app.services.jd_parser import parse_jd
from app.services.embedding_service import generate_jd_embedding, generate_embeddings_batch
from app.services.faiss_service import build_index, add_vectors, search_top_k
from app.services.bias_removal_service import remove_bias
from app.services.scoring_service import (
    calculate_semantic_score,
    calculate_skill_score,
    calculate_career_score,
    calculate_clean_activity_score,
    calculate_scores
)
from app.services.rerank_service import (
    rerank_candidates,
    apply_fairness_constraints,
    apply_tie_breaking
)
from app.services.explanation_service import (
    generate_explanation,
    generate_detailed_explanation,
    format_for_csv
)
from app.db.database import get_candidates, save_ranking_results
from app.utils.logger import get_logger
from app.utils.config import TOP_K, ALPHA, BETA, GAMMA, DELTA

logger = get_logger("RankingRoute")

router = APIRouter()


@router.post("/rank", response_model=RankingResponse, tags=["Ranking"])
def rank_candidates(request: JDRequest):
    """
    Rank candidates against a job description.
    
    COMPLETE PIPELINE:
    ==================
    1. Parse JD -> extract skills, experience, education, etc.
    2. Generate JD embedding (BGE model)
    3. Load candidates from database
    4. Generate candidate embeddings (batch)
    5. Build FAISS index
    6. Search top-k candidates
    7. Remove referral bias (fair ranking)
    8. Calculate 4 scores per candidate:
       - Semantic score (JD vs candidate embedding similarity)
       - Skill score (required vs candidate skills)
       - Career score (experience, education, certifications)
       - Clean activity score (profile quality)
    9. Calculate weighted final score: alpha*semantic + beta*skill + gamma*career + delta*clean_activity
    10. Rerank by final score
    11. Apply fairness constraints
    12. Apply tie-breaking
    13. Generate explanations
    14. Return ranked results
    
    Args:
        request (JDRequest): Job description request
        
    Returns:
        RankingResponse: Ranked candidates with all scores and explanations
    """
    try:
        logger.info("=" * 70)
        logger.info("STARTING COMPLETE RANKING PIPELINE (AS + CH Integration)")
        logger.info("=" * 70)

        # ============ STEP 1-7: RETRIEVAL & BIAS REMOVAL (AS) ============
        
        # Step 1: Parse JD
        logger.info("Step 1: Parsing Job Description...")
        jd_data = parse_jd(request.jd)
        logger.info(f"   Role: {jd_data['role']}")
        logger.info(f"   Skills: {jd_data['skills']}")
        logger.info(f"   Experience: {jd_data['experience']}+ years")

        # Step 2: Generate JD embedding
        logger.info("Step 2: Generating JD Embedding (BGE-Large)...")
        jd_embedding = generate_jd_embedding(request.jd)
        logger.info(f"   Embedding shape: {jd_embedding.shape}")

        # Step 3: Load candidates
        logger.info("Step 3: Loading Candidates...")
        candidates = get_candidates()
        if not candidates:
            logger.warning("   No candidates found in database")
            raise HTTPException(status_code=404, detail="No candidates found in database")
        logger.info(f"   Loaded {len(candidates)} candidates")

        # Step 4: Generate candidate embeddings (batch)
        logger.info("Step 4: Generating Candidate Embeddings (Batch)...")
        candidate_texts = []
        candidate_ids = []
        clean_candidates = []

        for candidate in candidates:
            # Remove bias fields FIRST for fair ranking
            clean_cand = remove_bias(candidate.copy())

            # Create profile text for embedding
            profile_parts = [
                str(clean_cand.get("name", "")),
                str(clean_cand.get("skills", "")),
                str(clean_cand.get("education", "")),
                str(clean_cand.get("experience", "")),
                str(clean_cand.get("projects", "")),
                str(clean_cand.get("certifications", ""))
            ]
            profile_text = " ".join(profile_parts)

            candidate_texts.append(profile_text)
            candidate_ids.append(clean_cand.get("id", f"cand_{len(candidate_ids)}"))
            clean_candidates.append(clean_cand)

        # Batch embed
        candidate_embeddings = generate_embeddings_batch(candidate_texts)
        logger.info(f"   Batch embeddings shape: {candidate_embeddings.shape}")

        # Step 5: Build FAISS index
        logger.info("Step 5: Building FAISS Index (IndexFlatIP)...")
        dim = len(jd_embedding)
        build_index(dim)
        add_vectors(candidate_embeddings, candidate_ids)
        logger.info(f"   FAISS index built with {len(candidates)} vectors")

        # Step 6: Search top-k
        logger.info(f"Step 6: Semantic Search - Retrieving Top {TOP_K} Candidates...")
        faiss_scores, faiss_indices = search_top_k(jd_embedding, k=min(TOP_K, len(candidates)))
        logger.info(f"   Retrieved {len(faiss_indices[0])} candidates")

        # ============ STEP 8-9: SCORING (CH - Chaturya/Rohith) ============
        
        logger.info("Step 8-9: Calculating Scores (Semantic + Skill + Career + Activity)...")
        
        all_candidates_with_scores = []
        
        for rank_idx, (faiss_score, faiss_idx) in enumerate(zip(faiss_scores[0], faiss_indices[0])):
            if faiss_idx < len(clean_candidates):
                candidate = clean_candidates[faiss_idx].copy()
                
                # ====== SCORE 1: SEMANTIC SCORE ======
                # Similarity between JD and candidate embeddings
                semantic_score = calculate_semantic_score(
                    jd_embedding,
                    candidate_embeddings[faiss_idx]
                )
                
                # ====== SCORE 2: SKILL SCORE ======
                # Match required skills with candidate skills
                required_skills = jd_data.get('skills', [])
                candidate_skills = candidate.get('skills', [])
                if isinstance(candidate_skills, str):
                    candidate_skills = [s.strip() for s in candidate_skills.split(',')]
                
                skill_score = calculate_skill_score(required_skills, candidate_skills)
                
                # ====== SCORE 3: CAREER SCORE ======
                # Experience, education, certifications matching
                candidate_experience = int(candidate.get('experience', 0))
                required_experience = jd_data.get('experience', 3)
                
                education_match = candidate.get('education', '').lower() in (
                    jd_data.get('education', '').lower() or ''
                )
                
                certifications = candidate.get('certifications', [])
                if isinstance(certifications, str):
                    certifications = [c.strip() for c in certifications.split(',') if c.strip()]
                
                career_score = calculate_career_score(
                    candidate_experience,
                    required_experience,
                    education_match,
                    len(certifications)
                )
                
                # ====== SCORE 4: CLEAN ACTIVITY SCORE ======
                # Profile quality, completeness, authenticity
                clean_activity_score = calculate_clean_activity_score(candidate)
                
                # ====== FINAL SCORE: WEIGHTED SUM ======
                weights = {
                    'alpha': ALPHA,    # 0.4
                    'beta': BETA,      # 0.3
                    'gamma': GAMMA,    # 0.2
                    'delta': DELTA     # 0.1
                }
                
                scores = calculate_scores(
                    semantic_score,
                    skill_score,
                    career_score,
                    clean_activity_score,
                    weights
                )
                
                # Combine with candidate data
                candidate_with_scores = {**candidate, **scores}
                all_candidates_with_scores.append(candidate_with_scores)
        
        logger.info(f"   Calculated scores for {len(all_candidates_with_scores)} candidates")

        # ============ STEP 10-12: RERANKING (CH) ============
        
        logger.info("Step 10: Reranking Candidates by Final Score...")
        
        # Extract scores only (for rerank function)
        scores_list = [
            {k: v for k, v in candidate.items() 
             if k in ['semantic_score', 'skill_score', 'career_score', 'clean_activity', 'final_score']}
            for candidate in all_candidates_with_scores
        ]
        
        ranked_candidates = rerank_candidates(all_candidates_with_scores, scores_list)
        logger.info(f"   Reranked {len(ranked_candidates)} candidates")

        # Step 11: Apply fairness constraints
        logger.info("Step 11: Applying Fairness Constraints...")
        ranked_candidates = apply_fairness_constraints(ranked_candidates)
        logger.info("   Fairness check passed")

        # Step 12: Apply tie-breaking
        logger.info("Step 12: Applying Tie-Breaking Logic...")
        ranked_candidates = apply_tie_breaking(ranked_candidates)
        logger.info("   Tie-breaking applied")

        # ============ STEP 13: EXPLANATIONS (CH) ============
        
        logger.info("Step 13: Generating Explanations...")
        final_results = []
        
        for candidate in ranked_candidates:
            # Generate explanation
            explanation = generate_explanation(candidate)
            candidate['explanation'] = explanation
            
            # Add detailed breakdown
            candidate['detailed_explanation'] = generate_detailed_explanation(candidate, jd_data)
            
            final_results.append(candidate)
        
        logger.info(f"   Generated explanations for {len(final_results)} candidates")

        # ============ SAVE RESULTS ============
        
        logger.info("Saving Ranking Results to CSV...")
        try:
            csv_results = [format_for_csv(candidate) for candidate in final_results]
            save_ranking_results(csv_results)
            logger.info("   Results saved to docs/output/ranked_output.csv")
        except Exception as e:
            logger.warning(f"   Could not save CSV: {str(e)}")

        # ============ RETURN RESULTS ============
        
        logger.info("=" * 70)
        logger.info("RANKING PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        
        logger.info(f"FINAL RESULTS: {len(final_results)} candidates ranked")
        if final_results:
            logger.info(f"   Top candidate: {final_results[0].get('name')} (Score: {final_results[0].get('final_score'):.2f})")

        return {
            "total": len(final_results),
            "results": final_results,
            "jd_parsed": jd_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ERROR in ranking pipeline: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ranking failed: {str(e)}")
