"""Lógica principal para análisis de estado de la pista."""

import requests
import cv2
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

from app import config as constants


def get_last_snapshot_time():
    """Obtiene el tiempo de la última snapshot disponible."""
    data = requests.get(constants.API_PANOMAX_URL).json()
    return datetime.strptime(data["images"][-1]["time"], "%H:%M:%S")


def format_snapshot_url(year, month, day, hour, minute, second):
    """Formatea la URL de la snapshot con los parámetros dados."""
    return constants.IMG_BASE_URL.format(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second
    )


def get_snapshot(url):
    """Descarga y decodifica una imagen desde una URL."""
    resp = requests.get(url)
    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def show_snapshot(url):
    """Descarga y muestra una snapshot en ventana."""
    resp = requests.get(url)
    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if frame is None:
        print("No se pudo descargar o decodificar la imagen.")
    else:
        cv2.imshow("Webcam Nordschleife", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def show_frame(frame):
    """Muestra un frame en ventana."""
    if frame is None:
        print("No se pudo decodificar la imagen.")
    else:
        cv2.imshow("Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def is_weekend(dt):
    """Verifica si una fecha corresponde a fin de semana."""
    return dt.weekday() >= 5


def get_track_state(roi):
    """Detecta el estado de la pista analizando los colores del semáforo."""
    # Convertir frame a HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Máscaras de color
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
    """Obtiene la región de interés (ROI) de la snapshot actual."""
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
    """Verifica el estado de la pista según horarios y obtiene su estado."""
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
