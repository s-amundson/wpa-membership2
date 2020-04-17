import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from flask import render_template
from Config import Config


class Email:
    """ Class for sending out emails using Gmail"""
    def __init__(self, project_directory):
        c = Config(project_directory)
        cfg = c.get_smtp()
        self.server = cfg["server"]
        self.user = cfg["user"]
        self.password = cfg["password"]
        self.site = c.get_site()['site']
        self.project_directory = project_directory
        print(project_directory)

    def send_email(self, toaddr, subject, template, table_rows=[], mem=None, fam=''):
        values = {'site': self.site, 'join':'joining'}
        if subject == "Renew":
            values['join'] = 'renewing with'
            subject = 'Woodley Park Archers Renewal'
        if mem is not None:
            values['name'] = mem["first_name"]
            values['id'] = mem["id"]
            values['email'] = mem["email"]
            values['email_code'] = mem['email_code']
            if "renew_code" in mem:
                values['renew_code'] = mem['renew_code']
                values['expire'] = mem["exp_date"].strftime("%d %B %Y")
            values['fam'] = fam
        values['total'] = 0
        if len(table_rows) > 0:
            table_rows, values['total'] = table_rows
        msg = render_template(template, rows=table_rows, values=values)
        # return msg
        # TODO change to toaddr when for production
        self.send_mail('sam.amundson@gmail.com', subject, msg) # , f"{self.project_directory}/static/header.png", "header.png")

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

        # Attach image
        img = dict(title=u'Header', path=f"{self.project_directory}/static/header.png", cid='header_img')
        with open(img['path'], 'rb') as file:
            msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
            msg.attach(msg_image)
        msg_image.add_header('Content-ID', "<header_img>")
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


if __name__ == '__main__':
    project_directory = '/home/sam/PycharmProjects/wpa-membership2/'
    e = Email(project_directory)
    e.send_email("", "test join", 'templates/email/verify.html')
