import os
import csv


def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data_str = file.read()
    return data_str


def add_missing_player(player_name, message):
    file_path = "data/missing_players.txt"
    with open(file_path, "a") as file:
        file.write(f"{player_name} - {message}\n")
    print(f"{player_name} added to missing_players.txt")


def add_player_CSV(player_data=None, **kwargs):
    file_path = "data/prem_players.csv"

    # Check if the file exists to determine if headers need to be written
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Add headers if the file is new
        if not file_exists:
            writer.writerow(["player_name", "age", "height",
                            "weight", "position", "team"])

        # Write the player's data
        if player_data:
            writer.writerow([
                player_data.get("player_name", "NA"),
                player_data.get("age", "NA"),
                player_data.get("height", "NA"),
                player_data.get("weight", "NA"),
                player_data.get("position", "NA"),
                player_data.get("team", "NA")
            ])
        else:
            writer.writerow([
                kwargs.get("player_name", "NA"),
                kwargs.get("age", "NA"),
                kwargs.get("height", "NA"),
                kwargs.get("weight", "NA"),
                kwargs.get("position", "NA"),
                kwargs.get("team", "NA")
            ])

    print(f"Added {player_data or kwargs} to CSV.")
