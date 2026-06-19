"""
Explanation service for SmartHire AI.
Generates human-readable explanations for rankings.
Responsible: Team Member 4 (Chaturya/Rohith)
"""

from typing import Dict, Any, List
from app.utils.logger import get_logger

logger = get_logger("ExplanationService")


def generate_explanation(candidate: Dict[str, Any]) -> str:
    """
    Generate human-readable explanation for candidate ranking.
    
    Args:
        candidate: Candidate with scores
        
    Returns:
        str: Human-readable explanation
    """
    try:
        explanations = []
        
        # Semantic fit explanation
        semantic = candidate.get('semantic_score', 0)
        if semantic > 0.85:
            explanations.append(f"Excellent semantic match ({semantic:.1%}) with job description")
        elif semantic > 0.70:
            explanations.append(f"Good semantic match ({semantic:.1%}) with job requirements")
        elif semantic > 0.50:
            explanations.append(f"Moderate semantic match ({semantic:.1%}) with job description")
        else:
            explanations.append(f"Limited semantic match ({semantic:.1%}) - profile differs from JD")
        
        # Skill match explanation
        skill = candidate.get('skill_score', 0)
        if skill > 0.85:
            explanations.append(f"Strong skill alignment ({skill:.1%}) - has most required skills")
        elif skill > 0.70:
            explanations.append(f"Good skill match ({skill:.1%}) with required competencies")
        elif skill > 0.50:
            explanations.append(f"Partial skill match ({skill:.1%}) - missing some key skills")
        else:
            explanations.append(f"Limited skills ({skill:.1%}) - significant skill gaps remain")
        
        # Career fit explanation
        career = candidate.get('career_score', 0)
        if career > 0.85:
            explanations.append(f"Excellent career progression ({career:.1%}) and deep relevant experience")
        elif career > 0.70:
            explanations.append(f"Good career fit ({career:.1%}) with relevant background")
        elif career > 0.50:
            explanations.append(f"Moderate experience ({career:.1%}) - meets minimum requirements")
        else:
            explanations.append(f"Limited experience ({career:.1%}) - early in career")
        
        # Clean activity explanation
        clean = candidate.get('clean_activity', 0)
        if clean > 0.85:
            explanations.append("Profile appears genuine with strong application quality")
        elif clean > 0.70:
            explanations.append("Profile appears legitimate with good activity patterns")
        elif clean > 0.50:
            explanations.append("Profile has some quality concerns but appears authentic")
        else:
            explanations.append("Profile shows signs of incomplete information or suspicious activity")
        
        explanation_text = ". ".join(explanations) + "."
        
        logger.debug(f"Generated explanation for {candidate.get('name', 'Unknown')}")
        return explanation_text
        
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        return "Unable to generate explanation."


