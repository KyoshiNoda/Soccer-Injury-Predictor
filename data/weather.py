import logging
import requests
import os
from datetime import datetime
import datetime

logging.basicConfig(level=logging.INFO)


def weather_prediction(match_day):
    if isinstance(match_day, str) and match_day == "No upcoming matches found":
        return match_day
    try:
        match_day_datetime = datetime.datetime.strptime(
            match_day[0], '%Y-%m-%d %H:%M:%S')
        date_diff = match_day_datetime - datetime.datetime.today()

        if date_diff.days < 5:
            response = get_weather_forecast(match_day[1])
            print(response)
        else:
            response = historical_weather_data(match_day[0], match_day[1])
            print(response)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_weather_forecast(location):
    api_key = os.getenv('TOMORROW_API_KEY')
    url = "https://api.tomorrow.io/v4/weather/forecast"
    params = {
        "location": location,
        "apikey": api_key,
        "timesteps": "1d"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        values_list = [
            result['timelines']['daily']
            for result in [response.json()]
        ]
        return values_list
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
    return None


def historical_weather_data(time, location):
    api_key = os.getenv('VISUALCROSSING_API_KEY')
    try:
        current_datetime_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        end_datetime_obj = current_datetime_obj.replace(
            year=current_datetime_obj.year - 1)
        start_datetime_obj = end_datetime_obj.replace(
            year=end_datetime_obj.year - 4)

        all_results = []

        for year in range(start_datetime_obj.year, end_datetime_obj.year + 1):
            specific_day = end_datetime_obj.replace(year=year)
            iso_datetime_str = specific_day.strftime('%Y-%m-%dT%H:%M:%S')

            base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history"

            params = {
                "aggregateHours": "24",
                "startDateTime": iso_datetime_str,
                "endDateTime": iso_datetime_str,
                "unitGroup": "us",
                "contentType": "json",
                "location": location,
                "key": api_key
            }

            response = requests.get(base_url, params=params)
            response.raise_for_status()

            all_results.append(response.json())
        values_list = [
            result['locations'][location]['values']
            for result in all_results
        ]

        return values_list

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        logging.error(f"Response content: {response.content}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    return None
