import psycopg2


class Database:
    def __init__(self):
        self.__host = "localhost"
        self.__database = "cricbuzz"
        self.__user = "mathsdada"
        self.__password = "1@gangadhar"
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(host=self.__host, database=self.__database, user=self.__user,
                                     password=self.__password)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None
