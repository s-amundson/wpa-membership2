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

    def test_joad_session_good(self):
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()
        self.mem['joad'] = "2020-04-18"
        self.mem['dob'] = '2010-03-12'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        mem = Member.objects.all()
        self.assertEquals(len(mem), 1)
        # self.assertEquals(Member.objects.get(pk=1).joad, d)
        jsr = Joad_session_registration.objects.filter(mem=mem[0])
        self.assertEquals(len(jsr), 1)
        self.assertEquals(len(session.items()), 0)
