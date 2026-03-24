import requests
import datetime
import time 
import random

date_and_time = datetime.datetime

def temp(sensor_id, value, timestamp):

    temp = {
        "sensor_id": sensor_id,
        "type": "temperature",
        "unit": "C",
        "value": value,
        "timestamp": timestamp 
    }

    return temp

url = "http://flask-server:8080/measurements"

while True: 
    try:
        sensor_id = 14
        value = random.randint(-20, 50)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d | %H:%M")
        data = temp(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 
