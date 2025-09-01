import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
from datetime import datetime

base_url = "https://panodata8.panomax.com/cams/2527/{year}/{month}/{day}/{hour}-{minute}-{second}_hd_3_0.jpg"
api_images_url = "https://api.panomax.com/1.0/cams/2527/images/day"
now = datetime.now()

def get_last_snapshot_time():
    data = requests.get(api_images_url).json()
    return datetime.strptime(data["images"][-1]["time"], "%H:%M:%S")

def format_snapshot_url(url, year, month, day, hour, minute, second):
        formatted_url = url.format(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second
        )
        return formatted_url
        
def show_snapshot(url):
    resp = requests.get(url)
    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if frame is None:
        print("No se pudo descargar o decodificar la imagen.")
    else:
        cv2.imshow("Webcam Nordschleife", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def get_snapshot(url):
    resp = requests.get(url)
    arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

time = get_last_snapshot_time()
snapshot_url = format_snapshot_url(
     base_url,
     now.year,
     f"{now.month:02d}",
     f"{now.day:02d}", 
     f"{time.hour:02d}", 
     f"{time.minute:02d}", 
     f"{time.second:02d}")

frame = get_snapshot(snapshot_url)

# Recortamos la ROI (ejemplo: pixel 100:200, 300:400)
roi = frame[100:200, 300:400]

# Convertir a espacio HSV (mejor para colores)
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Calcular media de color
mean_color = cv2.mean(hsv)

h, s, v = mean_color[0], mean_color[1], mean_color[2]

estado = "Desconocido"
if 35 < h < 85:   # rango verde en HSV
    estado = "Abierto"
elif 20 < h < 35: # rango amarillo
    estado = "Amarillo"
elif h < 10 or h > 170: # rango rojo
    estado = "Cerrado"

print("Estado de la pista:", estado)
