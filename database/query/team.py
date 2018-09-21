from database.query.common import Common


class Team:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def get_team_form(self, format, team_name):
        json_matches = []
        # Win - Loss like (W L L W W W L L). Get opposite team name as well.
        team_id = self.get_team_id(team_name)
        sql = """SELECT outcome, teams, winning_team_id FROM match 
                WHERE %s = ANY(teams) and format = %s ORDER BY date desc limit %s"""
        self.cursor.execute(sql, (team_id, format, 20))
        query_results = Common.extract_query_results(self.cursor)
        for match in query_results:
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

    def team_match_scores(self, team_name, format, num_of_matches):
        pass

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

    def get_team_id(self, team_name):
        sql = """SELECT id FROM team WHERE name = %s"""
        self.cursor.execute(sql, (team_name,))
        query_results = Common.extract_query_results(self.cursor)
        return query_results[0]['id']

    def __get_team_short_name_from_id(self, team_id):
        sql = """SELECT short_name FROM team WHERE id = %s"""
        self.cursor.execute(sql, (team_id,))
        query_results = Common.extract_query_results(self.cursor)
        return query_results[0]['short_name']
