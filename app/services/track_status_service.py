"""Core logic for track status analysis."""

import requests
import cv2
import numpy as np
from datetime import datetime
import app.config.settings as settings
import app.utils.formatters as formatters
import app.utils.date_helpers as date_helpers
from app.middleware.logger import get_logger

logger = get_logger(__name__)

class TrackStatusService:
    """Service for checking track status."""

    def __init__(self, api_client):
        self.api_client = api_client

    def get_track_state(self):
        """Get the current track state."""
        return self.api_client.get_last_snapshot_metadata()

    def check_track(self):
        return

    def get_last_snapshot_metadata():
        """Get the time of the last available snapshot."""
        data = requests.get(settings.API_PANOMAX_URL).json()
        return datetime.strptime(data["date"], "%Y-%m-%d"), datetime.strptime(data["images"][-1]["time"], "%H:%M:%S")


    def get_snapshot(url):
        """Download and decode an image from a URL."""
        resp = requests.get(url)
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)


    def show_snapshot(url):
        """Download and display a snapshot in a window."""
        resp = requests.get(url)
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if frame is None:
            print("Could not download or decode the image.")
        else:
            cv2.imshow("Webcam Nordschleife", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def show_frame(frame):
        """Display a frame in a window."""
        if frame is None:
            print("Could not decode the image.")
        else:
            cv2.imshow("Frame", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def get_track_state(roi):
        """Detect track state by analyzing traffic light colors."""
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
            state = "Green"
        elif cv2.countNonZero(mask_yellow) > settings.COLOR_THRESHOLD:
            state = "Yellow"
        elif cv2.countNonZero(mask_red) > settings.COLOR_THRESHOLD:
            state = "Closed"
        else:
            state = "Unknown"

        return state


    def get_roi():
        """Get the region of interest (ROI) from the current snapshot."""
        snapshot_date, last_snapshot_time = get_last_snapshot_metadata()
        snapshot_url = formatters.format_snapshot_url(
            snapshot_date.year,
            snapshot_date.month,
            snapshot_date.day,
            last_snapshot_time.hour,
            last_snapshot_time.minute,
            last_snapshot_time.second
        )
        frame = get_snapshot(snapshot_url)
        return frame[
            settings.ROI_COORDS[0]:settings.ROI_COORDS[1],
            settings.ROI_COORDS[2]:settings.ROI_COORDS[3]
        ]


    def check_track():
        """Check track status according to operating hours."""
        now = datetime.now()

        if date_helpers.is_weekend(now):
            if (now.hour >= settings.WEEKEND_OPEN_HOUR[0] and
                    now.hour < settings.WEEKEND_CLOSE_HOUR[0]):
                roi = get_roi()
                print("Track state:", get_track_state(roi))
            else:
                print("Track closed")
        else:
            if ((now.hour, now.minute) >= settings.WEEKDAY_OPEN_HOUR and
                    (now.hour, now.minute) < settings.WEEKDAY_CLOSE_HOUR):
                roi = get_roi()
                print("Track state:", get_track_state(roi))
            else:
                print("Track closed")

# Global instance of the track status service
track_status_service = TrackStatusService()