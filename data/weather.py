import requests
import os

def get_weather_forecast():
    api_key = os.getenv('API_KEY')
    url = "https://api.tomorrow.io/v4/weather/forecast?location=new%20york&apikey=" + api_key

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    return response.text
