import sys
import math 

current_sensor = None 
count = 0
total = 0
min_val = None 
max_val = None 

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue 

    sensor, value = line.split("\t")
    value = float(value)

    if current_sensor == sensor:
        count += 1
        total += value 
        min_val = value if min_val is None else min(min_val, value)
        max_val = value if max_val is None else max(max_val, value)

    else:
        if current_sensor is not None:
            avg = total / count
            print(f"{current_sensor}\tmin={min_val}, max={max_val}, avg={avg}")

        current_sensor = sensor 
        count = 1 
        total = value 
        min_val = value 
        max_val = value 

if current_sensor is not None:
    avg = total / count 
    print(f"{current_sensor}\tmin={min_val}, max={max_val}, avg={avg}")

    
