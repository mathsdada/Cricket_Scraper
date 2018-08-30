class Squad:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, match_id, team, squad):
        sql = """INSERT INTO schedule_squad VALUES(%s, %s, %s)"""
        self.cursor.execute(sql, (match_id, team, squad))

    def clear(self):
        sql = """DELETE FROM schedule_squad"""
        self.cursor.execute(sql)
