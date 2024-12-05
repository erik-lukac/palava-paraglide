import holfuy
import forecast
import rezervace
import database
import json
from datetime import datetime
import schedule
import time
import logging
from typing import Optional, Any, Dict, NoReturn
from collections.abc import Callable
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError
from pathlib import Path
import signal
import sys
from functools import partial
import structlog

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Switch to enable or disable scheduling
enable_scheduling = True  # Set to True to enable scheduling, False to disable

logger = structlog.get_logger()

# Main function to gather data and store it
def main() -> None:
    logging.info("Starting main function.")
    database.create_tables()
    logging.info("Tables created successfully.")

    def safe_get_data(module: Any, get_data_func: Callable[[], Optional[dict]]) -> Optional[dict]:
        try:
            data = get_data_func()
            # If data is already a string (JSON), parse it
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except JSONDecodeError as e:
                    logging.error(f"Error decoding JSON from {module.__name__}: {e}")
                    return None
            return data
        except (RequestException, ValueError) as e:
            logging.error(f"Error retrieving data from {module.__name__}: {e}")
            return None

    holfuy_data = safe_get_data(holfuy, holfuy.get_data)
    forecast_data = safe_get_data(forecast, forecast.get_current_weather)
    rezervace_data = safe_get_data(rezervace, rezervace.get_reservation_count)

    if holfuy_data:
        database.insert_holfuy_data(holfuy_data)
        logging.info("Holfuy data inserted successfully.")

    if forecast_data:
        database.insert_forecast_data(forecast_data)
        logging.info("Forecast data inserted successfully.")

    if rezervace_data:
        database.insert_rezervace_data(rezervace_data)
        logging.info("Rezervace data inserted successfully.")

    if not any([holfuy_data, forecast_data, rezervace_data]):
        logging.warning("No data was available to insert.")

def handle_shutdown(signum: int, frame: Any) -> NoReturn:
    """Handle shutdown gracefully."""
    logging.info("Received shutdown signal. Cleaning up...")
    # Perform cleanup
    sys.exit(0)

def run_scheduler() -> NoReturn:
    """Run the scheduler with proper signal handling."""
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    for schedule_time in Config.SCHEDULE_TIMES:
        schedule.every().hour.at(schedule_time).do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if enable_scheduling:
        logging.info("Scheduling is enabled.")
        run_scheduler()
    else:
        logging.info("Scheduling is disabled. Running main function once.")
        main()
