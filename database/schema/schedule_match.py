class Match:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, title, format, time, venue, teams, series_id, gender):
        sql = """INSERT INTO schedule_match VALUES(%s, %s, %s, %s, %s, ARRAY[%s, %s], %s, %s)"""
        self.cursor.execute(sql, (
                id, title, format, time, venue, teams[0], teams[1], series_id, gender))

    def clear(self):
        sql = """DELETE FROM schedule_match"""
        self.cursor.execute(sql)
