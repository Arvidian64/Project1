import json
import random
import request 
import time 
import datetime 

def pressure_sensor(sensor_id, value, timestamp):
    
    request = request.get.json()

    pressure = {
        "sensor_id": sensor_id,
        "type": "pressure",
        "unit": "hPa",
        "value": value,
        "timestamp": timestamp
    }

    return pressure

url = "http://127.0.0.1:8080/measurments"

while True: 
    try:
        sensor_id = 12
        value = random.randint(120, 180)
        timestamp = datetime.utcnow().strftime("%-%-% | %-%")
        data = pressure_sensor(sensor_id, value, timestamp)
        response = requests.post(url, json=data)
        time.sleep(2)

    except Exception as e:

        print("STOPPED")
        break 