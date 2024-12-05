from typing import Optional, Tuple
import sqlite3
import logging
from contextlib import contextmanager
from typing import Generator

def connect_db(db_name: str = 'database.db') -> sqlite3.Connection:
    """Connect to the database and return the connection object."""
    return sqlite3.connect(db_name)

def create_tables():
    """Create separate tables for each data source."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            
            # Create holfuy table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS holfuy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    station_id INTEGER,
                    station_name TEXT,
                    date_time TEXT,
                    wind_speed REAL,
                    wind_gust REAL,
                    wind_min REAL,
                    wind_direction REAL,
                    temperature REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create forecast table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS forecast (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    humidity REAL,
                    windspeed REAL,
                    winddirection REAL,
                    height REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create rezervace table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rezervace (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    day TEXT,
                    date TEXT,
                    reservation_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logging.info("All tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating tables: {e}")

@contextmanager
def get_db_connection(db_name: str = 'database.db') -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        yield conn
    finally:
        if conn:
            conn.close()

def insert_holfuy_data(data: dict) -> None:
    """Insert data into the holfuy table."""
    try:
        with get_db_connection() as conn:
            with conn:  # Transaction management
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO holfuy (
                        station_id, station_name, date_time, wind_speed, wind_gust, 
                        wind_min, wind_direction, temperature
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('station_id'),
                    data.get('station_name'),
                    data.get('date_time'),
                    data.get('wind_speed'),
                    data.get('wind_gust'),
                    data.get('wind_min'),
                    data.get('wind_direction'),
                    data.get('temperature')
                ))
        logging.info("Holfuy data inserted successfully.")
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to insert holfuy data: {e}")

def insert_forecast_data(data: dict) -> None:
    """Insert data into the forecast table."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO forecast (
                    temperature, humidity, windspeed, winddirection, height
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('temperature'),
                data.get('humidity'),
                data.get('windspeed'),
                data.get('winddirection'),
                data.get('height')
            ))
            conn.commit()
            logging.info("Forecast data inserted successfully.")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while inserting forecast data: {e}")

def insert_rezervace_data(data: dict) -> None:
    """Insert data into the rezervace table."""
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO rezervace (
                    day, date, reservation_count
                ) VALUES (?, ?, ?)
            ''', (
                data.get('Den'),
                data.get('Datum'),
                data.get('reservation_count')
            ))
            conn.commit()
            logging.info("Rezervace data inserted successfully.")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while inserting rezervace data: {e}")

def check_data(table_name: str = None):
    """Helper function to verify data in the database.
    
    Args:
        table_name: Optional name of specific table to check. If None, checks all tables.
    """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            
            if table_name:
                cursor.execute(f'SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT 5')
                print(f"\nLatest 5 entries from {table_name} table:")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                for table in ['holfuy', 'forecast', 'rezervace']:
                    cursor.execute(f'SELECT * FROM {table} ORDER BY created_at DESC LIMIT 5')
                    print(f"\nLatest 5 entries from {table} table:")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
    except sqlite3.Error as e:
        logging.error(f"An error occurred while checking data: {e}")
