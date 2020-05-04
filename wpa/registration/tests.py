from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from .models import Member, Family, Joad_sessions, Joad_session_registration
import logging
logger = logging.getLogger(__name__)

# Create your tests here.

# TODO create tests for registration validation.


class MemberModelTests(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.session = self.client.session
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
        self.mem.pop('terms', None)
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        self.assertRedirects(response, reverse('registration:register'))
        self.assertEquals(len(Member.objects.all()), 1)
        self.assertEquals(len(self.session.items()), 0)

    def test_family_good(self):

        # Enter first family member
        self.mem['level'] = 'family'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        for k, v in session.items():
            logging.debug(f"k = {k} v={v}")
        self.assertEquals(session['family_total'], 40)
        self.assertRedirects(response, reverse('registration:register'))

        # Enter second family member
        self.mem['first_name'] = 'Janet'
        self.mem['last_name'] = 'Conlan'
        self.mem['dob'] = '2010-03-12'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        self.assertRedirects(response, reverse('registration:register'))

        # Complete the family registration
        self.client.post(reverse('registration:fam_done'), self.mem, follow=True)
        with self.assertTemplateUsed('registration/message.html'):
            render_to_string('registration/message.html')

        member = Member.objects.all()
        self.assertEquals(len(member), 2)
        for m in member:
            self.assertEquals(m.fam, 1)

