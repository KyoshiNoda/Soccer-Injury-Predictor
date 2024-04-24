from understatapi import UnderstatClient
understat = UnderstatClient()

def get_player_shot_data(id):
    player_id = league_player_data[id]["id"]
    return understat.player(player=player_id).get_shot_data()

def league_player_data(leauge, year):
    return understat.league(league=leauge).get_player_data(season=year)

