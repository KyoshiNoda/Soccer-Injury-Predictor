def parse_player_info(data):
    return [
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

def parse_past_teams(data):
    past_teams_data = []
    for player in data:
        player_id = player[0]
        player_name = player[1].strip() if player[1] else ''
        if player[10]:
            for team in player[10]:
                past_teams_data.append([player_id, player_name] + list(team))
    return past_teams_data


def parse_injury_history(data):
    injuries_data = []
    for player in data:
        player_id = player[0]
        player_name = player[1].strip() if player[1] else ''
        if player[11]:
            for injury in player[11]:
                injuries_data.append([player_id, player_name] + list(injury))
    return injuries_data
