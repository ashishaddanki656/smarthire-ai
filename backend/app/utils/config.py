"""
Configuration module for SmartHire AI.
Loads environment variables and sets up configuration constants.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ==================== EMBEDDING MODEL ====================
MODEL_NAME = os.getenv("MODEL_NAME", "BAAI/bge-large-en-v1.5")
MODEL_DIMENSION = 1024  # BGE Large embedding dimension

# ==================== FAISS CONFIGURATION ====================
TOP_K = int(os.getenv("TOP_K", 100))  # Retrieve top 100 candidates
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "data/faiss_index.bin")
FAISS_ID_MAPPING_PATH = os.getenv("FAISS_ID_MAPPING_PATH", "data/faiss_id_mapping.pkl")

# ==================== DATABASE CONFIGURATION ====================
CANDIDATES_FILE = os.getenv("CANDIDATES_FILE", "data/candidates.csv")
OUTPUT_RANKING_FILE = os.getenv("OUTPUT_RANKING_FILE", "docs/output/ranked_output.csv")

# ==================== RANKING WEIGHTS ====================
ALPHA = float(os.getenv("ALPHA", 0.4))  # Semantic score weight
BETA = float(os.getenv("BETA", 0.3))   # Skill match weight
GAMMA = float(os.getenv("GAMMA", 0.2))  # Career score weight
DELTA = float(os.getenv("DELTA", 0.1))  # Clean activity weight

# ==================== API CONFIGURATION ====================
API_TITLE = "SmartHire AI"
API_DESCRIPTION = "Bias-Free AI Recruitment Engine - Merit First, Intelligence Always."
API_VERSION = "1.0.0"

# ==================== LOGGING CONFIGURATION ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== DEVICE CONFIGURATION ====================
DEVICE = os.getenv("DEVICE", "cpu")  # cpu or cuda

# ==================== VALIDATION ====================
# Ensure weights sum to 1.0 for proper normalization
TOTAL_WEIGHT = ALPHA + BETA + GAMMA + DELTA
if abs(TOTAL_WEIGHT - 1.0) > 0.01:
    print(f"Warning: Ranking weights sum to {TOTAL_WEIGHT}, not 1.0")