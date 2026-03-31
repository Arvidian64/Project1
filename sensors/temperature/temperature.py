import requests
import datetime
import time 
import random

date_and_time = datetime.datetime

def temp(sensor_id, value, timestamp):

    temp = {
        "sensor_id": sensor_id,
        "type": "Temperature Sensor",
        "unit": "°C",
        "value": value,
        "timestamp": timestamp 
    }

    return temp

url = "http://flask-server:5000/measurements"

while True: 
    try:
        sensor_id = 14
        value = random.randint(-20, 50)
        timestamp = date_and_time.now().strftime("%Y-%m-%d | %H:%M:%S")
        data = temp(sensor_id, value, timestamp)
        response = requests.post(url, json=data)

    except Exception as e:

        print("STOPPED", e)
    time.sleep(5)
