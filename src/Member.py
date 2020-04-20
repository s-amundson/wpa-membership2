import sys
import os
import string
import random
from Email import Email
from PayLogHelper import PayLogHelper
from datetime import date
import uuid


class Member:
    """Helper class for membership functions."""

    def __init__(self, db, project_directory):
        self.db = db
        self.mem = {}
        self.email_sent = False
        self.project_directory = project_directory

    def add(self, family):
        """Adds a member to the database, Returns member ID."""
        # consider checking to see if the member exists.
        if (self.mem["level"] == "family"):
            if (self.mem["fam"] is None):
                # Get the last family ID used
                row = self.db.execute("SELECT MAX(fam_id) as fid from family")
                if row[0]['fid'] is None:
                    self.mem["fam"] = 0
                else:
                    self.mem["fam"] = row[0]["fid"]

                # Increment the family id for new id.
                self.mem["fam"] += 1
                self.mem['fam'] = self.mem["fam"]

                # create email code for email verification
                self.mem["email_code"] = self.randomString()
            else:  # Family id exists
                # create email code for email verification
                self.mem["email_code"] = self.db.execute("SELECT * from member where fam = {}".format(
                    self.mem["fam"]))[0]["email_code"]
        else:  # not a family membership
            # create email code for email verification
            self.mem["email_code"] = self.randomString()

        # If benefactor was checked set to 1 otherwise set to 0
        if self.mem["benefactor"] is None:
            self.mem["benefactor"] = 0
        else:
            self.mem["benefactor"] = 1

        if self.mem["fam"] is None:
            fam = "NULL"
        else:
            fam = self.mem["fam"]

        # Insert membership data into database
        s = "INSERT INTO member (first_name, last_name, street, city, state, zip, phone, email, dob, level, " \
            "benefactor, fam, email_code, reg_date, exp_date) VALUES ( "
        self.db.execute("{} '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},{},'{}', CURDATE(), CURDATE())".format(
            s, self.mem["first_name"],
            self.mem["last_name"], self.mem["street"], self.mem["city"],
            self.mem["state"], self.mem["zip"], self.mem["phone"], self.mem["email"], self.mem["dob"],
            self.mem["level"], self.mem["benefactor"], fam, self.mem["email_code"]))

        # Get the row from the database
        r = self.db.execute("SELECT id from member where last_name = '{}' and first_name = '{}'".format(
            self.mem["last_name"], self.mem["first_name"]))
        self.mem["id"] = r[len(r) - 1]["id"]

        # Add a family in database if family membership
        if (self.mem["level"] == "family"):
            self.db.execute("INSERT into family (fam_id, mem_id) values ({},{})".format(
                self.mem["fam"], self.mem["id"]))
            family.add_member(self.mem)

        else:
            # Send an email to the member
            path = os.path.join(self.project_directory, "email_templates", "verify.html")
            # self.send_email(path, "Email Verification Code")\
            Email(self.project_directory).send_email(self.mem['email'], "Email Verification Code", "email/verify.html",
                                                     mem=self.mem)
        return self.mem["id"]

    def check_duplicate(self):
        """ Checks for duplicate entries """
        col = ["street", "city", "state", "zip", "phone", "email", "dob"]
        matches = 0
        r = self.db.execute("SELECT * from member where last_name = '{}' and first_name = '{}'".format(
            self.mem["last_name"], self.mem["first_name"]))
        if len(r) > 0:
            for c in col:
                if self.mem[c] == r[c]:
                    matches += 1
        return matches > len(col) - 2

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

    def check_email(self, email, vcode):
        """ Checks to see if the email and the verification code match the database records. If so sets the pay code
        to start the payment process. This is done for initial verification of email address."""
        rows = self.db.execute(
            f"SELECT * from member where `email` = '{email}' and `email_code` = '{vcode}' ORDER BY `id`")
        if len(rows) > 0:
            self.setbyDict(rows[0])

            # if self.mem['pay_code'] is None:
            #     # self.set_pay_code()
            #     # self.set_member_pay_code_status(self.mem['pay_code'], 'start payment')
            return self.mem
        else:
            return None

    def expire_update(self, row):
        """ Update the expiration date of the row."""
        d = row["exp_date"]
        d = d.replace(year=d.year + 1)
        s = f"UPDATE member SET `exp_date` = '{d.isoformat()}', `email_code` = %s, `status` = 'member'  WHERE `id` = '{row['id']}'"
        self.db.execute(s, (None,))

    def find_by_email(self, email):
        """Returns member by their email address"""
        return self.db.execute("SELECT * from member where email = '{}'".format(email))

    def find_by_fam(self, fam):
        """Returns members by family id"""
        return self.db.execute("SELECT * from member where fam = '{}'".format(fam))

    def find_by_id(self, mem_id):
        """Returns members by id"""
        r = self.db.execute("SELECT * from member where id = '{}'".format(mem_id))[0]
        self.setbyDict(r)
        return r

    @staticmethod
    def isValidEmail(x):
        """Checks if a string is formatted as an email"""
        a = x.split('@')
        if (len(a) == 2 and len(a[0]) > 2):
            b = a[1].split('.')
            if (len(b) > 1):
                return True
        return False

    def isValidPhone(self, phone):
        """Checks if a string is formatted as an phone number"""
        for c in ['(', ')', '-', '.', ',']:
            phone = phone.replace(c, '')
        return (len(phone) > 9)

    def joad_register(self):
        """ Register a JOAD student and if session is not "None" register them for a joad session"""
        s = f"SELECT `mem_id` from joad_session_registration where `mem_id` = {self.mem['id']}"
        if len(self.db.execute(s)) == 0:
            s = f"INSERT INTO joad_session_registration (mem_id) VALUES ({self.mem['id']})"
            self.db.execute(s)

    def randomString(self, stringLength=16):
        """Generate a random string with the combination of lowercase and uppercase letters """
        # from https://pynative.com/python-generate-random-string/
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))

    # def send_email(self, file, subject, fam=""):
    #     """Sends an email from a template file replacing key words"""
    #     with open(file) as f:
    #         msg = f.read()
    #     # TODO insert image into email
    #     msg = msg.replace("NAME", self.mem["first_name"])
    #     msg = msg.replace("USERID", "{:06d}".format(self.mem["id"]))
    #     msg = msg.replace("EMAIL", self.mem["email"])
    #     if self.mem["email_code"] is not None:
    #         msg = msg.replace("CODE", self.mem["email_code"])
    #     # self.set_pay_code()
    #     if "renew_code" in self.mem:
    #         msg = msg.replace("RENEW", self.mem["renew_code"])
    #         msg = msg.replace("EXPIRE", self.mem["exp_date"].strftime("%d %B %Y"))
    #     msg = msg.replace("FAMILY", fam)
    #
    #     # TODO change this back
    #     # Email().send_mail(self.mem["email"], "Woodley Park Archers email verification", msg)

    def send_renewal(self, row):
        """ Sends an email with a renewal code"""
        d = date.today()
        d = d.replace(year=d.year + 1)
        self.mem = row
        if d > row['exp_date']:  # can renew
            self.mem["renew_code"] = self.randomString()

            # path = os.path.join(self.project_directory, "email_templates", "renew_code_email.html")
            # self.send_email(path, "Membership Renewal Notice")
            Email(self.project_directory).send_email(self.mem['email'], 'Membership Renewal Notice',
                                                     "email/renew_code_email.html", mem=self.mem)

            self.mem['email_code'] = row["renew_code"]
            self.db.execute(f"UPDATE member SET `email_code` = %s where `id` = %s",
                            (self.mem['email_code'], self.mem['id']))
        else:  # Cannot renew yet
            self.mem["renew_code"] = "None"
            # path = os.path.join(self.project_directory, "email_templates", "renew_invalid.html")
            # self.send_email(path, "Membership Renewal Notice")
            Email(self.project_directory).send_email(self.mem['email'], 'Membership Renewal Notice',
                                                     "email/renew_invalid.html", mem=self.mem)

    def setbyDict(self, mydict):
        """Sets the mem dict to the input dict"""
        self.mem = mydict

    def set_member_pay_code_status(self, code, status, mem_id=None):
        """ When email is verified status = start payment. When payment is in process = payment pending.
        When payment successful member"""
        if mem_id is None:
            mem_id = self.mem['id']
        if self.mem['fam'] is None:
            s = f"UPDATE member SET `pay_code` = %s, `status` = %s WHERE `id` = '{mem_id}'"
        else:
            s = f"UPDATE member SET `pay_code` = %s, `status` = %s WHERE `fam` = '{mem_id}'"
        self.db.execute(s, (code, status))

    # def set_pay_code(self):
    #     """Sets an unique payment code as required by square"""
    #     if 'pay_code' in self.mem:
    #         if self.mem['pay_code'] is None:
    #             self.mem['pay_code'] = str(uuid.uuid4())
    #     else:
    #         self.mem['pay_code'] = str(uuid.uuid4())
    #     return self.mem['pay_code']

    # def square_payment(self, square_result, description):
    #     members = ""
    #     print(f"MemberDb.square_payment fam = {self.mem['fam']} {self.mem['fam'] is None}")
    #     if self.mem['fam'] is not None:
    #         rows = self.find_by_fam(self.mem['fam'])
    #         for row in rows:
    #             members += f"{row['id']}, "
    #     else:
    #         members += f"{self.mem['id']}"
    #
    #     pay_status = PayLogHelper(self.db).add_square_payment(square_result, members.strip(", "), description,
    #                                                           self.mem['pay_code'])
    #     if pay_status == "OPEN":
    #         self.set_member_pay_code_status(self.mem['pay_code'], 'payment pending')
    #     elif pay_status == 'COMPLETED':
    #         self.set_member_pay_code_status(None, 'member')
    #         if self.mem['fam'] != None:
    #             rows = self.find_by_fam(self.mem['fam'])
    #             for row in rows:
    #                 self.expire_update(row)
    #         else:
    #             self.expire_update(self.mem)
    #     elif pay_status == "CANCELED":
    #         self.set_member_pay_code_status(self.mem['pay_code'], 'payment canceled')

    def update_record(self, reg):
        """For updating record in database"""
        s = f"UPDATE member SET "
        update_required = False
        if reg['dob'] == '':
            reg['dob'] = self.mem['dob']
        if reg['benefactor'] is None:
            reg['benefactor'] = 0
        if reg['level'] is None:
            reg['level'] = self.mem['level']
        print(f"MemberDb.update_record s = {reg} ")
        for k, v in reg.items():
            if self.mem[k] != v:
                s += f"{k} = {v}, "
                update_required = True
        if update_required:
            s = s[:-2] + f" WHERE id = {self.mem['id']}"
            print(f"MemberDb.update_record s = {s}")
            self.db.execute(s)
