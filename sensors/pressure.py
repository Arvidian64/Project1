import json
import time
import requests
import datetime
import time
import random

date_and_time = datetime.datetime

def pressure_sensor(sensor_id, value, timestamp):

    pressure = {
        "sensor_id": sensor_id,
        "type": "pressure",
        "unit": "hPa",
        "value": value,
        "timestamp": timestamp
    }

    return pressure

url = "http://127.0.0.1:8080/measurements"

while True: 
    try:
        sensor_id = 12
        value = random.randint(120, 180)
        timestamp = date_and_time.now(datetime.datetime.utc).strftime("Y%-m%-d% | %M-%S")
        data = pressure_sensor(sensor_id, value, timestamp)
        response = requests.post(url, json=data, timeout=5)
        print(response.json())
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 