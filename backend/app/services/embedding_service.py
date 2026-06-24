"""
Embedding Service for SmartHire AI.
Generates embeddings for JD and candidate profiles using BGE model.
"""

import numpy as np
from pathlib import Path
from typing import List
from app.utils.logger import get_logger
from app.utils.config import MODEL_NAME, DEVICE, MODEL_DIMENSION

logger = get_logger("EmbeddingService")


def _ensure_local_model_cache() -> None:
    """Keep Hugging Face cache inside the project when no cache is configured."""
    import os

    cache_dir = Path("data/model_cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(cache_dir))
    os.environ.setdefault("TRANSFORMERS_CACHE", str(cache_dir))


class EmbeddingService:
    """
    Service for generating embeddings using BAAI/bge-large-en-v1.5 model.
    Supports both single text and batch embedding generation.
    """

    _model = None

    @classmethod
    def get_model(cls):
        """Lazy load embedding model (singleton pattern)."""
        if cls._model is None:
            try:
                _ensure_local_model_cache()
                from sentence_transformers import SentenceTransformer

                logger.info(f"Loading embedding model: {MODEL_NAME}")
                cls._model = SentenceTransformer(MODEL_NAME, device=DEVICE)
                logger.info("Embedding model loaded successfully")
            except Exception as exc:
                logger.error(f"Could not load embedding model: {exc}")
                raise RuntimeError(
                    "Embedding model could not be loaded. Check that torch/sentence-transformers "
                    "are installed and allowed by Windows security policy."
                ) from exc
        return cls._model

    @staticmethod
    def generate_jd_embedding(jd_text: str) -> np.ndarray:
        """Generate embedding for job description."""
        if not jd_text or not isinstance(jd_text, str):
            logger.error("Invalid JD text provided")
            raise ValueError("JD text must be a non-empty string")

        try:
            model = EmbeddingService.get_model()
            logger.info("Generating JD embedding...")

            jd_text_with_prefix = "Represent the document for retrieval: " + jd_text
            embedding = model.encode(jd_text_with_prefix, convert_to_numpy=True)

            logger.info(f"JD embedding generated. Shape: {embedding.shape}")
            return embedding

        except Exception as e:
            logger.error(f"Error generating JD embedding: {str(e)}")
            raise

    @staticmethod
    def generate_candidate_embedding(candidate_profile: str) -> np.ndarray:
        """Generate embedding for candidate profile."""
        if not candidate_profile or not isinstance(candidate_profile, str):
            logger.error("Invalid candidate profile provided")
            raise ValueError("Profile text must be a non-empty string")

        try:
            model = EmbeddingService.get_model()

            profile_with_prefix = "Represent the document for retrieval: " + candidate_profile
            embedding = model.encode(profile_with_prefix, convert_to_numpy=True)

            logger.debug(f"Candidate embedding generated. Shape: {embedding.shape}")
            return embedding

        except Exception as e:
            logger.error(f"Error generating candidate embedding: {str(e)}")
            raise

    @staticmethod
    def generate_embeddings_batch(texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts in batch."""
        if not texts or len(texts) == 0:
            logger.error("Empty text list provided")
            raise ValueError("Text list cannot be empty")

        try:
            model = EmbeddingService.get_model()
            logger.info(f"Generating batch embeddings for {len(texts)} texts...")

            texts_with_prefix = [
                "Represent the document for retrieval: " + text for text in texts
            ]
            embeddings = model.encode(texts_with_prefix, convert_to_numpy=True)

            logger.info(f"Batch embeddings generated. Shape: {embeddings.shape}")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise

    @staticmethod
    def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings."""
        norm1 = embedding1 / np.linalg.norm(embedding1)
        norm2 = embedding2 / np.linalg.norm(embedding2)

        similarity = np.dot(norm1, norm2)
        return float(similarity)


def generate_jd_embedding(jd_text: str) -> np.ndarray:
    """Generate embedding for job description."""
    return EmbeddingService.generate_jd_embedding(jd_text)


def generate_candidate_embedding(candidate_profile: str) -> np.ndarray:
    """Generate embedding for candidate profile."""
    return EmbeddingService.generate_candidate_embedding(candidate_profile)


def generate_embeddings_batch(texts: List[str]) -> np.ndarray:
    """Generate embeddings for multiple texts."""
    return EmbeddingService.generate_embeddings_batch(texts)
