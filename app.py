from data.players import *
from data.weather import *
from data.utils import *
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

player_txt = read_data_from_file('data/player.txt')
parsed_data = parse_data(player_txt)
df_prem_2022 = league_player_data("EPL", "2022")
weather_data = get_weather_forecast()

df_players, df_past_teams, df_injuries = create_players_dataframe(parsed_data)

print(tabulate(df_players, headers=df_players.columns,
      tablefmt='psql', showindex=False))
