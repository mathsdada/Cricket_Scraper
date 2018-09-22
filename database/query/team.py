from database.query.common import Common


class Team:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def get_team_stats(self, format, team_name):
        team_id = self.__get_team_id(team_name)
        matches = self.__get_team_matches_list(team_id, format)
        team_stats = {'form': self.__get_team_form(team_id, matches),
                      'recent_matches': self.__get_recent_match_scores(matches)
                      }
        return team_stats

    def __get_team_form(self, team_id, matches):
        json_matches = []
        # Win - Loss like (W L L W W W L L). Get opposite team name as well.
        for match in matches:
            team_ids = match['teams']
            outcome = match['outcome']
            winning_team_id = match['winning_team_id']

            # get Opposite Team
            if team_ids[0] == team_id:
                opp_team_id = team_ids[1]
            else:
                opp_team_id = team_ids[0]
            opp_team_short_name = self.__get_team_short_name_from_id(opp_team_id)

            # get whether Team won the match or lost.
            if outcome == 'WIN' and team_id != winning_team_id:
                outcome = "LOST"
            json_matches.append(
                {'outcome': outcome, 'opp_team': opp_team_short_name})
        return json_matches

    def __get_recent_match_scores(self, matches):
        match_score_cards_list = []
        sql = """SELECT short_name, text (runs) as runs, text(wickets) as wickets, text(overs) as overs ,
                innings_number
                FROM innings_stats
                JOIN team on id = batting_team_id
                WHERE match_id = %s ORDER BY innings_number"""
        for match in matches:
            self.cursor.execute(sql, (match['id'],))
            match_score_cards = Common.extract_query_results(self.cursor)
            match_score_cards_list.append(match_score_cards)
        return match_score_cards_list

    def most_runs(self, team_squad, format, num_of_matches):
        # batsman_name num_matches runs balls highest_score
        # Array of above
        pass

    def most_wickets(self, team_squad, format, num_of_matches):
        # bowler_name num_matches wickets runs
        # Array of above
        pass

    def best_economy(self, team_squad, format, num_of_matches):
        # bowler_name num_matches overs runs wickets economy
        # Array of above
        pass

    def record_against_opposite_team(self, team_name, opposite_team_name, format, num_of_matches):
        pass

    def team_form_at_venue(self, team_name, venue, format, num_of_matches):
        pass

    def team_match_scores_at_venue(self, team_name, venue, format, num_of_matches):
        pass

    def most_runs_at_venue(self, team_squad, venue, format, num_of_matches):
        # batsman_name num_matches runs balls highest_score
        # Array of above
        pass

    def most_wickets_at_venue(self, team_squad, venue, format, num_of_matches):
        # bowler_name num_matches wickets runs
        # Array of above
        pass

    def best_economy_at_venue(self, team_squad, venue, format, num_of_matches):
        # bowler_name num_matches overs runs wickets economy
        # Array of above
        pass

    def record_against_opposite_team_at_venue(self, team_name, opposite_team_name, venue, format, num_of_matches):
        pass

    def __get_team_id(self, team_name):
        sql = """SELECT id FROM team WHERE name = %s"""
        self.cursor.execute(sql, (team_name,))
        query_results = Common.extract_query_results(self.cursor)
        return query_results[0]['id']

    def __get_team_short_name_from_id(self, team_id):
        sql = """SELECT short_name FROM team WHERE id = %s"""
        self.cursor.execute(sql, (team_id,))
        query_results = Common.extract_query_results(self.cursor)
        return query_results[0]['short_name']

    def __get_team_matches_list(self, team_id, format):
        sql = """SELECT * FROM match 
                WHERE outcome != 'NO RESULT' and %s = ANY(teams) and format = %s 
                ORDER BY date desc LIMIT %s"""
        self.cursor.execute(sql, (team_id, format, 20))
        return Common.extract_query_results(self.cursor)
