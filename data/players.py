import pandas as pd
from understatapi import UnderstatClient
import ast

understat = UnderstatClient()


def get_player_shot_data(player_id):
    player_data = understat.player(player=str(player_id)).get_shot_data()
    return pd.DataFrame(player_data)


def league_player_data(league, year):
    league_data = understat.league(league=str(
        league)).get_player_data(season=str(year))
    return pd.DataFrame(league_data)


def parse_data(data_str):
    return ast.literal_eval(data_str)


def create_players_dataframe(data):
    players_info = [
        [player[0], player[1].strip(), player[2], player[3], player[4], player[5],
         player[6].strip(), player[7], player[8], player[9]]
        for player in data
    ]
    return pd.DataFrame(players_info, columns=['ID', 'Name', 'Team', 'Value', 'DOB', 'Rating', 'Height', 'Nationality', 'Position', 'Foot'])


def create_transfers_dataframe(data):
    transfers = []
    for player in data:
        player_id = player[0]
        for transfer in player[10]:
            from_club, to_club, season, date = transfer
            transfers.append([player_id, from_club.strip(),
                             to_club.strip(), season, date])
    return pd.DataFrame(transfers, columns=['Player ID', 'From Club', 'To Club', 'Season', 'Date'])


def create_injuries_dataframe(data):
    injuries = []
    for player in data:
        player_id = player[0]
        for injury in player[11]:
            season, description, days = injury
            injuries.append([player_id, season, description.strip(), days])
    return pd.DataFrame(injuries, columns=['Player ID', 'Season', 'Injury', 'Days Missed'])
