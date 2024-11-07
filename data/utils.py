import os


def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data_str = file.read()
    return data_str


def add_missing_player(player_name, message):
    file_path = "data/missing_players.txt"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            missing_players = file.readlines()

        if any(player_name in line for line in missing_players):
            return
    with open(file_path, "a") as file:
        file.write(f"{player_name} - {message}\n")
    print(f"{player_name} added to missing_players.txt")
