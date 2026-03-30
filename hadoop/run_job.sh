#!/bin/bash
# run_job.sh: Scheduled execution script for Hadoop Streaming

# --- Configuration --- Make sure network addresses match
SERVER_URL="http://flask-server:5000/hadoop"
RESULTS_URL="http://flask-server:5000/hadoop_results"
LOCAL_DATA_FILE="local_sensor_data.csv"
HADOOP_OUTPUT_DIR="hadoop_output"

# Remember to check that this directory is correct
HADOOP_STREAMS_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar"

while true; do
  echo "--- Starting new job iteration ---"

  # Fetches server data
  echo "DEBUG: Fetching data from ${SERVER_URL}..."
  if ! curl -s -o "${LOCAL_DATA_FILE}" "${SERVER_URL}"; then
    echo "Error: Failed to fetch data. Waiting 30 seconds."
    sleep 30
    continue
  fi
  echo "DEBUG: Data length: $(stat -c%s "${LOCAL_DATA_FILE}") bytes"

  # Hadoop will error if the output directory already exists.
  rm -rf "${HADOOP_OUTPUT_DIR}"

  echo "DEBUG: Running Hadoop Streaming job..."
  hadoop jar "${HADOOP_STREAMS_JAR}" \
        -input "${LOCAL_DATA_FILE}" \
        -output "${HADOOP_OUTPUT_DIR}" \
        -mapper "./mapper.py" \
        -reducer "./reducer.py"

  # Checks job success and post results
  if [ $? -eq 0 ]; then
      echo "DEBUG: Job successful. Processing and posting results..."

      # Cat combines the output
      COMBINED_RESULTS_FILE="final_stats.txt"
      cat "${HADOOP_OUTPUT_DIR}"/part-* > "${COMBINED_RESULTS_FILE}"

      # Print results locally
      while IFS=$'\t' read -r sensor min val max val avg val; do
        echo -e "$sensor\tmin=$min, max=$max, avg=$avg"
      done < "${COMBINED_RESULTS_FILE}"


python3 <<EOF
import json
import requests
import sys

payload = []
try:
    with open("${COMBINED_RESULTS_FILE}", 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            sensor, min_v, max_v, avg_v = line.split('\t')
            payload.append({
                "sensor_id": sensor,
                "min": float(min_v),
                "max": float(max_v),
                "avg": float(avg_v)
            })

    # POST the constructed JSON to the results endpoint
    if payload:
        print(f"INFO: Posting {len(payload)} result records to ${RESULTS_URL}")
        resp = requests.post("${RESULTS_URL}", json=payload)
        if resp.status_code == 201:
            print("Successfully sent results.")
        else:
            print(f"Failed to send results: {resp.status_code} - {resp.text}")
except FileNotFoundError:
    print("Warning: final_stats.txt not found, results were not posted.")
except requests.exceptions.RequestException as e:
    print(f"Error posting results: {e}")
EOF

  else :
        echo "Error: Hadoop Streaming job failed."
    fi

    echo "INFO: Done. Waiting 30 seconds."
    sleep 30
done
