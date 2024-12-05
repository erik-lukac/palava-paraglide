import requests
import json
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables at the start of the script
load_dotenv()

def get_data() -> str:
    try:
        private_token = os.getenv('PRIVATE_TOKEN')
        if not private_token:
            print("Error: PRIVATE_TOKEN not found in environment variables")
            return json.dumps({})
            
        url = f'http://api.holfuy.com/live/?s=670&pw={private_token}&m=JSON&avg=1&tu=C&su=m/s'
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        weather_data = {
            'station_id': data.get('stationId'),
            'station_name': data.get('stationName'),
            'date_time': data.get('dateTime'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'wind_gust': data.get('wind', {}).get('gust'),
            'wind_min': data.get('wind', {}).get('min'),
            'wind_direction': data.get('wind', {}).get('direction'),
            'temperature': data.get('temperature')
        }
        
        return json.dumps(weather_data)
    
    except requests.RequestException as e:
        print(f"Error fetching data from Holfuy API: {e}")
        return json.dumps({})

# Example usage
if __name__ == "__main__":
    print(get_data()) 