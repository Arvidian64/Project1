import json
import requests
import time
import datetime
import random

def co2_sensor(sensor_id, value, timestamp):
    co2 = {
        "sensor_id": sensor_id,
        "type": "CO2",
        "unit": "ppm",
        "value": value,
        "timestamp": timestamp
    }

    return co2

url = "http://127.0.0.1:8080/measurments"

while True: 
    try:
        sensor_id = 11
        value = random.randint(300, 400)
        timestamp = datetime.utcnow().strftime("%-%-% | %-%")
        data = co2_sensor(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 