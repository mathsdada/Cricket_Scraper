from database.query.common import Common


class Team:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def get_team_form(self, team_name, venue, format):
        team_id = self.__get_team_id(team_name)
        matches = self.__get_team_matches_list(team_id, format)
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
        return {"overall": json_matches, "atVenue": json_matches}

    def get_batting_most_runs(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        sql = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) AND format = %s
                                 ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, matches.date,
                                 matches.teams FROM batting_stats 
                                 JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs,
                       SUM(balls_played) AS balls FROM batsmen
                JOIN player ON player.id = batsman_id WHERE player.name IN %s
                GROUP BY player.name ORDER BY runs DESC"""
        sql_venue = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) AND format = %s
                                      AND venue = %s
                                      ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, matches.date,
                                      matches.teams FROM batting_stats 
                                      JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs,
                            SUM(balls_played) AS balls FROM batsmen
                     JOIN player ON player.id = batsman_id WHERE player.name IN %s
                     GROUP BY player.name ORDER BY runs DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_best_batting_strike_rate(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        sql = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) AND format = %s
                                 ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, matches.date,
                                 matches.teams FROM batting_stats 
                                 JOIN matches ON matches.id = match_id WHERE team_id = %s AND balls_played != 0)
                SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs,
                SUM(balls_played) AS balls, (SUM(runs_scored)*100/SUM(balls_played)) AS strike_rate FROM batsmen
                JOIN player ON player.id = batsman_id WHERE player.name IN %s
                GROUP BY player.name ORDER BY strike_rate DESC"""
        sql_venue = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) AND format = %s
                                      AND venue = %s ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, matches.date,
                                      matches.teams FROM batting_stats 
                                      JOIN matches ON matches.id = match_id WHERE team_id = %s AND balls_played != 0)
                      SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs,
                      SUM(balls_played) AS balls, (SUM(runs_scored)*100/SUM(balls_played)) AS strike_rate FROM batsmen
                      JOIN player ON player.id = batsman_id WHERE player.name IN %s
                      GROUP BY player.name ORDER BY strike_rate DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_50s(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        sql = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) and format = %s 
                                        ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played,
                                        (runs_scored >= 50) AS is_fifty FROM batting_stats
                                        JOIN matches ON matches.id = match_id WHERE team_id = %s),
                     fifty_batsmen AS (SELECT player.name, COUNT(innings_number) AS innings,
                                              SUM(runs_scored) AS runs, SUM(balls_played) AS balls,
                                              SUM(is_fifty::int) AS fifties FROM batsmen
                                              JOIN player ON player.id = batsman_id WHERE player.name IN %s
                                              GROUP BY player.name ORDER BY fifties DESC, runs DESC)
                SELECT * FROM fifty_batsmen WHERE fifties != 0"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s 
                                      AND venue = %s ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played,
                                             (runs_scored >= 50) AS is_fifty FROM batting_stats
                                             JOIN matches ON matches.id = match_id WHERE team_id = %s),
                          fifty_batsmen AS (SELECT player.name, COUNT(innings_number) AS innings,
                                                   SUM(runs_scored) AS runs, SUM(balls_played) AS balls,
                                                   SUM(is_fifty::int) AS fifties FROM batsmen
                                                   JOIN player ON player.id = batsman_id WHERE player.name IN %s
                                                   GROUP BY player.name ORDER BY fifties DESC, runs DESC)
                     SELECT * FROM fifty_batsmen WHERE fifties != 0"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

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

    def get_team_stats(self, format, team_name):
        # team_id = self.__get_team_id(team_name)
        # matches = self.__get_team_matches_list(team_id, format)
        # team_stats = {'form': self.__get_team_form(team_id, matches),
        #               'recent_matches': self.__get_recent_match_scores(matches)
        #               }
        return None
