class Player:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, name, role, batting_style, bowling_style, gender):
        sql = """INSERT INTO schedule_player VALUES(%s, %s, %s, %s, %s, %s)"""
        if not self.__check_player_id(id):
            self.cursor.execute(sql, (id, name, role, batting_style, bowling_style, gender))

    def clear(self):
        sql = """DELETE FROM schedule_player"""
        self.cursor.execute(sql)

    def __check_player_id(self, id):
        sql = """SELECT * FROM schedule_player WHERE id = %s"""
        self.cursor.execute(sql, (id,))
        if self.cursor.rowcount > 0:
            return True
        return False
