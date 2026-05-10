"""Application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from app.api.app import router
from app.schemas.schemas import TrackStatus
from app.middleware.logger import get_logger, setup_logging
from app.config.settings import settings

#Setup logging
setup_logging()
logger = get_logger(__name__)


app = FastAPI(
    title="Ring Status API",
    description="API for checking the status of the Nordschleife track.",
    version="0.1.0"
)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(
    router=router,
    prefix="/api/v1",
    tags=["API"]
)

@app.lifespan("startup")
async def startup_event():
    """Startup event to validate configuration"""
    logger.info("Application startup initiated")
    logger.info(f"API Host: {settings.API_HOST}, Port: {settings.API_PORT}")

    logger.info("Configuration validation successful")
    logger.info("Application startup complete")


@app.lifespan("shutdown")
async def shutdown_event():
    """Shutdown event to close async resources."""
    logger.info("Application shutdown initiated")

    try:
        close_config_store()
    except Exception as e:
        logger.warning(f"Failed to close config store: {e}")

    logger.info("Application shutdown complete")


@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to the Ring Status API! Check /api/v1/track-status for the current track status.",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True
    )