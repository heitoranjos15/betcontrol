from db import mongo_cli


def insert_nfl_team(teams_list):
    mongo_cli.teams.insert_many(teams_list)


def insert_nfl_player(players_list):
    mongo_cli.player.insert_many(players_list)


def get_nfl_teams(season_year):
    return mongo_cli.teams.find({"season": season_year, "sport": "American Football", "league": "NFL"})
