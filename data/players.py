# players.py
from understatapi import UnderstatClient
understat = UnderstatClient()


def get_player_shot_data(player_id):
    return understat.player(player=str(player_id)).get_shot_data()


def league_player_data(league, year):
    return understat.league(league=str(league)).get_player_data(season=str(year))
