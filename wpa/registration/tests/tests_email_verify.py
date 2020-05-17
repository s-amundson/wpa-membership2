import json
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from registration.models import Member, Family, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)


# Create your tests here.


class EmailVerifyTests(TestCase):
    fixtures = ['email_verify_fixture.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'email_verify_fixture.json')
        logging.debug(path)
        with open(path) as f:
            data = json.load(f)

        self.member_data = []
        self.joad_sessions_data = []
        for r in data:
            if r['model'] == 'registration.member':
                f = r['fields']
                # f.pop('reg_date')
                # f.pop('exp_date')
                # f.pop('verification_code')
                # f.pop('status')
                # f.pop('pay_code')
                # f.pop('fam')
                # f['terms'] = True
                self.member_data.append(f)
            elif r['model'] == 'registration.joad_sessions':
                self.joad_sessions_data.append(r['fields'])
        path = os.path.join(settings.BASE_DIR, 'registration', 'tests', 'email_verify_line_items.json')
        with open(path) as json_data:
            self.line_items_list = json.load(json_data)


    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    #
    # def add_member(self):
    #     # submit a registration to be added.
    #     response = self.client.post(reverse('registration:register'), self.mem, follow=True)
    #     session = self.client.session
    #     self.assertRedirects(response, reverse('registration:register'))
    #     self.member = Member.objects.all()
    #     self.assertEquals(len(self.member), 1)
    #     self.assertEquals(len(session.items()), 0)

    def test_email_verification(self):
        # self.add_member()
        index = 0
        for line in self.line_items_list:
            logging.debug(self.member_data[index])
            self.client.get(reverse('registration:email_verify'),
                            {'e': self.member_data[index]['email'],
                             'c': self.member_data[index]['verification_code']})
            with self.assertTemplateUsed('registration/email_verify.html'):
                render_to_string('registration/email_verify.html')

            m = {'email': self.member_data[index]['email'], 'verification_code': self.member_data[index]['verification_code']}
            response = self.client.post(reverse('registration:email_verify'), m, follow=True)
            session = self.client.session
            # line = [{'name': 'Membership', 'quantity': '1', 'base_price_money': {'amount': 2000, 'currency': 'USD'}}]
            self.assertListEqual(session['line_items'], line)
            self.assertEquals(session['idempotency_key'], self.member_data[index]['verification_code'])
            m = Member.objects.filter(email=self.member_data[index]['email'],
                                      verification_code=self.member_data[index]['verification_code'])
            index += len(m)
            logging.debug(index + 12)
