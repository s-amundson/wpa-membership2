import sys
import string
import random
from Email import Email


class MemberDb:
    def __init__(self, db):
        self.db = db
        self.mem = {}
        self.email_sent = False

    def add(self, family):

        # consider checking to see if the member exists.
        if (self.mem["level"] == "family"):
            # family.add_member(self.mem)
            if (self.mem["fam"] is None):
                row = self.db.execute("SELECT MAX(fam_id) as fid from family")
                if row[0]['fid'] is None:
                    self.mem["fam"] = 0
                else:
                    self.mem["fam"] = row[0]["fid"]
                # if (self.mem["fam"] is None):

                self.mem["fam"] += 1
                self.mem['fam'] = self.mem["fam"]
                self.mem["val_code"] = self.randomString()
            else:
                self.mem["val_code"] = self.db.execute("SELECT * from member where fam = {}".format(
                                                    self.mem["fam"]))[0]["val_code"]
        else:
            self.mem["val_code"] = self.randomString()
        print("Bennefactor {}".format(self.mem["benefactor"]))
        if self.mem["benefactor"] is None:
            self.mem["benefactor"] = 0
        else:
            self.mem["benefactor"] = 1
        if self.mem["fam"] is None:
            fam = "NULL"
        else:
            fam = self.mem["fam"]

        s = "INSERT INTO member (first_name, last_name, street, city, state, zip, phone, email, dob, level, " \
            "benefactor, fam, val_code, reg_date, exp_date) VALUES ( "
        self.db.execute("{} '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},{},'{}', CURDATE(), CURDATE())".format(
                      s, self.mem["first_name"],
                      self.mem["last_name"], self.mem["street"], self.mem["city"],
                      self.mem["state"], self.mem["zip"], self.mem["phone"], self.mem["email"], self.mem["dob"],
                      self.mem["level"], self.mem["benefactor"], fam, self.mem["val_code"]))

        r = self.db.execute("SELECT id from member where last_name = '{}' and first_name = '{}'".format(
                                      self.mem["last_name"], self.mem["first_name"]))
        self.mem["id"] = r[len(r) - 1]["id"]

        if (self.mem["level"] == "family"):
            self.db.execute("INSERT into family (fam_id, mem_id) values ({},{})".format(
                self.mem["fam"], self.mem["id"]))
            family.add_member(self.mem)

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
                d = row["exp_date"]
                d = d.replace(year=d.year + 1)

                self.db.execute("UPDATE member SET `exp_date` = '{}', `val_code` = NULL WHERE `id` = {}".format(
                    d.isoformat(), row["id"]))

            else:
                self.db.execute("UPDATE member SET `val_code` = NULL WHERE `id` = {}".format(row["id"]))
            return True
        print("check_email_code False", file=sys.stdout)
        return False  # invalid code


    def find_by_email(self, email):
        return self.db.execute("SELECT * from member where email = '{}'".format(email))

    def find_by_fam(self, fam):
        return self.db.execute("SELECT * from member where fam = '{}'".format(fam))

    def find_by_id(self, mem_id):
        r = self.db.execute("SELECT * from member where id = '{}'".format(mem_id))[0]
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


    def send_email(self, file, fam=""):
        with open(file) as f:
            msg = f.read()
        # TODO insert image into email
        msg = msg.replace("NAME", self.mem["first_name"])
        msg = msg.replace("USERID", "{:06d}".format(self.mem["id"]))
        msg = msg.replace("EMAIL", self.mem["email"])
        msg = msg.replace("CODE", self.mem["val_code"])
        msg = msg.replace("RENEW", self.mem["renew_code"])
        msg = msg.replace("FAMILY", fam)

        # TODO change this back
        # Email().send_mail(self.mem["email"], "Woodley Park Archers email verification", msg)
        Email().send_mail("sam.amundson@gmailcom", "Woodley Park Archers email verification", msg)


    def send_renewal(self, row):
        row["renew_code"] = self.randomString()
        self.mem = row
        self.send_email("email_templates/renew_code_email.html")


    def setbyDict(self, mydict):
        self.mem = mydict
