from flask import Flask, request, jsonify
import datetime
import relational_database as database

app = Flask(__name__)

with database.sql.connect('readings.db') as conn:
    conn.execute("PRAGMA foreign_keys = ON")
database.setup_database()

@app.route('/measurements', methods=['POST'])
def recieve_measurement():
    data = request.get_json().copy()

    # Data validation
    required_keys = ["sensor_id", "value"]
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing data"}), 400

    # Either uses timestamp from client or server-side if not provided
    timestamp = data.get("timestamp") or datetime.time()

    try:
        database.add_measurement(timestamp, data["sensor_id"], data["value"])
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hadoop', methods=['GET'])
def get_measurements():
    try:
        rows = database.display_measurements()

        data = []
        for row in rows:
            timestamp = row[0]
            val = row[1]
            unit = row[2]
            lat = row[3]
            lon = row[4]
            s_type = row[5]

            line = f"{timestamp},sensor_{lat}_{lon},Active,{lat},{lon},{s_type},{val}"
            data.append(line)

        return "\n".join(data), 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        return jsonify({"Data retrieval error": str(e)}), 500


@app.route('/hadoop_results', methods=['POST'])
def receive_hadoop_results():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    try:
        database.save_hadoop_results(data)
        return jsonify({"status": "results saved"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/hadoop_table', methods=['GET'])
def display_hadoop_table():
    results = database.query_database("SELECT * FROM processed_results")

    html = """
    <html>
    <head><style>
        table { border-collapse: collapse; width: 50%; margin: 20px; font-family: sans-serif; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2 f2 f2; }
    </style></head>
    <body>
        <h2>Hadoop MapReduce Results</h2>
        <table>
            <tr><th>Sensor</th><th>Min</th><th>Max</th><th>Average</th><th>Processed At</th></tr>
    """

    for row in results:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]:.2f}</td><td>{row[4]}</td></tr>"

    html += "</table></body></html>"
    return html

@app.route('/measurements_table', methods=["GET"])
def display_measurements():
    result = database.display_measurements()

    grouped_data = {}
    for row in result:
        # row[5] is the sensor_type from your query
        s_type = row[5]
        if s_type not in grouped_data:
            grouped_data[s_type] = []
        grouped_data[s_type].append(row)

    html = "<html><head><style>table{width:100%; border-collapse:collapse; margin-bottom:20px;} th,td{border:1px solid #ddd; padding:8px;}</style></head><body>"
    html += "<h1>Sensor Measurements by Type</h1>"

    for s_type, rows in grouped_data.items():
        html += f"### {s_type} Readings"
        html += "<table><thead><tr><th>Time</th><th>Value</th><th>Unit</th><th>Lat</th><th>Lon</th></tr></thead><tbody>"

        for r in rows:
            html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"

        html += "</tbody></table>"

    html += "</body></html>"
    return html

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True, threaded=False)

