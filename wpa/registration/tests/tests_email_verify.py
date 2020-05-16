from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
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

    def add_member(self):
        # submit a registration to be added.
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        self.member = Member.objects.all()
        self.assertEquals(len(self.member), 1)
        self.assertEquals(len(session.items()), 0)

    def test_email_verification(self):
        self.add_member()
        logging.debug(self.member[0].email_code)
        self.client.get(reverse('registration:email_verify'),
                                   {'e': self.member[0].email,
                                    'c': self.member[0].email_code})
        with self.assertTemplateUsed('registration/email_verify.html'):
            render_to_string('registration/email_verify.html')

        m = {'email': self.member[0].email, 'email_code': self.member[0].email_code}
        response = self.client.post(reverse('registration:email_verify'), m, follow=True)
        session = self.client.session
        l = [{'name': 'Membership', 'quantity': '1', 'base_price_money': {'amount': 2000, 'currency': 'USD'}}]
        self.assertListEqual(session['line_items'], l)
        self.assertEquals(session['idempotency_key'], self.member[0].email_code)