import requests
from mapper import run_mapper
from reducer import run_reducer

url = "http://flask-server:8080/measurements"
x_lat = 60.0971
y_lon = 19.9348
max_dist = 400

def main(local=False):

    if local:
        try:
            with open("test.csv", "r") as f:
                data = f.readlines()
        except FileNotFoundError:
            print("Error: does test.csv exist in this folder?")
            return
    else:
        try:
            req = requests.get(url)
            data = req.text.splitlines()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

    # Filters by distance
    mapped_pairs = run_mapper(data, x_lat, y_lon, max_dist)

    # Sorts by sensor name (should be first element of the tuple)
    mapped_pairs.sort(key=lambda x: x[0])

    final_stats = run_reducer(mapped_pairs)

    for sensor, min_val, max_val, avg_val in final_stats:
        print(f"{sensor}\tmin={min_val}, max={max_val}, avg={avg_val:.2f}")

if __name__ == "__main__":
    main()

