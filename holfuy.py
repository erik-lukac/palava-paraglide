import requests
import json
import os

def get_data():
    try:
        # Access the token from the environment variable
        private_token = os.getenv('PRIVATE_TOKEN')

        # Define the URL for the Holfuy API with the token
        url = f'http://api.holfuy.com/live/?s=670&pw={private_token}&m=JSON&avg=1&tu=C&su=m/s'
        
        # Make a GET request to the API
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Extract relevant data
        station_id = data.get('stationId')
        station_name = data.get('stationName')
        date_time = data.get('dateTime')
        wind_speed = data['wind'].get('speed')
        wind_gust = data['wind'].get('gust')
        wind_min = data['wind'].get('min')
        wind_direction = data['wind'].get('direction')
        temperature = data.get('temperature')
        
        # Create a JSON object with the extracted data
        weather_data = {
            'station_id': station_id,
            'station_name': station_name,
            'date_time': date_time,
            'wind_speed': wind_speed,
            'wind_gust': wind_gust,
            'wind_min': wind_min,
            'wind_direction': wind_direction,
            'temperature': temperature
        }
        
        # Return the data as a JSON string
        return json.dumps(weather_data)
    
    except requests.RequestException as e:
        print(f"Error fetching data from Holfuy API: {e}")
        return json.dumps({})

# Example usage
if __name__ == "__main__":
    print(get_data()) 