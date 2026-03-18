from flask import Flask, request, jsonify
import datetime
import relational_database as database

app = Flask(__name__)

conn = database.sql.connect('readings.db')
conn.execute("PRAGMA foreign_keys = ON")
database.setup_database(conn)

@app.route('/measurements', methods=['POST'])
def recieve_measurement():
    data = request.get.json()

    # Data validation
    required_keys = ["sensor_id", "value"]
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing data"}), 400

    # Either uses timestamp from client or server-side if not provided
    timestamp = data.get("timestamp") or datetime.time()

    try:
        database.add_measurement(conn, timestamp, data["sensor_id"], data["value"])
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/measurements_table', method=["GET"])
def display_measurements():
    result = database.display_measurements(conn)
    html = ""
    for i in result:
        html = html + "<tr>" + i + "</tr>"
    return html

