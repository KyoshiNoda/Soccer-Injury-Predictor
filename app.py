from data.players import *
from data.weather import *
from data.utils import *
from dotenv import load_dotenv
from tabulate import tabulate
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

load_dotenv()

"""
Static text file with soccer data.
I believe we should only collect data for training or injury history.
This is because alot of the data is outdated such as missing prem players.
The following code just prints out the dataframe for injuries.
However there are others such as: df_players, df_past_teams in create_players_dataframe()
"""


def text_injuries():
    player_txt = read_data_from_file(
        'data/player.txt')  # training data strictly
    parsed_data = parse_data(player_txt)
    df_injuries = create_players_dataframe(parsed_data)
    print(tabulate(df_injuries.head(1000), headers='keys',
                   tablefmt='psql', showindex=False))

# text_injuries()


"""
PREM DATAFRAME: contains most players from the prem in 2024.
Feel free to print out the dataframe if you would like to see data.
Edge case: multiple teams in single season: EX: Cole Palmer: Man City and Chelsea
"""
df_prem_2024 = league_player_data("EPL", "2024")
df_player_biometrics = pd.read_csv('data/prem_players.csv') # 
# print(df_prem_2024)

"""
Scrapes data from the web to get player biometrics
sources: wikipedia and foxsports
Input constraints: Upper case letter for each player. (Has be a professional player)
"""
# web_scrape_player = get_player_biometrics("Leon Bailey")
# print(deeper_player_scrape("Leon Bailey"))


"""
Grabs player from the dataframe and attempts to grab the upcoming match
It then predicts the weather on either forecasted weather from the API or historical data
    Forecasted: If its less than 5 days, it will use the forecasted weather for that given date.
    Historical (WORK IN PROGRESS): more 5 days, it will look back 5 years on that specifc date and make predictions.
"""


def weather_predictions(player_name):
    player = df_prem_2024.loc[df_prem_2024['player_name'] == player_name]
    player_team = transform_team_name(
        player.team_title.to_string(index=False))
    player_matches = get_match_data(
        player_team, str(datetime.date.today().year))
    player_upcoming_matches = get_upcoming_match(player_matches)
    print(weather_prediction(player_upcoming_matches))

# weather_predictions("Erling Haaland")


def create_master_dataframe(df_prem_2024):
    """
    - player_name [x]
    - age [x]
    - height [x]
    - weight [x]
    - position [x]
    - team [x]
    - match_date [x]
    - opponent [x]
    - location [x]
    - weather_conditions [less than 5 days only.]
    """
    data_entries = []

    for _, player in df_prem_2024.iterrows():
        player_name = player['player_name']
        team_name = transform_team_name(player['team_title'])

        try:
            player_biometrics = get_player_biometrics(player_name, df_player_biometrics)
            # next_match_weather = get_player_weather_prediction(player_name)
        except Exception as e:
            print(f"Error retrieving biometrics for {player_name}: {e}")
            continue
        data_entry = {
            'player_name': player_name,
            'age': player_biometrics['age'],
            'height': player_biometrics['height'],
            'weight': player_biometrics['weight'],
            'position': player_biometrics['position'],
            'team': team_name,
        }
        # add_player_CSV(data_entry)
        data_entries.append(data_entry)

    master_dataframe = pd.DataFrame(data_entries)

    return master_dataframe


# fresh missing_player.txt
with open("data/missing_players.txt", "w") as file:
    pass

master_df = create_master_dataframe(df_prem_2024)
print(master_df.head())

# X = master_df.drop(['player_name', 'team', 'match_date', 'injury_status'], axis=1)
# y = master_df['injury_status']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)
# print(classification_report(y_test, y_pred))
# print(confusion_matrix(y_test, y_pred))
