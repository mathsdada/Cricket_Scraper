class Player:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, name, role, batting_style, bowling_style, gender):
        sql = """INSERT INTO schedule_player VALUES(%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (id, name, role, batting_style, bowling_style, gender))

    def clear(self):
        sql = """DELETE FROM schedule_player"""
        self.cursor.execute(sql)
