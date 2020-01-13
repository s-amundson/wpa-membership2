import sqlite3 as sql
import sys

class DbHelper:
    def __init__(self, file):
        # try:
        self.con = sql.connect(file)
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()
        # except:
        #     print(sys.exc_info()[0], file=sys.stderr)
        #     self.con = None
        #     self.cur = None

    def execute(self, statement, args=None):
        # try:
        self.cur.execute(statement, args)
        self.conn.commit()

        return self.cur.fetchall()
        # except:
        #     print(sys.exc_info()[0], file=sys.stderr)
        #     return None

        