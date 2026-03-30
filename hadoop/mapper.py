#!/usr/bin/env python3

import sys
import math

x_lat = 60.0971
y_lon = 19.9348
max_dist = 4000  # km

def haversine_dist(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    tmp_lat = math.sin(lat2_rad * 0.5 - lat1_rad * 0.5) ** 2
    tmp_lon = math.sin(lon2_rad * 0.5 - lon1_rad * 0.5) ** 2
    a = math.cos(lat1_rad) * math.cos(lat2_rad) * tmp_lon + tmp_lat
    return 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def run_mapper():
    mapped_result = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

            # Parsing logic from original mapper
        try:
            parts = line.split(",")
            sensor = parts[1]
            lat = float(parts[3])
            lon = float(parts[4])
            val = float(parts[6])

            dist = haversine_dist(x_lat, y_lon, lat, lon)

            if dist <= max_dist:
                print(f"{sensor}\t{val}")

        except (IndexError, ValueError):
            continue

    return mapped_result

