import json 
import time 
import requests 
import datetime 
import time 
import random 

def temp(sensor_id, value, timestamp):

    request = request.get.json()

    temp = {
        "sensor_id": sensor_id,
        "type": "temperature",
        "unit": "C",
        "value": value,
        "timestamp": timestamp 
    }

    return temp

url = "http://127.0.0.1:8080/measurments"

while True: 
    try:
        sensor_id = 14
        value = random.randint(-20, 50)
        timestamp = datetime.utcnow().strftime("%-%-% | %-%")
        data = temp(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 
