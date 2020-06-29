import json
import os

from django.conf import settings

from django.test import TestCase, Client
from django.urls import reverse

from registration.models import Membership, Joad_sessions, Joad_session_registration, Payment_log

import logging

logger = logging.getLogger(__name__)

class ProcessPaymentTests(TestCase):
    fixtures = ['membership1.json']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'membership1.json')
        logging.debug(path)
        self.membership_data = []
        with open(path) as f:
            data = json.load(f)
        for r in data:
            if r['model'] == 'registration.membership':
                f = r['fields']
                f['pk'] = r['pk']
                self.membership_data.append(f)
        self.costs = {'standard_membership': 20,
                      'family_membership': 40,
                      'joad_membership': 18,
                      'senior_membership': 18,
                      'benefactor': 100,
                      'joad_session': 95,
                      'pin_shoot': 15,
                      'joad_pin': 5,
                      'family_total': None}

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def line_items(self, line):
        line_items = []


    def test_process_membership(self):
        # Note: this does not test the amount.
        # self.add_member()
        for line in self.membership_data:
            logging.debug(line)
            session = self.client.session
            session['idempotency_key'] = line['verification_code']


            # make line items
            line_items = []
            li = {'name': 'Membership', 'quantity': '1', 'base_price_money':
                {'amount': 100, 'currency': 'USD'}}
            if line["benefactor"]:
                li['name'] = 'Benefactor Membership'
                li['base_price_money']['amount'] = self.costs['benefactor'] * 100
            else:
                li['base_price_money']['amount'] = self.costs[f"{line['level']}_membership"] * 100
            line_items.append(li)
            try:
                joad = Joad_session_registration.objects.filter(idempotency_key=line['verification_code'])
            except Joad_session_registration.DoesNotExist:
                joad = []
            joad_sessions = len(joad)
            cost = self.costs['joad_session'] * joad_sessions

            if joad_sessions > 0:
                line_items.append({'name': 'Joad Session 2020-05-15', 'quantity': str(joad_sessions),
                                   'base_price_money': {'amount': cost * 100, 'currency': 'USD'}})
            session['line_items'] = line_items
            session.save()
            self.client.post(reverse('registration:process_payment'))

            membership = Membership.objects.get(pk=line['pk'])
            self.assertEquals(membership.verification_code, '')
            log = Payment_log.objects.filter(idempotency_key=line['verification_code'])
            self.assertEquals(log[0].members, str(line['pk']))

# class ProcessPaymentTests(TestCase):
#     fixtures = ['membership1.json']
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'membership1.json')
#         logging.debug(path)
#         self.membership_data = []
#         with open(path) as f:
#             data = json.load(f)
#         for r in data:
#             if r['model'] == 'registration.membership':
#                 f = r['fields']
#                 f['pk'] = r['pk']
#                 self.membership_data.append(f)
#         self.costs = {'standard_membership': 20,
#                       'family_membership': 40,
#                       'joad_membership': 18,
#                       'senior_membership': 18,
#                       'benefactor': 100,
#                       'joad_session': 95,
#                       'pin_shoot': 15,
#                       'joad_pin': 5,
#                       'family_total': None}
#
#     def setUp(self):
#         # Every test needs a client.
#         self.client = Client()
#
#
#     def test_process_membership(self):
#         # self.add_member()
#         for line in self.membership_data:
#             logging.debug(line)
#             session = self.client.session
#             session['idempotency_key'] = line['verification_code']
#
#             # make line items
#             line_items = []
#             li = {'name': 'Membership', 'quantity': '1', 'base_price_money':
#                 {'amount': 100, 'currency': 'USD'}}
#             if line["benefactor"]:
#                 li['name'] = 'Benefactor Membership'
#                 li['base_price_money']['amount'] = self.costs['benefactor'] * 100
#             else:
#                 li['base_price_money']['amount'] = self.costs[f"{line['level']}_membership"] * 100
#             line_items.append(li)
#             try:
#                 joad = Joad_session_registration.objects.filter(idempotency_key=line['verification_code'])
#             except Joad_session_registration.DoesNotExist:
#                 joad = []
#             joad_sessions = len(joad)
#             cost = self.costs['joad_session'] * joad_sessions
#
#             if joad_sessions > 0:
#                 line_items.append({'name': 'Joad Session 2020-05-15', 'quantity': str(joad_sessions),
#                                    'base_price_money': {'amount': cost * 100, 'currency': 'USD'}})
#             session['line_items'] = line_items
#             session.save()
#             self.client.post(reverse('registration:process_payment'))
#
#             membership = Membership.objects.get(pk=line['pk'])
#             self.assertEquals(membership.verification_code, '')
#             log = Payment_log.objects.filter(idempotency_key=line['verification_code'])
#             self.assertEquals(log[0].members, str(line['pk']))
#
