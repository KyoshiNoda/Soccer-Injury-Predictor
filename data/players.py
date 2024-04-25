import pandas as pd
from understatapi import UnderstatClient
understat = UnderstatClient()


def get_player_shot_data(player_id):
    player_data = understat.player(player=str(player_id)).get_shot_data()
    return pd.DataFrame(player_data)


def league_player_data(league, year):
    league_data = understat.league(league=str(
        league)).get_player_data(season=str(year))
    return pd.DataFrame(league_data)
