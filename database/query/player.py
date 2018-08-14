from database.query.common import Common


class Player:
    def __init__(self, db_cursor):
        self.cursor = db_cursor

    def batting_stats_overall(self, batsman_name, format, num_of_matches):
        # TODO In TEST stats, we should consider showing latest match second innings_scores as latest score
        sql = """select batting_stats.runs_scored, batting_stats.balls_played from batting_stats
                    join player on player.id = batting_stats.batsman_id
                    join match on match.id = batting_stats.match_id
                    where player.name = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (batsman_name, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def batting_stats_at_venue(self, batsman_name, venue, format, num_of_matches):
        # TODO In TEST stats, we should consider showing latest match second innings_scores as latest score
        sql = """select batting_stats.runs_scored, batting_stats.balls_played from batting_stats
                    join player on player.id = batting_stats.batsman_id
                    join match on match.id = batting_stats.match_id
                    where player.name = %s and match.venue = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (batsman_name, venue, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def batting_stats_against_bowler(self, batsman_name, bowler_name, format, num_of_matches):
        sql = """select head_to_head_stats.runs, head_to_head_stats.balls, head_to_head_stats.wickets from head_to_head_stats
                    join player as batsman on batsman.id = head_to_head_stats.batsman_id
                    join player as bowler on bowler.id = head_to_head_stats.bowler_id
                    join match on match.id = head_to_head_stats.match_id
                    where batsman.name = %s and bowler.name = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (batsman_name, bowler_name, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def batting_stats_against_bowling_style(self, batsman_name, bowling_style, format, num_of_matches):
        sql = """select head_to_head_stats.runs, head_to_head_stats.balls, head_to_head_stats.wickets from head_to_head_stats
                    join player as batsman on batsman.id = head_to_head_stats.batsman_id
                    join player as bowler on bowler.id = head_to_head_stats.bowler_id
                    join match on match.id = head_to_head_stats.match_id
                    where batsman.name = %s and bowler.bowling_style = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (batsman_name, bowling_style, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def bowling_stats_overall(self, bowler_name, format, num_of_matches):
        # TODO In TEST stats, we should consider showing latest match second innings_scores as latest score
        sql = """select bowling_stats.wickets_taken, bowling_stats.runs_given, bowling_stats.overs_bowled, bowling_stats.economy from bowling_stats
                    join player on player.id = bowling_stats.bowler_id
                    join match on match.id = bowling_stats.match_id
                    where player.name = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (bowler_name, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def bowling_stats_at_venue(self, bowler_name, venue, format, num_of_matches):
        # TODO In TEST stats, we should consider showing latest match second innings_scores as latest score
        sql = """select bowling_stats.wickets_taken, bowling_stats.runs_given, bowling_stats.overs_bowled, bowling_stats.economy from bowling_stats
                    join player on player.id = bowling_stats.bowler_id
                    join match on match.id = bowling_stats.match_id
                    where player.name = %s and match.venue = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (bowler_name, venue, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def bowling_stats_against_batsman(self, bowler_name, batsman_name, format, num_of_matches):
        sql = """select head_to_head_stats.runs, head_to_head_stats.balls, head_to_head_stats.wickets from head_to_head_stats
                    join player as bowler on bowler.id = head_to_head_stats.bowler_id
                    join player as batsman on batsman.id = head_to_head_stats.batsman_id
                    join match on match.id = head_to_head_stats.match_id
                    where bowler.name = %s and batsman.name = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (bowler_name, batsman_name, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results

    def bowling_stats_against_batting_style(self, bowler_name, batting_style, format, num_of_matches):
        sql = """select head_to_head_stats.runs, head_to_head_stats.balls, head_to_head_stats.wickets from head_to_head_stats
                    join player as bowler on bowler.id = head_to_head_stats.bowler_id
                    join player as batsman on batsman.id = head_to_head_stats.batsman_id
                    join match on match.id = head_to_head_stats.match_id
                    where bowler.name = %s and batsman.batting_style = %s and match.format = %s
                    order by match.date desc limit %s"""
        self.cursor.execute(sql, (bowler_name, batting_style, format, num_of_matches))
        query_results = Common.extract_query_results(self.cursor)
        return query_results
