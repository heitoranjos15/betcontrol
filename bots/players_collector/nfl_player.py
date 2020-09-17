from bots import hosts
from db.teams import get_nfl_teams, insert_nfl_player
from bots.get_page_data import render_JS


def get_nfl_players(season_year):
    teams = get_nfl_teams(season_year)
    players = list()
    for t in teams:
        team_abreviation = t.get('abreviation')
        team_page = f"{hosts.get('NFL_HOST')}/teams/{team_abreviation}/{season_year}_roster.htm"
        html_render = render_JS(team_page)
        player_list = html_render.find('table tbody tr')
        for p in player_list:
            player_data = p.find('td')
            if player_data:
                players.append({
                    'name': player_data[0].text,
                    'age': player_data[1].text,
                    'position': player_data[2].text,
                    'heigth': player_data[6].text,
                    'college': player_data[7].text,
                    'birth': player_data[8].text
                })
    insert_nfl_player(players)
