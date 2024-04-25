# app.py
from data.players import *
from data.weather import *
from dotenv import load_dotenv

load_dotenv()

prem = league_player_data("EPL", "2022")  # Specify the year if needed
salah_id = prem[200]['id']
salah = get_player_shot_data(salah_id)

print(get_weather_forecast())
