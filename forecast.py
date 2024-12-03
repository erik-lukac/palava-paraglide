import requests
import datetime
import json

def get_current_weather():
    # Coordinates and height for the specific location
    latitude = 48.86902567024753
    longitude = 16.65037094992182
    height = 462.0  # Height in meters

    # Define the API endpoint and parameters
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m,relativehumidity_2m,windspeed_10m,winddirection_10m',
        'timezone': 'GMT'
    }

    try:
        # Send the GET request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        # Get the current hour in UTC
        current_time = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)

        # Find the closest available time in the API response
        available_times = data['hourly']['time']
        closest_time = min(
            available_times,
            key=lambda t: abs(datetime.datetime.fromisoformat(t).replace(tzinfo=datetime.timezone.utc) - current_time)
        )

        # Extract the index of the closest time
        time_index = available_times.index(closest_time)

        # Extract the relevant weather data
        temperature = data['hourly']['temperature_2m'][time_index]
        humidity = data['hourly']['relativehumidity_2m'][time_index]
        windspeed = data['hourly']['windspeed_10m'][time_index]
        winddirection = data['hourly']['winddirection_10m'][time_index]

        # Create a JSON object with the weather data
        weather_data = {
            'temperature': temperature,
            'humidity': humidity,
            'windspeed': windspeed,
            'winddirection': winddirection,
            'height': height  # Include height in the output
        }

        # Return the weather data as a JSON string
        return json.dumps(weather_data)

    except requests.RequestException as e:
        print(f"Error fetching current weather data: {e}")
        return None
    except ValueError as e:
        print(f"Error processing weather data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    current_weather_json = get_current_weather()
    if current_weather_json:
        print(current_weather_json) 