import logging

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.conf import settings

logger = logging.getLogger(__name__)


class Email:
    @staticmethod
    def verification_email(member_dict):
        subject = 'Email Verification Code'
        to_address = member_dict['email']
        logging.debug(settings.EMAIL_DEBUG)
        if settings.EMAIL_DEBUG:
            to_address = 'sam.amundson@gmail.com'

        htmly = get_template('email/verify.html')

        d = {'id': member_dict['id'], 'first_name': member_dict['first_name'],
             'verification_code': member_dict['verification_code'], 'site': ""}

        # text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [to_address])
        msg.content_subtype = "html"
        # msg.attach_alternative(html_content, "text/html")
        logging.debug(f"To: {to_address}, subject: {subject}")
        msg.send()


    # def payment_email(self, toaddr, subject, template, table_rows=[], mem=None, fam=[], receipt=''):
    #     if toaddr is None:
    #         return
    #     values = {'site': self.site, 'join': 'joining', 'receipt': receipt}
    #     if subject == "Renew":
    #         values['join'] = 'renewing with'
    #         subject = 'Woodley Park Archers Renewal'
    #     if mem is not None:
    #         values['name'] = mem["first_name"]
    #         values['id'] = mem["id"]
    #         values['email'] = mem["email"]
    #         values['email_code'] = mem['email_code']
    #         if "renew_code" in mem:
    #             values['renew_code'] = mem['renew_code']
    #         if 'exp_date' in mem:
    #             values['expire'] = mem["exp_date"].strftime("%d %B %Y")
    #         values['fam'] = fam
    #     values['total'] = 0
    #     if len(table_rows) > 0:
    #         table_rows, values['total'] = table_rows
    #     msg = render_template(template, rows=table_rows, values=values)
    #         # return msg
    #
    #         self.send_mail(toaddr, subject, msg)  # , f"{self.project_directory}/static/header.png", "header.png")

    @staticmethod
    def renewal_notice(email, exp_date):
        subject = 'Email Verification Code'
        to_address = email
        if settings.EMAIL_DEBUG:
            to_address = 'sam.amundson@gmail.com'
        text_content = f"Your membership is due to expire on {exp_date}. Please renew"
