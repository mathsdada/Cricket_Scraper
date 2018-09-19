class Team:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, name, short_name):
        sql = """INSERT INTO team  (name, short_name) VALUES(%s, %s)
                RETURNING id"""
        team_id = self.__check_team(name)
        if team_id is None:
            self.cursor.execute(sql, (name, short_name))
            team_id = self.cursor.fetchone()[0]
        return team_id

    def __check_team(self, name):
        sql = """SELECT * FROM team WHERE name = %s"""
        self.cursor.execute(sql, (name,))
        if self.cursor.rowcount > 0:
            return self.cursor.fetchone()[0]
        return None

    def clear(self):
        sql = """DELETE FROM team"""
        self.cursor.execute(sql)
