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


def transform_team_name(team_name):
    return team_name.replace(' ', '_')


def get_upcoming_match(df):
    upcoming_matches = df[df['isResult'] == False]
    if not upcoming_matches.empty:
        return (upcoming_matches.iloc[0].datetime,
                get_stadium_location(upcoming_matches.iloc[0].h)
        )
    else:
        return "No upcoming matches found"


def get_stadium_location(home_team):
    team_stadiums = {
        "Arsenal": "Emirates Stadium, London, UK",
        "Aston Villa": "Villa Park, Birmingham, UK",
        "Bournemouth": "Vitality Stadium, Bournemouth, UK",
        "Brentford": "Brentford Community Stadium, Brentford, UK",
        "Brighton": "Falmer Stadium, Brighton, UK",
        "Chelsea": "Stamford Bridge, London, UK",
        "Crystal Palace": "Selhurst Park, London, UK",
        "Everton": "Goodison Park, Liverpool, UK",
        "Fulham": "Craven Cottage, London, UK",
        "Liverpool": "Anfield, Liverpool, UK",
        "Manchester City": "Etihad Stadium, Manchester, UK",
        "Manchester United": "Old Trafford, Manchester, UK",
        "Newcastle United": "St James' Park, Newcastle, UK",
        "Nottingham Forest": "City Ground, Nottingham, UK",
        "Tottenham": "Tottenham Hotspur Stadium, London, UK",
        "West Ham": "London Stadium, London, UK",
        "Wolverhampton Wanderers": "Molineux Stadium, Wolverhampton, UK",
        "Leicester City": "King Power Stadium, Leicester, UK",
        "Ipswich Town": "Portman Road Stadium, Ipswich, UK",
        "Southampton": "St Mary's Stadium, Southampton, UK"
    }
    return team_stadiums[home_team['title']]