def generate_detailed_explanation(
    candidate: Dict[str, Any],
    jd_parsed: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate detailed explanation with breakdown by component.
    
    Args:
        candidate: Candidate with scores
        jd_parsed: Parsed job description
        
    Returns:
        Dict with detailed breakdown and explanations
    """
    try:
        semantic = candidate.get('semantic_score', 0)
        skill = candidate.get('skill_score', 0)
        career = candidate.get('career_score', 0)
        clean = candidate.get('clean_activity', 0)
        final = candidate.get('final_score', 0)
        
        return {
            "candidate_name": candidate.get('name', 'Unknown'),
            "rank": candidate.get('rank', 'N/A'),
            "final_score": final,
            "score_breakdown": {
                "semantic_score": {
                    "value": semantic,
                    "percentage": f"{semantic:.1%}",
                    "explanation": "How well the candidate's profile matches the job semantically"
                },
                "skill_score": {
                    "value": skill,
                    "percentage": f"{skill:.1%}",
                    "explanation": f"Skills match: {skill:.1%} of required skills present"
                },
                "career_score": {
                    "value": career,
                    "percentage": f"{career:.1%}",
                    "explanation": "Experience, education, and certification fit"
                },
                "clean_activity": {
                    "value": clean,
                    "percentage": f"{clean:.1%}",
                    "explanation": "Profile authenticity and application quality"
                }
            },
            "summary": generate_explanation(candidate),
            "key_strengths": extract_strengths(candidate, jd_parsed),
            "areas_for_growth": extract_gaps(candidate, jd_parsed),
            "recommendation": get_recommendation(final)
        }
        
    except Exception as e:
        logger.error(f"Error generating detailed explanation: {str(e)}")
        return {}


def extract_strengths(
    candidate: Dict[str, Any],
    jd_parsed: Dict[str, Any]
) -> List[str]:
    """
    Extract candidate strengths based on job requirements.
    
    Args:
        candidate: Candidate data
        jd_parsed: Parsed JD
        
    Returns:
        List of strengths
    """
    try:
        strengths = []
        
        # Parse skills from strings or lists
        candidate_skills = candidate.get('skills', [])
        if isinstance(candidate_skills, str):
            candidate_skills = [s.strip() for s in candidate_skills.split(',')]
        
        required_skills = jd_parsed.get('skills', [])
        if isinstance(required_skills, str):
            required_skills = [s.strip() for s in required_skills.split(',')]
        
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        # Matching skills
        matching_skills = [s for s in required_skills_lower if s in candidate_skills_lower]
        if matching_skills:
            match_count = len(matching_skills)
            total_count = len(required_skills_lower)
            strengths.append(f"Possesses {match_count} of {total_count} required skills")
        
        # Experience match
        candidate_exp = candidate.get('experience', 0)
        required_exp = jd_parsed.get('experience', 0)
        if candidate_exp >= required_exp:
            strength_desc = f"{candidate_exp} years of experience"
            if candidate_exp > required_exp:
                strength_desc += f" (exceeds {required_exp}+ requirement)"
            else:
                strength_desc += f" (meets requirement)"
            strengths.append(strength_desc)
        
        # Education match
        candidate_edu = candidate.get('education', '')
        jd_edu = jd_parsed.get('education', '')
        if candidate_edu and jd_edu:
            strengths.append(f"Educational background: {candidate_edu}")
        
        # Certifications
        certifications = candidate.get('certifications', [])
        if isinstance(certifications, str):
            certifications = [c.strip() for c in certifications.split(',') if c.strip()]
        
        if certifications:
            strengths.append(f"Relevant certifications: {', '.join(certifications[:3])}")
        
        # Projects
        projects = candidate.get('projects', [])
        if isinstance(projects, str):
            projects = [p.strip() for p in projects.split(',') if p.strip()]
        
        if projects:
            strengths.append(f"Demonstrated experience in: {', '.join(projects[:2])}")
        
        return strengths
        
    except Exception as e:
        logger.error(f"Error extracting strengths: {str(e)}")
        return []


def extract_gaps(
    candidate: Dict[str, Any],
    jd_parsed: Dict[str, Any]
) -> List[str]:
    """
    Extract skill gaps and development areas.
    
    Args:
        candidate: Candidate data
        jd_parsed: Parsed JD
        
    Returns:
        List of gaps and areas for growth
    """
    try:
        gaps = []
        
        # Parse skills from strings or lists
        candidate_skills = candidate.get('skills', [])
        if isinstance(candidate_skills, str):
            candidate_skills = [s.strip() for s in candidate_skills.split(',')]
        
        required_skills = jd_parsed.get('skills', [])
        if isinstance(required_skills, str):
            required_skills = [s.strip() for s in required_skills.split(',')]
        
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        # Missing skills
        missing_skills = [s for s in required_skills_lower if s not in candidate_skills_lower]
        if missing_skills:
            gaps.append(f"Would benefit from learning: {', '.join(missing_skills[:3])}")
        
        # Experience gap
        candidate_exp = candidate.get('experience', 0)
        required_exp = jd_parsed.get('experience', 0)
        if candidate_exp < required_exp:
            gap = required_exp - candidate_exp
            gaps.append(f"Need {gap} more years of experience (currently {candidate_exp}, need {required_exp}+)")
        
        # Education gap
        candidate_edu = candidate.get('education', '')
        jd_edu = jd_parsed.get('education', '')
        if jd_edu and not candidate_edu:
            gaps.append(f"Educational requirement: {jd_edu}")
        
        # Certification gap
        certifications = candidate.get('certifications', [])
        if isinstance(certifications, str):
            certifications = [c.strip() for c in certifications.split(',') if c.strip()]
        
        if not certifications:
            gaps.append("Consider pursuing relevant industry certifications")
        
        return gaps
        
    except Exception as e:
        logger.error(f"Error extracting gaps: {str(e)}")
        return []


def get_recommendation(final_score: float) -> str:
    """
    Get hiring recommendation based on final score.
    
    Args:
        final_score: Final calculated score
        
    Returns:
        str: Recommendation text
    """
    try:
        if final_score >= 0.90:
            return "STRONG RECOMMEND - Excellent fit for the role"
        elif final_score >= 0.80:
            return "RECOMMEND - Good fit with strong qualifications"
        elif final_score >= 0.70:
            return "CONSIDER - Reasonable fit, can succeed with training"
        elif final_score >= 0.60:
            return "REVIEW - Moderate fit, evaluate carefully"
        elif final_score >= 0.50:
            return "? MARGINAL - Limited fit, significant gaps exist"
        else:
            return "NOT RECOMMENDED - Poor fit for this role"
            
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return "UNABLE TO RECOMMEND"


def format_for_csv(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format candidate data for CSV export.
    
    Args:
        candidate: Ranked candidate
        
    Returns:
        Dict formatted for CSV
    """
    try:
        # Parse lists to strings
        skills = candidate.get('skills', [])
        if isinstance(skills, list):
            skills = '; '.join(skills[:10])
        
        certifications = candidate.get('certifications', [])
        if isinstance(certifications, list):
            certifications = '; '.join(certifications[:5])
        
        projects = candidate.get('projects', [])
        if isinstance(projects, list):
            projects = '; '.join(projects[:5])
        
        return {
            'rank': candidate.get('rank'),
            'name': candidate.get('name', 'Unknown'),
            'skills': skills,
            'experience_years': candidate.get('experience', 0),
            'education': candidate.get('education', ''),
            'certifications': certifications,
            'projects': projects,
            'semantic_score': f"{candidate.get('semantic_score', 0):.2f}",
            'skill_score': f"{candidate.get('skill_score', 0):.2f}",
            'career_score': f"{candidate.get('career_score', 0):.2f}",
            'clean_activity': f"{candidate.get('clean_activity', 0):.2f}",
            'final_score': f"{candidate.get('final_score', 0):.2f}",
            'explanation': generate_explanation(candidate)
        }
        
    except Exception as e:
        logger.error(f"Error formatting for CSV: {str(e)}")
        return {}
