import pandas as pd
import ast
import logging
from understatapi import UnderstatClient
from tabulate import tabulate
from data.player_utils import *
from bs4 import BeautifulSoup
import requests

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
        league_data = understat.league(
            league=league).get_player_data(season=year)
        return pd.DataFrame(league_data)
    except Exception as e:
        logging.error(f"Failed to get league player data: {e}")
        return pd.DataFrame()


def get_match_data(team, date):
    try:
        match_data = understat.team(team=team).get_match_data(season=date)
        return pd.DataFrame(match_data)
    except Exception as e:
        logging.error(f"Failed to get match data: {e}")
        return pd.DataFrame()


def parse_data(data_str):
    try:
        return ast.literal_eval(data_str)
    except SyntaxError as e:
        logging.error(f"Error parsing data: {e}")
        return []


def create_players_dataframe(data):
    # for now I believe I only need the injury datasets, since the other ones are expired.
    try:
        # df_players = pd.DataFrame(parse_player_info(data), columns=[
        #     'ID', 'Name', 'Team', 'Value', 'DOB', 'Rating', 'Height', 'Nationality', 'Position', 'Foot'
        # ])

        # df_past_teams = pd.DataFrame(parse_past_teams(data), columns=[
        #     'ID', 'Name', 'Current Team', 'New Team', 'Season', 'Date'
        # ])

        df_injuries = pd.DataFrame(parse_injury_history(data), columns=[
            'ID', 'Name', 'Season', 'Injury Type', 'Absences'
        ])

        return df_injuries

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


def get_player_weight(player_name):
    parsed_player = player_name.replace(" ", "-")
    response = requests.get(
        f"https://www.foxsports.com/soccer/{parsed_player.lower()}-player-bio")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='data-table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1 and "Height, Weight" in cells[0].get_text(strip=True):
                    weight_data_text = cells[1].get_text(strip=True)
                    try:
                        weight = weight_data_text.split(", ")[1]
                        return weight
                    except IndexError:
                        return "Weight information not found."
            return "Height, Weight row not found."
        else:
            return "Data table not found."
    else:
        return "Weight information not found."


def get_player_height(player_name):
    parsed_player = player_name.replace(" ", "_")
    url = f'https://en.wikipedia.org/wiki/{parsed_player}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        height_row = soup.find('th', text='Height').parent if soup.find(
            'th', text='Height') else None
        if height_row:
            height = height_row.find('td', class_='infobox-data').text.strip()
            return height[0:6]
        else:
            print("Height information not found.")
    else:
        print(
            f"Failed to retrieve webpage, status code: {response.status_code}")


def get_player_age(player_name):
    parsed_player = player_name.replace(" ", "_")
    url = f'https://en.wikipedia.org/wiki/{parsed_player}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        dob_row = soup.find('th', text='Date of birth').parent if soup.find(
            'th', text='Date of birth') else None
        if dob_row:
            age = dob_row.find('span', class_='ForceAgeToShow').text.strip()
            age = ''.join(filter(str.isdigit, age))
            return age
        else:
            return "Age information not found."
    else:
        return f"Failed to retrieve webpage, status code: {response.status_code}"

def get_player_position(player_name):
    parsed_player = player_name.replace(" ", "_")
    url = f'https://en.wikipedia.org/wiki/{parsed_player}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        position_row = soup.find('th', text='Position(s)').parent if soup.find(
            'th', text='Position(s)') else None
        if position_row:
            position = position_row.find('td', class_='infobox-data').text.strip()
            return position
        else:
            print("Position information not found.")
    else:
        print(
            f"Failed to retrieve webpage, status code: {response.status_code}")