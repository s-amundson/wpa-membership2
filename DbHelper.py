import pymysql

from Config import Config

class DbHelper:
    def __init__(self):
        self.cfg = Config().get_database()
        self.connect()

        # code = None
        # status = 'member'
        # s = f"UPDATE member SET `pay_code` = %s, `status` = %s WHERE `fam` = '1'"
        # self.execute(s, (code, status))
    def connect(self):
        # Open database connection

        self.db = pymysql.connect(self.cfg["server"], self.cfg["user"], self.cfg["password"], self.cfg["db"])


        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)


    def execute(self, statement, args=None):
        try:
            print(f"DbHelper {statement}, args={args}")
            if args is None:
                self.cursor.execute(statement)
            else:
                self.cursor.execute(statement, args)
            self.db.commit()
            rows = self.cursor.fetchall()
            print(f"DBHelper {rows}")
        except pymysql.err.OperationalError as e:
            print("DbHelper Error: {}".format(e))
            if e[0] == 2006:
                try:
                    self.connect()
                except:
                    raise e
        #     self.db.rollback()
        #     rows = None
        return rows


if __name__ == '__main__':
    DbHelper()
