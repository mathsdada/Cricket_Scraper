class BowlingStats:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, bowler_id, match_id, innings_num, wickets_taken, overs_bowled, runs_given, economy, playing_team):
        sql = """INSERT INTO bowling_stats VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (
            bowler_id, match_id, innings_num, wickets_taken, overs_bowled, runs_given, economy, playing_team))
