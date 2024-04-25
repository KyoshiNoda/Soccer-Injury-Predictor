from data.players import *
from data.weather import *
from dotenv import load_dotenv

load_dotenv()

prem_df = league_player_data("EPL", "2022")
salah = prem_df.iloc[3]
# print(get_weather_forecast())
