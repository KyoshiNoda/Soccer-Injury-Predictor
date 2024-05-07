import logging
import requests
import os
import json

logging.basicConfig(level=logging.INFO)


def get_weather_forecast():
    api_key = os.getenv('API_KEY')
    url = f"https://api.tomorrow.io/v4/weather/forecast?location=new%20york&apikey={api_key}"

    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return json.dumps(response.json(), indent=4)
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
    return None
