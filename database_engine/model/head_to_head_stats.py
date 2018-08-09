class HeadToHeadStats:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, bowler_id, batsman_id, match_id, runs, balls, wickets):
        sql = """INSERT INTO head_to_head_stats VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sql, (bowler_id, batsman_id, balls, runs, wickets, match_id))
