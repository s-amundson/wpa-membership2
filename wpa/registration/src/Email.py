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
        if settings.DEBUG:
            to_address = 'sam.amundson@gmail.com'

        htmly = get_template('email/verify.html')

        d = {'id': member_dict['id'], 'first_name': member_dict['first_name'],
             'email_code': member_dict['email_code'], 'site': ""}

        # text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [to_address])
        msg.content_subtype = "html"
        # msg.attach_alternative(html_content, "text/html")
        msg.send()
