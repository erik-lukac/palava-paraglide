import sqlite3
import logging

def connect_db(db_name='database.db'):
    """Connect to the database and return the connection object."""
    return sqlite3.connect(db_name)

def create_tables():
    """Create a unified table for all data sources."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            # Create a unified table for all data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prehled_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    station_id INTEGER,
                    station_name TEXT,
                    date_time TEXT,
                    wind_speed REAL,
                    wind_gust REAL,
                    wind_min REAL,
                    wind_direction REAL,
                    temperature REAL,
                    forecast_temperature REAL,
                    forecast_humidity REAL,
                    forecast_windspeed REAL,
                    forecast_winddirection REAL,
                    forecast_height REAL,
                    day TEXT,
                    date TEXT,
                    reservations INTEGER
                )
            ''')
            conn.commit()
            logging.info("Tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating tables: {e}")

def insert_data(data):
    """Insert data into the unified table."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO prehled_table (
                    station_id, station_name, date_time, wind_speed, wind_gust, wind_min, wind_direction, temperature,
                    forecast_temperature, forecast_humidity, forecast_windspeed, forecast_winddirection, forecast_height,
                    day, date, reservations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()
            logging.info("Data inserted successfully.")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while inserting data: {e}")

# Remove or update the alter_table function as needed
