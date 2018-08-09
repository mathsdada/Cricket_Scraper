class Series:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, title, year):
        sql = """INSERT INTO series VALUES(%s, %s, %s)"""
        self.cursor.execute(sql, (id, title, year))
