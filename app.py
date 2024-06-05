from data.players import *
from data.weather import *
from data.utils import *
from dotenv import load_dotenv
from tabulate import tabulate
import datetime

load_dotenv()

"""
Static text file with soccer data.
I believe we should only collect data for training or injury history.
This is because alot of the data is outdated such as missing prem players.
The following code just prints out the dataframe for injuries.
However there are others such as: df_players, df_past_teams in create_players_dataframe()
"""
def text_injuries():
    player_txt = read_data_from_file('data/player.txt')  # training data strictly
    parsed_data = parse_data(player_txt)
    df_injuries = create_players_dataframe(parsed_data)
    print(tabulate(df_injuries.head(1000), headers='keys',
        tablefmt='psql', showindex=False))

"""
PREM DATAFRAME: contains most players from the prem in 2024.
Feel free to print out the dataframe if you would like to see data.
Edge case: multiple teams in single season: EX: Cole Palmer: Man City and Chelsea
"""
df_prem_2024 = league_player_data("EPL", "2024")
# print(df_prem_2024)

"""
Scrapes data from the web to get player biometrics
sources: wikipedia and foxsports
Input constraints: Upper case letter for each player. (Has be a professional player)
"""
def player_biometrics():
    print(get_player_age("Erling Haaland"))
    print(get_player_height("Erling Haaland"))
    print(get_player_weight("Erling Haaland"))


"""
Grabs player from the dataframe and attempts to grab the upcoming match
It then predicts the weather on either forecasted weather from the API or historical data
    Forecasted: If its less than 5 days, it will use the forecasted weather for that given date.
    Historical (WORK IN PROGRESS): more 5 days, it will look back 5 years on that specifc date and make predictions.
"""
def weather_predictions():
    haaland = df_prem_2024.loc[df_prem_2024['player_name'] == "Erling Haaland"]
    haaland_team = transform_team_name(
        haaland.team_title.to_string(index=False))
    haaland_matches = get_match_data(
        haaland_team, str(datetime.date.today().year))
    haaland_upcoming_match = get_upcoming_match(haaland_matches)
    print(tabulate(df_prem_2024, headers='keys', tablefmt='psql', showindex=False))
    print(weather_prediction(haaland_upcoming_match))
