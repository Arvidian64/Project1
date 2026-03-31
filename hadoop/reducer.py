#!/usr/bin/env python3

import sys

def run_reducer():
    #Reads from stdin and looks for changes in the key sensor_id
    current_sensor = None
    sensor = None
    count = 0
    total = 0
    min_val = None
    max_val = None

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            sensor, value_str = line.split("\t",1)
            value = float(value_str)
        except ValueError:
            continue

    if current_sensor == sensor:
        count += 1
        total += value
        min_val = min(min_val, value)
        max_val = max(max_val, value)
    else:
        if current_sensor is not None:
            if count > 0:
                avg_val = total / count
                print(f"{current_sensor}\t{min_val}\t{max_val}\t{avg_val:.2f}")

        current_sensor = sensor
        count = 1
        total = value
        min_val = value
        max_val = value

    if current_sensor is not None:
        if count > 0:
            avg_val = total / count
            print(f"{current_sensor}\t{min_val}\t{max_val:.2f}")


if __name__ == "__main__":
    run_reducer()
