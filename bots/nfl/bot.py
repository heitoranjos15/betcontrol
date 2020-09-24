from bots.get_page_data import page_soup, render_JS


class NFLBot:

    def __init__(self, season_year):
        self.season_year = season_year
        self.host = "https://www.pro-football-reference.com"

    def get_teams(self):
        team_page = f"{self.host}/years/{self.season_year}"
        soup = page_soup(team_page)
        conferences = soup.find_all('table', class_='sortable stats_table')
        teams = list()
        for conf in conferences:
            conference_name = conf.get('id')
            teams_tr = conf.select('tbody tr')
            division = ''
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
                        'season': self.season_year,
                        'abreviation': team.get('href').split('/')[2],
                        'name': team.get_text()
                    })
        return teams

    def get_players_from_teams(self, teams):
        players = list()
        for t in teams:
            team_abreviation = t.get('abreviation')
            team_page = f"{self.host}/teams/{team_abreviation}/{self.season_year}_roster.htm"
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
                        'college': player_data[7].text.split(','),
                        'birth': player_data[8].text
                    })
        return players

    def get_games_stats(self, week):
        games_stats = list()
        week_games_page = f"{self.host}/years/{self.season_year}/week_{week}.htm"
        html_games_pages_render = render_JS(week_games_page)
        week_games_links = html_games_pages_render.find('td.gamelink > a')
        for game in week_games_links:
            game_page = game.attrs.get('href')
            game_url = f"{self.host}{game_page}"

            game_render = render_JS(game_url)

            teams_name = game_render.find('div.scorebox > div > div > strong > a')
            week_day = game_render.find('div.scorebox_meta > div', first=True).text

            score_board_table = game_render.find('table.linescore > tbody > tr')
            score_board_data = self._get_score_board_data(score_board_table)

            teams_stats_table = [
                game_render.xpath('//td[@data-stat="vis_stat"]'),
                game_render.xpath('//td[@data-stat="home_stat"]')
            ]
            teams_stats = self._get_teams_stats(teams_stats_table)

            players_offensive_table = game_render.find('table#player_offense > tbody > tr')
            players_offensive_stats = self._get_players_offensive_stats(players_offensive_table)

            games_stats.append({
                'week': week,
                'week_day': week_day,
                'season': self.season_year,
                'home_team': teams_name[1],
                'away_team': teams_name[0],
                'score_board': score_board_data,
                'teams_stats': teams_stats,
                'player_offensive_stats': players_offensive_stats
            })
        return games_stats

    def _get_score_board_data(self, score_board_table):
        score_data_teams = list()
        for team_scores in score_board_table:
            scores_columns = team_scores.find('td')
            score_data_teams.append({
                'first_quarter': scores_columns[2].text,
                'second_quarter': scores_columns[3].text,
                'third_quarter': scores_columns[4].text,
                'fourth_quarter': scores_columns[5].text,
                'final': scores_columns[6].text
            })
        return score_data_teams

    def _get_teams_stats(self, teams_table):
        stats_data_teams = list()
        for stats in teams_table:
            stats_data_teams.append({
                'first_downs': stats[0].text,
                'rush': stats[1].text.split('-'),
                'pass': stats[2].text.split('-'),
                'sacks': stats[3].text.split('-'),
                'fumbles': stats[6].text.split('-'),
                'turnovers': stats[7].text,
                'penalties': stats[8].text.split('-'),
                'third_down_conversion': stats[9].text.split('-'),
                'fourth_down_conversion': stats[10].text.split('-'),
                'possession': stats[11].text
            })
        return stats_data_teams

    def _get_players_offensive_stats(self, players_table):
        stats_players = list()
        for stats in players_table:
            name = stats.find('th > a', first=True)
            if name:
                columns_stats = stats.find('td')

                stats = self._build_stats_player(columns_stats)
                stats.update({'name': name.text})

                stats_players.append(stats)

        return stats_players

    def _build_stats_player(self, columns_stats):
        stats_dict = dict()
        if int(columns_stats[2].text):
            stats_dict.update({
                'passing': {
                    'completions': columns_stats[1].text,
                    'attempts': columns_stats[2].text,
                    'yards': columns_stats[3].text,
                    'td': columns_stats[4].text,
                    'int': columns_stats[5].text,
                    'sacked': columns_stats[6].text,
                    'rating': columns_stats[9].text
                }
            })
        if int(columns_stats[10].text):
            stats_dict.update({
                'rushing': {
                    'attempts': columns_stats[10].text,
                    'yards': columns_stats[11].text,
                    'td': columns_stats[12].text,
                    'fumble': columns_stats[19].text,
                    'fumble_lost': columns_stats[20].text,
                }
            })
        if int(columns_stats[14].text):
            stats_dict.update({
                'receiving': {
                    'targets': columns_stats[14].text,
                    'received': columns_stats[15].text,
                    'yards': columns_stats[16].text,
                    'td': columns_stats[17].text
                }
            })
        return stats_dict
