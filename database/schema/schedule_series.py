class Series:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, id, title, gender, category):
        sql = """INSERT INTO schedule_series VALUES(%s, %s, %s, %s)"""
        self.cursor.execute(sql, (id, title, gender, category))

    def clear(self):
        sql = """DELETE FROM schedule_series"""
        self.cursor.execute(sql)
