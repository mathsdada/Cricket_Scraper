class Series:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, title, year):
        sql = """INSERT INTO series VALUES(%s, %s, %s)"""
        if not self.__check_series_id(id):
            self.cursor.execute(sql, (id, title, year))
            return True
        return False

    def __check_series_id(self, id):
        sql = """SELECT * FROM series WHERE series.id = %s"""
        self.cursor.execute(sql, (id,))
        if self.cursor.fetchone() is None:
            return False
        return True
