from bots import hosts
from db.teams import insert_nfl_team
from bots.get_page_data import page_soup


def get_nfl_teams(season_year):
    team_page = f"{hosts.get('NFL_HOST')}/years/{season_year}"
    soup = page_soup(team_page)
    conferences = soup.find_all('table', class_='sortable stats_table')
    teams = list()
    for conf in conferences:
        conference_name = conf.get('id')
        teams_tr = conf.select('tbody tr')
        division = 'East'
        for t in teams_tr:
            if t.get('class'):
                division = t.get_text().split(' ')[2]
            else:
                team = t.select('th a')[0]
                teams.append({
                    'sport': 'American Football',
                    'league': 'NFL',
                    'conference': conference_name,
                    'division': division,
                    'season': season_year,
                    'abreviation': team.get('href').split('/')[2],
                    'name': team.get_text()
                })
    insert_nfl_team(teams)
