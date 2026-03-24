from flask import Flask, request, jsonify
import datetime
import relational_database as database

app = Flask(__name__)

conn = database.sql.connect('readings.db')
conn.execute("PRAGMA foreign_keys = ON")
database.setup_database(conn)

@app.route('/measurements', methods=['POST'])
def recieve_measurement():
    data = request.get_json()

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

@app.route('/hadoop', methods=['GET'])
def get_measurements():
    try:
        rows = database.display_measurements(conn)

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

@app.route('/measurements_table', methods=["GET"])
def display_measurements():
    result = database.display_measurements(conn)
    html = ""
    for i in result:
        html = html + "<tr>" + i + "</tr>"
    return html

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True, threaded=True)

