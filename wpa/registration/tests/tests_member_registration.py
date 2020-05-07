from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from registration.models import Member, Family, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)


# Create your tests here.


class MemberModelTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
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

    def test_add_member(self):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        self.assertEquals(len(Member.objects.all()), 1)
        self.assertEquals(len(session.items()), 0)

    def test_duplicate_member(self):
        # # submit a registration to be added.
        self.test_add_member()
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
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)

        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

        # TODO test session clear - should there be a session clear with this?

    # def test_joad_session_good(self): # Broken, because the session options are now sent with the form,
    #   and this test does not preform the get portion.
    #     d = date.fromisoformat("2020-04-18")
    #     js = Joad_sessions(start_date=d, state='open')
    #     js.save()
    #     self.mem['joad'] = "2020-04-18"
    #     self.mem['dob'] = '2010-03-12'
    #     response = self.client.post(reverse('registration:register'), self.mem, follow=True)
    #     session = self.client.session
    #     self.assertRedirects(response, reverse('registration:register'))
    #     mem = Member.objects.all()
    #     self.assertEquals(len(mem), 1)
    #     # self.assertEquals(Member.objects.get(pk=1).joad, d)
    #     jsr = Joad_session_registration.objects.filter(mem=mem[0])
    #     self.assertEquals(len(jsr), 1)
    #     self.assertEquals(len(session.items()), 0)

    # def test_joad_session_to_old(self): # Broken, because the session options are now sent with the form,
    #   and this test does not preform the get portion.
    #     d = date.fromisoformat("2020-04-18")
    #     js = Joad_sessions(start_date=d, state='open')
    #     js.save()
    #     self.mem['joad'] = "2020-04-18"
    #     response = self.client.post(reverse('registration:register'), self.mem, follow=True)
    #     session = self.client.session
    #     self.assertRedirects(response, reverse('registration:register'))
    #     mem = Member.objects.all()
    #     self.assertEquals(len(mem), 0)
    #     # The form is invalid therefore the member is not saved
    #     # # self.assertEquals(Member.objects.get(pk=1).joad, d)
    #     # jsr = Joad_session_registration.objects.filter(mem=mem[0])
    #     # self.assertEquals(len(jsr), 0)
    #     # self.assertEquals(len(session.items()), 0)

    def test_terms_bad(self):
        # submit a registration to be added.
        self.mem.pop('terms', None)
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        # self.assertRedirects(response, reverse('registration:register'), status_code=200)
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")
        self.assertEquals(len(Member.objects.all()), 0)
        self.assertEquals(len(session.items()), 0)

    def test_family_good(self):
        # Enter first family member
        self.mem['level'] = 'family'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
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
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/register.html'):
            render_to_string('registration/register.html')

        # Complete the family registration
        self.client.post(reverse('registration:fam_done'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

        member = Member.objects.all()
        self.assertEquals(len(member), 2)
        for m in member:
            self.assertEquals(m.fam, 1)
