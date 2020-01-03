import sqlite3 as sql

class DbHelper:
    def __init__(self, file):
        try:
            self.con = sql.connect(file)
            self.con.row_factory = sql.Row
            self.cur = con.cursor()
        except:
            self.con = None
            self.cur = None

    def execute(self, statement):
        try:
            self.cur.execute(statement)
            return self.cur.fetchall()
        except:
            return None

        