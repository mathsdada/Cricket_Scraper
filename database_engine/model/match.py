class Match:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, title, date, format, venue, playing_teams, winning_team, outcome, series_id):
        sql = """INSERT INTO match VALUES(%s, %s, %s, %s, ARRAY[%s, %s], %s, %s, %s, %s)"""
        self.cursor.execute(sql, (
            id, title, format, venue, playing_teams[0], playing_teams[1], winning_team, date, outcome, series_id))
