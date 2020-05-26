import json
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from registration.models import Member, Membership, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)


# Create your tests here.


class MemberModelTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'registration_fixture.json')
        logging.debug(path)
        with open(path) as f:
            data = json.load(f)

        self.member_data = []
        self.joad_sessions_data = []
        for r in data:
            if r['model'] == 'registration.member':
                f = r['fields']
                f.pop('reg_date')
                f.pop('exp_date')
                f.pop('verification_code')
                f.pop('status')
                f.pop('pay_code')
                f.pop('fam')
                f['terms'] = True
                self.member_data.append(f)
            elif r['model'] == 'registration.joad_sessions':
                self.joad_sessions_data.append(r['fields'])

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        for d in self.joad_sessions_data:
            js = Joad_sessions.objects.get_or_create(d)
            # js.save()
        self.joad_date = Joad_sessions.objects.filter(state="open")[0]
        self.mem = {'csrfmiddlewaretoken': ['SQW46AFNMMUdA2MBIRrppw2xImcSwPyiKJr6AWTNy8ZYzrz2puQd4lzIps84GUVp'],
                    'member_set-TOTAL_FORMS': ['2'],
                    'member_set-INITIAL_FORMS': ['0'],
                    'member_set-MIN_NUM_FORMS': ['0'],
                    'member_set-MAX_NUM_FORMS': ['1000'],
                    'member_set-0-first_name': ['Pearl'],
                    'member_set-0-last_name': ['Fafe'],
                    'member_set-0-dob': ['1978-02-15'],
                    'member_set-0-joad': [''],
                    'member_set-1-first_name': [''],
                    'member_set-1-last_name': [''],
                    'member_set-1-dob': [''],
                    'member_set-1-joad': [''],
                    'street': ['1339 Kelly Drive'],
                    'city': ['Charlston'],
                    'state': ['WV'],
                    'post_code': ['12344'],
                    'email': ['pear.fafe@example.com'],
                    'phone': ['123.123.1234'],
                    'level': ['standard'],
                    'terms': ['on']}

    def add_member(self, mem):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), mem, follow=True)
        self.session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        self.member = Member.objects.all()


    def test_duplicate_member(self):
        self.add_member(self.mem)
        self.assertEquals(len(self.member), 1)
        membership = Membership.objects.all()
        self.assertEquals(len(membership), 1)
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')
        self.assertEquals(len(Member.objects.all()), 1)
        self.assertEquals(len(Membership.objects.all()), 1)

    def test_invalid_level(self):
        # if javascript is off then the form could be submitted with and invalid value.
        self.mem['level'] = 'invalid'
        self.client.post(reverse('registration:register'), self.mem, follow=True)

        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

    def test_joad_session_good(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        self.mem['member_set-0-joad'] = "2020-04-18"
        self.mem['member_set-0-dob'] = '2010-03-12'

        self.client.get(reverse('registration:register'))
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')

        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        mem = Member.objects.all()
        self.assertEquals(len(mem), 1)
        # self.assertEquals(Member.objects.get(pk=1).joad, d)
        jsr = Joad_session_registration.objects.filter(mem=mem[0])
        self.assertEquals(len(jsr), 1)
        self.assertEquals(len(session.items()), 0)

    def test_terms_bad(self):
        # submit a registration to be added.
        self.mem.pop('terms', None)
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")
        self.assertEquals(len(Member.objects.all()), 0)
        self.assertEquals(len(session.items()), 0)

    def test_family_joad_good(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        # Enter first family member
        self.mem['level'] = 'family'
        self.mem['member_set-1-first_name'] = 'Janet'
        self.mem['member_set-1-last_name'] = 'Conlan'
        self.mem['member_set-1-dob'] = '2010-03-12'
        self.mem['member_set-1-joad'] = "2020-04-18"
        self.client.post(reverse('registration:register'), self.mem, follow=True)

        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')

        member = Member.objects.all()
        self.assertEquals(len(member), 2)
        membership = Membership.objects.all()
        self.assertEquals(len(membership), 1)
        jsr = Joad_session_registration.objects.filter(mem=member[1])
        self.assertEquals(len(jsr), 1)

    def test_family_good(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        # Enter first family member
        self.mem['level'] = 'family'
        self.mem['member_set-1-first_name'] = 'Janet'
        self.mem['member_set-1-last_name'] = 'Conlan'
        self.mem['member_set-1-dob'] = '2010-03-12'

        self.client.post(reverse('registration:register'), self.mem, follow=True)

        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')

        member = Member.objects.all()
        self.assertEquals(len(member), 2)
        membership = Membership.objects.all()
        self.assertEquals(len(membership), 1)
        jsr = Joad_session_registration.objects.filter(mem=member[1])
        self.assertEquals(len(jsr), 0)


    def test_joad_register_invalid_request_method(self):
        response = self.client.put(reverse('registration:register'))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse('registration:register'))
        self.assertEqual(response.status_code, 405)

    def test_member_combinations(self):
        js_count = 0
        family_count = 0
        index = 0
        # standard membership
        self.add_member(self.member_data[index])
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, False)

        # standard, joad session;
        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.add_member(self.member_data[index])
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)

        # verification code is supposed to be the same in Joad_session_registration as it is in the member table.
        js = Joad_session_registration.objects.filter(idempotency_key=self.member[index - 1].verification_code)
        self.assertEquals(len(js), 1)
        self.assertEquals(self.member[index - 1].benefactor, False)

        # standard, benefactor;
        self.add_member(self.member_data[index])
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, True)

        # benefactor, joad session
        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.add_member(self.member_data[index])
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, True)

        # family,
        # self.add_member(self.member_data[index])
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        # session = self.client.session
        index += 1
        self.assertEquals(len(self.member), index)
        family_count += 1
        self.assertEquals(self.member[index - 1].fam, family_count)
        self.assertEquals(self.member[index - 1].benefactor, False)
        ik = self.member[index - 1].verification_code

        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].verification_code, ik)
        self.assertEquals(self.member[index - 1].fam, family_count)
        self.client.post(reverse('registration:fam_done'))
        session = self.client.session
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")

        # family, joad session;
        logging.debug('family, joad session')
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        self.assertEquals(len(self.member), index)
        family_count += 1
        self.assertEquals(self.member[index - 1].fam, family_count)
        self.assertEquals(self.member[index - 1].benefactor, False)
        ik = self.member[index - 1].verification_code

        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].verification_code, ik)
        js = Joad_session_registration.objects.filter(idempotency_key=self.member[index - 1].verification_code)
        self.assertEquals(len(js), 1)
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)
        self.client.post(reverse('registration:fam_done'))
        session = self.client.session
        self.assertIsNone(session.get('fam_id', None))

        # family, multiple joad session;
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        self.assertEquals(len(self.member), index)
        family_count += 1
        self.assertEquals(self.member[index - 1].fam, family_count)
        self.assertEquals(self.member[index - 1].benefactor, False)
        ik = self.member[index - 1].verification_code

        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].verification_code, ik)

        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].verification_code, ik)
        js = Joad_session_registration.objects.filter(idempotency_key=self.member[index - 1].verification_code)
        self.assertEquals(len(js), 2)
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)
        self.client.post(reverse('registration:fam_done'))
        session = self.client.session
        self.assertIsNone(session.get('fam_id', None))

        # family, benefactor;
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        self.assertEquals(len(self.member), index)
        family_count += 1
        self.assertEquals(self.member[index - 1].fam, family_count)
        self.assertEquals(self.member[index - 1].benefactor, True)
        ik = self.member[index - 1].verification_code

        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].verification_code, ik)
        self.client.post(reverse('registration:fam_done'))
        session = self.client.session
        self.assertIsNone(session.get('fam_id', None))

        # family, joad session, benefactor;
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        self.assertEquals(len(self.member), index)
        family_count += 1
        self.assertEquals(self.member[index - 1].fam, family_count)
        self.assertEquals(self.member[index - 1].benefactor, True)
        ik = self.member[index - 1].verification_code

        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.client.post(reverse('registration:register'), self.member_data[index], follow=True)
        self.member = Member.objects.all()
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].verification_code, ik)
        js = Joad_session_registration.objects.filter(idempotency_key=self.member[index - 1].verification_code)
        self.assertEquals(len(js), 1)
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)
        self.client.post(reverse('registration:fam_done'))
        session = self.client.session
        self.assertIsNone(session.get('fam_id', None))

    # joad;
        self.add_member(self.member_data[index])
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, False)
        self.assertEquals(self.member[index - 1].level, 'joad')
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)

    # joad, joad session;
        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.add_member(self.member_data[index])
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, False)
        js = Joad_session_registration.objects.filter(idempotency_key=self.member[index - 1].verification_code)
        self.assertEquals(len(js), 1)
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)

    # joad, benefactor;
        self.add_member(self.member_data[index])
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, True)
        self.assertEquals(self.member[index - 1].level, 'joad')
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)

    # joad, joad session, benefactor;
        self.member_data[index]['joad'] = self.joad_date.start_date.isoformat()
        self.add_member(self.member_data[index])
        index += 1
        js_count += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, True)
        js = Joad_session_registration.objects.filter(idempotency_key=self.member[index - 1].verification_code)
        self.assertEquals(len(js), 1)
        js = Joad_session_registration.objects.all()
        self.assertEquals(len(js), js_count)

    # senior;
        self.add_member(self.member_data[index])
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, False)
        self.assertEquals(self.member[index - 1].level, 'senior')

    # senior, benefactor;
        self.add_member(self.member_data[index])
        index += 1
        self.assertEquals(len(self.member), index)
        self.assertEquals(self.member[index - 1].benefactor, True)
        self.assertEquals(self.member[index - 1].level, 'senior')
