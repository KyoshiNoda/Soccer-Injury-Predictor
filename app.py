from data.players import *
from data.weather import *
from dotenv import load_dotenv

load_dotenv()

prem_df = league_player_data("EPL", "2022")
salah = prem_df.iloc[3]


# Sample data as a string
data_str = """
[(u'238223', u'Ederson', u'Manchester City', u'1,14 Bill. €', u'1993-08-17', u'89', u'1,88\xa0', u'Brazil', u'Goalkeeper', u'left', [(u'Benfica ', u'Man City ', u'17/18', u'Jul 1, 2017'), (u'Rio Ave FC ', u'Benfica ', u'15/16', u'Jul 1, 2015')], [(u'16/17', u'Meniscal Injury', u'29')]),
 (u'40423', u'Claudio Bravo', u'Manchester City', u'1,14 Bill. €', u'1983-04-13', u'84', u'1,84\xa0', u'Chile', u'Goalkeeper', u'right', [(u'FC Barcelona ', u'Man City ', u'16/17', u'Aug 25, 2016')], [(u'18/19', u'Achilles tendon rupture', u'314')])]
"""

parsed_data = parse_data(data_str)

df_players = create_players_dataframe(parsed_data)
df_transfers = create_transfers_dataframe(parsed_data)
df_injuries = create_injuries_dataframe(parsed_data)

print(df_players.head())
print(df_transfers.head())
print(df_injuries.head())


# get_weather_forecast()