import requests
import time
from mapper import run_mapper
from reducer import run_reducer

url = "http://flask-server:5000/hadoop"
x_lat = 60.0971
y_lon = 19.9348
max_dist = 4000

def map_reduce(local=False):
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

            print(f"DEBUG: Status Code: {req.status_code}")
            print(f"DEBUG: Data length: {len(req.text)} characters")

            if req.status_code != 200:
                print(f"Error: Server returned {req.status_code}: {req.text}")
                return

            data = req.text.splitlines()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

    # Filters by distance
    mapped_pairs = run_mapper(data, x_lat, y_lon, max_dist)

    print(mapped_pairs)

    # Sorts by sensor name (should be first element of the tuple)
    mapped_pairs.sort(key=lambda x: x[0])

    final_stats = run_reducer(mapped_pairs)

    print(final_stats)

    results_payload = []
    for sensor, min_val, max_val, avg_val in final_stats:
        print(f"{sensor}\tmin={min_val}, max={max_val}, avg={avg_val:.2f}")
        results_payload.append({
            "sensor_id": sensor,
            "min": min_val,
            "max": max_val,
            "avg": avg_val
        })

    results_url = "http://127.0.0.1:5000/hadoop_results"
    try:
        resp = requests.post(results_url, json=results_payload)
        if resp.status_code == 201:
            print("Successfully sent MapReduce results to server.")
        else:
            print(f"Failed to send results: {resp.status_code}")
    except Exception as e:
        print(f"Error sending results back: {e}")

def main():
    while True:
        map_reduce()
        time.sleep(30)

if __name__ == "__main__":
    main()

