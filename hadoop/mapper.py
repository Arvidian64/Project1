#!/usr/bin/env python3

import sys
import math

x_lat = 60.0971
y_lon = 19.9348
max_dist = 12800  # km

def haversine_dist(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    tmp_lat = math.sin(lat2_rad * 0.5 - lat1_rad * 0.5) ** 2
    tmp_lon = math.sin(lon2_rad * 0.5 - lon1_rad * 0.5) ** 2
    a = math.cos(lat1_rad) * math.cos(lat2_rad) * tmp_lon + tmp_lat
    return 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def run_mapper():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

            # Parsing logic

        parts = line.split(",")

        if len(parts) < 7:
            continue
        
        try:
            sensor = parts[1].strip().replace('"', '')
            lat = float(parts[3]).replace('"', '')
            lon = float(parts[4]).replace('"', '')
            val = float(parts[6]).replace('"', '')

            dist = haversine_dist(x_lat, y_lon, lat, lon)

            if dist <= max_dist:
                print(f"{sensor}\t{val}")

        except (IndexError, ValueError):
            continue


if __name__ == "__main__":
    run_mapper()
