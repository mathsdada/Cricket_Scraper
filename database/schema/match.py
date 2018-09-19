class Match:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, title, date, format, venue, outcome, series_id, gender, playing_teams, winning_team_id):
        sql = """INSERT INTO match VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (
            id, title, format, venue, date, outcome, series_id, gender, playing_teams, winning_team_id))

    def check_match_id(self, id):
        sql = """SELECT * FROM match WHERE match.id = %s"""
        self.cursor.execute(sql, (id,))
        if self.cursor.rowcount > 0:
            return True
        return False
