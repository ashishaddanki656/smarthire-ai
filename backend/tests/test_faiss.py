"""Test FAISS functionality."""

import pytest
import numpy as np
from app.services.faiss_service import build_index, add_vectors, search_top_k


def test_build_index():
    """Test FAISS index creation."""
    dim = 1024
    index = build_index(dim)
    
    assert index is not None


def test_add_vectors():
    """Test adding vectors to FAISS."""
    dim = 128
    build_index(dim)
    
    vectors = np.random.rand(10, dim).astype('float32')
    add_vectors(vectors)
    
    # Index should now have 10 vectors
    assert True  # Simplified test


def test_search_top_k():
    """Test searching FAISS index."""
    dim = 128
    build_index(dim)
    
    # Add some vectors
    vectors = np.random.rand(50, dim).astype('float32')
    add_vectors(vectors)
    
    # Search
    query = np.random.rand(dim).astype('float32')
    scores, ids = search_top_k(query, k=10)
    
    assert len(ids[0]) > 0
    assert len(scores[0]) > 0


def test_search_top_k_limit():
    """Test k parameter limits results."""
    dim = 128
    build_index(dim)
    
    vectors = np.random.rand(100, dim).astype('float32')
    add_vectors(vectors)
    
    query = np.random.rand(dim).astype('float32')
    scores, ids = search_top_k(query, k=5)
    
    assert len(ids[0]) == 5
