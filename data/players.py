import pandas as pd
import ast
import logging
from understatapi import UnderstatClient
from tabulate import tabulate

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
        # Main player information
        players_info = [
            [
                player[0],
                player[1].strip() if player[1] else '',
                player[2],
                player[3],
                player[4],
                player[5],
                player[6].strip() if player[6] else '',
                player[7],
                player[8],
                player[9]
            ]
            for player in data
        ]
        df_players = pd.DataFrame(players_info, columns=[
            'ID', 'Name', 'Team', 'Value', 'DOB', 'Rating', 'Height', 'Nationality', 'Position', 'Foot'
        ])

        # Past teams
        past_teams_data = []
        for player in data:
            player_id = player[0]
            player_name = player[1].strip() if player[1] else ''
            if player[10]:
                for team in player[10]:
                    past_teams_data.append(
                        [player_id, player_name] + list(team))

        df_past_teams = pd.DataFrame(past_teams_data, columns=[
            'ID', 'Name', 'Current Team', 'New Team', 'Season', 'Date'
        ])

        # Injuries
        injuries_data = []
        for player in data:
            player_id = player[0]
            player_name = player[1].strip() if player[1] else ''
            if player[11]:
                for injury in player[11]:
                    injuries_data.append(
                        [player_id, player_name] + list(injury))

        df_injuries = pd.DataFrame(injuries_data, columns=[
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
