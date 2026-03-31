import sqlite3 as sql

def query_database(query, params = None):
    if not query:
        print("Error: No query provided")
        return None
    try:
        with sql.connect("readings.db") as conn:
            cursor = conn.cursor()

            if params:
                result = cursor.execute(query, params)
            else:
                result = cursor.execute(query)

        return result

    except Exception as e:
        print(f"Database Error: {e}")
        return None

def is_tables():
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    result = query_database(query)
    return result

def setup_database():

    query_database('''CREATE TABLE IF NOT EXISTS sensortypes
                        (sensor_type TEXT NOT NULL PRIMARY KEY,
                        unit TEXT NOT NULL
                        )''')

    query_database('''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("Temperature Sensor", "°C")''')
    query_database('''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("Pressure Sensor", "hPa")''')
    query_database('''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("Air Quality Sensor", "PM10")''')
    query_database('''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("CO2 Sensor", "ppm")''')


    query_database('''CREATE TABLE IF NOT EXISTS sensors
                        (
                        sensor_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        sensor_latitude REAL NOT NULL,
                        sensor_longitude REAL NOT NULL,
                        sensor_type TEXT NOT NULL REFERENCES sensortypes(sensor_type)
                        )''')

    add_sensor(11, 43.7, 19.4, "CO2 Sensor")
    add_sensor(12, 67.4, 21.6, "Pressure Sensor")
    add_sensor(13, 49.4, 28.7, "Air Quality Sensor")
    add_sensor(14, 37.4, 39.2, "Temperature Sensor")

    query_database('''CREATE TABLE IF NOT EXISTS measurements
                         (sensor_timestamp TEXT NOT NULL PRIMARY KEY,
                         sensor_id INTEGER NOT NULL REFERENCES sensors(sensor_id),
                         sensor_value INTEGER)''')

    setup_hadoop_table()

def add_sensor(sensor_id, lat, lon, sensor_type):
    query = f'''INSERT OR IGNORE INTO
            sensors (sensor_id, sensor_latitude, sensor_longitude, sensor_type)
            VALUES (?,?,?,?)'''

    params = (sensor_id, lat, lon, sensor_type)

    return query_database(query, params)

def add_measurement(sensor_timestamp, sensor_id, sensor_value):
    query = f'''INSERT OR IGNORE INTO
                measurements (sensor_timestamp, sensor_id, sensor_value)
                VALUES (?,?,?)'''

    params = (sensor_timestamp, sensor_id, sensor_value)

    return query_database(query, params)

def display_measurements():
    query = '''SELECT
                    m.sensor_timestamp,
                    m.sensor_value,
                    st.unit,
                    s.sensor_latitude,
                    s.sensor_longitude,
                    st.sensor_type
               FROM measurements m
                     INNER JOIN sensors s
                                ON s.sensor_id = m.sensor_id
                     INNER JOIN sensortypes st
                                ON s.sensor_type = st.sensor_type'''
    result = query_database(query)
    return result


def setup_hadoop_table():
    # Create a table for the processed results
    query_database('''CREATE TABLE IF NOT EXISTS processed_results
                      (
                            sensor_id TEXT PRIMARY KEY,
                            min_val REAL,
                            max_val REAL,
                            avg_val REAL,
                            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')

def save_hadoop_results(results):
    # We use REPLACE so that if we run Hadoop again, it updates the values
    query = '''INSERT OR REPLACE INTO processed_results 
               (sensor_id, min_val, max_val, avg_val) VALUES (?, ?, ?, ?)'''

    for item in results:
        params = (item['sensor_id'], item['min'], item['max'], item['avg'])
        query_database(query, params)


def main():
    with sql.connect('readings.db') as conn:
        conn.execute("PRAGMA foreign_keys = ON")
    setup_database()
    print("Tables:")
    for i in is_tables():
        print(i)
    # add_sensor(conn, 1, '10', '10', 'Air Quality Sensor')
    # add_sensor(conn, 2, '11', '12', 'Air Quality Sensor')
    # add_measurement(conn, 20260303,1, 60)
    # add_measurement(conn,20260304,2, 67)
    # add_measurement(conn,20260305,1, 70)
    # add_measurement(conn,20260306,2, 80)

    # for i in display_measurements():
    #     print(i)


if __name__ == "__main__":
    main()
