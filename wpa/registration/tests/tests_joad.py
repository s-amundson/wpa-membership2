from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datetime_safe import  date
from registration.models import Member, Joad_sessions, Joad_session_registration

import logging

logger = logging.getLogger(__name__)


# Create your tests here.


class JoadRegistrtionTests(TestCase):
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
        self.joad_mem = {'first_name': 'Emily',
                         'last_name': 'Conlan',
                         'email': 'EmilyNConlan@einrot.com',
                         'terms': True}
        d = date.fromisoformat("2020-04-18")
        js = Joad_sessions(start_date=d, state='open')
        js.save()

    def add_joad_member(self):
        self.mem['dob'] = '2010-03-12'
        response = self.client.post(reverse('registration:register'), self.mem, follow=True)
        # session = self.client.session
        self.assertRedirects(response, reverse('registration:register'))
        mem = Member.objects.all()
        self.assertEquals(len(mem), 1)

    def test_joad_register_good(self):
        self.add_joad_member()
        self.client.get(reverse('registration:joad_registration'))
        with self.assertTemplateUsed('registration/joad_registration.html'):
            render_to_string('registration/joad_registration.html')

        self.joad_mem['joad'] = "2020-04-18"
        self.client.post(reverse('registration:joad_registration'), self.joad_mem, follow=True)
        reg = Joad_session_registration.objects.all()
        self.assertEquals(len(reg), 1)

    def test_joad_register_invalid_form(self):
        """Leave out one input and submit, check if returns error message"""
        self.add_joad_member()
        self.joad_mem['joad'] = "2020-04-18"
        logging.debug(self.joad_mem)
        keys = list(self.joad_mem.keys())
        for k in keys:
            jm = self.joad_mem.copy()
            jm.pop(k)
            self.client.get(reverse('registration:joad_registration'))
            with self.assertTemplateUsed('registration/joad_registration.html'):
                render_to_string('registration/joad_registration.html')

            response = self.client.post(reverse('registration:joad_registration'), jm, follow=True)
            with self.assertTemplateUsed('registration/message.html'):
                render_to_string('registration/message.html')
                self.assertContains(response, 'Error on form.')
            reg = Joad_session_registration.objects.all()
            self.assertEquals(len(reg), 0)

    def test_joad_register_invalid_request_method(self):

        response = self.client.put(reverse('registration:joad_registration'))
        self.assertEqual(response.status_code, 404)
        # with self.assertTemplateUsed('registration/message.html'):
        #     render_to_string('registration/message.html')
        # self.assertContains(response, 'Error on form.')

        response = self.client.delete(reverse('registration:joad_registration'))
        self.assertEqual(response.status_code, 404)
