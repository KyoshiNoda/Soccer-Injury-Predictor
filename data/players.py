import pandas as pd
import ast
import logging
from understatapi import UnderstatClient
from tabulate import tabulate
from data.player_utils import *

logging.basicConfig(level=logging.INFO)

understat = UnderstatClient()


def get_player_shot_data(player_id):
    try:
        player_data = understat.player(player=str(player_id)).get_shot_data()
        df = pd.DataFrame(player_data)
        return tabulate(df, headers='keys', tablefmt='psql', showindex=False)
    except Exception as e:
        logging.error(f"Failed to get player shot data: {e}")
        return pd.DataFrame()


def league_player_data(league, year):
    try:
        league_data = understat.league(league=str(
            league)).get_player_data(season=str(year))
        df = pd.DataFrame(league_data)
        return tabulate(df, headers=df.columns, tablefmt='psql', showindex=False)
    except Exception as e:
        logging.error(f"Failed to get league player data: {e}")
        return pd.DataFrame()


def parse_data(data_str):
    try:
        return ast.literal_eval(data_str)
    except SyntaxError as e:
        logging.error(f"Error parsing data: {e}")
        return []


def create_players_dataframe(data):
    try:
        df_players = pd.DataFrame(parse_player_info(data), columns=[
            'ID', 'Name', 'Team', 'Value', 'DOB', 'Rating', 'Height', 'Nationality', 'Position', 'Foot'
        ])

        df_past_teams = pd.DataFrame(parse_past_teams(data), columns=[
            'ID', 'Name', 'Current Team', 'New Team', 'Season', 'Date'
        ])

        df_injuries = pd.DataFrame(parse_injury_history(data), columns=[
            'ID', 'Name', 'Season', 'Injury Type', 'Absences'
        ])

        return df_players, df_past_teams, df_injuries

    except Exception as e:
        logging.error(f"Failed to create dataframes: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def create_transfers_dataframe(data):
    try:
        transfers = []
        for player in data:
            player_id = player[0]
            for transfer in player[10]:
                from_club, to_club, season, date = transfer
                transfers.append(
                    [player_id, from_club.strip(), to_club.strip(), season, date])
        df = pd.DataFrame(transfers, columns=[
                          'Player ID', 'From Club', 'To Club', 'Season', 'Date'])
        return tabulate(df, headers='keys', tablefmt='psql', showindex=False)
    except Exception as e:
        logging.error(f"Failed to create transfers dataframe: {e}")
        return pd.DataFrame()


def create_injuries_dataframe(data):
    try:
        injuries = []
        for player in data:
            player_id = player[0]
            for injury in player[11]:
                season, description, days = injury
                injuries.append([player_id, season, description.strip(), days])
        df = pd.DataFrame(injuries, columns=[
                          'Player ID', 'Season', 'Injury', 'Days Missed'])
        return tabulate(df, headers='keys', tablefmt='psql', showindex=False)
    except Exception as e:
        logging.error(f"Failed to create injuries dataframe: {e}")
        return pd.DataFrame()
