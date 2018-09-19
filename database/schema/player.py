from database.query.common import Common


class Player:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, name, role, batting_style, bowling_style, gender):
        sql = """INSERT INTO player VALUES(%s, %s, %s, %s, %s, %s)"""

        player_data = self.__get_player_data(id)
        if player_data is None:
            self.cursor.execute(sql, (id, name, role, batting_style, bowling_style, gender))
        else:
            if (player_data['role'] != role) or (player_data['batting_style'] != batting_style) or \
                    (player_data['bowling_style'] != bowling_style):
                self.update(id, name, role, batting_style, bowling_style, gender)

    def update(self, id, name, role, batting_style, bowling_style, gender):
        sql = """UPDATE player SET role = %s, batting_style = %s, bowling_style = %s WHERE id = %s"""
        self.cursor.execute(sql, (role, batting_style, bowling_style, id))

    def __get_player_data(self, id):
        sql = """SELECT * FROM player WHERE player.id = %s"""
        self.cursor.execute(sql, (id,))
        if self.cursor.rowcount > 0:
            return Common.extract_query_results(self.cursor)
        return None
