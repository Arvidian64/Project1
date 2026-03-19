import json
import time 
import requests 
import datetime
import time 
import random 

def air_quality(sensor_id, value, timestamp):
    
    request = request.get.json()

    air = {
        "sensor_id": sensor_id,
        "type": "air quality",
        "unit": "PM10",
        "value": value,
        "timestamp": timestamp
    }

    return air

url = "http://127.0.0.1:8080/measurments"

while True: 
    try:
        sensor_id = 13
        value = random.randint(0, 500)
        timestamp = datetime.utcnow().strftime("%-%-% | %-%")
        data = air_quality(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 