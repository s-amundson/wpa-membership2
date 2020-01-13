import sys
import sqlite3 as sql
import string
import random
from datetime import datetime


# CREATE TABLE "member" ( `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT, `first_name` varchar ( 100 ) NOT NULL,
# `last_name` varchar ( 100 ) NOT NULL, `street` varchar ( 150 ) NOT NULL, `city` varchar ( 100 ) NOT NULL,
# `state` varchar ( 3 ) NOT NULL, `zip` varchar ( 10 ), `phone` varchar ( 20 ), `email` varchar ( 150 ) NOT NULL,
# `dob` date NOT NULL, `level` varchar ( 20 ) NOT NULL, `reg_date` date NOT NULL DEFAULT CURRENT_DATE,
# `exp_date` date NOT NULL DEFAULT CURRENT_DATE, `fam` INTEGER DEFAULT NULL, `benefactor` BOOLEAN DEFAULT 'FALSE' )

# CREATE TABLE `family` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `fam_id` INTEGER NOT NULL,
# `mem_id` INTEGER )


# noinspection PyComparisonWithNone
class MemberDb:
    def __init__(self, file):
        self.con = sql.connect(file)
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()

        self.uid = None
        self.first_name = None
        self.last_name = None
        self.street = None
        self.city = None
        self.state = None
        self.zip = None
        self.phone = None
        self.email = None
        self.dob = None
        self.level = None
        self.reg_date = None
        self.exp_date = None
        self.fam = None
        self.benefactor = False

        self.mem_dict = {}

    def add(self, family):

        # consider checking to see if the member exists.
        if (self.level == "family"):
            # family.add_member(self.mem_dict)
            if (self.fam is None):
                self.fam = self.execute("SELECT MAX(fam_id) as fid from family")[0]["fid"]
                if (self.fam is None):
                    self.fam = 0
                self.fam += 1
                self.mem_dict['fam'] = self.fam
                self.mem_dict["val_code"] = self.randomString()
            else:
                print(self.fam, file=sys.stdout)
                self.mem_dict["val_code"] = self.execute("SELECT * from member where fam = ?",
                                                         (self.fam,))[0]["val_code"]
        else:
            self.mem_dict["val_code"] = self.randomString()
        s = "INSERT INTO member (first_name, last_name, street, city, state, zip, phone, email, dob, level, " \
            "benefactor, fam, val_code) VALUES ( "
        self.execute("{} ?,?,?,?,?,?,?,?,?,?,?,?,?)".format(s),
                     (self.first_name, self.last_name, self.street, self.city, self.state, self.zip, self.phone,
                      self.email, self.dob, self.level, self.benefactor, self.fam, self.mem_dict["val_code"]))

        self.uid = self.execute("SELECT id from member where last_name =? and first_name =?",
                                (self.last_name, self.first_name))
        self.uid = self.uid[len(self.uid) - 1]["id"]
        print(self.uid, file=sys.stdout)
        print(self.fam, file=sys.stdout)
        self.mem_dict['id'] = self.uid
        if (self.level == "family"):
            print(self.fam, file=sys.stdout)
            self.execute("INSERT into family (fam_id, mem_id) values (?,?)", (self.fam, self.uid))
            family.add_member(self.mem_dict)
            # self.execute("UPDATE `member` SET `fam`=? WHERE _rowid_=?", (self.fam, self.uid))

        return self.uid


    def checkInput(self):
        """ Check input for sterilization issues returns sterilized input"""
        v = True
        print("first: {}, Last: {}".format(self.first_name, self.last_name), file=sys.stdout)
        if (self.first_name == "" or self.last_name == ""):
            print("name issue", file=sys.stdout)
            v = False
        if (self.street == "" or self.city == "" or self.state == "" or self.zip == ""):
            print("address issue", file=sys.stdout)
            v = False
        if not (self.isValidEmail(self.email)):
            print("email issue", file=sys.stdout)
            v = False
        return v

    def email_verify(self, row, code):
        print(row["exp_date"], file=sys.stdout)
        if (row["val_code"] is not None and row["val_code"] == code):
            if (row["exp_date"] == row["reg_date"]):
                # date and datetime is not working fromisoformat not found
                d = row["exp_date"].split('-')
                d = "{}-{}-{}".format(int(d[0]) + 1, d[1], d[2])
                self.execute("UPDATE member SET `exp_date` = ?, `val_code` = ? WHERE `id` = ?", (d, None, row["id"]))
            else:
                self.execute("UPDATE member SET `val_code` = ? WHERE `id` = ?", (None, row["id"]))
            return True
        return False  # invalid code

    def execute(self, statement, args=None):
        # try:
        if (args is None):
            self.cur.execute(statement)
        else:
            self.cur.execute(statement, args)
        self.con.commit()

        return self.cur.fetchall()

    def find_by_email(self, email):
        print(email, file=sys.stdout)
        return self.execute("SELECT * from member where email = ?", (email,))

    def find_by_fam(self, fam):
        return self.execute("SELECT * from member where fam = '?'", (fam,))

    def find_by_id(self, mem_id):
        r = self.execute("SELECT * from member where id = '?'", (mem_id,))[0]
        self.setbyDict(r)
        return r

    @staticmethod
    def isValidEmail(x):
        a = x.split('@')
        if (len(a) == 2 and len(a[0]) > 2):
            b = a[1].split('.')
            if (len(b) > 1):
                return True

            return False

    @staticmethod
    def isValidPhone(phone):
        phone = phone.strip(['(', ')', '-', '.', ','])
        print(phone, file=sys.stdout)
        return (len(phone) > 9)


    @staticmethod
    def randomString(stringLength=16):
        """Generate a random string with the combination of lowercase and uppercase letters """
        # from https://pynative.com/python-generate-random-string/
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))

    def setbyDict(self, mydict):
        self.mem_dict = mydict
        self.first_name = mydict["first_name"]
        self.last_name = mydict["last_name"]
        self.street = mydict["street"]
        self.city = mydict["city"]
        self.state = mydict["state"]
        self.zip = mydict["zip"]
        self.phone = mydict["phone"]
        self.email = mydict["email"]
        self.dob = mydict["dob"]
        self.level = mydict["level"]
        # self.reg_date = mydict["reg_date"]
        # self.exp_date = mydict["exp_date"]
        self.fam = mydict["fam"]
