import json
import time
import requests
import datetime
import time
import random

date_and_time = datetime.datetime

def co2_sensor(sensor_id, value, timestamp):
    co2 = {
        "sensor_id": sensor_id,
        "type": "CO2",
        "unit": "ppm",
        "value": value,
        "timestamp": timestamp
    }

    return co2

url = "http://flask-server:8080/measurements"

while True: 
    try:
        sensor_id = 11
        value = random.randint(300, 400)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d | %H:%M")
        data = co2_sensor(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 