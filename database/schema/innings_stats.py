class InningsStats:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, match_id, innings_num, runs, wickets, overs, batting_team_id, bowling_team_id):
        sql = """INSERT INTO innings_stats VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (match_id, innings_num, runs, wickets, overs, batting_team_id, bowling_team_id))
