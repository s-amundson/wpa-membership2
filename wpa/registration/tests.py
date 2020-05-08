from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from registration.models import Member, Family, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)


# Create your tests here.

class Temporary_Tests(TestCase):
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


    def add_member(self):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        self.assertEquals(len(Member.objects.all()), 1)
        self.assertEquals(len(session.items()), 0)

    def test_joad_register_invalid_request_method(self):
        response = self.client.put(reverse('registration:register'))
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(reverse('registration:register'))
        self.assertEqual(response.status_code, 404)

