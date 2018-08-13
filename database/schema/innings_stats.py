class InningsStats:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, match_id, innings_num, batting_team, bowling_team, runs, wickets, overs):
        sql = """INSERT INTO innings_stats VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (match_id, innings_num, batting_team, bowling_team, runs, wickets, overs))
