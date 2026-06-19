"""
Bias Removal Service for SmartHire AI.
Ensures fair ranking by removing referral-related bias fields.
"""

from typing import Dict, Any
from app.utils.logger import get_logger

logger = get_logger("BiasRemovalService")


class BiasRemovalService:
    """
    Service to remove bias-related fields from candidate profiles.
    
    Removes fields that could introduce referral bias:
    - employee_id: Internal employee identifier
    - referred_by: Who referred the candidate
    - referral_flag: Whether candidate was referred
    - manager_name: Hiring manager's name
    """

    # Fields that must be removed to ensure fairness
    BIAS_FIELDS = [
        "employee_id",
        "referred_by",
        "referral_flag",
        "manager_name",
        "internal_reference",
        "referral_date",
        "referrer_name",
        "hiring_manager",
        "department_head"
    ]

    @staticmethod
    def remove_bias(candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Remove bias fields from candidate profile."""
        if not isinstance(candidate, dict):
            logger.error(f"Invalid candidate type: {type(candidate)}")
            raise ValueError("Candidate must be a dictionary")

        try:
            logger.debug(f"Removing bias fields from candidate...")
            clean_candidate = candidate.copy()

            removed_fields = []
            for field in BiasRemovalService.BIAS_FIELDS:
                if field in clean_candidate:
                    clean_candidate.pop(field)
                    removed_fields.append(field)

            if removed_fields:
                logger.debug(f"Removed bias fields: {removed_fields}")

            return clean_candidate

        except Exception as e:
            logger.error(f"Error removing bias: {str(e)}")
            raise

    @staticmethod
    def is_fair(candidate: Dict[str, Any]) -> bool:
        """Check if candidate profile contains any bias fields."""
        if not isinstance(candidate, dict):
            return False

        for field in BiasRemovalService.BIAS_FIELDS:
            if field in candidate:
                logger.debug(f"Bias field detected: {field}")
                return False

        return True

    @staticmethod
    def get_bias_fields(candidate: Dict[str, Any]) -> list:
        """Get list of bias fields present in candidate."""
        if not isinstance(candidate, dict):
            return []

        found_fields = []
        for field in BiasRemovalService.BIAS_FIELDS:
            if field in candidate:
                found_fields.append(field)

        return found_fields


def remove_bias(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Remove bias fields from candidate profile."""
    return BiasRemovalService.remove_bias(candidate)


def is_fair(candidate: Dict[str, Any]) -> bool:
    """Check if candidate is fair (no bias fields)."""
    return BiasRemovalService.is_fair(candidate)


def get_bias_fields(candidate: Dict[str, Any]) -> list:
    """Get bias fields in candidate."""
    return BiasRemovalService.get_bias_fields(candidate)
