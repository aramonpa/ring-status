"""Application entry point."""

from fastapi import APIRouter, HTTPException
from app.middleware.logger import get_logger
from services.track_status import track_status
from app.utils.formatters import format_snapshot_url
from app.schemas.schemas import TrackStatusResponse

logger = get_logger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/track-status", response_model=TrackStatusResponse)
async def track_status() -> TrackStatusResponse:
    try:
        status = track_status.get_track_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")









