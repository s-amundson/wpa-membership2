import sys
import sqlite3 as sql
import string
import random
from Email import Email


# CREATE TABLE "member" ( `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT, `first_name` varchar ( 100 ) NOT NULL,
# `last_name` varchar ( 100 ) NOT NULL, `street` varchar ( 150 ) NOT NULL, `city` varchar ( 100 ) NOT NULL,
# `state` varchar ( 3 ) NOT NULL, `zip` varchar ( 10 ), `phone` varchar ( 20 ), `email` varchar ( 150 ) NOT NULL,
# `dob` date NOT NULL, `level` varchar ( 20 ) NOT NULL, `reg_date` date NOT NULL DEFAULT CURRENT_DATE,
# `exp_date` date NOT NULL DEFAULT CURRENT_DATE, `fam` INTEGER DEFAULT NULL, `benefactor` BOOLEAN DEFAULT 'FALSE',
# `val_code` varchar (20) )

# CREATE TABLE `family` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `fam_id` INTEGER NOT NULL,
# `mem_id` INTEGER )


# noinspection PyComparisonWithNone
class MemberDb:
    def __init__(self, file):
        self.con = sql.connect(file)
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()

        self.mem = {}
        self.email_sent = False

    def add(self, family):

        # consider checking to see if the member exists.
        if (self.mem["level"] == "family"):
            # family.add_member(self.mem)
            if (self.mem["fam"] is None):
                self.mem["fam"] = self.execute("SELECT MAX(fam_id) as fid from family")[0]["fid"]
                if (self.mem["fam"] is None):
                    self.mem["fam"] = 0
                self.mem["fam"] += 1
                self.mem['fam'] = self.mem["fam"]
                self.mem["val_code"] = self.randomString()
            else:
                self.mem["val_code"] = self.execute("SELECT * from member where fam = ?",
                                                    (self.mem["fam"],))[0]["val_code"]
        else:
            self.mem["val_code"] = self.randomString()
        s = "INSERT INTO member (first_name, last_name, street, city, state, zip, phone, email, dob, level, " \
            "benefactor, fam, val_code) VALUES ( "
        self.execute("{} ?,?,?,?,?,?,?,?,?,?,?,?,?)".format(s),
                     (self.mem["first_name"], self.mem["last_name"], self.mem["street"], self.mem["city"],
                      self.mem["state"], self.mem["zip"], self.mem["phone"], self.mem["email"], self.mem["dob"],
                      self.mem["level"], self.mem["benefactor"], self.mem["fam"], self.mem["val_code"]))

        self.mem["id"] = self.execute("SELECT id from member where last_name =? and first_name =?",
                                      (self.mem["last_name"], self.mem["first_name"]))
        self.mem["id"] = self.mem["id"][len(self.mem["id"]) - 1]["id"]
        print(self.mem["id"], file=sys.stdout)
        print(self.mem["fam"], file=sys.stdout)
        if (self.mem["level"] == "family"):
            self.execute("INSERT into family (fam_id, mem_id) values (?,?)", (self.mem["fam"], self.mem["id"]))
            family.add_member(self.mem)
            # if not self.email_sent:
            #     self.send_email("email_templates/verify.html")
            # # TODO send family email - Put in spplication.py

        else:
            self.send_email("email_templates/verify.html")

        return self.mem["id"]

    def checkInput(self):
        """ Check input for values"""
        v = True
        if (self.mem["first_name"] == "" or self.mem["last_name"] == ""):
            print("name issue", file=sys.stdout)
            v = False
        if (self.mem["street"] == "" or self.mem["city"] == "" or self.mem["state"] == "" or self.mem["zip"] == ""):
            print("address issue", file=sys.stdout)
            v = False
        if not (self.isValidEmail(self.mem["email"])):
            print("email issue", file=sys.stdout)
            v = False
        if not self.isValidPhone(self.mem["phone"]):
            v = False
        return v

    def check_email_code(self, row, code):
        print(row["val_code"], file=sys.stdout)
        if (row["val_code"] is not None and row["val_code"] == code):
            if (row["exp_date"] == row["reg_date"]):
                # date and datetime is not working fromisoformat not found
                d = row["exp_date"].split('-')
                d = "{}-{}-{}".format(int(d[0]) + 1, d[1], d[2])
                self.execute("UPDATE member SET `exp_date` = ?, `val_code` = ? WHERE `id` = ?", (d, None, row["id"]))

            else:
                self.execute("UPDATE member SET `val_code` = ? WHERE `id` = ?", (None, row["id"]))
            return True
        print("check_email_code False", file=sys.stdout)
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


    def isValidPhone(self, phone):
        print(phone, file=sys.stdout)
        for c in ['(', ')', '-', '.', ',']:
            phone = phone.strip(c)
        print(phone, file=sys.stdout)
        return (len(phone) > 9)


    def randomString(self, stringLength=16):
        """Generate a random string with the combination of lowercase and uppercase letters """
        # from https://pynative.com/python-generate-random-string/
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))


    def send_email(self, file, fam=""):  # TODO update for family
        with open(file) as f:
            msg = f.read()

        msg = msg.replace("NAME", self.mem["first_name"])
        msg = msg.replace("USERID", "{:06d}".format(self.mem["id"]))
        msg = msg.replace("EMAIL", self.mem["email"])
        msg = msg.replace("CODE", self.mem["val_code"])
        msg = msg.replace("FAMILY", fam)

        # Email().send_mail(self.mem["email"], "Woodley Park Archers email verification", msg)
        Email().send_mail("sam.amundson@gmailcom", "Woodley Park Archers email verification", msg)

    def setbyDict(self, mydict):
        self.mem = mydict
