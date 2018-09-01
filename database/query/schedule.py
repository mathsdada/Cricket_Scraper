from database.query.common import Common


class Schedule:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def get_schedule(self):
        schedule = []
        for series in self.__get_series_list():
            series_info = {'series_title': series['title'], 'series_data': []}
            for match in self.__get_matches_list_of_series(series['id']):
                series_info['series_data'].append(self.__process_match(match))
            schedule.append(series_info)
        return schedule

    def __get_series_list(self):
        sql = """select id, title, gender from schedule_series"""
        self.cursor.execute(sql)
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def __get_matches_list_of_series(self, series_id):
        sql = """select id as match_id, title as match_title, format as match_format, time as match_time,
                        venue as match_venue, teams as match_teams, gender as match_gender
                 from schedule_match
                 where series_id = %s"""
        self.cursor.execute(sql, (series_id, ))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def __get_squad(self, match_id, team):
        sql = """select squad from schedule_squad where match_id=%s and team=%s"""
        self.cursor.execute(sql, (match_id, team))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def __get_player_info(self, player_id):
        sql = """select name as player_name, role as player_role,
                        batting_style as player_batting_style, bowling_style as player_bowling_style,
                        gender as player_gender
                 from schedule_player where id = %s"""
        self.cursor.execute(sql, (player_id, ))
        query_results = Common.extract_query_results(self.cursor)
        return query_results[0]

    def __process_squad(self, squad):
        players = []
        for player_id in squad:
            players.append(self.__get_player_info(player_id))
        return players

    def __process_match(self, match):
        id = match['match_id']
        # remove id as client doesn't need this
        del match['match_id']
        # add team squad to each team
        teams = match['match_teams']
        match['match_teams'] = []
        for team in teams:
            team_squad = self.__get_squad(id, team)[0]
            match['match_teams'].append(
                {'team_name': team, 'team_squad': self.__process_squad(team_squad['squad'])})

        return match
