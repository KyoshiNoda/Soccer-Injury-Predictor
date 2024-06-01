from data.players import *
from data.weather import *
from data.utils import *
from dotenv import load_dotenv
from tabulate import tabulate
import datetime

load_dotenv()

player_txt = read_data_from_file('data/player.txt')  # training data strictly
parsed_data = parse_data(player_txt)
# FROM TEXT FILE: left out other datasets since its outdated (maybe come back to this.)
df_injuries = create_players_dataframe(parsed_data)

# print("INJURY HISTORY")
# print(tabulate(df_injuries.head(1000), headers='keys',
#       tablefmt='psql', showindex=False))

# edge case: multiple teams in single season: EX: Cole Palmer: Man City and Chelsea
df_prem_2024 = league_player_data("EPL", "2024")
"""
PARSED OUT upcoming match for a given player.
"""
haaland = df_prem_2024.loc[df_prem_2024['player_name'] == "Erling Haaland"]
haaland_team = transform_team_name(haaland.team_title.to_string(index=False))
haaland_matches = get_match_data(haaland_team, str(datetime.date.today().year))
haaland_upcoming_match = get_upcoming_match(haaland_matches)


print(get_player_age("Erling Haaland"))
print(get_player_height("Erling Haaland"))
print(get_player_weight("Erling Haaland"))

# print(tabulate(df_prem_2024, headers='keys', tablefmt='psql', showindex=False))
# print(weather_prediction(haaland_upcoming_match))