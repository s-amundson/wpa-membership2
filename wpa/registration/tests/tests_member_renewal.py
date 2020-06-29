import json
import logging
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from registration.models import Membership, OrphanMember

logger = logging.getLogger(__name__)


class MembershipRenewalTests(TestCase):
    fixtures = ['renewal1.json']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'renewal1.json')
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
                f['status'] = 'member'
                self.membership_data.append(f)

        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'renewal_fixture.json')
        logging.debug(path)
        with open(path) as f:
            self.member_data = json.load(f)

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        logging.debug('here')


    # def test_renewal_no_change(self):
    #     # self.add_member()
    #     for line in self.membership_data:
    #         logging.debug(line)
    #         self.client.get(reverse('registration:renew_membership'),
    #                         {'e': line['email'],
    #                          'c': line['verification_code']})
    #         session = self.client.session
    #         with self.assertTemplateUsed('registration/register.html'):
    #             render_to_string('registration/register.html')
    #         # self.assertIn(session['membership_id'])
    #
    #         line_items = []
    #         for m in self.member_data:
    #             if m['email'][0] == line['email']:
    #                 mid = session.get('membership_id', None)
    #                 logging.debug(mid)
    #                 n = int(m["member_set-TOTAL_FORMS"][0])
    #
    #                 self.client.post(reverse('registration:renew_membership'), m, follow=True)
    #                 session = self.client.session
    #
    #                 li = {'name': 'Membership', 'quantity': '1', 'base_price_money':
    #                     {'amount': 100, 'currency': 'USD'}}
    #                 if line["benefactor"]:
    #                     li['name'] = 'Benefactor Membership'
    #                     li['base_price_money']['amount'] = self.costs['benefactor'] * 100
    #                 else:
    #                     li['base_price_money']['amount'] = self.costs[f"{line['level']}_membership"] * 100
    #                 line_items.append(li)
    #                 cost = 0
    #                 joad_sessions = 0
    #
    #                 for i in range(n):
    #                     if m[f"member_set-{i}-joad"][0] != "":
    #                         cost += self.costs['joad_session']
    #                         joad_sessions += 1
    #                 if joad_sessions > 0:
    #                     line_items.append({'name': 'Joad Session 2020-05-15', 'quantity': str(joad_sessions),
    #                                        'base_price_money': {'amount': cost * 100, 'currency': 'USD'}})
    #         logging.debug(session['line_items'])
    #         logging.debug(line_items)
    #         self.assertListEqual(session['line_items'], line_items)
    #         self.assertEquals(session['idempotency_key'], line['verification_code'])
    #         n = int(m["member_set-TOTAL_FORMS"][0])
    #         mship = Membership.objects.get(id=mid)
    #         self.assertEquals(len(mship.member_set.all()), n)
    #         logging.debug(f"len = {len(mship.member_set.all())}, n = {n}")

    def test_renewal_remove_family_member(self):
        # self.add_member()
        for line in self.membership_data:

            if line['level'] != 'family':
                continue

            self.client.get(reverse('registration:renew_membership'),
                            {'e': line['email'],
                             'c': line['verification_code']})
            line_items = []
            for m in self.member_data:
                if m['email'][0] == line['email']:
                    logging.debug(m)
                    n = int(m['member_set-TOTAL_FORMS'][0])
                    mem = m.copy()

                    mem[f'member_set-{n-1}-DELETE'] = "on"
                    # mem['member_set-TOTAL_FORMS'][0] = f'{n-1}'

                    self.client.post(reverse('registration:renew_membership'), mem, follow=True)
                    session = self.client.session
                    mid = session.get('membership_id', None)

                    # remove membership from test calculations
                    del mem[f'member_set-{n - 1}-id']
                    del mem[f'member_set-{n - 1}-first_name']
                    del mem[f'member_set-{n - 1}-last_name']
                    del mem[f'member_set-{n - 1}-dob']
                    del mem[f'member_set-{n - 1}-joad']
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
                    for i in range(int(mem["member_set-TOTAL_FORMS"][0]) - 1):
                        if mem[f"member_set-{i}-joad"][0] != "":
                            cost += self.costs['joad_session']
                            joad_sessions += 1
                    if joad_sessions > 0:
                        line_items.append({'name': 'Joad Session 2020-05-15', 'quantity': str(joad_sessions),
                                           'base_price_money': {'amount': cost * 100, 'currency': 'USD'}})

            self.assertListEqual(session['line_items'], line_items)
            self.assertEquals(session['idempotency_key'], line['verification_code'])
            mship = Membership.objects.get(id=mid)
            self.assertEquals(len(mship.member_set.all()), n-1)
            self.assertEquals(len(OrphanMember.objects.filter(membership=mid)), 1)


    def test_renewal_remove_first_family_member(self):
        # self.add_member()
        for line in self.membership_data:

            if line['level'] != 'family':
                continue

            self.client.get(reverse('registration:renew_membership'),
                            {'e': line['email'],
                             'c': line['verification_code']})
            line_items = []
            for m in self.member_data:
                if m['email'][0] == line['email']:
                    logging.debug(m)
                    n = int(m['member_set-TOTAL_FORMS'][0])
                    mem = m.copy()

                    mem[f'member_set-{0}-DELETE'] = "on"
                    # mem['member_set-TOTAL_FORMS'][0] = f'{n-1}'

                    self.client.post(reverse('registration:renew_membership'), mem, follow=True)
                    session = self.client.session
                    mid = session.get('membership_id', None)

                    # remove membership from test calculations
                    del mem[f'member_set-{0}-id']
                    del mem[f'member_set-{0}-first_name']
                    del mem[f'member_set-{0}-last_name']
                    del mem[f'member_set-{0}-dob']
                    del mem[f'member_set-{0}-joad']
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
                    for i in range(int(mem["member_set-TOTAL_FORMS"][0]) - 1):
                        if mem[f"member_set-{i + 1}-joad"][0] != "":
                            cost += self.costs['joad_session']
                            joad_sessions += 1
                    if joad_sessions > 0:
                        line_items.append({'name': 'Joad Session 2020-05-15', 'quantity': str(joad_sessions),
                                           'base_price_money': {'amount': cost * 100, 'currency': 'USD'}})
            logging.debug(session['line_items'])
            logging.debug(line_items)
            self.assertListEqual(session['line_items'], line_items)
            self.assertEquals(session['idempotency_key'], line['verification_code'])
            mship = Membership.objects.get(id=mid)
            self.assertEquals(len(mship.member_set.all()), n-1)
            self.assertEquals(len(OrphanMember.objects.filter(membership=mid)), 1)
            logging.debug(len(mship.member_set.all()))
