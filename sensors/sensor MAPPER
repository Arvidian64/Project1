import sys 
import math 

#MAPPER 
x_lat = float(sys.argv[1])
y_lon = float(sys.argv[2])
max_dist = float(sys.argv[3])

def haversine_dist(lat1, lon1, lat2, lon2): 
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    tmp_lat = math.sin(lat2_rad * 0.5 - lat1_rad * 0.5)**2
    tmp_lon = math.sin(lon2_rad * 0.5 - lon1_rad * 0.5)**2
    a = math.cos(lat1_rad) * math.cos(lat2_rad) * tmp_lon + tmp_lat
    return 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue 

    data = line.split(",")

    sensor = data[1]
    lat = float(data[3])
    lon = float(data[4])
    val = float(data[6])

    dist = haversine_dist(x_lat, y_lon, lat, lon)
    if dist <= max_dist:
        print(f"{sensor}\t{val}")
