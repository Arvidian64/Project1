import requests
import datetime
import time
import random

date_and_time = datetime.datetime

def sensor(sensor_id, value, timestamp):
    co2 = {
        "sensor_id": sensor_id,
        "type": "CO2 Sensor",
        "unit": "ppm",
        "value": value,
        "timestamp": timestamp
    }

    return co2

url = "http://flask-server:5000/measurements"

while True: 
    try:
        sensor_id = 11
        value = random.randint(300, 400)
        timestamp = date_and_time.now().strftime("%Y-%m-%d | %H:%M:%S")
        data = sensor(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(5)

    except Exception as e:
        print("STOPPED", e)