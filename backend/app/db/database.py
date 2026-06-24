"""
Database operations for SmartHire AI.
Handles loading, saving, and managing candidate data.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.utils.logger import get_logger
from app.utils.config import CANDIDATES_FILE, OUTPUT_RANKING_FILE, SAMPLE_CANDIDATES_FILE

logger = get_logger("Database")


class Database:
    """
    Database service for candidate data management.
    Uses CSV files for data storage in this MVP.
    """

    @staticmethod
    def load_candidates() -> pd.DataFrame:
        """
        Load candidates from CSV file.
        
        Returns:
            pd.DataFrame: Candidates DataFrame
        """
        candidates_path = Path(CANDIDATES_FILE)

        try:
            if not candidates_path.exists():
                sample_path = Path(SAMPLE_CANDIDATES_FILE)
                if sample_path.exists():
                    logger.warning(
                        f"Candidates file not found at {CANDIDATES_FILE}; "
                        f"falling back to {SAMPLE_CANDIDATES_FILE}"
                    )
                    candidates_path = sample_path
                else:
                    logger.warning(f"Candidates file not found at {CANDIDATES_FILE}")
                    return pd.DataFrame()

            logger.info(f"Loading candidates from {candidates_path}...")
            df = pd.read_csv(candidates_path)
            df = Database._normalize_candidate_columns(df)
            logger.info(f"Loaded {len(df)} candidates")
            return df

        except Exception as e:
            logger.error(f"Error loading candidates: {str(e)}")
            raise

    @staticmethod
    def _normalize_candidate_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize SR dataset columns into the fields used by ranking."""
        if df.empty:
            return df

        normalized = df.copy()

        rename_map = {
            "candidate_id": "id",
            "years_experience": "experience",
            "education_text": "education",
            "certs_text": "certifications",
            "career_text": "projects",
            "profile_completeness": "profile_completeness_score",
        }
        normalized = normalized.rename(
            columns={old: new for old, new in rename_map.items() if old in normalized.columns}
        )

        if "skills" not in normalized.columns:
            for source_col in ("top_skills_text", "skills_list", "assessment_skills_text"):
                if source_col in normalized.columns:
                    normalized["skills"] = normalized[source_col]
                    break

        if "activity_score" not in normalized.columns and "profile_completeness_score" in normalized.columns:
            normalized["activity_score"] = normalized["profile_completeness_score"].fillna(0) / 100

        if "candidate_text" not in normalized.columns and "embedding_text" in normalized.columns:
            normalized["candidate_text"] = normalized["embedding_text"]

        if "name" not in normalized.columns:
            normalized["name"] = normalized.get("id", "Unknown")

        if "id" not in normalized.columns:
            normalized.insert(0, "id", [f"cand_{idx + 1:03d}" for idx in range(len(normalized))])

        return normalized

    @staticmethod
    def load_jobs() -> pd.DataFrame:
        """Load job rows from the root data folder."""
        jobs_path = Path("data/jobs.csv")

        try:
            if not jobs_path.exists():
                logger.warning("Jobs file not found at data/jobs.csv")
                return pd.DataFrame()

            logger.info(f"Loading jobs from {jobs_path}...")
            df = pd.read_csv(jobs_path)
            if "id" not in df.columns:
                df.insert(0, "id", [f"job_{idx + 1:03d}" for idx in range(len(df))])
            logger.info(f"Loaded {len(df)} jobs")
            return df

        except Exception as e:
            logger.error(f"Error loading jobs: {str(e)}")
            raise

    @staticmethod
    def get_jobs() -> List[Dict[str, Any]]:
        """Get all jobs as a list of dictionaries."""
        df = Database.load_jobs()
        if df.empty:
            logger.warning("No jobs found")
            return []

        return df.where(pd.notna(df), None).to_dict(orient="records")

    @staticmethod
    def get_candidates() -> List[Dict[str, Any]]:
        """
        Get all candidates as list of dicts.
        
        Returns:
            List[Dict]: Candidates as list of dictionaries
        """
        df = Database.load_candidates()
        if df.empty:
            logger.warning("No candidates found")
            return []

        # Convert NaN to None for JSON serialization
        return df.where(pd.notna(df), None).to_dict(orient="records")

    @staticmethod
    def get_candidate_by_id(candidate_id: str) -> Optional[Dict[str, Any]]:
        """
        Get candidate by ID.
        
        Args:
            candidate_id (str): Candidate ID
            
        Returns:
            Dict: Candidate data or None
        """
        df = Database.load_candidates()

        if df.empty:
            return None

        # Try different ID column names
        id_columns = ['id', 'candidate_id', 'cand_id', 'ID']
        for col in id_columns:
            if col in df.columns:
                result = df[df[col] == candidate_id]
                if not result.empty:
                    return result.iloc[0].to_dict()

        logger.warning(f"Candidate {candidate_id} not found")
        return None

    @staticmethod
    def save_ranking_results(results: List[Dict[str, Any]], output_path: str = OUTPUT_RANKING_FILE) -> None:
        """
        Save ranking results to CSV.
        
        Args:
            results (List[Dict]): Ranking results
            output_path (str): Output file path
        """
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            df = pd.DataFrame(results)
            logger.info(f"Saving {len(results)} ranking results to {output_path}...")
            df.to_csv(output_path, index=False)
            logger.info(f"Ranking results saved successfully")

        except Exception as e:
            logger.error(f"Error saving ranking results: {str(e)}")
            raise

    @staticmethod
    def create_sample_candidates(output_path: str = CANDIDATES_FILE) -> None:
        """
        Create sample candidate data for testing.
        
        Args:
            output_path (str): Path to save sample data
        """
        sample_data = [
            {
                "id": "cand_001",
                "name": "John Doe",
                "skills": "Python, FastAPI, Docker, AWS",
                "experience": 5,
                "education": "BTech",
                "projects": "Project A, Project B",
                "certifications": "AWS Certified",
                "activity_score": 0.95
            },
            {
                "id": "cand_002",
                "name": "Jane Smith",
                "skills": "Python, Django, PostgreSQL, Kubernetes",
                "experience": 4,
                "education": "Master",
                "projects": "Project C, Project D",
                "certifications": "Kubernetes Certified",
                "activity_score": 0.92
            },
            {
                "id": "cand_003",
                "name": "Bob Johnson",
                "skills": "Java, Spring, Docker, GCP",
                "experience": 6,
                "education": "BTech",
                "projects": "Project E, Project F",
                "certifications": "GCP Certified",
                "activity_score": 0.88
            },
            {
                "id": "cand_004",
                "name": "Alice Williams",
                "skills": "Python, FastAPI, Redis, AWS, Machine Learning",
                "experience": 7,
                "education": "Master",
                "projects": "ML Project, Data Pipeline",
                "certifications": "AWS Certified, ML Certified",
                "activity_score": 0.96
            },
            {
                "id": "cand_005",
                "name": "Charlie Brown",
                "skills": "Python, Flask, MongoDB",
                "experience": 2,
                "education": "BTech",
                "projects": "Internship Project",
                "certifications": "",
                "activity_score": 0.75
            },
        ]

        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            df = pd.DataFrame(sample_data)
            logger.info(f"Creating sample candidates at {output_path}...")
            df.to_csv(output_path, index=False)
            logger.info(f"Sample candidates created successfully")

        except Exception as e:
            logger.error(f"Error creating sample candidates: {str(e)}")
            raise


def load_candidates() -> pd.DataFrame:
    """Load candidates from CSV."""
    return Database.load_candidates()


def get_candidates() -> List[Dict[str, Any]]:
    """Get all candidates."""
    return Database.get_candidates()


def get_jobs() -> List[Dict[str, Any]]:
    """Get all jobs."""
    return Database.get_jobs()


def save_ranking_results(results: List[Dict[str, Any]]) -> None:
    """Save ranking results."""
    return Database.save_ranking_results(results)
