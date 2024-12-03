import holfuy
import forecast
import rezervace
import database
import json
from datetime import datetime
import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Switch to enable or disable scheduling
enable_scheduling = True  # Set to True to enable scheduling, False to disable

# Main function to gather data and store it
def main():
    logging.info("Starting main function.")
    database.create_tables()
    logging.info("Tables created successfully.")

    def safe_get_data(module, get_data_func):
        try:
            data = get_data_func()
            # If data is already a string (JSON), parse it
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON from {module.__name__}: {e}")
                    return None
            return data
        except Exception as e:
            logging.error(f"Error retrieving data from {module.__name__}: {e}")
            return None

    holfuy_data = safe_get_data(holfuy, holfuy.get_data)
    forecast_data = safe_get_data(forecast, forecast.get_current_weather)
    rezervace_data = safe_get_data(rezervace, rezervace.get_reservation_count)

    if holfuy_data and forecast_data and rezervace_data:
        unified_record = (
            holfuy_data.get('station_id'),
            holfuy_data.get('station_name'),
            holfuy_data.get('date_time'),
            holfuy_data.get('wind_speed'),
            holfuy_data.get('wind_gust'),
            holfuy_data.get('wind_min'),
            holfuy_data.get('wind_direction'),
            holfuy_data.get('temperature'),
            forecast_data.get('temperature'),
            forecast_data.get('humidity'),
            forecast_data.get('windspeed'),
            forecast_data.get('winddirection'),
            forecast_data.get('height'),
            rezervace_data.get('Den'),
            rezervace_data.get('Datum'),
            rezervace_data.get('reservation_count')
        )
        database.insert_data(unified_record)
        logging.info("Data inserted successfully.")
    else:
        logging.warning("Incomplete data. Skipping insertion.")

# Schedule the main function to run every 15 minutes, starting at 2 minutes past the hour
def schedule_jobs():
    logging.info("Scheduling jobs.")
    schedule.every().hour.at(":02").do(main)
    schedule.every().hour.at(":17").do(main)
    schedule.every().hour.at(":32").do(main)
    schedule.every().hour.at(":47").do(main)
    logging.info("Jobs scheduled at :02, :17, :32, :47 every hour.")

if __name__ == "__main__":
    if enable_scheduling:
        logging.info("Scheduling is enabled.")
        schedule_jobs()
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        logging.info("Scheduling is disabled. Running main function once.")
        main()
