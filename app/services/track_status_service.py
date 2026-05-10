"""Core logic for track status analysis."""

import requests
import cv2
import numpy as np
from datetime import datetime
import app.config.settings as settings
import app.utils.formatters as formatters
import app.utils.date_helpers as date_helpers
from app.middleware.logger import get_logger
from app.schemas.schemas import TrackStatusResponse

logger = get_logger(__name__)

class TrackStatusService:
    """Service for checking track status."""

    def __init__(self, api_client=None):
        self.api_client = api_client

    def check_track_status(self) -> TrackStatusResponse:
        """Check track status according to operating hours and return response."""
        try:
            now = datetime.now()

            # Check if track is open based on hours
            if not self._is_track_open(now):
                return TrackStatusResponse(
                    response="ok",
                    status="Closed",
                    img_url=""
                )

            # Get and process snapshot
            snapshot_date, last_snapshot_time = self.get_last_snapshot_metadata()
            snapshot_url = formatters.format_snapshot_url(
                snapshot_date.year,
                snapshot_date.month,
                snapshot_date.day,
                last_snapshot_time.hour,
                last_snapshot_time.minute,
                last_snapshot_time.second
            )
            frame = self.get_snapshot(snapshot_url)
            roi = self._get_roi(frame)
            track_state = self._process_image(roi)

            # Map internal state to schema status
            status_map = {
                "open": "Open",
                "warning": "Unknown",  # Assuming warning maps to Unknown
                "closed": "Closed",
                "unknown": "Unknown"
            }
            status = status_map.get(track_state, "Unknown")

            return TrackStatusResponse(
                response="ok",
                status=status,
                img_url=snapshot_url
            )

        except Exception as e:
            logger.error(f"Error checking track status: {e}")
            return TrackStatusResponse(
                response="error",
                status="Unknown",
                img_url=""
            )

    def _is_track_open(self, now: datetime) -> bool:
        """Check if track is open at the given time."""
        if date_helpers.is_weekend(now):
            open_time = settings.WEEKEND_OPEN_HOUR
            close_time = settings.WEEKEND_CLOSE_HOUR
        else:
            open_time = settings.WEEKDAY_OPEN_HOUR
            close_time = settings.WEEKDAY_CLOSE_HOUR

        current_time = (now.hour, now.minute)
        return open_time <= current_time < close_time


    def get_last_snapshot_metadata(self) -> tuple[datetime, datetime]:
        """Get the time of the last available snapshot."""
        try:
            data = requests.get(settings.API_PANOMAX_URL, timeout=10)
            data.raise_for_status()
            json_data = data.json()
            snapshot_date = datetime.strptime(json_data["date"], "%Y-%m-%d")
            last_snapshot_time = datetime.strptime(json_data["images"][-1]["time"], "%H:%M:%S")
            return snapshot_date, last_snapshot_time
        except Exception as e:
            logger.error(f"Failed to get snapshot metadata: {e}")
            raise


    def get_snapshot(self, url: str) -> np.ndarray:
        """Download and decode an image from a URL."""
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is None:
                raise ValueError("Failed to decode image")
            return frame
        except Exception as e:
            logger.error(f"Failed to get snapshot from {url}: {e}")
            raise


    # TODO - Add more endpoints, e.g. Update config (update roi, color thresholds, etc.), get ROI image, etc...

    

    def get_snapshot(self, url):
        """Download the snapshot image as jpg."""
        resp = requests.get(url)
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if frame is None:
            print("Could not download or decode the image.")   
        else:
            return frame


    def _process_image(self, roi: np.ndarray) -> str:
        """Process the region of interest to determine track state."""
        # Convert frame to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Color masks
        mask_green = cv2.inRange(
            hsv,
            settings.LOWER_GREEN_MASK_RANGE,
            settings.UPPER_GREEN_MASK_RANGE
        )
        mask_yellow = cv2.inRange(
            hsv,
            settings.LOWER_YELLOW_MASK_RANGE,
            settings.UPPER_YELLOW_MASK_RANGE
        )
        mask_red1 = cv2.inRange(
            hsv,
            settings.LOWER_RED1_MASK_RANGE,
            settings.UPPER_RED1_MASK_RANGE
        )
        mask_red2 = cv2.inRange(
            hsv,
            settings.LOWER_RED2_MASK_RANGE,
            settings.UPPER_RED2_MASK_RANGE
        )
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        if cv2.countNonZero(mask_green) > settings.COLOR_THRESHOLD:
            state = "open"
        elif cv2.countNonZero(mask_yellow) > settings.COLOR_THRESHOLD:
            state = "warning"
        elif cv2.countNonZero(mask_red) > settings.COLOR_THRESHOLD:
            state = "closed"
        else:
            state = "unknown"

        return state


    def _get_roi(self, frame: np.ndarray) -> np.ndarray:
        """Get the region of interest (ROI) from the current snapshot."""
        return frame[
            settings.ROI_COORDS[0]:settings.ROI_COORDS[1],
            settings.ROI_COORDS[2]:settings.ROI_COORDS[3]
        ]


# Global instance of the track status service
track_status_service = TrackStatusService()