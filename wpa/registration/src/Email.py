import logging

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


class Email:

    @staticmethod
    def payment_email(log, line_items, mem=None):
        logging.debug(log.description)
        logging.debug(log.description.find('Membership'))
        if settings.EMAIL_DEBUG:
            to_address = 'sam.amundson@gmail.com'
        else:
            to_address = log.email_address

        if log.description.find('Membership') >= 0:

            # This is a membership email
            logging.debug(mem.member_set.all())
            ms = mem.member_set.all()
            logging.debug(ms[0].first_name)
            text_lines = ""
            html_lines = []
            rows = line_items.copy()
            for row in rows:
                row['amount'] = int(int(row['base_price_money']['amount']) / 100)
                row['cost'] = row['quantity'] * row['amount']
                html_lines.append({'name': row['name'], 'quantity': row['quantity'], 'amount': row['amount'], 'cost': row['cost']})

                total = int(int(log.total_money)/100)
                logging.debug(total)
            d = {'id': log.members, 'name': ms[0].first_name, 'fam': [], 'total': total,
                 'lines': html_lines}
            subject = "Welcome to Woodley Park Archers"
            html_content = get_template('email/join.html').render(d)
            text_content = get_template('email/join.txt').render(d)

        else:
            # Not a membership email
            subject = ""
            html_content = ""
            text_content = ''

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_address])
        msg.content_subtype = "text"
        msg.attach_alternative(html_content, "text/html")
        msg.send()

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
    def renewal_notice(membership):
        subject = "Woodley Park Archers renewal notice"
        to_address = membership.email
        if settings.EMAIL_DEBUG:
            to_address = 'sam.amundson@gmail.com'

        logging.debug(membership.member_set.all())
        ms = membership.member_set.all()
        d = {'id': membership.id, 'first_name': ms[0].first_name, 'date': membership.exp_date,
             'verification_code': membership.verification_code[:13], 'email': membership.email,
             'site': settings.SITE_URL + "/registration"}

        html_content = get_template('email/renew_notice.html').render(d)
        text_content = get_template('email/renew_notice.txt').render(d)

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_address])
        msg.content_subtype = "text"
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @staticmethod
    def verification_email(member_dict):
        # for k, v in member_dict.items():
        #     member_dict[k] = str(v)
        logging.debug(member_dict)
        member_dict['site'] = settings.SITE_URL + "/registration/email_verify"
        subject = 'Email Verification Code'
        to_address = member_dict['email']
        logging.debug(settings.EMAIL_DEBUG)
        if settings.EMAIL_DEBUG:
            to_address = 'sam.amundson@gmail.com'

        plaintext = get_template('email/verify.txt')
        htmly = get_template('email/verify.html')

        d = {'id': member_dict['id'], 'first_name': member_dict['first_name'],
             'verification_code': member_dict['verification_code'], 'site': member_dict['site'],
             'email': member_dict['email']}

        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_address])
        msg.content_subtype = "text"
        msg.attach_alternative(html_content, "text/html")
        logging.debug(f"To: {to_address}, subject: {subject}")
        msg.send()