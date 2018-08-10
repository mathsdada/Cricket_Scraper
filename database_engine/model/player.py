class Player:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, name, role, batting_style, bowling_style):
        sql = """INSERT INTO player VALUES(%s, %s, %s, %s, %s)"""
        if not self.__check_player_id(id):
            self.cursor.execute(sql, (id, name, role, batting_style, bowling_style))
            return True
        return False

    def __check_player_id(self, id):
        sql = """SELECT * FROM player WHERE player.id = %s"""
        self.cursor.execute(sql, (id,))
        if self.cursor.fetchone() is None:
            return False
        return True
