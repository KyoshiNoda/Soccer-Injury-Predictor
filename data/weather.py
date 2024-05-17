import logging
import requests
import os
import json
import datetime

logging.basicConfig(level=logging.INFO)


def weather_prediction(match_day):
    match_day_datetime = datetime.datetime.strptime(
        match_day[0], '%Y-%m-%d %H:%M:%S')
    date_diff = match_day_datetime - datetime.datetime.today()
    if date_diff.days < 5:
        response = get_weather_forecast(match_day[1])
        print(len(response['timelines']['dailys']))
    else:
        historical_weather_data(match_day[1])


def get_weather_forecast(location):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&timesteps=1d&apikey={api_key}"

    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
    return None


def historical_weather_data(location):
    print(location)
