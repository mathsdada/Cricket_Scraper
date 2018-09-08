class Team:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, name, short_name, squad):
        sql = """INSERT INTO schedule_team  (name, short_name, squad) VALUES(%s, %s, %s)
                RETURNING id"""
        self.cursor.execute(sql, (name, short_name, squad))
        # Return Team ID
        return self.cursor.fetchone()[0]

    def clear(self):
        sql = """DELETE FROM schedule_team"""
        self.cursor.execute(sql)
