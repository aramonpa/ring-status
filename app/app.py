"""Core logic for track status analysis."""

import requests
import cv2
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

from app import config as constants


def get_last_snapshot_time():
    """Get the time of the last available snapshot."""
    data = requests.get(constants.API_PANOMAX_URL).json()
    return datetime.strptime(data["images"][-1]["time"], "%H:%M:%S")


def format_snapshot_url(year, month, day, hour, minute, second):
    """Format the snapshot URL with the given parameters."""
    return constants.IMG_BASE_URL.format(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second
    )


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


def is_weekend(dt):
    """Check if a date is a weekend."""
    return dt.weekday() >= 5


def get_track_state(roi):
    """Detect track state by analyzing traffic light colors."""
    # Convert frame to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Color masks
    mask_green = cv2.inRange(
        hsv,
        constants.LOWER_GREEN_MASK_RANGE,
        constants.UPPER_GREEN_MASK_RANGE
    )
    mask_yellow = cv2.inRange(
        hsv,
        constants.LOWER_YELLOW_MASK_RANGE,
        constants.UPPER_YELLOW_MASK_RANGE
    )
    mask_red1 = cv2.inRange(
        hsv,
        constants.LOWER_RED1_MASK_RANGE,
        constants.UPPER_RED1_MASK_RANGE
    )
    mask_red2 = cv2.inRange(
        hsv,
        constants.LOWER_RED2_MASK_RANGE,
        constants.UPPER_RED2_MASK_RANGE
    )
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    if cv2.countNonZero(mask_green) > constants.COLOR_THRESHOLD:
        state = "Green"
    elif cv2.countNonZero(mask_yellow) > constants.COLOR_THRESHOLD:
        state = "Yellow"
    elif cv2.countNonZero(mask_red) > constants.COLOR_THRESHOLD:
        state = "Closed"
    else:
        state = "Unknown"

    return state


def get_roi():
    """Get the region of interest (ROI) from the current snapshot."""
    last_time = get_last_snapshot_time()
    now = datetime.now()
    snapshot_url = format_snapshot_url(
        now.year,
        now.month,
        now.day,
        last_time.hour,
        last_time.minute,
        last_time.second
    )

    frame = get_snapshot(snapshot_url)
    return frame[
        constants.ROI_COORDS[0]:constants.ROI_COORDS[1],
        constants.ROI_COORDS[2]:constants.ROI_COORDS[3]
    ]


def check_track():
    """Check track status according to operating hours."""
    now = datetime.now()

    if is_weekend(now):
        if (now.hour >= constants.WEEKEND_OPEN_HOUR[0] or
                now.hour < constants.WEEKEND_CLOSE_HOUR[0]):
            roi = get_roi()
            print("Track state:", get_track_state(roi))
        else:
            print("Track closed")
    else:
        if ((now.hour, now.minute) >= constants.WEEKDAY_OPEN_HOUR and
                (now.hour, now.minute) < constants.WEEKDAY_CLOSE_HOUR):
            roi = get_roi()
            print("Track state:", get_track_state(roi))
        else:
            print("Track closed")
