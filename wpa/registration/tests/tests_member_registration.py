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
        path = os.path.join(settings.BASE_DIR, 'registration', 'fixtures', 'email_verify_fixture.json')
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
        self.mem = {'first_name': 'Emily',
                    'last_name': 'Conlan',
                    'street': "1984 Jones Avenue",
                    'city': 'Hays',
                    'state': 'NC',
                    'post_code': 28635,
                    'phone': '336-696-6307',
                    'email': 'EmilyNConlan@einrot.com',
                    'dob': '1995-03-12',
                    'level': 'standard',
                    'terms': True}

    def add_member(self, mem):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), mem, follow=True)
        self.session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        self.member = Member.objects.all()


    def test_duplicate_member(self):
        # # submit a registration to be added.
        self.add_member(self.mem)
        self.assertEquals(len(self.member), 1)
        self.assertEquals(len(self.session.items()), 0)
        # resubmit a registration to test duplication.
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')
        self.assertEquals(len(Member.objects.all()), 1)
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")
        self.assertEquals(len(session.items()), 0)

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
        self.mem['joad'] = "2020-04-18"
        self.mem['dob'] = '2010-03-12'

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


    def test_joad_session_to_old(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        self.mem['level'] = 'joad'
        self.mem['joad'] = "2020-04-18"

        self.client.get(reverse('registration:register'))
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')

        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')
            self.assertContains(response, 'Error on form.')

        mem = Member.objects.all()
        self.assertEquals(len(mem), 0)

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
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")
        self.assertEquals(session['family_total'], 40)
        # self.assertRedirects(response, reverse('registration:register'))
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')
        # Enter second family member
        self.mem['first_name'] = 'Janet'
        self.mem['last_name'] = 'Conlan'
        self.mem['dob'] = '2010-03-12'
        self.mem['joad'] = "2020-04-18"
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')
        self.assertEquals(session['family_total'], 135)

        # Complete the family registration
        self.client.post(reverse('registration:fam_done'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

        member = Member.objects.all()
        self.assertEquals(len(member), 2)
        for m in member:
            self.assertEquals(m.fam, 1)


    def test_family_good(self):

        # Enter first family member
        self.mem['level'] = 'family'
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")
        self.assertEquals(session['family_total'], 40)

        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')
        # Enter second family member
        self.mem['first_name'] = 'Janet'
        self.mem['last_name'] = 'Conlan'
        self.mem['dob'] = '2010-03-12'
        self.client.post(reverse('registration:register'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')
        self.assertEquals(session['family_total'], 40)

        # Complete the family registration
        self.client.post(reverse('registration:fam_done'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

        member = Member.objects.all()
        self.assertEquals(len(member), 2)
        for m in member:
            self.assertEquals(m.fam, 1)


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
