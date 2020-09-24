from datetime import datetime
from bots.nfl.bot import NFLBot
from db import nfl as nfl_db


def _get_NFL_bot(season_year):
    if not season_year:
        return NFLBot(datetime.now().strftime('%Y'))
    return NFLBot(season_year)


def nfl_save_teams(season_year=''):
    bot = _get_NFL_bot(season_year)
    season_teams = bot.get_teams()
    nfl_db.insert_nfl_teams(season_teams)


def nfl_save_players(season_year=''):
    bot = _get_NFL_bot(season_year)
    teams_season = nfl_db.get_nfl_teams(season_year)
    new_players = bot.get_players_from_teams(teams_season)
    nfl_db.insert_nfl_players(new_players)


def nfl_save_games_stats(season_year=''):
    bot = _get_NFL_bot(season_year)
    bot.get_games_stats("1")
