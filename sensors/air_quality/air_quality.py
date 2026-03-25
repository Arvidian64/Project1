import requests
import datetime
import time 
import random

date_and_time = datetime.datetime

def sensor(sensor_id, value, timestamp):

    air = {
        "sensor_id": sensor_id,
        "type": "Air Quality",
        "unit": "PM10",
        "value": value,
        "timestamp": timestamp
    }

    return air

url = "http://flask-server:5000/measurements"

while True: 
    try:
        sensor_id = 13
        value = random.randint(0, 500)
        timestamp = date_and_time.now().strftime("%Y-%m-%d | %H:%M:%S")
        data = sensor(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(5)

    except Exception as e:

        print("STOPPED", e)