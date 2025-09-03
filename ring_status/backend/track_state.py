import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
from datetime import datetime
import constants

def get_last_snapshot_time():
    data = requests.get(constants.API_PANOMAX_URL).json()
    return datetime.strptime(data["images"][-1]["time"], "%H:%M:%S")

def format_snapshot_url(year, month, day, hour, minute, second):
        return constants.IMG_BASE_URL.format(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second
        )

def get_snapshot(url):
    resp = requests.get(url)
    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

def show_snapshot(url):
    resp = requests.get(url)
    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if frame is None:
        print("No se pudo descargar o decodificar la imagen.")
    else:
        cv2.imshow("Webcam Nordschleife",
         frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def show_frame(frame):
    if frame is None:
        print("No se pudo decodificar la imagen.")
    else:
        cv2.imshow("Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def is_weekend(datetime):
    return datetime.weekday() >= 5

def get_track_state(roi):
    # Converting frame to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Color masks
    mask_green = cv2.inRange(hsv, constants.LOWER_GREEN_MASK_RANGE, constants.UPPER_GREEN_MASK_RANGE)
    mask_yellow = cv2.inRange(hsv, constants.LOWER_YELLOW_MASK_RANGE, constants.UPPER_YELLOW_MASK_RANGE)
    mask_red1 = cv2.inRange(hsv, constants.LOWER_RED1_MASK_RANGE, constants.UPPER_RED1_MASK_RANGE)
    mask_red2 = cv2.inRange(hsv, constants.LOWER_RED2_MASK_RANGE, constants.UPPER_RED2_MASK_RANGE)
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
    last_time = get_last_snapshot_time()
    snapshot_url = format_snapshot_url(
        constants.IMG_BASE_URL,
        now.year,
        now.month,
        now.day, 
        last_time.hour, 
        last_time.minute, 
        last_time.second
        )

    frame = get_snapshot(snapshot_url) 
    return frame[constants.ROI_COORDS]

def check_track():
    if is_weekend(now):
        if now.hour >= constants.WEEKEND_OPEN_HOUR or now.hour < constants.WEEKEND_CLOSE_HOUR:
            roi = get_roi()
            print("Track state:", get_track_state(roi))
        else:
            print("Track closed")
    else:
        if (now.hour, now.minute) >= constants.WEEKDAY_OPEN_HOUR and (now.hour, now.minute) < constants.WEEKDAY_CLOSE_HOUR:
            roi = get_roi()
            print("Track state:", get_track_state(roi))
        else:
            print("Track closed")

if __name__ == "__main__":
    now = datetime.now()
    check_track()