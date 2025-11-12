import re


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


def is_snowflake_player(player_name):
    players = {
        'Harry Clarke': ['Kyle Jameson 3', 'Harry Clarke (footballer, born 2001)'],
        'Enzo Fernández': ['Santiago Sosa 3', 'Enzo_Fernández'],
        'Patson Daka': [],
        'Omari Hutchinson': [],
        'Ethan Nwaneri': [],
        'Mateus Fernandes': [],
        'Bilal El Khannouss': [],
        'Justin Devenny': [],
        'Matt O\'Riley': [],
        'Callum Wilson': [],
        'Danny Ward': [],
        'Fraser Forster': [],
        'Luke Shaw': [],
        'Tyrone Mings': [],
        'Kepa': [],
        'Estupiñán': [],
        'Martin Dubravka': [],
        'Ryan Sessegnon': [],
        'Robin Olsen': [],
        'Max Aarons': [],
        'Armando Broja': [],
        'Tommy Doyle': [],
        'Luke Thomas': [],
        'Dara O\'Shea': [],
        'Stefan Ortega Moreno': [],
        'Filip Jorgensen': [],
        'Nathan Broadhead': [],
        'Paris Maghoma': [],
        'Nathan Patterson': [],
        'Leny Yoro': [],
        'James Hill': [],
        'Tyrell Malacia': [],
        'Antony': [],
        'Jake O\'Brien': [],
        'Joshua King': [],
        'Yunus Konak': [],
        'Joe Lumley': [],
        'Nathan Wood': [],
        'Lucas Bergvall': [],
        'Roman Dixon': [],
        'George Edmundson': [],
        'Jack Clarke': [],
        'André': [],
        'Luis Guilherme': [],
        'Asher Agbinone': [],
        'Ross Stewart': [],
        'Morato': [],
        'Carlos Forbs': [],
        'Vítezslav Jaros': [],
        'Alfie Pond': [],
        'Will Lankshear': [],
        'Caleb Kporha': [],
        'Ryan Manning': [],
        'Jahmai Simpson-Pusey': [],
        'Thiago': [],
        'Ronnie Edwards': []
    }

    if player_name in players:
        return players.get(player_name)
    else:
        return None


def get_missing_players(df, textfile):
    missing_players = []

    # Read the text file line by line
    with open(textfile, 'r') as file:
        for line in file:
            # Extract the first and last name from the line format
            parts = line.split(" - ")
            if len(parts) > 0:
                full_name = parts[0].strip()  # First and last name combined

                # Check if the player exists in the DataFrame
                if not df['player_name'].str.contains(full_name, case=False, na=False).any():
                    missing_players.append(full_name)

    return missing_players


def extract_formatted_height(height_str):
    ft_in_match = re.search(r'(\d+)\s*ft\s*(\d+)?\s*in', height_str)

    if ft_in_match:
        feet = int(ft_in_match.group(1))
        inches = int(ft_in_match.group(2)) if ft_in_match.group(2) else 0
        return f"{feet} ft {inches} in"

    meters_match = re.search(r'(\d+\.\d+)\s*m', height_str)
    if meters_match:
        meters = float(meters_match.group(1))
        total_inches = round(meters * 39.3701)
        feet = total_inches // 12
        inches = total_inches % 12
        return f"{feet} ft {inches} in"

    raise ValueError(f"Invalid height format: {height_str}")
