from database.query.common import Common


class Team:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def get_team_form(self, team_name, venue, format):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
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
        if team_id is None:
            return None
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
        if team_id is None:
            return None
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
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) and format = %s 
                                        ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played,
                                        (runs_scored >= 50) AS is_fifty FROM batting_stats
                                        JOIN matches ON matches.id = match_id WHERE team_id = %s),
                     fifty_batsmen AS (SELECT player.name as batsman, COUNT(innings_number) AS innings,
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
                          fifty_batsmen AS (SELECT player.name as batsman, COUNT(innings_number) AS innings,
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

    def get_most_100s(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id, date, teams FROM match WHERE %s = ANY(teams) and format = %s 
                                        ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played,
                                        (runs_scored >= 100) AS is_hundred FROM batting_stats
                                        JOIN matches ON matches.id = match_id WHERE team_id = %s),
                     century_batsmen AS (SELECT player.name as batsman, COUNT(innings_number) AS innings,
                                              SUM(runs_scored) AS runs, SUM(balls_played) AS balls,
                                              SUM(is_hundred::int) AS hundreds FROM batsmen
                                              JOIN player ON player.id = batsman_id WHERE player.name IN %s
                                              GROUP BY player.name ORDER BY hundreds DESC, runs DESC)
                SELECT * FROM century_batsmen WHERE hundreds != 0"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s 
                                      AND venue = %s ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played,
                                             (runs_scored >= 100) AS is_hundred FROM batting_stats
                                             JOIN matches ON matches.id = match_id WHERE team_id = %s),
                          century_batsmen AS (SELECT player.name as batsman, COUNT(innings_number) AS innings,
                                                   SUM(runs_scored) AS runs, SUM(balls_played) AS balls,
                                                   SUM(is_hundred::int) AS hundreds FROM batsmen
                                                   JOIN player ON player.id = batsman_id WHERE player.name IN %s
                                                   GROUP BY player.name ORDER BY hundreds DESC, runs DESC)
                     SELECT * FROM century_batsmen WHERE hundreds != 0"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_4s(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, num_fours FROM batting_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs, SUM(balls_played) AS balls, SUM(num_fours) AS fours FROM batsmen JOIN player ON player.id = batsman_id WHERE player.name IN %s GROUP BY player.name ORDER BY fours DESC, runs DESC"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, num_fours FROM batting_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs, SUM(balls_played) AS balls, SUM(num_fours) AS fours FROM batsmen JOIN player ON player.id = batsman_id WHERE player.name IN %s GROUP BY player.name ORDER BY fours DESC, runs DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_6s(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, num_sixes FROM batting_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs, SUM(balls_played) AS balls, SUM(num_sixes) AS sixes FROM batsmen JOIN player ON player.id = batsman_id WHERE player.name IN %s GROUP BY player.name ORDER BY sixes DESC, runs DESC"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, num_sixes FROM batting_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs, SUM(balls_played) AS balls, SUM(num_sixes) AS sixes FROM batsmen JOIN player ON player.id = batsman_id WHERE player.name IN %s GROUP BY player.name ORDER BY sixes DESC, runs DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_high_scores(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, num_fours FROM batting_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs, SUM(balls_played) AS balls, MAX(runs_scored) AS high_score FROM batsmen JOIN player ON player.id = batsman_id WHERE player.name IN %s GROUP BY player.name ORDER BY high_score DESC, runs DESC"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          batsmen AS (SELECT batsman_id, innings_number, runs_scored, balls_played, num_fours FROM batting_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name as batsman, COUNT(innings_number) AS innings, SUM(runs_scored) AS runs, SUM(balls_played) AS balls, MAX(runs_scored) AS high_score FROM batsmen JOIN player ON player.id = batsman_id WHERE player.name IN %s GROUP BY player.name ORDER BY high_score DESC, runs DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_wickets(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, innings_number, wickets_taken FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY wickets DESC"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, innings_number, wickets_taken FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY wickets DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_best_bowling_economy(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, innings_number, wickets_taken, economy FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s AND economy != 0)
                SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1)::text as economy FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY economy"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, innings_number, wickets_taken, economy FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s AND economy != 0)
                     SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1)::text as economy FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY economy"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_best_bowling_strike_rate(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, innings_number, wickets_taken, balls_bowled, economy FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s),
	                  players AS (SELECT player_id, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1) as economy, SUM(balls_bowled) as balls FROM bowlers WHERE wickets != 0)
                SELECT player.name as bowler, innings, wickets, economy, (balls/wickets) AS strike_rate FROM players JOIN player ON player.id = player_id WHERE player.name IN %s GROUP BY player.name ORDER BY strike_rate"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, innings_number, wickets_taken, balls_bowled, economy FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s),
	                       players AS (SELECT player_id, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1) as economy, SUM(balls_bowled) as balls FROM bowlers WHERE wickets != 0)
                     SELECT player.name as bowler, innings, wickets, economy, (balls/wickets) AS strike_rate FROM players JOIN player ON player.id = player_id WHERE player.name IN %s GROUP BY player.name ORDER BY strike_rate"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_4_plus_wickets(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, innings_number, wickets_taken, economy, (wickets_taken >= 4) AS is_four_plus FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s),
	                 four_plus_bowlers AS (SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1)::text as economy, SUM(is_four_plus::int) as four_plus FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY four_plus DESC)
                SELECT * FROM four_plus_bowlers WHERE four_plus != 0"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, innings_number, wickets_taken, economy, (wickets_taken >= 4) AS is_four_plus FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s),
	                      four_plus_bowlers AS (SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1)::text as economy, SUM(is_four_plus::int) as four_plus FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY four_plus DESC)
                     SELECT * FROM four_plus_bowlers WHERE four_plus != 0"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_5_plus_wickets(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, innings_number, wickets_taken, economy, (wickets_taken >= 5) AS is_five_plus FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s),
	                 five_plus_bowlers AS (SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1)::text as economy, SUM(is_five_plus::int) as five_plus FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY five_plus DESC)
                SELECT * FROM five_plus_bowlers WHERE five_plus != 0	 """
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, innings_number, wickets_taken, economy, (wickets_taken >= 5) AS is_five_plus FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s),
	                      five_plus_bowlers AS (SELECT player.name as bowler, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , ROUND(AVG(economy),1)::text as economy, SUM(is_five_plus::int) as five_plus FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY five_plus DESC)
                      SELECT * FROM five_plus_bowlers WHERE five_plus != 0"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_maidens(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, innings_number, wickets_taken, maidens FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , SUM(maidens) AS maidens FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY maidens DESC"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, innings_number, wickets_taken, maidens FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name, COUNT(innings_number) AS innings, SUM(wickets_taken) AS wickets , SUM(maidens) AS maidens FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s GROUP BY player.name ORDER BY maidens DESC"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_most_runs_conceded_in_innings(self, team_name, venue, format, squad):
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, wickets_taken, overs_bowled, runs_given FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as bowler, wickets_taken AS wickets, overs_bowled::text AS overs, runs_given AS runs FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s ORDER BY runs DESC, overs_bowled LIMIT 20"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, wickets_taken, overs_bowled, runs_given FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                      SELECT player.name as bowler, wickets_taken AS wickets, overs_bowled::text AS overs, runs_given AS runs FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s ORDER BY runs DESC, overs_bowled LIMIT 20"""
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_best_bowling_figure_in_innings(self, team_name, venue, format, squad):
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     bowlers AS (SELECT bowler_id, wickets_taken, overs_bowled, runs_given FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                SELECT player.name as bowler, wickets_taken AS wickets, runs_given AS runs, overs_bowled::text AS overs FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s ORDER BY wickets DESC, runs LIMIT 20"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                          bowlers AS (SELECT bowler_id, wickets_taken, overs_bowled, runs_given FROM bowling_stats JOIN matches ON matches.id = match_id WHERE team_id = %s)
                     SELECT player.name as bowler, wickets_taken AS wickets, runs_given AS runs, overs_bowled::text AS overs FROM bowlers JOIN player ON player.id = bowler_id WHERE player.name IN %s ORDER BY wickets DESC, runs LIMIT 20"""
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        self.cursor.execute(sql, (team_id, format, team_id, tuple(squad)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, team_id, tuple(squad)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_runs_against_bowling_styles(self, team_name, venue, format, batsmen, bowling_styles):
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20)
                SELECT bowler.bowling_style, COUNT(DISTINCT matches.id) as matches, SUM(balls) AS balls, SUM(runs) AS runs, SUM(wickets) AS wickets, (100*SUM(runs)/SUM(balls)) AS strike_rate FROM head_to_head_stats JOIN matches ON matches.id = match_id
                       JOIN player AS batsman ON batsman.id = batsman_id
                       JOIN player AS bowler ON bowler.id = bowler_id
                       WHERE batsman.name IN %s AND bowler.bowling_style IN %s
                       GROUP BY bowler.bowling_style
                       ORDER BY wickets DESC, strike_rate"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20)
                        SELECT bowler.bowling_style, COUNT(DISTINCT matches.id) as matches, SUM(balls) AS balls, SUM(runs) AS runs, SUM(wickets) AS wickets, (100*SUM(runs)/SUM(balls)) AS strike_rate FROM head_to_head_stats JOIN matches ON matches.id = match_id
                               JOIN player AS batsman ON batsman.id = batsman_id
                               JOIN player AS bowler ON bowler.id = bowler_id
                               WHERE batsman.name IN %s AND bowler.bowling_style IN %s
                               GROUP BY bowler.bowling_style
                               ORDER BY wickets DESC, strike_rate"""
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        self.cursor.execute(sql, (team_id, format, tuple(batsmen), tuple(bowling_styles)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, format, venue, tuple(batsmen), tuple(bowling_styles)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_runs_against_bowlers(self, team_name, venue, format, batsmen, opp_team, bowlers):
        sql = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20)
                SELECT bowler.name as bowler, COUNT(DISTINCT matches.id) as matches, SUM(balls) AS balls, SUM(runs) AS runs, SUM(wickets) AS wickets, (100*SUM(runs)/SUM(balls)) AS strike_rate FROM head_to_head_stats JOIN matches ON matches.id = match_id
                       JOIN player AS batsman ON batsman.id = batsman_id
                       JOIN player AS bowler ON bowler.id = bowler_id
                       WHERE batsman.name IN %s AND bowler.name IN %s
                       GROUP BY bowler.name
                       ORDER BY wickets DESC, strike_rate"""
        sql_venue = """WITH matches AS (SELECT id FROM match WHERE %s = ANY(teams) AND %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20)
                        SELECT bowler.name as bowler, COUNT(DISTINCT matches.id) AS matches, SUM(balls) AS balls, SUM(runs) AS runs, SUM(wickets) AS wickets, (100*SUM(runs)/SUM(balls)) AS strike_rate FROM head_to_head_stats JOIN matches ON matches.id = match_id
                               JOIN player AS batsman ON batsman.id = batsman_id
                               JOIN player AS bowler ON bowler.id = bowler_id
                               WHERE batsman.name IN %s AND bowler.name IN %s
                               GROUP BY bowler.name
                               ORDER BY wickets DESC, strike_rate"""
        team_id = self.__get_team_id(team_name)
        opp_team_id = self.__get_team_id(opp_team)
        if team_id is None or opp_team_id is None:
            return None
        self.cursor.execute(sql, (team_id, opp_team_id, format, tuple(batsmen), tuple(bowlers)))
        results = Common.extract_query_results(self.cursor)
        self.cursor.execute(sql_venue, (team_id, opp_team_id, format, venue, tuple(batsmen), tuple(bowlers)))
        results_venue = Common.extract_query_results(self.cursor)
        return {"overall": results, "atVenue": results_venue}

    def get_recent_match_scores(self, team_name, format, venue):
        sql = """WITH matches AS (SELECT id, date FROM match WHERE %s = ANY(teams) AND format = %s ORDER BY date DESC LIMIT 20),
                     matches_scores AS (SELECT innings_stats.match_id, matches.date, innings_stats.innings_number, team.name || '@' || runs || '-' || wickets || ' (' || overs || ')' AS score FROM innings_stats JOIN matches on matches.id = innings_stats.match_id JOIN team on team.id = innings_stats.batting_team_id ORDER BY date DESC, innings_number)
                SELECT matches_scores.date::text AS match_date, string_agg(matches_scores.score, ', ') AS match_score FROM matches_scores GROUP BY matches_scores.date ORDER BY matches_scores.date DESC """
        sql_venue = """WITH matches AS (SELECT id, date FROM match WHERE %s = ANY(teams) AND format = %s AND venue = %s ORDER BY date DESC LIMIT 20),
                         matches_scores AS (SELECT innings_stats.match_id, matches.date, innings_stats.innings_number, team.name || '@' || runs || '-' || wickets || ' (' || overs || ')' AS score FROM innings_stats JOIN matches on matches.id = innings_stats.match_id JOIN team on team.id = innings_stats.batting_team_id ORDER BY date DESC, innings_number)
                     SELECT matches_scores.date::text AS match_date, string_agg(matches_scores.score, ', ') AS match_score FROM matches_scores GROUP BY matches_scores.date ORDER BY matches_scores.date DESC """
        team_id = self.__get_team_id(team_name)
        if team_id is None:
            return None
        self.cursor.execute(sql, (team_id, format))
        results = self.__process_match_scores(Common.extract_query_results(self.cursor))
        self.cursor.execute(sql_venue, (team_id, format, venue))
        results_venue = self.__process_match_scores(Common.extract_query_results(self.cursor))
        return {"overall": results, 'atVenue': results_venue}

    def __process_match_scores(self, matches_scores):
        for match_score in matches_scores:
            match_innings_scores = match_score['match_score'].split(', ')
            processed_match_scores = []
            for match_innings_score in match_innings_scores:
                innings_score = match_innings_score.split('@')
                processed_match_scores.append({'batting_team': innings_score[0], 'innings_score': innings_score[1]})
            match_score['match_score'] = processed_match_scores
            match_score['match_outcome'] = "Yet to be Added. Need to make changes in DB"
        return matches_scores

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
        if len(query_results) != 0:
            return query_results[0]['id']
        return None

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
