#MAPPER OCH REDUCER, GÖR EN MAIN.py SOM REQUESTAR 
# OCH TAR EMOT DATA FRÅN SERVERN OCH RÄKNAR UT VÄRDEN 
# OCH SKRIVER UT DET I KONSOLEN 
from mapper import mapper
from reducer import reducer 
import requests

url = "http://server"

x_lat = 60.0971
y_lon = 19.9348
max_dist = 400

def main():
    req = requests.get(url)
    data = req.text.splitlines()

    map = mapper(data, x_lat, y_lon, max_dist)
    red = reducer(map)

    for sensor, min_value, max_value, avg_value in red:
        print(f"{sensor}\tmin={min_value}, max={max_value} avg={avg_value}")


if __name__=="__main__":
    main()


