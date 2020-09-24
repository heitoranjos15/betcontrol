from db import mongo_cli


def insert_nfl_teams(teams_list):
    mongo_cli.team.insert_many(teams_list)


def insert_nfl_players(players_list):
    mongo_cli.player.insert_many(players_list)


def get_nfl_teams(season_year):
    return mongo_cli.team.find({"season": season_year, "sport": "American Football", "league": "NFL"})
