import sqlite3 as sql

def query_database(conn, query, params = None):
    if not query:
        print("Error: No query provided")
        return None
    try:
        with conn:
            cursor = conn.cursor()

            if params:
                result = cursor.execute(query, params)
            else:
                result = cursor.execute(query)

        return result

    except Exception as e:
        print(f"Database Error: {e}")
        return None

def is_tables(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    result = query_database(conn, query)
    return result

def setup_database(conn):

    query_database(conn, '''CREATE TABLE IF NOT EXISTS sensortypes
                        (sensor_type TEXT NOT NULL PRIMARY KEY,
                        unit TEXT NOT NULL
                        )''')

    query_database(conn, '''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("Temperature Sensor", "°C")''')
    query_database(conn, '''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("Pressure Sensor", "hPa")''')
    query_database(conn, '''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("Air Quality Sensor", "PM10")''')
    query_database(conn, '''INSERT OR IGNORE INTO sensortypes (sensor_type, unit) VALUES ("CO2 Sensor", "ppm")''')

    query_database(conn, '''CREATE TABLE IF NOT EXISTS sensors
                        (
                        sensor_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        sensor_latitude REAL NOT NULL,
                        sensor_longitude REAL NOT NULL,
                        senor_type TEXT NOT NULL REFERENCES sensortypes(sensor_type)
                        )''')

    query_database(conn, '''CREATE TABLE IF NOT EXISTS measurements
                         (timestamp INTEGER NOT NULL PRIMARY KEY,
                         sensor_id INTEGER NOT NULL REFERENCES sensors(sensor_id),
                         value INTEGER)''')

def add_sensor(conn, id, lat, lon, type):

    query = f'''INSERT OR IGNORE INTO
            sensors (sensor_id, sensor_latitude, sensor_longitude, sensor_type)
            VALUES (?,?,?,?)'''

    params = (id, lat, lon, type)

    return query_database(conn, query, params)


def main():
    conn = sql.connect('readings.db')
    conn.execute("PRAGMA foreign_keys = ON")
    setup_database(conn)
    print("Tables:")
    for i in is_tables(conn):
        print(i)



if __name__ == "__main__":
    main()
