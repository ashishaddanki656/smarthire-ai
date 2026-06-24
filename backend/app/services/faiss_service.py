"""
FAISS Vector Search Service for SmartHire AI.
Manages FAISS index operations for semantic candidate search.
"""

import faiss
import numpy as np
import pickle
from typing import Tuple, List, Optional
from pathlib import Path
from app.utils.logger import get_logger
from app.utils.config import FAISS_INDEX_PATH, FAISS_ID_MAPPING_PATH, MODEL_DIMENSION

logger = get_logger("FAISSService")


class FAISSService:
    """
    Service for managing FAISS vector index operations.
    Provides methods for building, adding, searching, and persisting index.
    """

    _index = None
    _id_mapping = {}

    @staticmethod
    def build_index(dimension: int = MODEL_DIMENSION) -> faiss.IndexFlatIP:
        """Build a new FAISS index with IndexFlatIP."""
        try:
            logger.info(f"Building FAISS index with dimension: {dimension}")
            FAISSService._index = faiss.IndexFlatIP(dimension)
            FAISSService._id_mapping = {}
            logger.info("FAISS index built successfully")
            return FAISSService._index

        except Exception as e:
            logger.error(f"Error building FAISS index: {str(e)}")
            raise

    @staticmethod
    def add_vectors(vectors: np.ndarray, candidate_ids: List[str] = None) -> None:
        """Add vectors to FAISS index."""
        if FAISSService._index is None:
            raise ValueError("Index not initialized. Call build_index() first")

        try:
            vectors = np.array(vectors, dtype=np.float32)
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            vectors = vectors / norms

            logger.info(f"Adding {len(vectors)} vectors to FAISS index...")
            FAISSService._index.add(vectors)

            if candidate_ids:
                for idx, cand_id in enumerate(candidate_ids):
                    faiss_idx = FAISSService._index.ntotal - len(vectors) + idx
                    FAISSService._id_mapping[faiss_idx] = cand_id

            logger.info(f"FAISS index now contains {FAISSService._index.ntotal} vectors")

        except Exception as e:
            logger.error(f"Error adding vectors to FAISS: {str(e)}")
            raise

    @staticmethod
    def search_top_k(query_vector: np.ndarray, k: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Search for top-k similar vectors."""
        if FAISSService._index is None:
            raise ValueError("Index not initialized. Call build_index() first")

        if FAISSService._index.ntotal == 0:
            logger.warning("FAISS index is empty")
            return np.array([[]]), np.array([[]])

        try:
            query_vector = np.array([query_vector], dtype=np.float32)
            if query_vector.shape[1] != FAISSService._index.d:
                raise ValueError(
                    f"Query dimension {query_vector.shape[1]} does not match "
                    f"FAISS index dimension {FAISSService._index.d}"
                )

            query_norm = np.linalg.norm(query_vector, axis=1, keepdims=True)
            query_norm[query_norm == 0] = 1.0
            query_vector = query_vector / query_norm

            k = min(k, FAISSService._index.ntotal)

            logger.info(f"Searching FAISS index for top {k} candidates...")
            distances, indices = FAISSService._index.search(query_vector, k)

            logger.info(f"Found top {k} candidates")
            return distances, indices

        except Exception as e:
            logger.error(f"Error searching FAISS: {str(e)}")
            raise

    @staticmethod
    def save_index(path: str = FAISS_INDEX_PATH) -> None:
        """Save FAISS index to disk."""
        if FAISSService._index is None:
            logger.warning("No index to save")
            return

        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving FAISS index to {path}...")
            faiss.write_index(FAISSService._index, path)

            id_mapping_path = FAISS_ID_MAPPING_PATH
            Path(id_mapping_path).parent.mkdir(parents=True, exist_ok=True)
            with open(id_mapping_path, 'wb') as f:
                pickle.dump(FAISSService._id_mapping, f)

            logger.info(f"FAISS index saved successfully")

        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")
            raise

    @staticmethod
    def load_index(path: str = FAISS_INDEX_PATH) -> Optional[faiss.IndexFlatIP]:
        """Load FAISS index from disk."""
        try:
            if not Path(path).exists():
                logger.warning(f"Index file not found at {path}")
                return None

            logger.info(f"Loading FAISS index from {path}...")
            FAISSService._index = faiss.read_index(path)

            id_mapping_path = FAISS_ID_MAPPING_PATH
            if Path(id_mapping_path).exists():
                with open(id_mapping_path, 'rb') as f:
                    FAISSService._id_mapping = pickle.load(f)

            logger.info(f"FAISS index loaded. Total vectors: {FAISSService._index.ntotal}")
            return FAISSService._index

        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            raise

    @staticmethod
    def get_index_stats() -> dict:
        """Get FAISS index statistics."""
        if FAISSService._index is None:
            return {"status": "uninitialized"}

        return {
            "total_vectors": FAISSService._index.ntotal,
            "dimension": FAISSService._index.d,
            "id_mapping_count": len(FAISSService._id_mapping)
        }


def build_index(dim: int = MODEL_DIMENSION) -> faiss.IndexFlatIP:
    """Build FAISS index."""
    return FAISSService.build_index(dim)


def add_vectors(vectors: np.ndarray, candidate_ids: List[str] = None) -> None:
    """Add vectors to index."""
    return FAISSService.add_vectors(vectors, candidate_ids)


def search_top_k(query_vector: np.ndarray, k: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """Search for top-k vectors."""
    return FAISSService.search_top_k(query_vector, k)


def load_index(path: str = FAISS_INDEX_PATH) -> Optional[faiss.IndexFlatIP]:
    """Load FAISS index from disk."""
    return FAISSService.load_index(path)


def get_index_stats() -> dict:
    """Get loaded FAISS index statistics."""
    return FAISSService.get_index_stats()
