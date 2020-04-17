import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import render_template
from Config import Config


class Email:
    """ Class for sending out emails using Gmail"""
    def __init__(self, project_directory):
        cfg = Config(project_directory).get_smtp()
        self.server = cfg["server"]
        self.user = cfg["user"]
        self.password = cfg["password"]

    def send_email(self, toaddr, subject, template, table_rows=None, mem=None, fam=''):
        user = {}
        if mem is not None:
            user['name'] = mem["first_name"]
            user['id'] = mem["id"]
            user['email'] = mem["email"]
            user['email_code'] = mem['email_code']
            if "renew_code" in mem:
                user['renew_code'] = mem['renew_code']
                user['expire'] = mem["exp_date"].strftime("%d %B %Y")
            user['fam'] = fam

        msg = render_template(template, rows=table_rows, user=user)
        # print(msg)
        # TODO change to toaddr when for production
        self.send_mail('sam.amundson@gmail.com', subject, msg)

    def send_mail(self, toaddr, subject, body, attach_path=None, attach_filename=None):
        "Send an email"
        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = self.user

        # storing the receivers email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = subject

        # string to store the body of the mail
        # body = "Body_of_the_mail"

        # # attach the body with the msg instance
        msg.attach(MIMEText(body, 'html'))
        if attach_path is not None:
            # open the file to be sent
            # filename = "File_name_with_extension"
            attachment = open(attach_path, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % attach_filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)

        # creates SMTP session
        # s = smtplib.SMTP('smtp.gmail.com', 587)
        s = smtplib.SMTP(self.server)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(self.user, self.password)

        # sending the mail
        s.sendmail(toaddr, self.user, msg.as_string())

        # terminating the session
        s.quit()
