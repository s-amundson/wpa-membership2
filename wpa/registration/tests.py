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


