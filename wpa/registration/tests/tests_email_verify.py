import json
import logging
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse

logger = logging.getLogger(__name__)


class EmailVerifyTests(TestCase):
    fixtures = ['membership1.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'membership1.json')
        logging.debug(path)
        with open(path) as f:
            data = json.load(f)

        self.membership_data = []
        self.joad_sessions_data = []
        self.joad_registration_data = []
        self.costs = {'standard_membership': 20,
                      'family_membership': 40,
                      'joad_membership': 18,
                      'senior_membership': 18,
                      'benefactor': 100,
                      'joad_session': 95,
                      'pin_shoot': 15,
                      'joad_pin': 5,
                      'family_total': None}
        for r in data:
            if r['model'] == 'registration.membership':
                f = r['fields']
                self.membership_data.append(f)

        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'registration_fixture.json')
        logging.debug(path)
        with open(path) as f:
            self.member_data = json.load(f)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        logging.debug('here')


    def test_email_verification(self):
        # self.add_member()
        for line in self.membership_data:
            # logging.debug(self.membership_data[index])
            self.client.get(reverse('registration:email_verify'),
                            {'e': line['email'],
                             'c': line['verification_code']})
            with self.assertTemplateUsed('registration/email_verify.html'):
                render_to_string('registration/email_verify.html')

            m = {'email': line['email'], 'verification_code': line['verification_code']}
            self.client.post(reverse('registration:email_verify'), m, follow=True)
            session = self.client.session

            line_items = []
            for m in self.member_data:
                if m['email'][0] == line['email']:
                    li = {'name': 'Membership', 'quantity': '1', 'base_price_money':
                        {'amount': 100, 'currency': 'USD'}}
                    if line["benefactor"]:
                        li['name'] = 'Benefactor Membership'
                        li['base_price_money']['amount'] = self.costs['benefactor'] * 100
                    else:
                        li['base_price_money']['amount'] = self.costs[f"{line['level']}_membership"] * 100
                    line_items.append(li)
                    cost = 0
                    joad_sessions = 0
                    for i in range(int(m["member_set-TOTAL_FORMS"][0])):
                        if m[f"member_set-{i}-joad"][0] != "":
                            cost += self.costs['joad_session']
                            joad_sessions += 1
                    if joad_sessions > 0:
                        line_items.append({'name': 'Joad Session 2020-05-15', 'quantity': str(joad_sessions),
                                           'base_price_money': {'amount': cost * 100, 'currency': 'USD'}})
            logging.debug(session['line_items'])
            logging.debug(line_items)
            self.assertListEqual(session['line_items'], line_items)
            self.assertEquals(session['idempotency_key'], line['verification_code'])
