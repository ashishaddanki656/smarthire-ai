
"""
SmartHire AI - Main FastAPI Application
Bias-aware AI recruitment system for intelligent candidate ranking.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.jd import router as jd_router
from app.api.routes.candidate import router as candidate_router
from app.api.routes.rank import router as rank_router
from app.utils.logger import get_logger
from app.utils.config import API_TITLE, API_DESCRIPTION, API_VERSION

logger = get_logger("Main")

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(jd_router)
app.include_router(candidate_router)
app.include_router(rank_router)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint providing API information.
    
    Returns:
        dict: API information and available endpoints
    """
    logger.info("Root endpoint accessed")
    return {
        "service": "SmartHire AI",
        "message": "Bias-aware AI Recruitment Engine - Merit First, Intelligence Always.",
        "version": API_VERSION,
        "status": "operational",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "parse_jd": "/parse-jd",
            "candidates": "/candidates",
            "rank": "/rank"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("=" * 60)
    logger.info(f"Starting {API_TITLE}")
    logger.info("=" * 60)
    logger.info("SmartHire AI Backend initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("=" * 60)
    logger.info("Shutting down SmartHire AI Backend")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn

    logger.info("Running SmartHire AI with Uvicorn")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
